from src.interview.state import InterviewState
from src.data.loader import QuestionLoader


def create_initial_state(
    candidate: dict
) -> InterviewState:

    # --------------------------------------------------
    # Load Question Banks
    # --------------------------------------------------

    loader = QuestionLoader()

    llm_questions = loader.load(
        "data/llm_interview_questions.json"
    )

    rag_questions = loader.load(
        "data/rag_interview_questions.json"
    )

    # --------------------------------------------------
    # Combine Question Banks
    # --------------------------------------------------

    question_bank = (
        llm_questions + rag_questions
    )

    # --------------------------------------------------
    # Initial State
    # --------------------------------------------------

    return {
        "candidate": candidate,

        "question_bank": question_bank,

        "selected_questions": [],

        "current_question": None,

        "current_question_index": 0,

        "current_difficulty": "easy",

        "user_answer": None,

        "answers": [],

        "question_count": 0,

        "interview_finished": False,
    }
