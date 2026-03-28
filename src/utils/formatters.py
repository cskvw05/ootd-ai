def format_profile_summary(profile: dict) -> str:
    """Create a readable summary of the user profile for display."""
    parts = []
    if profile.get("body_type"):
        parts.append(f"Body: {profile['body_type']}")
    if profile.get("styles"):
        parts.append(f"Style: {profile['styles']}")
    if profile.get("budget"):
        parts.append(f"Budget: {profile['budget']}")
    if profile.get("gender_expression"):
        parts.append(f"Expression: {profile['gender_expression']}")
    if profile.get("skin_tone"):
        parts.append(f"Skin tone: {profile['skin_tone']}")
    if profile.get("location"):
        parts.append(f"Location: {profile['location']}")
    return " | ".join(parts) if parts else "No profile set — fill out the sidebar for personalized advice!"
