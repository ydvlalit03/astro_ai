from backend.state import AstroState
from tools.astro_engine import compute_natal_chart
from datetime import datetime

def natal_chart(state: AstroState) -> dict:
    print(f"DEBUG: natal_chart - state.get('coordinates'): {state.get('coordinates')}")
    print(f"DEBUG: natal_chart - state.get('utc_time'): {state.get('utc_time')}")
    print(f"DEBUG: natal_chart - state.get('name'): {state.get('name')}")
    print(f"DEBUG: natal_chart - state.get('dob'): {state.get('dob')}")
    print(f"DEBUG: natal_chart - state.get('time'): {state.get('time')}")
    print(f"DEBUG: natal_chart - state.get('place'): {state.get('place')}")

    required_fields = ["coordinates", "utc_time", "name", "dob", "time", "timezone"]
    if not all(state.get(field) for field in required_fields):
        print("DEBUG: natal_chart - Missing required state fields, returning early.")
        return {}

    name = state.get("name")
    dob_str = state.get("dob")
    time_str = state.get("time")
    lat, lon = state.get("coordinates")
    tz_str = state.get("timezone")

    # Parse DOB and time
    dob_datetime = datetime.strptime(dob_str, "%Y-%m-%d")
    time_datetime = datetime.strptime(time_str, "%H:%M")

    year = dob_datetime.year
    month = dob_datetime.month
    day = dob_datetime.day
    hour = time_datetime.hour
    minute = time_datetime.minute

    chart = compute_natal_chart(name, year, month, day, hour, minute, lat=lat, lon=lon, tz_str=tz_str)
    return {"chart": chart}
