from strands import Agent, tool
from strands.models.anthropic import AnthropicModel

# THE HANDS — a real Python function. No print statements in here at all.
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city.

    Args:
        city: The name of the city to check.
    """
    weather_data = {
        "boston": "68°F, partly cloudy",
        "mumbai": "89°F, humid and sunny",
        "london": "59°F, light rain",
    }
    return weather_data.get(city.lower(), "Weather data not available for this city.")


# A small formatter for what Strands ALREADY tells us, live, as it happens.
# This function does not decide anything — it just labels events the SDK
# itself is sending us in real time. This is the proof: these labels are
# driven by Strands' own event stream, not something we injected.
def show_whats_happening(**event):
    if "current_tool_use" in event and event["current_tool_use"].get("name"):
        print(f"\n🔧 STRANDS JUST REPORTED A TOOL CALL: {event['current_tool_use']['name']}")
    elif "data" in event:
        print(event["data"], end="", flush=True)


model = AnthropicModel(
    client_args={"api_key": "YOUR_ANTHROPIC_API_KEY"},
    max_tokens=1028,
    model_id="claude-sonnet-4-6",  # check docs.anthropic.com if this changes
    params={"temperature": 0.7},
)

agent = Agent(model=model, tools=[get_weather], callback_handler=show_whats_happening)

agent("What's the weather like in Boston right now?")
