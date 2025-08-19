from backend.state import AstroState
from tools.maps_geocode import geocode_place
from tools.timezone_lookup import infer_timezone

def geocoding(state: AstroState) -> dict:
    try:
        print(f"DEBUG: Geocoding - Input place: {state.get('place')}")
        lat, lon = geocode_place(state["place"])
        print(f"DEBUG: Geocoding - Received coordinates: ({lat}, {lon})")
        timezone = infer_timezone(lat, lon)
        print(f"DEBUG: Geocoding - Timezone inferred: {timezone}")
        return {"coordinates": (lat, lon), "timezone": timezone}
    except Exception as e:
        print(f"DEBUG: Geocoding - Error: {e}")
        return {"status": "error", "error": f"Geocoding failed: {e}"}
