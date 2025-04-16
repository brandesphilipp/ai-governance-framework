"""Defines the Main Governance Orchestrator Agent.

This agent acts as the primary entry point for the multi-agent system.
It analyzes user requests to determine the relevant governance context
(Planning, Execution, Evaluation, Reflection, Resolution) and routes
the request to the corresponding specialized Context Orchestrator agent.
"""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Import the context orchestrators
from .context_orchestrators import (
    planning_orchestrator,
    execution_orchestrator,
    evaluation_orchestrator,
    reflection_orchestrator,
    resolution_orchestrator
)

# Define the model for the main orchestrator
AGENT_MODEL = LiteLlm(model="openai/gpt-4.1-mini")

# Define the Main Orchestrator (Root Agent)
main_orchestrator = Agent(
    name="GovernanceOrchestrator",
    description="Central orchestrator that analyzes user requests and routes them to the appropriate governance context orchestrator (Planning, Execution, Evaluation, Reflection, Resolution).",
    model=AGENT_MODEL,
    instruction="""You are the main Governance Orchestrator. Your primary function is to determine the correct governance context for a user's request and transfer control to the appropriate specialized orchestrator.

1.  **Analyze the user request** carefully.
2.  **Identify the primary governance context** based on the request's intent. The available contexts are:
    *   **Planning:** Creating/refining plans, tasks, timelines, resources, analyzing meetings for planning purposes.
    *   **Execution:** Tracking progress, status updates, logging work, marking tasks complete.
    *   **Evaluation:** Assessing outcomes, checking alignment with goals/values, evaluating meetings or tasks.
    *   **Reflection:** Facilitating team learning, gathering sentiment, capturing lessons learned.
    *   **Resolution:** Addressing conflicts, making decisions between options, formalizing agreements.
3.  **Transfer control to ONLY ONE** of the following context orchestrators based on your analysis:
    *   `PlanningOrchestrator`
    *   `ExecutionOrchestrator`
    *   `EvaluationOrchestrator`
    *   `ReflectionOrchestrator`
    *   `ResolutionOrchestrator`
4.  **CRITICAL: Do NOT attempt to answer the request directly or use any tools.** Your sole responsibility is to route the request to the correct context orchestrator using `transfer_to_agent`.
5.  If the context is ambiguous or unclear, you can ask a clarifying question, but prefer to route if possible based on the most likely context.
""",
    sub_agents=[
        planning_orchestrator,
        execution_orchestrator,
        evaluation_orchestrator,
        reflection_orchestrator,
        resolution_orchestrator
    ],
    # This main orchestrator should NOT have tools, its only job is routing.
    tools=[]
)
