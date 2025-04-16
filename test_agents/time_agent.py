from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Import tools from the new package structure
from test_agents import tools

# Define which model to use
AGENT_MODEL = "openai/gpt-4.1-mini"  # You can use any model you prefer

# Define our time agent
# 
time_agent = Agent(
    name="TimeAgent",
    model=LiteLlm(model=AGENT_MODEL),
    description="Provides current time for specified time zone",
    instruction="""
    You are a helpful time assistant. Your primary goal is to provide the current time for given time zones or cities.
    
    When the user asks for a time in a specific city or time zone, you must use the get_current_time tool.
    
    Analyze the tool's response:
    - If the status is "error", inform the user politely about the error message.
    - If the status is "success", present the information clearly.
    
    Only use tools when appropriate for a time-related request.
    """,
    tools=[tools.get_current_time]
)
