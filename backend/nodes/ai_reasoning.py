from backend.state import AstroState
from tools.gemini_client import generate_interpretation

def ai_reasoning(state: AstroState) -> AstroState:
    if not state.get("chart"):
        print("DEBUG: Chart not available in state, returning early from ai_reasoning.")
        return state
    print(f"DEBUG: Chart data in ai_reasoning before calling generate_interpretation: {state.get("chart")}")
    text = generate_interpretation(
        name=state.get("name"),
        dob=state.get("dob"),
        time=state.get("time"),
        place=state.get("place"),
        chart=state.get("chart"),
        utc_iso=(state.get("utc_time").isoformat() if state.get("utc_time") else ""),
    )
    state["interpretation"] = text
    return state