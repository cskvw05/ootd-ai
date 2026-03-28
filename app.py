import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from src.crew import OoftdCrew
from src.utils.session import init_session, get_user_profile, QUICK_PROMPTS
from src.utils.formatters import format_profile_summary
from src.utils.theme import inject_custom_css, render_header, render_welcome

# --- Page Config ---
st.set_page_config(
    page_title="ooftd",
    page_icon="\ud83d\udc57",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Inject Theme ---
inject_custom_css()

# --- Session Init ---
init_session()

# --- Sidebar ---
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 10px 0;">
            <span style="font-size: 2.5rem;">
                \ud83d\udc57
            </span>
            <h2 style="
                font-family: 'Space Grotesk', sans-serif;
                background: linear-gradient(135deg, #7c3aed, #ec4899);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 4px 0 0 0;
                font-weight: 700;
            ">ooftd</h2>
            <p style="color: #9a94a8; font-size: 0.8rem; margin-top: 2px;">
                AI Fashion Intelligence
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    profile = get_user_profile()

    st.divider()
    st.markdown("### Quick Questions")
    for prompt in QUICK_PROMPTS:
        if st.button(prompt, key=f"quick_{prompt}", use_container_width=True):
            st.session_state.pending_prompt = prompt

    st.divider()
    st.markdown(
        """
        <div style="
            background: linear-gradient(145deg, rgba(124,58,237,0.1), rgba(236,72,153,0.05));
            border: 1px solid rgba(124,58,237,0.2);
            border-radius: 12px;
            padding: 14px;
            margin-top: 8px;
        ">
            <p style="color: #c4b5fd; font-size: 0.78rem; margin: 0 0 6px 0; font-weight: 600;">
                \ud83c\udfaf Your Profile
            </p>
            <p style="color: #9a94a8; font-size: 0.75rem; margin: 0; line-height: 1.5;">
                """ + format_profile_summary(profile).replace("|", "<br>") + """
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Main Chat Area ---
render_header()

# Welcome card
if not st.session_state.messages:
    render_welcome()

# Display chat history
for msg in st.session_state.messages:
    avatar = "\ud83d\udc57" if msg["role"] == "assistant" else "\ud83d\udc64"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Handle input (chat input or quick prompt)
user_input = st.chat_input("Ask me anything about fashion... \u2728")

if st.session_state.get("pending_prompt"):
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="\ud83d\udc64"):
        st.markdown(user_input)

    # Run crew and display response
    with st.chat_message("assistant", avatar="\ud83d\udc57"):
        with st.spinner("\u2728 Researching fashion insights... hang tight!"):
            try:
                crew = OoftdCrew()
                result = crew.kickoff(
                    inputs={
                        "query": user_input,
                        "user_profile": profile,
                    }
                )
                st.markdown(result)
                st.session_state.messages.append({"role": "assistant", "content": result})
            except Exception as e:
                error_msg = (
                    f"\u26a0\ufe0f **Oops!** Something went wrong:\n\n"
                    f"`{str(e)}`\n\n"
                    f"Please check your API keys in the `.env` file and try again."
                )
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
