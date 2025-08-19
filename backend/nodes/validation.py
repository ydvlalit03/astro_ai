from backend.state import AstroState

def input_validation(state: AstroState) -> AstroState:
    # Pydantic already normalizes dob/time via validators when state is built
    state["status"] = "success"
    return state

def error_handler(state: AstroState) -> AstroState:
    if state.get("status") == "error" and not state.get("interpretation"):
        state["interpretation"] = f"⚠️ {state.get('error') or 'Unknown error'}"
    return state