from src.interview.evaluator import Evaluator
from src.interview.session import create_initial_state
from src.interview.graph import build_interview_graph
from src.ui.rtl import apply_rtl
import streamlit as st


# --------------------------------------------------
# Persian Number Helper
# --------------------------------------------------

def to_persian_digits(value):
    translation = str.maketrans(
        "0123456789",
        "۰۱۲۳۴۵۶۷۸۹"
    )
    return str(value).translate(translation)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ارزیابی شغلی",

)

apply_rtl()

st.title("ارزیابی شغلی")


# --------------------------------------------------
# Check Candidate Information
# --------------------------------------------------

if "candidate" not in st.session_state:

    st.warning(
        "ابتدا اطلاعات ارزیابی را تکمیل کنید."
    )

    if st.button("← بازگشت به صفحه اصلی"):
        st.switch_page("app.py")

    st.stop()


candidate = st.session_state.candidate


# --------------------------------------------------
# Initialize Graph
# --------------------------------------------------

if "interview_graph" not in st.session_state:

    st.session_state.interview_graph = (
        build_interview_graph()
    )


graph = st.session_state.interview_graph


# --------------------------------------------------
# Initialize Interview State
# --------------------------------------------------

if "interview_state" not in st.session_state:

    st.session_state.interview_state = (
        create_initial_state(candidate)
    )

    # Select first question
    st.session_state.interview_state = (
        graph.invoke(
            st.session_state.interview_state
        )
    )


state = st.session_state.interview_state


# --------------------------------------------------
# Candidate Information
# --------------------------------------------------

with st.sidebar:

    st.subheader("👤 اطلاعات داوطلب")

    st.write(
        f"**نام:** {candidate['name']}"
    )

    st.write(
        f"**سطح:** {candidate['level']}"
    )

    st.write(
        f"**موقعیت:** {candidate['position']}"
    )

    st.write(
        f"**شرکت:** {candidate['company']}"
    )

    st.divider()

    if not state["interview_finished"]:

        question_count = to_persian_digits(
            state["question_count"]
        )

        st.write(
            f"سؤال "
            f"{question_count} "
            f"از ۱۰"
        )


# --------------------------------------------------
# Interview Completed
# --------------------------------------------------

if state["interview_finished"]:

    st.success(
        "ارزیابی شما با موفقیت به پایان رسید."
    )

    # --------------------------------------------------
    # Evaluate Interview
    # --------------------------------------------------

    evaluator = Evaluator(
        questions=state["question_bank"],
        answers=state["answers"]
    )

    result = evaluator.evaluate()

    # --------------------------------------------------
    # Overall Score
    # --------------------------------------------------

    st.subheader("نتیجه ارزیابی")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "امتیاز نهایی",
            f"{result['score']:.0f}%"
        )

    with col2:

        st.metric(
            "پاسخ‌های صحیح",
            f"{result['correct_answers']} "
            f"از "
            f"{result['total_questions']}"
        )

    # --------------------------------------------------
    # Difficulty Performance
    # --------------------------------------------------

    st.subheader(
        "📈 عملکرد بر اساس سطح سؤال"
    )

    difficulty_order = [
        "easy",
        "medium",
        "hard"
    ]

    difficulty_names = {
        "easy": "آسان",
        "medium": "متوسط",
        "hard": "سخت"
    }

    for difficulty in difficulty_order:

        if difficulty not in result[
            "difficulty_performance"
        ]:
            continue

        stats = result[
            "difficulty_performance"
        ][difficulty]

        correct = to_persian_digits(
            stats["correct"]
        )

        total = to_persian_digits(
            stats["total"]
        )

        score = to_persian_digits(
            f"{stats['score']:.0f}"
        )

        st.write(
            f"**{difficulty_names[difficulty]}** — "
            f"{correct} از "
            f"{total} "
            f"({score}٪)"
        )

        st.progress(
            stats["score"] / 100
        )

    st.stop()


# --------------------------------------------------
# Current Question
# --------------------------------------------------

current_question = (
    state["current_question"]
)

if current_question is None:

    st.error(
        "سؤالی برای نمایش وجود ندارد."
    )

    st.stop()


# --------------------------------------------------
# Progress
# --------------------------------------------------

question_number = (
    state["question_count"]
)

progress = question_number / 10

question_number_fa = to_persian_digits(
    question_number
)

st.progress(
    progress,
    text=(
        f"سؤال "
        f"{question_number_fa} "
        f"از ۱۰"
    )
)


# --------------------------------------------------
# Difficulty
# --------------------------------------------------

difficulty_labels = {
    "easy": "آسان",
    "medium": "متوسط",
    "hard": "سخت",
}

difficulty = difficulty_labels.get(
    state["current_difficulty"],
    state["current_difficulty"]
)

st.caption(
    f"سطح سؤال: {difficulty}"
)


# --------------------------------------------------
# Question
# --------------------------------------------------

st.subheader(
    current_question["question"]
)


# --------------------------------------------------
# Answer Options
# --------------------------------------------------

selected_option = st.radio(
    "پاسخ خود را انتخاب کنید:",
    options=current_question["options"],
    index=None,
    key=(
        f"question_"
        f"{current_question['id']}"
    )
)


# --------------------------------------------------
# Submit Answer
# --------------------------------------------------

if st.button(
    "ثبت پاسخ →",
    type="primary",
    use_container_width=True
):

    if selected_option is None:

        st.warning(
            "لطفاً یکی از گزینه‌ها را انتخاب کنید."
        )

        st.stop()

    # --------------------------------------------------
    # Convert Option To Index
    # --------------------------------------------------

    selected_index = (
        current_question["options"]
        .index(selected_option)
    )

    # --------------------------------------------------
    # Update State
    # --------------------------------------------------

    state["user_answer"] = (
        selected_index
    )

    # --------------------------------------------------
    # Evaluate + Agent Selects Next Question
    # --------------------------------------------------

    updated_state = graph.invoke(
        state
    )

    # --------------------------------------------------
    # Save State
    # --------------------------------------------------

    st.session_state.interview_state = (
        updated_state
    )

    # --------------------------------------------------
    # Refresh Page
    # --------------------------------------------------

    st.rerun()
