import streamlit as st
from src.ui.rtl import apply_rtl

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ارزیابی استخدامی هوشمند",
    # page_icon="🤖"
)
apply_rtl()

st.title("ارزیابی استخدامی")

st.write(
    "اطلاعات خود را تکمیل کنید تا ارزیابی شغلی شما آغاز شود."
)


# --------------------------------------------------
# Personal Information
# --------------------------------------------------

st.subheader(
    "اطلاعات فردی",
    divider="rainbow"
)

name = st.text_input(
    "نام",
    placeholder="مثلاً: علی رضایی"
)

with st.expander("💡 راهنمای این بخش"):

    st.write(
        "نامی را وارد کنید که می‌خواهید در فرآیند "
        "ارزیابی با آن شناخته شوید."
    )


experience = st.text_area(
    "سابقه کاری",
    placeholder=(
        "مثلاً: دو سال تجربه در Python و Machine Learning..."
    )
)

with st.expander("💡 راهنمای این بخش"):

    st.write(
        "به‌طور خلاصه درباره سابقه کاری خود بنویسید. "
        "می‌توانید نقش‌های قبلی، میزان تجربه و "
        "فناوری‌هایی که با آن‌ها کار کرده‌اید را ذکر کنید."
    )


skills = st.multiselect(
    "مهارت‌ها",
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
    placeholder="مهارت‌های خود را انتخاب کنید"
)

with st.expander("💡 راهنمای این بخش"):

    st.write(
        "مهارت‌هایی را انتخاب کنید که در آن‌ها "
        "تجربه یا دانش دارید. می‌توانید چند مهارت را "
        "به‌صورت هم‌زمان انتخاب کنید."
    )


# --------------------------------------------------
# Job Information
# --------------------------------------------------

st.subheader(
    "اطلاعات شغلی",
    divider="rainbow"
)

col1, col2 = st.columns(2)


with col1:

    level = st.radio(
        "سطح شغلی:",
        options=[
            "Junior",
            "Mid-level",
            "Senior"
        ]
    )


with col2:

    position = st.selectbox(
        "موقعیت شغلی:",
        options=[
            "LLM Engineer",
            "Generative AI Engineer",
            "RAG Engineer",
            "Prompt Engineer"
        ]
    )


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
    ]
)


# --------------------------------------------------
# Assessment Preview
# --------------------------------------------------

st.subheader(" خلاصه اطلاعات")

st.write(
    f"**نام:** "
    f"{name if name else 'وارد نشده'}"
)

st.write(
    f"**مهارت‌ها:** "
    f"{', '.join(skills) if skills else 'انتخاب نشده'}"
)

st.write(
    f"**سطح شغلی:** {level}"
)

st.write(
    f"**موقعیت شغلی:** {position}"
)

st.write(
    f"**شرکت:** {company}"
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

    elif not experience.strip():

        st.error(
            "لطفاً سابقه کاری خود را وارد کنید."
        )

    elif not skills:

        st.error(
            "لطفاً حداقل یک مهارت را انتخاب کنید."
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
