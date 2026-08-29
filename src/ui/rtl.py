import streamlit as st


def apply_rtl():
    st.markdown(
        """
        <style>

        /* =========================================
           Global RTL
        ========================================= */

        .stApp {
            direction: rtl;
            text-align: right;
        }

        .main {
            direction: rtl;
            text-align: right;
        }

        [data-testid="stAppViewContainer"] {
            direction: rtl;
        }

        [data-testid="stMain"] {
            direction: rtl;
            text-align: right;
        }


        /* =========================================
           Soft White / Red Gradient Background
        ========================================= */

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(
                    circle at 8% 8%,
                    rgba(254, 226, 226, 0.75),
                    transparent 34%
                ),
                radial-gradient(
                    circle at 92% 88%,
                    rgba(255, 228, 230, 0.70),
                    transparent 36%
                ),
                radial-gradient(
                    circle at 50% 45%,
                    rgba(255, 247, 247, 0.75),
                    transparent 48%
                ),
                linear-gradient(
                    135deg,
                    #ffffff 0%,
                    #fff7f7 48%,
                    #ffffff 100%
                );

            background-attachment: fixed;
        }


        /* =========================================
           Streamlit Top Header
        ========================================= */

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stToolbar"] {
            background: transparent !important;
        }

        [data-testid="stDecoration"] {
            background: transparent !important;
        }


        /* =========================================
           Main Glass Container
           Compact Layout
        ========================================= */

        [data-testid="stMainBlockContainer"] {
            direction: rtl;

            max-width: 1080px;

            margin-top: 0.6rem;
            margin-bottom: 2rem;

            padding: 1.7rem 2.2rem 2.1rem 2.2rem;

            background: rgba(
                255,
                255,
                255,
                0.68
            );

            border: 1px solid rgba(
                255,
                255,
                255,
                0.82
            );

            border-radius: 22px;

            box-shadow:
                0 16px 40px rgba(
                    127,
                    29,
                    29,
                    0.06
                ),
                inset 0 1px 0 rgba(
                    255,
                    255,
                    255,
                    0.9
                );

            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }


        /* =========================================
           Main Vertical Spacing
        ========================================= */

        [data-testid="stVerticalBlock"] {
            gap: 0.65rem;
        }

        [data-testid="stHorizontalBlock"] {
            gap: 1rem;
        }


        /* =========================================
           Typography
        ========================================= */

        [data-testid="stMarkdownContainer"] {
            direction: rtl;
            text-align: right;
        }

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            direction: rtl;
            text-align: right;
        }

        h1 {
            font-size: 1.75rem !important;
            font-weight: 700 !important;

            letter-spacing: -0.3px;

            margin-top: 0 !important;
            margin-bottom: 0.15rem !important;

            line-height: 1.4 !important;
        }


        /* Section Titles */

        h2 {
            font-size: 1.25rem !important;
            font-weight: 700 !important;

            line-height: 1.5 !important;
        }

        h3 {
            font-size: 1.05rem !important;
            font-weight: 700 !important;

            line-height: 1.5 !important;
        }


        /* Normal Text */

        p {
            direction: rtl;
            text-align: right;

            font-size: 0.92rem !important;

            line-height: 1.65;

            margin-bottom: 0.3rem;
        }


        /* Labels */

        label {
            direction: rtl !important;
            text-align: right !important;

            font-size: 0.88rem !important;
        }


        /* =========================================
           Subheaders
        ========================================= */

        [data-testid="stSubheader"] {
            direction: rtl;
            text-align: right;

            font-size: 1.08rem;
            font-weight: 700;

            line-height: 1.6;

            margin-top: 0.75rem;
            margin-bottom: 0.35rem;
        }


        /* =========================================
           Input Fields
        ========================================= */

        input,
        textarea {
            direction: rtl !important;
            text-align: right !important;
        }

        [data-baseweb="input"],
        [data-baseweb="textarea"],
        [data-baseweb="select"] {
            border-radius: 10px !important;
        }


        /* =========================================
           Compact Input Height
        ========================================= */

        [data-baseweb="input"] input {
            padding-top: 0.55rem !important;
            padding-bottom: 0.55rem !important;
        }

        [data-baseweb="textarea"] textarea {
            padding-top: 0.55rem !important;
            padding-bottom: 0.55rem !important;
        }


        /* =========================================
           Selectbox
        ========================================= */

        [data-baseweb="select"] {
            direction: rtl;
            text-align: right;
        }

        [data-baseweb="select"] > div {
            direction: rtl;
            text-align: right;

            border-radius: 10px;
        }


        /* =========================================
           Radio Buttons
        ========================================= */

        [data-testid="stRadio"] {
            direction: rtl !important;
            text-align: right !important;
        }

        [data-testid="stRadio"] label {
            direction: rtl !important;
            text-align: right !important;

            margin-bottom: 3px;

            line-height: 1.5;

            color: #374151;
        }

        [data-testid="stRadio"] input[type="radio"] {
            accent-color: #dc2626 !important;
        }

        [data-testid="stRadio"] label:has(
            input[type="radio"]:checked
        ) {
            color: #991b1b !important;
        }

        [data-testid="stRadio"] label:hover {
            color: #991b1b !important;
        }


        /* =========================================
           Buttons
        ========================================= */

        button {
            direction: rtl !important;
            border-radius: 10px !important;
        }

        .stButton button {
            border-radius: 10px !important;

            min-height: 2.5rem;
        }


        /* =========================================
           Primary Button
        ========================================= */

        button[kind="primary"],
        button[data-testid="baseButton-primary"] {
            background-color: #dc2626 !important;
            border-color: #dc2626 !important;

            color: #ffffff !important;
        }

        button[kind="primary"]:hover,
        button[data-testid="baseButton-primary"]:hover {
            background-color: #b91c1c !important;
            border-color: #b91c1c !important;

            color: #ffffff !important;
        }


        /* =========================================
           Pills / Skills
        ========================================= */

        [data-testid="stPills"] {
            direction: rtl !important;
        }

        [data-testid="stPills"] button {
            border-radius: 9px !important;

            min-height: 2.15rem !important;

            padding: 0.25rem 0.7rem !important;

            background-color: rgba(
                255,
                255,
                255,
                0.70
            ) !important;

            border-color: rgba(
                153,
                27,
                27,
                0.15
            ) !important;

            color: #374151 !important;
        }


        /* Selected pill */

        [data-testid="stPills"]
        button[aria-pressed="true"] {
            background-color: #fee2e2 !important;

            border-color: #dc2626 !important;

            color: #991b1b !important;

            box-shadow:
                0 2px 7px rgba(
                    153,
                    27,
                    27,
                    0.07
                );
        }


        /* Selected pill hover */

        [data-testid="stPills"]
        button[aria-pressed="true"]:hover {
            background-color: #fecaca !important;

            border-color: #b91c1c !important;

            color: #7f1d1d !important;
        }


        /* Unselected pill hover */

        [data-testid="stPills"] button:hover {
            border-color: #f87171 !important;

            color: #991b1b !important;
        }


        /* =========================================
           Selectbox Focus
        ========================================= */

        [data-baseweb="select"]:focus-within {
            border-color: #dc2626 !important;

            box-shadow:
                0 0 0 1px #dc2626 !important;
        }


        /* =========================================
           Text Input Focus
        ========================================= */

        [data-baseweb="input"]:focus-within {
            border-color: #dc2626 !important;

            box-shadow:
                0 0 0 1px #dc2626 !important;
        }


        /* =========================================
           Textarea Focus
        ========================================= */

        [data-baseweb="textarea"]:focus-within {
            border-color: #dc2626 !important;

            box-shadow:
                0 0 0 1px #dc2626 !important;
        }


        /* =========================================
           Expanders
        ========================================= */

        [data-testid="stExpander"] {
            direction: rtl;
            text-align: right;

            border-radius: 10px;

            background: rgba(
                255,
                255,
                255,
                0.40
            );

            border: 1px solid rgba(
                153,
                27,
                27,
                0.07
            );

            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }


        /* =========================================
           Alerts / Messages
        ========================================= */

        [data-testid="stAlert"] {
            direction: rtl;
            text-align: right;

            border-radius: 12px;
        }


        /* =========================================
           Success Alert
           Red / White Glass Style
        ========================================= */

        [data-testid="stAlert"][data-baseweb="notification"] {
            background:
                linear-gradient(
                    135deg,
                    rgba(255, 255, 255, 0.78),
                    rgba(254, 242, 242, 0.86)
                ) !important;

            border: 1px solid rgba(
                220,
                38,
                38,
                0.18
            ) !important;

            color: #991b1b !important;

            box-shadow:
                0 8px 25px rgba(
                    127,
                    29,
                    29,
                    0.06
                );

            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        [data-testid="stAlert"][data-baseweb="notification"] p {
            color: #991b1b !important;
        }


        /* =========================================
           Main Streamlit Sidebar
           Glass Effect
        ========================================= */

        [data-testid="stSidebar"] {
            direction: rtl;
            text-align: right;

            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.72),
                    rgba(255, 245, 245, 0.58)
                ) !important;

            border-left: 1px solid rgba(
                153,
                27,
                27,
                0.08
            );

            box-shadow:
                0 10px 35px rgba(
                    127,
                    29,
                    29,
                    0.05
                );

            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }

        [data-testid="stSidebar"] * {
            direction: rtl;
            text-align: right;
        }


        /* =========================================
           Sidebar Navigation
        ========================================= */

        [data-testid="stSidebarNav"] {
            background: transparent !important;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 10px !important;

            margin: 3px 6px !important;

            transition:
                background-color 0.2s ease,
                color 0.2s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: rgba(
                254,
                226,
                226,
                0.65
            ) !important;
        }

        [data-testid="stSidebarNav"]
        a[aria-current="page"] {
            background: rgba(
                254,
                226,
                226,
                0.85
            ) !important;

            color: #991b1b !important;
        }


        /* =========================================
           Progress
        ========================================= */

        [data-testid="stProgress"] {
            direction: rtl;
        }

        [data-testid="stProgress"]
        > div
        > div
        > div {
            background-color: #dc2626 !important;
        }


        /* =========================================
           Chat
        ========================================= */

        [data-testid="stChatMessage"] {
            direction: rtl;
            text-align: right;
        }

        [data-testid="stChatMessage"] p {
            direction: rtl;
            text-align: right;
        }


        /* =========================================
           Dividers
        ========================================= */

        hr {
            margin-top: 0.55rem !important;
            margin-bottom: 0.55rem !important;
        }


        /* =========================================
           Mobile Responsive
        ========================================= */

        @media (max-width: 768px) {

            [data-testid="stMainBlockContainer"] {
                margin-top: 0;
                margin-bottom: 0;

                padding: 1.2rem 1rem 1.7rem 1rem;

                border-radius: 0;
            }

            h1 {
                font-size: 1.8rem !important;
            }

            [data-testid="stHorizontalBlock"] {
                gap: 0.7rem;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )
