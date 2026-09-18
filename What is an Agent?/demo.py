from strands import Agent, tool
from strands.models.anthropic import AnthropicModel

# ---------------------------------------------------------
# THE "HANDS" — a real Python function the code can execute.
# The LLM will NEVER run this directly. It can only ask for it.
# ---------------------------------------------------------
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city.

    Args:
        city: The name of the city to check.
    """
    print(f"\n🔧 TOOL EXECUTING: get_weather(city='{city}')")
    print("   (this line only runs because the CODE decided to run it —")
    print("    the LLM only ever wrote a request in plain text)\n")

    # Mocked data so this runs instantly with no extra API key needed.
    # In a real app, this line would call a real weather API instead.
    weather_data = {
        "boston": "68°F, partly cloudy",
        "mumbai": "89°F, humid and sunny",
        "london": "59°F, light rain",
    }
    return weather_data.get(city.lower(), "Weather data not available for this city.")


# ---------------------------------------------------------
# THE "BRAIN" — Claude, connected through Strands.
# ---------------------------------------------------------
model = AnthropicModel(
    client_args={
        "api_key": "YOUR_ANTHROPIC_API_KEY",  # or read from an env variable
    },
    max_tokens=1028,
    model_id="claude-sonnet-4-6",  # check docs.anthropic.com if this changes
    params={"temperature": 0.7},
)

agent = Agent(model=model, tools=[get_weather])

# ---------------------------------------------------------
# Run it. Watch the console output during recording —
# the print statements above make the brain/hands handoff visible.
# ---------------------------------------------------------
response = agent("What's the weather like in Boston right now?")
print("\n💬 FINAL ANSWER FROM THE AGENT:\n", response)
