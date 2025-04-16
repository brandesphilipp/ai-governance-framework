from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from . import tools  # Import the tools package

# Define the model for this agent (consistent with others)
# Use 'model' argument instead of 'model_name'
AGENT_MODEL = LiteLlm(model="openai/gpt-4.1-mini")

# Define the BASE Value Soul Agent definition
# This can be used to instantiate multiple instances if needed.
value_soul_agent_base = Agent(
    name="ValueSoulAgent", # Keep the functional name
    description="Evaluates plans and decisions against core values defined in partnership agreements",
    model=AGENT_MODEL,
    tools=[
        tools.read_partnership_documents, # Assign the specific tool
    ],
    instruction=(
        "Your role is to consult the partnership documents (agreement or companion) "
        "when requested. Use the 'read_partnership_documents' tool to fetch the "
        "content of the specified document ('agreement' or 'companion'). "
        "Present the retrieved information clearly. If the tool fails, report the error."
    )
)
