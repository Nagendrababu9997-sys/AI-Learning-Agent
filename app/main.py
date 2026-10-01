from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import LearningContent
from .agent import generate_learning_content


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(

    title="AI Learning Content Agent",

    description="""
    Agentic AI Learning Platform.

    Generates personalized learning lessons and quizzes
    based on topic, learner level, and learning goal.

    Technologies:
    - FastAPI
    - LangGraph
    - LangChain
    - Ollama
    - Llama 3.1 8B
    - SQLite
    """,

    version="1.0.0",

    docs_url="/docs",

    redoc_url="/redoc"

)


# =========================================================
# TEMPLATES
# =========================================================

templates = Jinja2Templates(

    directory="templates"

)


# =========================================================
# REQUEST MODEL
# =========================================================

class LearningRequest(BaseModel):

    topic: str = Field(

        ...,

        min_length=2,

        max_length=200,

        description="Topic the learner wants to study"

    )

    level: str = Field(

        ...,

        description="Learner level"

    )

    learning_goal: str = Field(

        ...,

        description="Learning goal"

    )


# =========================================================
# HOME PAGE
# =========================================================

@app.get(

    "/",

    response_class=HTMLResponse,

    tags=["Web UI"]

)
def home(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="index.html"

    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get(

    "/health",

    tags=["System"]

)
def health_check():

    return {

        "status": "healthy",

        "application":
            "AI Learning Content Agent",

        "version":
            "1.0.0"

    }


# =========================================================
# API INFORMATION
# =========================================================

@app.get(

    "/api/info",

    tags=["System"]

)
def api_info():

    return {

        "application":
            "AI Learning Content Agent",

        "version":
            "1.0.0",

        "llm":
            "Llama 3.1 8B via Ollama",

        "agent_framework":
            "LangGraph",

        "llm_framework":
            "LangChain",

        "api_framework":
            "FastAPI",

        "database":
            "SQLite",

        "features": [

            "Personalized Lessons",

            "Interactive Quizzes",

            "Quiz Score Calculation",

            "Performance Analysis",

            "Learning Recommendations",

            "Learning History"

        ]

    }


# =========================================================
# GENERATE PERSONALIZED LEARNING CONTENT
# =========================================================

@app.post(

    "/generate",

    tags=["Learning"]

)
def generate_content(

    data: LearningRequest,

    db: Session = Depends(get_db)

):

    try:

        # -------------------------------------------------
        # Validate Learner Level
        # -------------------------------------------------

        allowed_levels = [

            "Beginner",

            "Intermediate",

            "Advanced"

        ]


        if data.level not in allowed_levels:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Invalid learner level. "
                    "Choose Beginner, Intermediate, "
                    "or Advanced."
                )

            )


        # -------------------------------------------------
        # Validate Learning Goal
        # -------------------------------------------------

        allowed_goals = [

            "Interview Preparation",

            "Project Development",

            "Exam Preparation",

            "Skill Development"

        ]


        if data.learning_goal not in allowed_goals:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Invalid learning goal. "
                    "Choose a valid learning goal."
                )

            )


        # -------------------------------------------------
        # Clean Topic
        # -------------------------------------------------

        topic = data.topic.strip()


        if not topic:

            raise HTTPException(

                status_code=400,

                detail="Topic cannot be empty."

            )


        # -------------------------------------------------
        # Run LangGraph AI Agent
        # -------------------------------------------------

        result = generate_learning_content(

            topic=topic,

            level=data.level,

            learning_goal=data.learning_goal

        )


        lesson = result["lesson"]

        quiz = result["quiz"]


        # -------------------------------------------------
        # Save Learning Content
        # -------------------------------------------------

        record = LearningContent(

            topic=topic,

            level=data.level,

            learning_goal=data.learning_goal,

            content_type="lesson_and_quiz",

            lesson=lesson,

            quiz=quiz

        )


        db.add(record)

        db.commit()

        db.refresh(record)


        # -------------------------------------------------
        # FINAL API RESPONSE
        #
        # IMPORTANT:
        # Keep fields at top level because the existing
        # frontend expects:
        #
        # data.topic
        # data.level
        # data.learning_goal
        # data.lesson
        # data.quiz
        # -------------------------------------------------

        return {

            "success": True,

            "message":
                "Personalized learning content generated successfully.",

            "id":
                record.id,

            "topic":
                record.topic,

            "level":
                record.level,

            "learning_goal":
                record.learning_goal,

            "lesson":
                record.lesson,

            "quiz":
                record.quiz

        }


    except HTTPException:

        raise


    except Exception as e:

        # -------------------------------------------------
        # Rollback Database Transaction
        # -------------------------------------------------

        db.rollback()


        raise HTTPException(

            status_code=500,

            detail=(
                "Failed to generate learning content. "
                f"Error: {str(e)}"
            )

        )


# =========================================================
# GET LEARNING HISTORY
# =========================================================

@app.get(

    "/history",

    tags=["History"]

)
def get_history(

    db: Session = Depends(get_db)

):

    records = (

        db.query(LearningContent)

        .order_by(

            LearningContent.id.desc()

        )

        .all()

    )


    return {

        "success": True,

        "count":
            len(records),

        "data": [

            {

                "id":
                    item.id,

                "topic":
                    item.topic,

                "level":
                    item.level,

                "learning_goal":
                    item.learning_goal,

                "created_at":
                    item.created_at

            }

            for item in records

        ]

    }


# =========================================================
# GET SINGLE LEARNING CONTENT
# =========================================================

@app.get(

    "/history/{content_id}",

    tags=["History"]

)
def get_history_content(

    content_id: int,

    db: Session = Depends(get_db)

):

    item = (

        db.query(LearningContent)

        .filter(

            LearningContent.id == content_id

        )

        .first()

    )


    # -----------------------------------------------------
    # Content Not Found
    # -----------------------------------------------------

    if not item:

        raise HTTPException(

            status_code=404,

            detail="Learning content not found."

        )


    # -----------------------------------------------------
    # Return Saved Content
    # -----------------------------------------------------

    return {

        "success": True,

        "id":
            item.id,

        "topic":
            item.topic,

        "level":
            item.level,

        "learning_goal":
            item.learning_goal,

        "lesson":
            item.lesson,

        "quiz":
            item.quiz,

        "created_at":
            item.created_at

    }