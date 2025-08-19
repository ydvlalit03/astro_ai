from typing import Dict, Any
from kerykeion import AstrologicalSubject

def compute_natal_chart(name: str, year: int, month: int, day: int, hour: int, minute: int, lat: float, lon: float, tz_str: str) -> Dict[str, Any]:
    """Compute natal chart using Kerykeion."""

    # Create subject (person for whom chart is calculated)
    chart = AstrologicalSubject(name, year, month, day, hour, minute, lat=lat, lng=lon, tz_str=tz_str)

    # Extract data
    ascendant = chart.first_house.sign
    sun = chart.sun
    moon = chart.moon

    # Houses data
    house_names = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth"]
    houses_data = {}
    for i, name in enumerate(house_names):
        house_number = i + 1
        house_attribute = f"{name}_house"
        house_object = getattr(chart, house_attribute)
        houses_data[str(house_number)] = house_object.sign

    return {
        "ascendant": ascendant,
        "sun": {"sign": sun.sign, "degree": sun.position},
        "moon": {"sign": moon.sign, "degree": moon.position},
        "houses": houses_data,
    }