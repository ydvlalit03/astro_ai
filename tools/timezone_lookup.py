import os, requests
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder

# TZ_API = os.getenv("GOOGLE_TIMEZONE_API_KEY")
_tf = TimezoneFinder()

def infer_timezone(lat: float, lon: float) -> str:
    tz = _tf.timezone_at(lng=lon, lat=lat)
    if not tz:
        tz = _tf.closest_timezone_at(lat=lat, lng=lon)
    if not tz:
        tz = "UTC"
    return tz

def to_utc(dob_iso: str, tob_iso: str, tz_name: str) -> datetime:
    local = pytz.timezone(tz_name)
    naive = datetime.strptime(f"{dob_iso} {tob_iso}", "%Y-%m-%d %H:%M")
    localized = local.localize(naive)
    return localized.astimezone(pytz.utc)