from typing import TypedDict

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, START, END

from .prompts import LESSON_PROMPT, QUIZ_PROMPT


# =========================================================
# Agent State
# =========================================================

class LearningState(TypedDict):

    topic: str

    level: str

    learning_goal: str

    lesson: str

    quiz: str


# =========================================================
# Ollama LLM
# =========================================================

llm = ChatOllama(

    model="llama3.1:8b",

    temperature=0.4,

    num_predict=600,

    num_ctx=4096,

    keep_alive="10m"

)


# =========================================================
# Generate Personalized Lesson
# =========================================================

def generate_lesson(state: LearningState):

    prompt = LESSON_PROMPT.format(

        topic=state["topic"],

        level=state["level"],

        learning_goal=state["learning_goal"]

    )


    response = llm.invoke(

        [
            HumanMessage(
                content=prompt
            )
        ]

    )


    return {

        "lesson":
            response.content

    }


# =========================================================
# Generate Personalized Quiz
# =========================================================

def generate_quiz(state: LearningState):

    prompt = QUIZ_PROMPT.format(

        topic=state["topic"],

        level=state["level"],

        learning_goal=state["learning_goal"],

        lesson=state["lesson"]

    )


    response = llm.invoke(

        [
            HumanMessage(
                content=prompt
            )
        ]

    )


    return {

        "quiz":
            response.content

    }


# =========================================================
# LangGraph Workflow
# =========================================================

workflow = StateGraph(
    LearningState
)


workflow.add_node(

    "generate_lesson",

    generate_lesson

)


workflow.add_node(

    "generate_quiz",

    generate_quiz

)


workflow.add_edge(

    START,

    "generate_lesson"

)


workflow.add_edge(

    "generate_lesson",

    "generate_quiz"

)


workflow.add_edge(

    "generate_quiz",

    END

)


learning_agent = workflow.compile()


# =========================================================
# Main Agent Function
# =========================================================

def generate_learning_content(

    topic: str,

    level: str,

    learning_goal: str

):

    result = learning_agent.invoke(

        {

            "topic":
                topic,

            "level":
                level,

            "learning_goal":
                learning_goal,

            "lesson":
                "",

            "quiz":
                ""

        }

    )


    return result