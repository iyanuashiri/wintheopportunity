"""Prompts for the application form scraper agent."""

EXTRACTION_PROMPT = """
You are a form-extraction expert. Analyze the HTML of an application form
and extract every question/field.

FORM HTML:
{html}

For each field, extract:
- question_text: the question or field label
- field_type: text, textarea, dropdown, checkbox, file, etc.
- is_required: whether the field is required
- max_characters: max character limit, if specified
- max_words: max word limit, if specified
- order_index: the order of the field in the form

Also extract the page title from the <title> tag.

If you cannot extract any questions (e.g. the form requires login, is behind
authentication, is fully JS-rendered, or has no visible fields), set
extraction_reason to a short, user-friendly explanation of why. Leave
extraction_reason null if you successfully extracted at least one question.

Return the structured result.
"""