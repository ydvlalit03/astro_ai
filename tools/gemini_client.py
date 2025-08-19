import os, google.generativeai as genai

genai.configure(api_key="AIzaSyDSJyT8iZ_3UgPeY6m5z-gogJGUp_lkf9o")
MODEL = "gemini-2.5-flash"
    

_prompt_template = (
    "You are an expert Vedic astrologer. Provide factual information about the provided astrological chart. "
    "Do not provide any interpretations or readings. "
    "User: {name}\nDOB: {dob} {time} ({place}) UTC: {utc}\n"
    "Chart: Ascendant={asc}, Sun={sun_sign}, Moon={moon_sign}. ")

def generate_interpretation(name: str, dob: str, time: str, place: str, chart: dict, utc_iso: str) -> str:
    print(f"DEBUG: Chart data received by generate_interpretation: {chart}")

    # Check for essential chart data
    if not all(chart.get(key) for key in ["ascendant", "sun", "moon"]):
        return "Error: Incomplete chart data. Cannot generate interpretation."

    # Extract sign information safely
    asc_sign = chart.get("ascendant")
    sun_data = chart.get("sun", {})
    moon_data = chart.get("moon", {})
    sun_sign = sun_data.get("sign")
    moon_sign = moon_data.get("sign")

    if not all([asc_sign, sun_sign, moon_sign]):
        return "Error: Missing essential astrological signs in chart data."

    prompt = _prompt_template.format(
        name=name,
        dob=dob,
        time=time,
        place=place,
        utc=utc_iso,
        asc=asc_sign,
        sun_sign=sun_sign,
        moon_sign=moon_sign,
    )
    print(f"DEBUG: Prompt sent to Gemini: {prompt}")
    model = genai.GenerativeModel(MODEL)
    try:
        resp = model.generate_content(prompt)
        print(f"DEBUG: Gemini API response: {resp}")
        try:
            return resp.text.strip()
        except Exception as e:
            # Check if there's a finish_reason that indicates a problem
            if resp.candidates and resp.candidates[0].finish_reason:
                return "I apologize, but I was unable to generate a reading at this time. The AI model stopped due to a content policy or safety concern. Please try again with a different request."
            else:
                return "I apologize, but I was unable to generate a reading at this time. The AI model did not return any content. Please try again."
    except Exception as e:
        return f"An error occurred during the Gemini API call: {e}. Please check your internet connection or API key."