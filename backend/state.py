from typing import Optional, Tuple, Dict, Any, Literal
from typing_extensions import Annotated, TypedDict
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from dateutil import parser


# -------------------------------
# Pydantic Model (validation only)
# -------------------------------
class AstroStateModel(BaseModel):
    model_config = ConfigDict(extra="ignore")  # ignore unknown fields safely

    # User input
    name: Annotated[str, Field(..., min_length=2, description="Full name of the user")]
    dob: Annotated[str, Field(..., description="Date of birth (any format)")]
    time: Annotated[str, Field(..., description="Time of birth (any format, e.g. '5:30 am')")]
    place: Annotated[str, Field(..., min_length=2, description="Birthplace of the user")]

    # -------------------
    # Validators
    # -------------------
    @field_validator("dob", mode="before")
    @classmethod
    def normalize_dob(cls, v: str) -> str:
        """Accepts any common date format and converts to YYYY-MM-DD"""
        try:
            dt = parser.parse(v, dayfirst=False)  # handles '10 Jan 2001', '01/10/2001', etc.
            return dt.strftime("%Y-%m-%d")
        except Exception:
            raise ValueError("Invalid date format. Try like '2001-01-10' or '10 Jan 2001'.")

    @field_validator("time", mode="before")
    @classmethod
    def normalize_time(cls, v: str) -> str:
        """Accepts any common time format and converts to HH:MM (24hr)"""
        try:
            dt = parser.parse(v)
            return dt.strftime("%H:%M")
        except Exception:
            raise ValueError("Invalid time format. Try like '5:30 AM' or '17:30'.")


# -------------------------------
# LangGraph TypedDict (workflow state)
# -------------------------------
class AstroState(TypedDict, total=False):
    # User input
    name: Annotated[str, lambda a, b: b]   # overwrite with latest value
    dob: Annotated[str, lambda a, b: b]
    time: Annotated[str, lambda a, b: b]
    place: Annotated[str, lambda a, b: b]

    # Derived fields
    coordinates: Annotated[Tuple[float, float], lambda a, b: b] # Added reducer function
    timezone: Annotated[Optional[str], lambda a, b: b] # Added reducer function
    utc_time: Annotated[Optional[datetime], lambda a, b: b] # Added reducer function

    # Astrology outputs
    chart: Annotated[Optional[Dict[str, Any]], lambda a, b: b] # Added reducer function
    horoscope: Annotated[Optional[str], lambda a, b: b] # Added reducer function
    interpretation: Annotated[Optional[str], lambda a, b: b] # Added reducer function

    # System / workflow info
    db_saved: Annotated[bool, lambda a, b: b]
    status: Annotated[Literal["success", "error", "pending"], lambda a, b: b]
    error: Annotated[Optional[str], lambda a, b: b]


    # -------------------
    # Validators (flexible date/time parsing)
    # -------------------
    @field_validator("dob", mode="before")
    @classmethod
    def normalize_dob(cls, v: str) -> str:
        """Accepts any common date format and converts to YYYY-MM-DD"""
        try:
            dt = parser.parse(v, dayfirst=False)  # handles '10 Jan 2001', '01/10/2001', etc.
            return dt.strftime("%Y-%m-%d")
        except Exception:
            raise ValueError("Invalid date format. Try like '2001-01-10' or '10 Jan 2001'.")

    @field_validator("time", mode="before")
    @classmethod
    def normalize_time(cls, v: str) -> str:
        """Accepts any common time format and converts to HH:MM (24hr)"""
        try:
            dt = parser.parse(v)
            return dt.strftime("%H:%M")
        except Exception:
            raise ValueError("Invalid time format. Try like '5:30 AM' or '17:30'.")