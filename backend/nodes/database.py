import os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from backend.state import AstroState

DB_URL = os.getenv("DATABASE_URL", "sqlite:///data/sqlite.db")
engine = create_engine(DB_URL, echo=False, future=True)

# Init tables (simple schema)
with engine.begin() as conn:
    conn.exec_driver_sql(
        """
        CREATE TABLE IF NOT EXISTS readings (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          dob TEXT,
          time TEXT,
          place TEXT,
          lat REAL,
          lon REAL,
          timezone TEXT,
          utc_time TEXT,
          chart_json TEXT,
          horoscope TEXT,
          interpretation TEXT,
          created_at TEXT
        );
        """
    )

def database_node(state: AstroState) -> AstroState:
    try:
        lat, lon = (state.get("coordinates") or (None, None))
        utc_time_iso = state.get("utc_time").isoformat() if state.get("utc_time") else None
        chart_str = str(state.get("chart")) if state.get("chart") else None

        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                    INSERT INTO readings
                    (name, dob, time, place, lat, lon, timezone, utc_time, chart_json, horoscope, interpretation, created_at)
                    VALUES (:name, :dob, :time, :place, :lat, :lon, :timezone, :utc_time, :chart_json, :horoscope, :interpretation, :created_at)
                    """
                ),
                {
                    "name": state.get("name"),
                    "dob": state.get("dob"),
                    "time": state.get("time"),
                    "place": state.get("place"),
                    "lat": lat,
                    "lon": lon,
                    "timezone": state.get("timezone"),
                    "utc_time": utc_time_iso,
                    "chart_json": chart_str,
                    "horoscope": state.get("horoscope"),
                    "interpretation": state.get("interpretation"),
                    "created_at": datetime.utcnow().isoformat(),
                },
            )
        state["db_saved"] = True
    except SQLAlchemyError as e:
        state["db_saved"] = False
        state["status"] = "error"
        state["error"] = f"DB error: {e}"
    return state
