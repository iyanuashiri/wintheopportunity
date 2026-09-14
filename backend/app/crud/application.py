from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func
from app.models.application import Application, Question, Answer, Image
from app.schemas.application import ApplicationCreate, ImageCreate


def create_application(session: Session, application_in: ApplicationCreate, user_id: int) -> Application:
    db_application = Application(
        user_id=user_id,
        title=application_in.title,
        opportunity_id=application_in.opportunity_id,
        application_url=application_in.application_url,
        mode=application_in.mode,
        status=application_in.status,
        questions_extracted=application_in.questions_extracted,
        extraction_note=application_in.extraction_note,
        extraction_reason=application_in.extraction_reason,
    )
    
    for q_data in application_in.questions:
        question = Question(
            question_text=q_data.question_text,
            field_type=q_data.field_type,
            is_required=q_data.is_required,
            max_characters=q_data.max_characters,
            max_words=q_data.max_words,
            order_index=q_data.order_index,
        )
        for a_data in q_data.answers:
            answer = Answer(answer_text=a_data.answer_text)
            question.answers.append(answer)
        db_application.questions.append(question)

    session.add(db_application)
    session.commit()
    session.refresh(db_application)
    return db_application


def create_image(session: Session, application_id: int, image_in: ImageCreate) -> Image:
    db_image = Image(
        application_id=application_id,
        image_path=image_in.image_path,
    )
    session.add(db_image)
    session.commit()
    session.refresh(db_image)
    return db_image


def get_user_applications(session: Session, user_id: int, skip: int = 0, limit: int = 20) -> list[dict]:
    # Query applications and count associated questions
    statement = (
        select(Application, func.count(Question.id).label("questions_count"))
        .outerjoin(Question, Application.id == Question.application_id)
        .where(Application.user_id == user_id)
        .group_by(Application.id)
        .offset(skip)
        .limit(limit)
    )
    results = session.execute(statement).all()

    applications_summary = []
    for app, count in results:
        app_dict = {
            "id": app.id,
            "user_id": app.user_id,
            "opportunity_id": app.opportunity_id,
            "title": app.title,
            "application_url": app.application_url,
            "mode": app.mode,
            "status": app.status,
            "questions_extracted": app.questions_extracted,
            "extraction_note": app.extraction_note,
            "extraction_reason": app.extraction_reason,
            "created_at": app.created_at,
            "questions_count": count,
        }
        applications_summary.append(app_dict)
        
    return applications_summary


def get_application_by_id(session: Session, application_id: int, user_id: int) -> Application | None:
    # Eagerly load nested questions -> answers -> evaluations, plus images
    statement = (
        select(Application)
        .options(
            joinedload(Application.questions)
            .joinedload(Question.answers)
            .joinedload(Answer.evaluations),
            joinedload(Application.images),
        )
        .where(Application.id == application_id, Application.user_id == user_id)
    )
    return session.scalars(statement).unique().first()