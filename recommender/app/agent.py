"""Agent 2: Recommendation / RAG Agent (standalone service).

This agent runs daily after the scraper. It:
1. Fetches opportunities created in the recent lookback window.
2. Chunks + embeds them into a local ChromaDB vector store.
3. For each NGO, queries the vector store for top-K similar opportunities.
4. Uses the LLM (Gemma 4 31B via OpenRouter) to score/rank the candidates.
5. Saves the scored recommendations to the backend.

The matching is hybrid: vector search (fast recall) + LLM scoring (quality).
"""

from __future__ import annotations

import logging

from strands import Agent

from app.config import settings
from app.model import get_agent_model
from app.prompts import SCORING_PROMPT
from app.rag import index_opportunities, search_similar
from app.schemas import RecommendationResult
from app.tools import (
    ALL_TOOLS,
    fetch_all_opportunities,
    fetch_ngos,
    fetch_new_opportunities,
    fetch_recommended_opportunity_ids,
    save_recommendations,
)

logger = logging.getLogger(__name__)


def _ngo_to_text(ngo: dict) -> str:
    """Build a searchable text blob from an NGO profile."""
    return " ".join(
        filter(
            None,
            [
                ngo.get("org_name", ""),
                ngo.get("mission_statement", ""),
                ngo.get("focus_areas", ""),
                ngo.get("target_beneficiaries", ""),
                ngo.get("background_info", ""),
            ],
        )
    )


def _opportunity_to_text(opp: dict) -> str:
    """Build a displayable text blob for an opportunity."""
    return (
        f"ID: {opp.get('id', '')}\n"
        f"Title: {opp.get('title', '')}\n"
        f"Organization: {opp.get('organization_name', '')}\n"
        f"Description: {opp.get('description', '')}\n"
        f"Eligibility: {opp.get('eligibility_criteria', '')}\n"
        f"Category: {opp.get('category', '')}\n"
        f"Deadline: {opp.get('deadline', '')}"
    )


def build_recommender_agent() -> Agent:
    """Build the recommendation agent."""
    return Agent(
        model=get_agent_model(),
        tools=ALL_TOOLS,
    )


async def _recommend_for_ngo(
    agent: Agent,
    ngo: dict,
    opp_by_id: dict[int, dict],
) -> RecommendationResult | None:
    """Score and save recommendations for a single NGO.

    Args:
        agent: The recommender agent.
        ngo: The NGO profile dict.
        opp_by_id: Map of opportunity id -> opportunity dict.

    Returns:
        The scored result, or None if nothing to recommend.
    """
    ngo_text = _ngo_to_text(ngo)
    if not ngo_text.strip():
        return None

    # Exclude opportunities already recommended to this user
    already_recommended = set(fetch_recommended_opportunity_ids(ngo["user_id"]))

    # Vector search for top-K candidates
    candidates = search_similar(ngo_text)
    candidate_opps = []
    for c in candidates:
        opp = opp_by_id.get(c["opportunity_id"])
        if opp and opp["id"] not in already_recommended:
            candidate_opps.append(opp)

    if not candidate_opps:
        return None

    # LLM scores the candidates
    prompt = SCORING_PROMPT.format(
        ngo_profile=ngo_text,
        opportunities="\n\n".join(
            _opportunity_to_text(o) for o in candidate_opps
        ),
    )
    result = await agent.invoke_async(
        prompt, structured_output_model=RecommendationResult
    )
    scored = result.structured_output

    # Save the recommendations
    payload = [
        {
            "user_id": ngo["user_id"],
            "opportunity_id": rec.opportunity_id,
            "relevance_score": rec.relevance_score,
            "match_reason": rec.match_reason,
            "source": "hybrid",
        }
        for rec in scored.recommendations
    ]
    if payload:
        save_recommendations(payload)
        return scored
    return None


async def run_recommender() -> list[RecommendationResult]:
    """Run the daily batch recommendation pipeline for all NGOs.

    Only processes opportunities created in the lookback window, and
    excludes opportunities already recommended to each user.

    Returns:
        list[RecommendationResult]: Scored recommendations per NGO.
    """
    # 1. Fetch new opportunities and index them
    opportunities = fetch_new_opportunities()
    logger.info("Fetched %d new opportunities", len(opportunities))
    if not opportunities:
        return []

    index_opportunities(opportunities)
    opp_by_id = {opp["id"]: opp for opp in opportunities}

    # 2. Fetch all NGOs
    ngos = fetch_ngos()
    logger.info("Fetched %d NGOs", len(ngos))

    agent = build_recommender_agent()
    all_results: list[RecommendationResult] = []

    for ngo in ngos:
        scored = await _recommend_for_ngo(agent, ngo, opp_by_id)
        if scored:
            all_results.append(scored)

    return all_results


async def run_recommender_for_user(user_id: int) -> RecommendationResult | None:
    """Run on-demand recommendations for a single (new) user.

    Uses ALL non-expired opportunities, excluding any already recommended.

    Args:
        user_id: The NGO user's ID.

    Returns:
        The scored result, or None if nothing to recommend.
    """
    # 1. Fetch all opportunities and index them
    opportunities = fetch_all_opportunities()
    logger.info("Fetched %d total opportunities", len(opportunities))
    if not opportunities:
        return None

    index_opportunities(opportunities)
    opp_by_id = {opp["id"]: opp for opp in opportunities}

    # 2. Find the NGO profile for this user
    ngos = fetch_ngos()
    ngo = next((n for n in ngos if n["user_id"] == user_id), None)
    if not ngo:
        logger.warning("No NGO profile found for user %d", user_id)
        return None

    agent = build_recommender_agent()
    return await _recommend_for_ngo(agent, ngo, opp_by_id)


if __name__ == "__main__":
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(description="Run the recommender agent")
    parser.add_argument(
        "--user-id",
        type=int,
        default=None,
        help="Run recommendations for a single user (onboarding). If omitted, runs for all users.",
    )
    args = parser.parse_args()

    if args.user_id is not None:
        asyncio.run(run_recommender_for_user(args.user_id))
    else:
        asyncio.run(run_recommender())