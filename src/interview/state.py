from typing import TypedDict


class InterviewState(TypedDict):

    # --------------------------------------------------
    # Candidate
    # --------------------------------------------------

    candidate: dict

    # --------------------------------------------------
    # Question Bank
    # --------------------------------------------------

    question_bank: list

    # --------------------------------------------------
    # Questions
    # --------------------------------------------------

    selected_questions: list

    current_question: dict | None

    current_question_index: int

    current_difficulty: str

    # --------------------------------------------------
    # Answers
    # --------------------------------------------------

    user_answer: int | None

    answers: list

    # --------------------------------------------------
    # Interview
    # --------------------------------------------------

    question_count: int

    interview_finished: bool
