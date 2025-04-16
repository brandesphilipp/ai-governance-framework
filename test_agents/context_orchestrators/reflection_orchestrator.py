"""Defines the Reflection Context Orchestrator Agent.

This agent manages workflows related to the 'Reflection' governance context.
It identifies the specific reflection variant (e.g., Targeted Reflection,
Sentiment Gathering) and orchestrates calls to specialized agents (Business,
ValueSoul, TeamSpirit) and HITL tools to facilitate team learning and capture insights.
"""
import copy
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Import base agent definitions
from test_agents.business_agent import business_agent
from test_agents.value_soul_agent_base import value_soul_agent_base
from test_agents.team_spirit_agent_base import team_spirit_agent_base
from test_agents import tools # For HITL tools

# Define the model for this orchestrator
AGENT_MODEL = LiteLlm(model="openai/gpt-4.1-mini")

# Instantiate local copies for this context
reflection_business_agent = copy.deepcopy(business_agent)
reflection_value_soul_agent = copy.deepcopy(value_soul_agent_base)
reflection_team_spirit_agent = copy.deepcopy(team_spirit_agent_base)

# Define the Reflection Orchestrator Agent
reflection_orchestrator = Agent(
    name="ReflectionOrchestrator",
    description="Manages reflection processes, facilitating team learning, process improvement, and capturing insights.",
    model=AGENT_MODEL,
    instruction="""You are the Reflection Orchestrator. Your goal is to manage governance tasks related to reflection and learning.

1.  **Analyze the input** to determine the reflection variant:
    *   If it's a request to reflect on a specific event, meeting, or period, it's **Targeted Reflection**.
    *   If it's a request to gather general team sentiment or feedback, it's **Sentiment Gathering**.
    *   If it's a request to identify lessons learned from a project phase, it's **Lessons Learned Capture**.
    *   If unsure, ask for clarification using the 'request_user_clarification' tool.

2.  **Execute the corresponding workflow step-by-step, calling ONLY ONE sub-agent or HITL tool per turn:**

    *   **If Targeted Reflection (e.g., on a meeting):**
        1. Call `TeamSpiritAgent` to retrieve relevant context (e.g., read meeting log, read profiles).
        2. Call `ValueSoulAgent` to frame reflection points based on values.
        3. (HITL) Call `request_user_clarification` to pose reflection questions to the user/team.
        4. Call `BusinessAgent` to synthesize the reflection and document key insights or action items.
        5. (Optional HITL) Call `present_for_review_and_approval` with the documented reflection summary.

    *   **If Sentiment Gathering:**
        1. Call `TeamSpiritAgent` to read team profiles or recent relevant meeting logs.
        2. (HITL) Call `request_user_clarification` to ask specific sentiment-related questions (e.g., "How is the team feeling about workload?").
        3. Call `TeamSpiritAgent` again to analyze and summarize the sentiment based on user input and potentially profile data.
        4. (Optional) Call `BusinessAgent` to document the sentiment summary.

    *   **If Lessons Learned Capture:**
        1. Call `BusinessAgent` to retrieve project documents (plans, status reports) for the relevant phase.
        2. Call `TeamSpiritAgent` to gather team perspectives (e.g., read related meeting logs, or use HITL `request_user_clarification` to ask team members).
        3. Call `ValueSoulAgent` to analyze the lessons learned through the lens of partnership values.
        4. Call `BusinessAgent` to synthesize and document the lessons learned.
        5. Call `present_for_review_and_approval` tool with the documented lessons learned.

3.  Once a workflow is complete and potentially approved via HITL, provide the final consolidated reflection output or confirmation.
4.  **CRITICAL: You MUST call sub-agents sequentially as defined for the variant. Only call ONE sub-agent or HITL tool per turn.**
5.  **CRITICAL: You do NOT have direct access to tools like 'read_meeting_log' or 'read_team_profile'. You MUST delegate tasks requiring those tools to your sub-agents (`ReflectionBusinessAgent`, `ReflectionValueSoulAgent`, `ReflectionTeamSpiritAgent`).**
""",
    sub_agents=[
        reflection_business_agent,
        reflection_value_soul_agent,
        reflection_team_spirit_agent
    ],
    # This orchestrator might need access to HITL tools directly
    tools=[
        tools.request_user_clarification,
        tools.present_for_review_and_approval,
        tools.ask_user_to_choose_option,
    ]
)
