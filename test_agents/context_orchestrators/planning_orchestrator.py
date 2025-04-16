"""Defines the Planning Context Orchestrator Agent.

This agent manages workflows related to the 'Planning' governance context.
It identifies the specific planning variant (e.g., Standard, Meeting Analysis)
and orchestrates calls to specialized agents (Business, ValueSoul, TeamSpirit)
and HITL tools to execute the corresponding planning process.
"""
import copy
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Import base agent definitions (adjust paths/imports as needed)
# Assuming base definitions are accessible from the parent directory or package structure allows it
# Example: from test_agents.agent_bases.business_agent_base import business_agent_base (if structure changes)
# Using absolute imports from the top-level 'test_agents' package:
from test_agents.business_agent import business_agent # Assuming business_agent is the instance defined in business_agent.py
from test_agents.value_soul_agent_base import value_soul_agent_base
from test_agents.team_spirit_agent_base import team_spirit_agent_base
from test_agents import tools # To potentially access HITL tools if needed directly (though likely called by sub-agents based on instructions)

# Define the model for this orchestrator
AGENT_MODEL = LiteLlm(model="openai/gpt-4.1-mini")

# --- Step 2.1.3: Instantiate local copies for this context ---
# Create independent instances of the base agents for this specific orchestrator
planning_business_agent = copy.deepcopy(business_agent)
planning_value_soul_agent = copy.deepcopy(value_soul_agent_base)
planning_team_spirit_agent = copy.deepcopy(team_spirit_agent_base)

# --- Step 2.1.4: Define the Planning Orchestrator Agent ---
planning_orchestrator = Agent(
    name="PlanningOrchestrator",
    description="Manages planning processes including standard planning, meeting analysis, and weekly reviews. Determines the planning variant and calls specialized agents (Business, ValueSoul, TeamSpirit) in the correct sequence.",
    model=AGENT_MODEL,
    instruction="""You are the Planning Orchestrator. Your goal is to manage all planning-related governance tasks.

1.  **Analyze the input** to determine the planning variant:
    *   If it's a request to create a new plan from scratch, it's **Standard Planning**.
    *   If the input is primarily a meeting transcript or mentions analyzing a meeting, it's **Meeting Analysis Planning**.
    *   If it's a request to review progress against an existing plan or a periodic review, it's **Weekly Review Planning**.
    *   If unsure, ask for clarification using the 'request_user_clarification' tool.

2.  **Execute the corresponding workflow step-by-step, calling ONLY ONE sub-agent or HITL tool per turn:**

    *   **If Standard Planning:**
        1. Call `BusinessAgent` to create the initial draft plan.
        2. Call `present_for_review_and_approval` tool with the draft plan. Ask the user to review it.
        3. If approved:
            a. Call `ValueSoulAgent` to evaluate the plan against values.
            b. Call `BusinessAgent` again to finalize the plan based on any value feedback.
        4. If rejected or approved_with_comments:
            a. Call `BusinessAgent` again to revise the plan based on user feedback (`comments` from the tool result).
            b. Go back to step 2 (present the revised plan for review).

    *   **If Meeting Analysis Planning:**
        1. Call `TeamSpiritAgent` to analyze interactions in the transcript/meeting context.
        2. Call `BusinessAgent` to extract tasks and decisions from the analysis.
        3. Call `ValueSoulAgent` to check value alignment of extracted items.
        4. Call `present_for_review_and_approval` tool with the extracted tasks/decisions.
        5. If approved:
            a. Call `BusinessAgent` to write the outputs to relevant governance documents.
        6. If rejected or approved_with_comments:
            a. Call `BusinessAgent` to revise extracted items based on feedback.
            b. Go back to step 4 (present revised items for review).

    *   **If Weekly Review Planning:**
        1. Call `BusinessAgent` to analyze current status against the existing plan.
        2. Call `TeamSpiritAgent` to incorporate team feedback/sentiment (may involve reading profiles or recent logs if specified).
        3. Call `ValueSoulAgent` to check progress alignment with values.
        4. Call `present_for_review_and_approval` tool with the review summary and proposed updates.
        5. If approved:
            a. Call `BusinessAgent` to update plans and create a final summary.
        6. If rejected or approved_with_comments:
            a. Call `BusinessAgent` to revise updates based on feedback.
            b. Go back to step 4 (present revised review/updates).

3.  Once a workflow is complete, provide the final consolidated result.
4.  **CRITICAL: You MUST call sub-agents sequentially as defined for the variant. Only call ONE sub-agent or HITL tool per turn.**
5.  **CRITICAL: You do NOT have direct access to tools like 'read_partnership_documents' or 'read_meeting_log'. You MUST delegate tasks requiring those tools to your sub-agents (`PlanningBusinessAgent`, `PlanningValueSoulAgent`, `PlanningTeamSpiritAgent`).**
""",
    sub_agents=[
        planning_business_agent,
        planning_value_soul_agent,
        planning_team_spirit_agent
    ],
    # This orchestrator might need access to HITL tools directly
    tools=[
        tools.request_user_clarification,
        tools.present_for_review_and_approval,
        tools.ask_user_to_choose_option,
    ]
)
