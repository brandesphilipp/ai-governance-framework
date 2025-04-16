"""Defines the Execution Context Orchestrator Agent.

This agent manages workflows related to the 'Execution' governance context.
It identifies the specific execution variant (e.g., Status Update, Progress Logging)
and orchestrates calls to specialized agents (Business, ValueSoul, TeamSpirit)
and HITL tools to execute the corresponding process.
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
execution_business_agent = copy.deepcopy(business_agent)
execution_value_soul_agent = copy.deepcopy(value_soul_agent_base)
execution_team_spirit_agent = copy.deepcopy(team_spirit_agent_base)

# Define the Execution Orchestrator Agent
execution_orchestrator = Agent(
    name="ExecutionOrchestrator",
    description="Manages execution processes including status updates, progress tracking, and task completion.",
    model=AGENT_MODEL,
    instruction="""You are the Execution Orchestrator. Your goal is to manage governance tasks related to project execution.

1.  **Analyze the input** to determine the execution variant:
    *   If it's a request for a simple status update on a task/project, it's **Status Update**.
    *   If it's a request to log completed work or detailed progress, it's **Progress Logging**.
    *   If it's a request to mark a task as complete, it's **Task Completion**.
    *   If unsure, ask for clarification using the 'request_user_clarification' tool.

2.  **Execute the corresponding workflow step-by-step, calling ONLY ONE sub-agent or HITL tool per turn:**

    *   **If Status Update:**
        1. Call `BusinessAgent` to read the relevant task list or project document.
        2. (Optional HITL) Call `request_user_clarification` if specific details are needed from the user about what status they need.
        3. Synthesize the status and provide it.

    *   **If Progress Logging:**
        1. Call `BusinessAgent` to update the relevant task list or project document with the provided progress details.
        2. (Optional) Call `TeamSpiritAgent` if the progress involves team interactions or sentiment to log.
        3. (Optional HITL) Call `present_for_review_and_approval` to confirm the logged progress before finalizing.
        4. Provide confirmation of the logged progress.

    *   **If Task Completion:**
        1. Call `BusinessAgent` to mark the specified task as complete in the task list (using `edit_task`).
        2. (Optional) Call `ValueSoulAgent` to briefly check if the completed task aligns with project values or goals, based on task description.
        3. (Optional HITL) Call `present_for_review_and_approval` to confirm task completion and any value assessment.
        4. Provide confirmation of task completion.

3.  Once a workflow is complete, provide the final consolidated result or confirmation.
4.  **CRITICAL: You MUST call sub-agents sequentially as defined for the variant. Only call ONE sub-agent or HITL tool per turn.**
5.  **CRITICAL: You do NOT have direct access to tools like 'read_task_list' or 'edit_task'. You MUST delegate tasks requiring those tools to your sub-agents (`ExecutionBusinessAgent`, `ExecutionValueSoulAgent`, `ExecutionTeamSpiritAgent`).**
""",
    sub_agents=[
        execution_business_agent,
        execution_value_soul_agent,
        execution_team_spirit_agent
    ],
    # This orchestrator might need access to HITL tools directly
    tools=[
        tools.request_user_clarification,
        tools.present_for_review_and_approval,
        tools.ask_user_to_choose_option,
    ]
)
