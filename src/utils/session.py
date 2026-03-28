import streamlit as st

QUICK_PROMPTS = [
    "What's trending on TikTok right now?",
    "What should I wear in Tokyo in spring?",
    "GenZ vs Millennial fashion — what's the difference?",
    "Sustainable fashion brands I should know about",
    "Date night outfit ideas on a budget",
    "What are the color trends for 2026?",
]


def init_session():
    """Initialize Streamlit session state with defaults."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


def get_user_profile() -> dict:
    """Render the sidebar profile form and return the user profile dict."""
    st.markdown("### About You")
    st.caption("Help ooftd personalize your fashion advice")

    body_type = st.selectbox(
        "Body Type",
        ["Not specified", "Petite", "Tall", "Athletic", "Curvy", "Plus-size", "Slim", "Average"],
        index=0,
    )

    styles = st.multiselect(
        "Preferred Styles",
        [
            "Casual", "Streetwear", "Minimalist", "Bohemian", "Classic/Preppy",
            "Edgy/Punk", "Romantic/Feminine", "Sporty/Athleisure", "Vintage",
            "Quiet Luxury", "Y2K", "Avant-garde", "Business/Professional",
        ],
    )

    budget = st.select_slider(
        "Budget Range",
        options=["$", "$$", "$$$", "$$$$"],
        value="$$",
        help="$ = Under $50 | $$ = $50-150 | $$$ = $150-400 | $$$$ = $400+",
    )

    gender_expression = st.selectbox(
        "Gender Expression",
        ["Not specified", "Feminine", "Masculine", "Androgynous", "Non-binary / Fluid"],
        index=0,
    )

    skin_tone = st.selectbox(
        "Skin Tone (for color advice)",
        ["Not specified", "Warm", "Cool", "Neutral", "Deep"],
        index=0,
    )

    location = st.text_input("Your Location", placeholder="e.g. New York, London, Mumbai")

    profile = {
        "body_type": body_type if body_type != "Not specified" else "",
        "styles": ", ".join(styles) if styles else "",
        "budget": budget,
        "gender_expression": gender_expression if gender_expression != "Not specified" else "",
        "skin_tone": skin_tone if skin_tone != "Not specified" else "",
        "location": location,
    }

    st.session_state.user_profile = profile
    return profile
