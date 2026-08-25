import streamlit as st
import json

from langgraph.graph import StateGraph, START, END

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from src.interview.state import InterviewState


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MAX_QUESTIONS = 10


# --------------------------------------------------
# Initialize Groq Model
# --------------------------------------------------

def get_llm():

    api_key = st.secrets["GROQ_API_KEY"]

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable is not set."
        )

    return ChatGroq(
        api_key=api_key,
        model="openai/gpt-oss-120b",
        temperature=0,
    )


# --------------------------------------------------
# Select Initial Question
# --------------------------------------------------

def select_initial_question(
    state: InterviewState
) -> InterviewState:

    questions = state["question_bank"]

    if not questions:
        raise ValueError(
            "Question bank is empty."
        )

    # --------------------------------------------------
    # Start With Easy Question
    # --------------------------------------------------

    easy_questions = [
        question
        for question in questions
        if question["difficulty"] == "easy"
    ]

    if easy_questions:
        question = easy_questions[0]
    else:
        question = questions[0]

    # --------------------------------------------------
    # Update State
    # --------------------------------------------------

    state["current_question"] = question

    state["current_question_index"] = (
        questions.index(question)
    )

    state["current_difficulty"] = (
        question["difficulty"]
    )

    state["question_count"] = 1

    state["user_answer"] = None

    return state


# --------------------------------------------------
# Evaluate Answer
# --------------------------------------------------

def evaluate_answer(
    state: InterviewState
) -> InterviewState:

    question = state["current_question"]

    if question is None:
        raise ValueError(
            "Current question is missing."
        )

    user_answer = state["user_answer"]

    if user_answer is None:
        raise ValueError(
            "User answer is missing."
        )

    correct_answer = (
        question["correct_answer"]
    )

    is_correct = (
        user_answer == correct_answer
    )

    # --------------------------------------------------
    # Save Answer
    # --------------------------------------------------

    state["answers"].append(
        {
            "question_id": question["id"],
            "selected_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,

            "category": question["category"],
            "difficulty": question["difficulty"],
        }
    )

    # --------------------------------------------------
    # Adaptive Difficulty
    # --------------------------------------------------

    current_difficulty = (
        state["current_difficulty"]
    )

    if is_correct:

        if current_difficulty == "easy":
            next_difficulty = "medium"

        elif current_difficulty == "medium":
            next_difficulty = "hard"

        else:
            next_difficulty = "hard"

    else:

        if current_difficulty == "hard":
            next_difficulty = "medium"

        elif current_difficulty == "medium":
            next_difficulty = "easy"

        else:
            next_difficulty = "easy"

    state["current_difficulty"] = (
        next_difficulty
    )

    # --------------------------------------------------
    # Clear Answer
    # --------------------------------------------------

    state["user_answer"] = None

    return state


# --------------------------------------------------
# Agent Select Question
# --------------------------------------------------

def agent_select_question(
    state: InterviewState
) -> InterviewState:

    questions = state["question_bank"]

    if not questions:
        raise ValueError(
            "Question bank is empty."
        )

    # --------------------------------------------------
    # Check Interview Limit
    # --------------------------------------------------

    if state["question_count"] >= MAX_QUESTIONS:

        state["interview_finished"] = True

        return state

    # --------------------------------------------------
    # Remove Already Asked Questions
    # --------------------------------------------------

    asked_ids = {
        answer["question_id"]
        for answer in state["answers"]
    }

    available_questions = [
        question
        for question in questions
        if question["id"] not in asked_ids
    ]

    if not available_questions:

        state["interview_finished"] = True

        return state

    # --------------------------------------------------
    # Prepare Questions For Agent
    # --------------------------------------------------

    question_options = []

    for question in available_questions:

        question_options.append(
            {
                "id": question["id"],
                "question": question["question"],
                "difficulty": question["difficulty"],
                "category": question["category"],
            }
        )

    # --------------------------------------------------
    # Previous Interview Context
    # --------------------------------------------------

    previous_answers = []

    for answer in state["answers"]:

        previous_answers.append(
            {
                "question_id":
                    answer["question_id"],

                "is_correct":
                    answer["is_correct"],

                "difficulty":
                    answer["difficulty"],
            }
        )

    # --------------------------------------------------
    # Agent Prompt
    # --------------------------------------------------

    prompt = f"""
You are an adaptive technical interviewer.

Your task is to select the best NEXT question
from the provided question bank.

Candidate information:
{json.dumps(
        state["candidate"],
        ensure_ascii=False
    )}

Current target difficulty:
{state["current_difficulty"]}

Previous answers:
{json.dumps(
        previous_answers,
        ensure_ascii=False
    )}

Available questions:
{json.dumps(
        question_options,
        ensure_ascii=False
    )}

Rules:

1. Select exactly ONE question.
2. The selected question MUST come from
   the available questions.
3. Return ONLY the question ID.
4. Do not create a new question.
5. Do not return an explanation.
6. Prefer the requested difficulty when possible.
7. Avoid repeating previously asked questions.
8. Consider the candidate's previous performance
   when selecting the next question.
9. Maintain diversity across technical areas.
10. Avoid repeatedly selecting questions from
    the same technical source or domain.
11. When possible, prefer a question from a
    different source or domain than the most
    recently asked questions.
12. Do NOT enforce an equal distribution between
    LLM and RAG questions.
13. Technical coverage and adaptive difficulty
    are more important than equal distribution.
"""

    # --------------------------------------------------
    # Call Groq
    # --------------------------------------------------

    llm = get_llm()

    response = llm.invoke(
        [
            HumanMessage(
                content=prompt
            )
        ]
    )

    selected_id = (
        response.content.strip()
    )

    # --------------------------------------------------
    # Validate Agent Response
    # --------------------------------------------------

    selected_question = None

    for question in available_questions:

        if question["id"] == selected_id:

            selected_question = question

            break

    # --------------------------------------------------
    # Fallback
    # --------------------------------------------------

    if selected_question is None:

        matching_difficulty = [
            question
            for question in available_questions
            if question["difficulty"]
            == state["current_difficulty"]
        ]

        if matching_difficulty:

            selected_question = (
                matching_difficulty[0]
            )

        else:

            selected_question = (
                available_questions[0]
            )

    # --------------------------------------------------
    # Update State
    # --------------------------------------------------

    state["current_question"] = (
        selected_question
    )

    state["current_question_index"] = (
        questions.index(selected_question)
    )

    state["question_count"] += 1

    # Important:
    # Store the ACTUAL difficulty of the
    # question selected by the Agent.

    state["current_difficulty"] = (
        selected_question["difficulty"]
    )

    state["user_answer"] = None

    return state


# --------------------------------------------------
# Route Initial / Existing Interview
# --------------------------------------------------

def route_start(
    state: InterviewState
):

    if state["question_count"] == 0:

        return "initial"

    return "evaluate"


# --------------------------------------------------
# Build Interview Graph
# --------------------------------------------------

def build_interview_graph():

    builder = StateGraph(
        InterviewState
    )

    # --------------------------------------------------
    # Nodes
    # --------------------------------------------------

    builder.add_node(
        "select_initial_question",
        select_initial_question
    )

    builder.add_node(
        "evaluate_answer",
        evaluate_answer
    )

    builder.add_node(
        "agent_select_question",
        agent_select_question
    )

    # --------------------------------------------------
    # START
    # --------------------------------------------------

    builder.add_conditional_edges(
        START,
        route_start,
        {
            "initial":
                "select_initial_question",

            "evaluate":
                "evaluate_answer",
        }
    )

    # --------------------------------------------------
    # First Question
    # --------------------------------------------------

    builder.add_edge(
        "select_initial_question",
        END
    )

    # --------------------------------------------------
    # Evaluate Answer
    # --------------------------------------------------

    builder.add_edge(
        "evaluate_answer",
        "agent_select_question"
    )

    # --------------------------------------------------
    # Agent Selects Next Question
    # --------------------------------------------------

    builder.add_edge(
        "agent_select_question",
        END
    )

    return builder.compile()
