"""Defines the Evaluation Context Orchestrator Agent.

This agent manages workflows related to the 'Evaluation' governance context.
It identifies the specific evaluation variant (e.g., Task/Milestone Evaluation,
Meeting Evaluation) and orchestrates calls to specialized agents (Business,
ValueSoul, TeamSpirit) and HITL tools to execute the corresponding assessment process.
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
evaluation_business_agent = copy.deepcopy(business_agent)
evaluation_value_soul_agent = copy.deepcopy(value_soul_agent_base)
evaluation_team_spirit_agent = copy.deepcopy(team_spirit_agent_base)

# Define the Evaluation Orchestrator Agent
evaluation_orchestrator = Agent(
    name="EvaluationOrchestrator",
    description="Manages evaluation processes, assessing outcomes against goals, values, and team dynamics.",
    model=AGENT_MODEL,
    instruction="""You are the Evaluation Orchestrator. Your goal is to manage governance tasks related to evaluating project outcomes, processes, and alignment.

1.  **Analyze the input** to determine the evaluation variant:
    *   If it's a request to evaluate a specific completed task or milestone against its goals, it's **Task/Milestone Evaluation**.
    *   If it's a request to evaluate a recent meeting's effectiveness or alignment, it's **Meeting Evaluation**.
    *   If it's a broader request to evaluate project alignment with partnership values, it's **Value Alignment Check**.
    *   If unsure, ask for clarification using the 'request_user_clarification' tool.

2.  **Execute the corresponding workflow step-by-step, calling ONLY ONE sub-agent or HITL tool per turn:**

    *   **If Task/Milestone Evaluation:**
        1. Call `BusinessAgent` to retrieve the task definition, goals, and recorded outcomes/status.
        2. Call `ValueSoulAgent` to evaluate the outcome against defined project/partnership values.
        3. (Optional) Call `TeamSpiritAgent` if team feedback on the task process is relevant (e.g., read related meeting logs).
        4. Synthesize the evaluation findings.
        5. Call `present_for_review_and_approval` tool with the evaluation summary.

    *   **If Meeting Evaluation:**
        1. Call `TeamSpiritAgent` to read the specified meeting log.
        2. Call `ValueSoulAgent` to evaluate the meeting discussion/decisions against partnership values (using the log content).
        3. Call `BusinessAgent` to identify any actionable outcomes or tasks generated from the meeting evaluation.
        4. Synthesize the meeting evaluation.
        5. Call `present_for_review_and_approval` tool with the meeting evaluation summary.

    *   **If Value Alignment Check:**
        1. Call `ValueSoulAgent` to read the primary partnership documents (agreement/companion).
        2. Call `BusinessAgent` to retrieve relevant project plans or status documents to be checked.
        3. Call `ValueSoulAgent` again to perform the alignment check between the documents and the values.
        4. Synthesize the alignment report.
        5. Call `present_for_review_and_approval` tool with the alignment report.

3.  Once a workflow is complete and potentially approved via HITL, provide the final consolidated evaluation report.
4.  **CRITICAL: You MUST call sub-agents sequentially as defined for the variant. Only call ONE sub-agent or HITL tool per turn.**
5.  **CRITICAL: You do NOT have direct access to tools like 'read_partnership_documents' or 'read_meeting_log'. You MUST delegate tasks requiring those tools to your sub-agents (`EvaluationBusinessAgent`, `EvaluationValueSoulAgent`, `EvaluationTeamSpiritAgent`).**
""",
    sub_agents=[
        evaluation_business_agent,
        evaluation_value_soul_agent,
        evaluation_team_spirit_agent
    ],
    # This orchestrator might need access to HITL tools directly
    tools=[
        tools.request_user_clarification,
        tools.present_for_review_and_approval,
        tools.ask_user_to_choose_option,
    ]
)
