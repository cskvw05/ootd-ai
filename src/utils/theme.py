import streamlit as st


def inject_custom_css():
    """Inject the full custom CSS theme for ooftd."""
    st.markdown(
        """
        <style>
        /* ===== IMPORTS ===== */
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

        /* ===== ROOT VARIABLES ===== */
        :root {
            --ooftd-purple: #7c3aed;
            --ooftd-pink: #ec4899;
            --ooftd-blue: #3b82f6;
            --ooftd-teal: #14b8a6;
            --ooftd-orange: #f97316;
            --ooftd-yellow: #eab308;
            --ooftd-dark: #0f0a1a;
            --ooftd-dark-card: #1a1128;
            --ooftd-dark-surface: #231a33;
            --ooftd-text: #e2e0ea;
            --ooftd-text-muted: #9a94a8;
            --gradient-primary: linear-gradient(135deg, #7c3aed 0%, #ec4899 50%, #f97316 100%);
            --gradient-blue: linear-gradient(135deg, #3b82f6 0%, #14b8a6 100%);
            --gradient-card: linear-gradient(145deg, rgba(124, 58, 237, 0.1), rgba(236, 72, 153, 0.05));
            --glass-bg: rgba(26, 17, 40, 0.7);
            --glass-border: rgba(124, 58, 237, 0.2);
        }

        /* ===== GLOBAL ===== */
        .stApp {
            background: var(--ooftd-dark) !important;
            font-family: 'Inter', sans-serif !important;
        }

        .stApp::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(ellipse at 20% 20%, rgba(124, 58, 237, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(59, 130, 246, 0.05) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }

        /* ===== SIDEBAR ===== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0a1a 0%, #1a1128 50%, #0f0a1a 100%) !important;
            border-right: 1px solid var(--glass-border) !important;
        }

        section[data-testid="stSidebar"] .stMarkdown h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700 !important;
        }

        section[data-testid="stSidebar"] .stSelectbox > div > div,
        section[data-testid="stSidebar"] .stMultiSelect > div > div,
        section[data-testid="stSidebar"] .stTextInput > div > div > input {
            background: var(--ooftd-dark-surface) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            color: var(--ooftd-text) !important;
            transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
        }

        section[data-testid="stSidebar"] .stSelectbox > div > div:focus-within,
        section[data-testid="stSidebar"] .stMultiSelect > div > div:focus-within,
        section[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
            border-color: var(--ooftd-purple) !important;
            box-shadow: 0 0 15px rgba(124, 58, 237, 0.3) !important;
        }

        /* Sidebar buttons (quick prompts) */
        section[data-testid="stSidebar"] .stButton > button {
            background: var(--gradient-card) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            color: var(--ooftd-text) !important;
            font-size: 0.82rem !important;
            padding: 10px 16px !important;
            transition: all 0.3s ease !important;
            text-align: left !important;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.25), rgba(236, 72, 153, 0.15)) !important;
            border-color: var(--ooftd-pink) !important;
            box-shadow: 0 4px 20px rgba(236, 72, 153, 0.2) !important;
            transform: translateY(-1px) !important;
        }

        /* ===== CHAT MESSAGES ===== */
        .stChatMessage {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin-bottom: 16px !important;
            animation: fadeSlideIn 0.4s ease-out !important;
        }

        /* User messages — blue gradient accent */
        .stChatMessage[data-testid="stChatMessage"]:has(.stChatMessageAvatarUser) {
            border-left: 3px solid transparent !important;
            border-image: var(--gradient-blue) 1 !important;
            border-image-slice: 1 !important;
        }

        /* Bot messages — purple-pink gradient accent */
        .stChatMessage[data-testid="stChatMessage"]:has(.stChatMessageAvatarAssistant),
        .stChatMessage[data-testid="stChatMessage"]:has(img) {
            border-left: 3px solid transparent !important;
            border-image: var(--gradient-primary) 1 !important;
            border-image-slice: 1 !important;
        }

        /* ===== CHAT INPUT ===== */
        .stChatInput {
            border-radius: 16px !important;
            overflow: hidden !important;
        }

        .stChatInput > div {
            background: var(--ooftd-dark-surface) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 16px !important;
            transition: all 0.3s ease !important;
        }

        .stChatInput > div:focus-within {
            border-color: var(--ooftd-purple) !important;
            box-shadow: 0 0 20px rgba(124, 58, 237, 0.25), 0 0 40px rgba(236, 72, 153, 0.1) !important;
        }

        .stChatInput textarea {
            color: var(--ooftd-text) !important;
            font-family: 'Inter', sans-serif !important;
        }

        .stChatInput textarea::placeholder {
            color: var(--ooftd-text-muted) !important;
        }

        /* ===== SPINNER ===== */
        .stSpinner > div {
            border-top-color: var(--ooftd-purple) !important;
        }

        .stSpinner > div > div {
            color: var(--ooftd-pink) !important;
            font-family: 'Space Grotesk', sans-serif !important;
        }

        /* ===== DIVIDERS ===== */
        hr {
            border-color: var(--glass-border) !important;
            opacity: 0.5 !important;
        }

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 6px;
        }
        ::-webkit-scrollbar-track {
            background: var(--ooftd-dark);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--glass-border);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--ooftd-purple);
        }

        /* ===== MULTISELECT TAGS ===== */
        span[data-baseweb="tag"] {
            background: linear-gradient(135deg, var(--ooftd-purple), var(--ooftd-pink)) !important;
            border-radius: 8px !important;
            border: none !important;
        }

        /* ===== SLIDER ===== */
        .stSlider > div > div > div > div {
            background: var(--gradient-primary) !important;
        }

        /* ===== ANIMATIONS ===== */
        @keyframes fadeSlideIn {
            from {
                opacity: 0;
                transform: translateY(12px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes glow {
            0%, 100% { box-shadow: 0 0 15px rgba(124, 58, 237, 0.3); }
            50% { box-shadow: 0 0 25px rgba(236, 72, 153, 0.4); }
        }

        /* ===== MARKDOWN IN CHAT ===== */
        .stChatMessage .stMarkdown {
            color: var(--ooftd-text) !important;
        }

        .stChatMessage .stMarkdown h1,
        .stChatMessage .stMarkdown h2,
        .stChatMessage .stMarkdown h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stChatMessage .stMarkdown strong {
            color: #c4b5fd !important;
        }

        .stChatMessage .stMarkdown em {
            color: #f9a8d4 !important;
        }

        .stChatMessage .stMarkdown code {
            background: var(--ooftd-dark-surface) !important;
            color: var(--ooftd-teal) !important;
            border-radius: 6px !important;
            padding: 2px 6px !important;
        }

        .stChatMessage .stMarkdown ul li::marker {
            color: var(--ooftd-pink) !important;
        }

        .stChatMessage .stMarkdown a {
            color: var(--ooftd-blue) !important;
            text-decoration: none !important;
        }

        .stChatMessage .stMarkdown a:hover {
            color: var(--ooftd-pink) !important;
            text-decoration: underline !important;
        }

        /* ===== CAPTION / MUTED TEXT ===== */
        .stCaption, small {
            color: var(--ooftd-text-muted) !important;
        }

        /* ===== HEADER AREA ===== */
        .ooftd-header {
            text-align: center;
            padding: 20px 0 10px 0;
            animation: fadeSlideIn 0.6s ease-out;
        }

        .ooftd-header h1 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 3rem !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #7c3aed, #ec4899, #f97316, #eab308);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift 4s ease infinite;
            margin-bottom: 0 !important;
        }

        .ooftd-subtitle {
            color: var(--ooftd-text-muted);
            font-size: 1rem;
            font-family: 'Inter', sans-serif;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 4px;
        }

        /* ===== WELCOME CARD ===== */
        .welcome-card {
            background: var(--gradient-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            margin: 20px auto;
            max-width: 700px;
            animation: fadeSlideIn 0.6s ease-out 0.2s both;
        }

        .welcome-card h3 {
            font-family: 'Space Grotesk', sans-serif;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.3rem;
            margin-bottom: 16px;
        }

        .welcome-card p {
            color: var(--ooftd-text);
            line-height: 1.6;
            font-size: 0.95rem;
        }

        .prompt-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 16px;
        }

        .prompt-chip {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(236, 72, 153, 0.1));
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 8px 16px;
            color: #c4b5fd;
            font-size: 0.85rem;
            cursor: default;
            transition: all 0.3s ease;
        }

        .prompt-chip:hover {
            border-color: var(--ooftd-pink);
            color: #f9a8d4;
            box-shadow: 0 2px 12px rgba(236, 72, 153, 0.2);
        }

        /* ===== FEATURE BADGES ===== */
        .feature-badges {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin: 16px 0;
        }

        .feature-badge {
            background: var(--ooftd-dark-surface);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 10px 18px;
            color: var(--ooftd-text);
            font-size: 0.82rem;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* ===== HIDE DEFAULT STREAMLIT ===== */
        #MainMenu, header[data-testid="stHeader"], footer {
            display: none !important;
        }

        .block-container {
            padding-top: 1rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """Render the animated ooftd header."""
    st.markdown(
        """
        <div class="ooftd-header">
            <h1>ooftd</h1>
            <div class="ooftd-subtitle">AI-Powered Fashion Intelligence</div>
        </div>
        <div class="feature-badges">
            <div class="feature-badge">\U0001f525 Trends</div>
            <div class="feature-badge">\U0001f30d Culture</div>
            <div class="feature-badge">\U0001f457 Outfits</div>
            <div class="feature-badge">\U0001f331 Brands</div>
            <div class="feature-badge">\U0001f3a8 Colors</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_welcome():
    """Render the welcome card with prompt suggestions."""
    st.markdown(
        """
        <div class="welcome-card">
            <h3>\u2728 Hey! I'm ooftd, your AI fashion research assistant</h3>
            <p>
                I can help you with fashion trends, cultural style guides, personalized outfits,
                brand ethics, color palettes, and more. Fill out the sidebar profile for
                personalized recommendations!
            </p>
            <div class="prompt-chips">
                <div class="prompt-chip">\U0001f4f1 TikTok trends</div>
                <div class="prompt-chip">\U0001f5fc Tokyo style guide</div>
                <div class="prompt-chip">\U0001f46b GenZ vs Millennial</div>
                <div class="prompt-chip">\U0001f331 Sustainable brands</div>
                <div class="prompt-chip">\U0001f3a8 Color palettes</div>
                <div class="prompt-chip">\U0001f48b Date night outfits</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
