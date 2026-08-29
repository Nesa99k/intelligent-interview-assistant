import streamlit as st
import json
import time

from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from src.interview.state import InterviewState


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MAX_QUESTIONS = 10

# Number of candidate questions presented to the Agent
CANDIDATE_LIMIT = 15


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
    # Initial question
    #
    # Start from Easy questions, but choose randomly
    # instead of always selecting the first question.
    # --------------------------------------------------

    import random

    easy_questions = [
        question
        for question in questions
        if question["difficulty"] == "easy"
    ]

    if easy_questions:
        question = random.choice(easy_questions)
    else:
        question = random.choice(questions)

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
    # Clear User Answer
    # --------------------------------------------------

    state["user_answer"] = None

    return state


# --------------------------------------------------
# Prepare Candidate Questions
# --------------------------------------------------

def prepare_candidate_questions(
    state: InterviewState
):

    questions = state["question_bank"]

    # --------------------------------------------------
    # Remove already asked questions
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
        return []

    # --------------------------------------------------
    # Recently asked categories
    # --------------------------------------------------

    recent_answers = state["answers"][-3:]

    recent_categories = {
        answer["category"]
        for answer in recent_answers
    }

    # --------------------------------------------------
    # Group questions by difficulty
    # --------------------------------------------------

    easy_questions = [
        q for q in available_questions
        if q["difficulty"] == "easy"
    ]

    medium_questions = [
        q for q in available_questions
        if q["difficulty"] == "medium"
    ]

    hard_questions = [
        q for q in available_questions
        if q["difficulty"] == "hard"
    ]

    # --------------------------------------------------
    # Prefer category diversity
    #
    # Questions from recently used categories are
    # deprioritized, not completely removed.
    # --------------------------------------------------

    def diversity_score(question):

        if question["category"] in recent_categories:
            return 0

        return 1

    easy_questions.sort(
        key=diversity_score,
        reverse=True
    )

    medium_questions.sort(
        key=diversity_score,
        reverse=True
    )

    hard_questions.sort(
        key=diversity_score,
        reverse=True
    )

    # --------------------------------------------------
    # Build diverse candidate pool
    #
    # We intentionally expose multiple difficulties
    # to the Agent.
    # --------------------------------------------------

    candidates = []

    # Easy candidates
    candidates.extend(
        easy_questions[:5]
    )

    # Medium candidates
    candidates.extend(
        medium_questions[:6]
    )

    # Hard candidates
    candidates.extend(
        hard_questions[:4]
    )

    # --------------------------------------------------
    # If we have more than the limit, trim.
    # --------------------------------------------------

    candidates = candidates[:CANDIDATE_LIMIT]

    # --------------------------------------------------
    # Safety fallback
    # --------------------------------------------------

    if len(candidates) < CANDIDATE_LIMIT:

        existing_ids = {
            q["id"]
            for q in candidates
        }

        remaining = [
            q
            for q in available_questions
            if q["id"] not in existing_ids
        ]

        candidates.extend(
            remaining[
                :CANDIDATE_LIMIT - len(candidates)
            ]
        )

    return candidates


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
    # Prepare Candidate Questions
    # --------------------------------------------------

    candidate_questions = (
        prepare_candidate_questions(state)
    )

    if not candidate_questions:

        state["interview_finished"] = True

        return state

    # --------------------------------------------------
    # Prepare Questions For Agent
    # --------------------------------------------------

    question_options = []

    for question in candidate_questions:

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

                "category":
                    answer["category"],
            }
        )

    # --------------------------------------------------
    # Recent Categories
    # --------------------------------------------------

    recent_categories = [
        answer["category"]
        for answer in state["answers"][-3:]
    ]

    # --------------------------------------------------
    # Agent Prompt
    # --------------------------------------------------

    prompt = f"""
You are an adaptive technical interviewer.

Your job is to make the BEST possible decision
about the candidate's next interview question.

You have full responsibility for deciding:

1. The appropriate difficulty of the next question.
2. The technical area that should be assessed.
3. Which ONE question should be selected.

Candidate information:

{json.dumps(
        state["candidate"],
        ensure_ascii=False
    )}

Previous interview performance:

{json.dumps(
        previous_answers,
        ensure_ascii=False
    )}

Recently used categories:

{json.dumps(
        recent_categories,
        ensure_ascii=False
    )}

Current question difficulty:

{state["current_difficulty"]}

Candidate questions available for selection:

{json.dumps(
        question_options,
        ensure_ascii=False
    )}

IMPORTANT DECISION PRINCIPLES:

- You are NOT following a fixed difficulty progression.
- You decide the next difficulty based on the
  candidate's demonstrated ability.
- Correct answers may justify a harder question,
  but do not automatically require one.
- Incorrect answers may justify an easier question,
  but do not automatically require one.
- Consider the candidate's overall performance.
- Consider the difficulty of previous questions.
- Consider the technical categories already assessed.
- Prefer technical diversity when it improves the
  quality of the assessment.
- Avoid repeatedly testing the same technical category
  when other useful categories are available.
- Consider Hard questions when the candidate's
  demonstrated performance justifies deeper assessment.
- Do not avoid Hard questions merely because they are
  less numerous in the question bank.
- Do not artificially force an Easy, Medium, or Hard
  distribution.
- Do not artificially force an LLM/RAG distribution.
- Your objective is to maximize the information gained
  about the candidate's actual technical ability.

SELECTION RULES:

1. Select exactly ONE question.
2. The selected question MUST come from the candidate
   questions provided above.
3. Do not create a new question.
4. Do not select a previously asked question.
5. Return ONLY the question ID.
6. Do not return an explanation.

Think carefully about the candidate's ability,
difficulty, category diversity, and assessment value
before making the decision.

Return ONLY the selected question ID.
"""

    # --------------------------------------------------
    # Call Groq
    # --------------------------------------------------

    llm = get_llm()

    print(
        f"[PROMPT SIZE] "
        f"{len(prompt)} characters"
    )

    llm_start = time.perf_counter()

    response = llm.invoke(
        [
            HumanMessage(
                content=prompt
            )
        ]
    )

    llm_elapsed = (
        time.perf_counter()
        - llm_start
    )

    print(
        f"[LLM LATENCY] "
        f"{llm_elapsed:.2f} seconds"
    )

    print(
        f"[LLM RESPONSE] "
        f"{response.content}"
    )

    selected_id = (
        response.content.strip()
    )

    # --------------------------------------------------
    # Validate Agent Response
    # --------------------------------------------------

    selected_question = None

    for question in candidate_questions:

        if question["id"] == selected_id:

            selected_question = question

            break

    # --------------------------------------------------
    # Fallback
    # --------------------------------------------------

    if selected_question is None:

        selected_question = (
            candidate_questions[0]
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

    # IMPORTANT:
    #
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
