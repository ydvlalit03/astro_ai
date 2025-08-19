from backend.state import AstroState
def response_aggregator(state: AstroState) -> dict:
    return {
        "name": state.get("name"),
        "dob": state.get("dob"),
        "time": state.get("time"),
        "place": state.get("place"),
        "coordinates": state.get("coordinates"),
        "timezone": state.get("timezone"),
        "utc_time": state.get("utc_time").isoformat() if state.get("utc_time") else None,
        "chart": state.get("chart"),
        "horoscope": state.get("horoscope"),
        "interpretation": state.get("interpretation"),
        "db_saved": state.get("db_saved"),
        "status": state.get("status"),
        "error": state.get("error"),
    }
