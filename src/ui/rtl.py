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
           Main Content
        ========================================= */

        [data-testid="stVerticalBlock"] {
            direction: rtl;
        }

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

        p {
            direction: rtl;
            text-align: right;
        }


        /* =========================================
           Sidebar
        ========================================= */

        [data-testid="stSidebar"] {
            direction: rtl;
            text-align: right;
        }

        [data-testid="stSidebar"] * {
            direction: rtl;
            text-align: right;
        }


        /* =========================================
           Input Fields
        ========================================= */

        input,
        textarea {
            direction: rtl !important;
            text-align: right !important;
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
        }


        /* =========================================
           Radio Buttons
        ========================================= */

        [data-testid="stRadio"] {
            direction: rtl;
            text-align: right;
        }

        [data-testid="stRadio"] label {
            direction: rtl;
            text-align: right;
        }


        /* =========================================
           Buttons
        ========================================= */

        button {
            direction: rtl;
        }


        /* =========================================
           Expanders
        ========================================= */

        [data-testid="stExpander"] {
            direction: rtl;
            text-align: right;
        }


        /* =========================================
           Alerts / Messages
        ========================================= */

        [data-testid="stAlert"] {
            direction: rtl;
            text-align: right;
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
           Progress
        ========================================= */

        [data-testid="stProgress"] {
            direction: rtl;
        }
        
        /* =========================================
          Question Title
          ========================================= */
          
          [data-testid="stSubheader"] {
          direction: rtl;
          text-align: right;
          font-size: 1.25rem;
          line-height: 1.8;
          }
          /* =========================================
            Radio Options
            ========================================= */
            [data-testid="stRadio"] label {
            direction: rtl;
            text-align: right;
            margin-bottom: 15px;
            line-height: 1.8;
          }
          
        </style>
        """,
        unsafe_allow_html=True
    )
