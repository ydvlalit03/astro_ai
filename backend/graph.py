from langgraph.graph import StateGraph, END
from backend.state import AstroState
from backend.nodes.validation import input_validation, error_handler
from backend.nodes.geocoding import geocoding
from backend.nodes.timezone import time_conversion
from backend.nodes.astrology import natal_chart
from backend.nodes.horoscope import daily_horoscope
from backend.nodes.ai_reasoning import ai_reasoning
from backend.nodes.database import database_node
from backend.nodes.aggregator import response_aggregator


# Build graph
graph = StateGraph(AstroState)

# Nodes
graph.add_node("Input Validation", input_validation)
graph.add_node("Error Handler", error_handler)
graph.add_node("Geocoding", geocoding)
graph.add_node("Time Conversion", time_conversion)
graph.add_node("Natal Chart", natal_chart)
graph.add_node("Daily Horoscope", daily_horoscope)
graph.add_node("AI Reasoning", ai_reasoning)
graph.add_node("Database", database_node)
graph.add_node("Response Aggregator", response_aggregator)

# Entry
graph.set_entry_point("Input Validation")

# Conditional from validation -> either geocoding or error
def _ok_or_error(state: AstroState) -> str:
    return "Error Handler" if state.get("status") == "error" else "Geocoding"

graph.add_conditional_edges(
    "Input Validation",
    _ok_or_error,
    {"Error Handler": "Error Handler", "Geocoding": "Geocoding"},
)

# Sequential flow
graph.add_edge("Geocoding", "Time Conversion")
graph.add_edge("Time Conversion", "Natal Chart")

# Post-chart parallel
graph.add_edge("Natal Chart", "Daily Horoscope")
graph.add_edge("Natal Chart", "AI Reasoning")

# Finalization parallel
graph.add_edge("Daily Horoscope", "Database")
graph.add_edge("AI Reasoning", "Database")

# Database to Aggregator to END
graph.add_edge("Database", "Response Aggregator")
graph.add_edge("Response Aggregator", END)

# Error path
graph.add_edge("Error Handler", END)

app = graph.compile()