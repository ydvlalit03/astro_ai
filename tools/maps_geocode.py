import os, requests
from typing import Tuple
from dotenv import load_dotenv

# Load .env file
#load_dotenv()



from typing import Tuple
from geopy.geocoders import Nominatim

# Initialize Nominatim geocoder (identify your app with user_agent)
geolocator = Nominatim(user_agent="astro_ai")

def geocode_place(place: str) -> Tuple[float, float]:
    """Geocode a place name into (latitude, longitude) using OpenStreetMap Nominatim."""
    location = geolocator.geocode(place)
    if not location:
        raise ValueError(f"Geocoding failed: Could not find location for '{place}'")
    return location.latitude, location.longitude
