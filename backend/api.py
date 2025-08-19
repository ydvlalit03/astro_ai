from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import traceback

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.state import AstroStateModel, AstroState
from backend.graph import app
from tools.gemini_client import generate_interpretation, genai, MODEL

# FastAPI app
api = FastAPI(title="Astro AI API", description="Astrology readings and Q&A")

# Enable CORS for frontend
api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",  # Vite sometimes uses this port
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Request models
class BirthChartRequest(BaseModel):
    name: str
    dob: str  # Date of birth
    time: str  # Time of birth
    place: str  # Place of birth

class QuestionRequest(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None  # Optional birth chart context

# Response models
class BirthChartResponse(BaseModel):
    name: str
    chart: Optional[Dict[str, Any]]
    horoscope: Optional[str]
    interpretation: Optional[str]
    timezone: Optional[str]
    utc_time: Optional[str]
    status: str
    error: Optional[str] = None

class QuestionResponse(BaseModel):
    question: str
    answer: str
    status: str
    error: Optional[str] = None

@api.get("/")
async def root():
    return {"message": "Astro AI API is running"}

@api.post("/birth-chart", response_model=BirthChartResponse)
async def get_birth_chart(request: BirthChartRequest):
    """Generate birth chart and interpretation"""
    try:
        # Validate input using existing Pydantic model
        astro = AstroStateModel(
            name=request.name,
            dob=request.dob,
            time=request.time,
            place=request.place
        )
        
        # Convert to LangGraph state
        state: AstroState = astro.model_dump()
        
        # Run the existing LangGraph workflow
        result = app.invoke(state)
        
        # Handle utc_time - it might be a datetime object or already a string
        utc_time_value = result.get("utc_time")
        if utc_time_value:
            if hasattr(utc_time_value, 'isoformat'):
                utc_time_str = utc_time_value.isoformat()
            else:
                utc_time_str = str(utc_time_value)
        else:
            utc_time_str = None
            
        return BirthChartResponse(
            name=result.get("name", ""),
            chart=result.get("chart"),
            horoscope=result.get("horoscope"),
            interpretation=result.get("interpretation"),
            timezone=result.get("timezone"),
            utc_time=utc_time_str,
            status=result.get("status", "success"),
            error=result.get("error")
        )
        
    except Exception as e:
        print(f"Error in birth-chart endpoint: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))

@api.post("/ask-question", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Answer astrology-related questions"""
    try:
        # Create context-aware prompt
        context_str = ""
        if request.context and request.context.get("chart"):
            chart = request.context["chart"]
            context_str = f"""
            Birth Chart Context:
            - Name: {request.context.get('name', 'Unknown')}
            - Ascendant: {chart.get('ascendant', 'Unknown')}
            - Sun Sign: {chart.get('sun', {}).get('sign', 'Unknown')}
            - Moon Sign: {chart.get('moon', {}).get('sign', 'Unknown')}
            """
        
        prompt = f"""You are an expert Vedic astrologer. Answer the following question with accurate astrological insights.
        
        {context_str}
        
        Question: {request.question}
        
        Please provide a helpful, informative response based on astrological principles."""
        
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        
        answer = response.text.strip() if response.text else "I apologize, but I couldn't generate a response to your question. Please try rephrasing it."
        
        return QuestionResponse(
            question=request.question,
            answer=answer,
            status="success"
        )
        
    except Exception as e:
        print(f"Error in ask-question endpoint: {traceback.format_exc()}")
        return QuestionResponse(
            question=request.question,
            answer=f"I'm sorry, but I encountered an error while processing your question: {str(e)}",
            status="error",
            error=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)