from src.ui.rtl import apply_rtl
import streamlit as st


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ارزیابی استخدامی هوشمند",
    # page_icon="🤖"
)

apply_rtl()


# --------------------------------------------------
# Page Header
# --------------------------------------------------

st.title("ارزیابی استخدامی")

st.write(
    "اطلاعات خود را تکمیل کنید تا ارزیابی شغلی شما آغاز شود."
)


# --------------------------------------------------
# Main Two-Column Layout
# --------------------------------------------------

left_col, right_col = st.columns(
    2,
    gap="large"
)


# ==================================================
# Personal Information
# ==================================================

with left_col:

    st.subheader(
        "اطلاعات فردی"
    )

    # --------------------------------------------------
    # Name
    # --------------------------------------------------

    name = st.text_input(
        "نام",
        placeholder="نام خود را برای شروع مصاحبه وارد کنید"
    )

    # --------------------------------------------------
    # Work Experience
    # --------------------------------------------------

    experience = st.radio(
        "سابقه کاری:",
        options=[
            "بدون سابقه کاری",
            "۱ تا ۳ سال",
            "۳ تا ۶ سال",
            "بیش از ۶ سال"
        ],
        horizontal=True
    )

    # --------------------------------------------------
    # Skills
    # --------------------------------------------------

    skills = st.pills(
        "مهارت‌ها:",
        options=[
            "Python",
            "Documentation",
            "LLM APIs",
            "Prompt Design",
            "NLP",
            "Testing",
            "Cloud",
            "Vector DBs",
            "Prompt Engineering",
            "Fine-tuning",
            "Embeddings",
            "LLMs",
            "Search Systems",
            "LangChain",
        ],
        selection_mode="multi",
        default=[],
    )


# ==================================================
# Job Information
# ==================================================

with right_col:

    st.subheader(
        "اطلاعات شغلی"
    )

    # --------------------------------------------------
    # Job Level
    # --------------------------------------------------

    level = st.radio(
        "سطح شغلی:",
        options=[
            "Junior",
            "Mid-level",
            "Senior"
        ],
        horizontal=True
    )

    # --------------------------------------------------
    # Position
    # --------------------------------------------------

    position = st.selectbox(
        "موقعیت شغلی:",
        options=[
            "LLM Engineer",
            "Generative AI Engineer",
            "RAG Engineer",
            "Prompt Engineer"
        ],
        index=None,
        placeholder="موقعیت شغلی را انتخاب کنید"
    )

    # --------------------------------------------------
    # Company
    # --------------------------------------------------

    company = st.selectbox(
        "شرکت:",
        options=[
            "Amazon",
            "Meta",
            "Udemy",
            "365 Company",
            "Nestle",
            "LinkedIn",
            "Spotify"
        ],
        index=None,
        placeholder="شرکت را انتخاب کنید"
    )

    # --------------------------------------------------
    # Assessment Preview
    # --------------------------------------------------

    st.divider()

    st.subheader(
        "خلاصه اطلاعات"
    )

    preview_col1, preview_col2 = st.columns(2)

    with preview_col1:

        st.write(
            f"**نام:** "
            f"{name if name else 'وارد نشده'}"
        )

        st.write(
            f"**سابقه کاری:** "
            f"{experience if experience else 'انتخاب نشده'}"
        )

        st.write(
            f"**مهارت‌ها:** "
            f"{', '.join(skills) if skills else 'انتخاب نشده'}"
        )

    with preview_col2:

        st.write(
            f"**سطح شغلی:** "
            f"{level}"
        )

        st.write(
            f"**موقعیت شغلی:** "
            f"{position if position else 'انتخاب نشده'}"
        )

        st.write(
            f"**شرکت:** "
            f"{company if company else 'انتخاب نشده'}"
        )


# --------------------------------------------------
# Start Assessment
# --------------------------------------------------

st.divider()

if st.button(
    "شروع ارزیابی",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------
    # Validate Information
    # --------------------------------------------------

    if not name.strip():

        st.error(
            "لطفاً نام خود را وارد کنید."
        )

    elif not experience:

        st.error(
            "لطفاً سابقه کاری خود را انتخاب کنید."
        )

    elif not skills:

        st.error(
            "لطفاً حداقل یک مهارت را انتخاب کنید."
        )

    elif not position:

        st.error(
            "لطفاً موقعیت شغلی را انتخاب کنید."
        )

    elif not company:

        st.error(
            "لطفاً شرکت را انتخاب کنید."
        )

    elif position == "Prompt Engineer":

        st.warning(
            "ارزیابی موقعیت شغلی Prompt Engineer "
            "در نسخه فعلی آماده نیست."
        )

    else:

        # --------------------------------------------------
        # Save Candidate Information
        # --------------------------------------------------

        st.session_state.candidate = {
            "name": name,
            "experience": experience,
            "skills": skills,
            "level": level,
            "position": position,
            "company": company
        }

        # --------------------------------------------------
        # Reset Assessment State
        # --------------------------------------------------

        st.session_state.current_question_index = 0
        st.session_state.answers = []
        st.session_state.selected_questions = []
        st.session_state.interview_started = True

        # --------------------------------------------------
        # Navigate to Assessment
        # --------------------------------------------------

        st.switch_page(
            "pages/interview.py"
        )
