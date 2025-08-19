from backend.state import AstroState
from tools.timezone_lookup import to_utc

def time_conversion(state: AstroState) -> dict:
    if not (state.get("coordinates") and state.get("timezone")):
        return {}
    try:
        utc_time = to_utc(state.get("dob"), state.get("time"), state.get("timezone"))
        return {"utc_time": utc_time}
    except Exception as e:
        return {"status": "error", "error": f"Time conversion failed: {e}"}
