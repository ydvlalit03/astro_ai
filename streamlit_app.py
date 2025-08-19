import streamlit as st
import datetime
from backend.state import AstroStateModel, AstroState
from backend.graph import app


with st.form("birth_form"):
    name = st.text_input("Name", value="Lalit Rao")
    dob_date = st.date_input("Date of Birth", value=datetime.date(2001, 1, 10))
    tob_time = st.time_input("Time of Birth", value=datetime.time(5, 30))
    dob = dob_date.strftime("%Y-%m-%d")
    tob = tob_time.strftime("%H:%M")
    place = st.text_input("Place of Birth", value="Delhi, India")
    submitted = st.form_submit_button("Get Reading")

if submitted:
    try:
        # 1. Validate + normalize input using Pydantic
        astro = AstroStateModel(name=name, dob=dob, time=tob, place=place)

        # 2. Convert to dict for LangGraph state
        state: AstroState = astro.model_dump()

        # 3. Run graph
        result = app.invoke(state)

        # 4. Show results
        st.subheader("🌀 Your Natal Chart")
        st.json(result.get("chart") or {"info": "Chart not available"})

        st.subheader("🌟 Daily Horoscope")
        st.write(result.get("horoscope") or "—")

        st.subheader("📖 Interpretation")
        st.write(result.get("interpretation") or "—")

        st.caption(f"Time Zone: {result.get('timezone')} • UTC: {result.get('utc_time')}")
        if result.get("status") == "error":
            st.error(f"Error: {result.get('error')}")
        st.caption(f"Status: {result.get('status')} • DB Saved: {result.get('db_saved')}")

    except Exception as e:
        st.error(f"Error: {e}")
