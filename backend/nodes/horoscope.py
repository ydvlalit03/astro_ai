from backend.state import AstroState

def daily_horoscope(state: AstroState) -> AstroState:
    if not state.get("chart"):
        return state
    sun = state.get("chart").get("sun", {}).get("sign", "")
    tips = {
        "Cap": "Plan your week and take one solid step today.",
        "Tau": "Prioritize comfort but don’t skip the small risk.",
    }
    state["horoscope"] = tips.get(sun, "Focus on consistency and small wins today.")
    return state