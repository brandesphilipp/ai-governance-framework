# ADK Multi-Agent System (Context-Specific Orchestrator Architecture)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
<!-- Optional: Add ADK version badge if known, e.g., [![ADK Version](https://img.shields.io/badge/ADK-vX.Y.Z-green.svg)](https://github.com/google/adk-python) -->

This project implements an **AI Governance Framework**, an innovative approach to organizational governance using AI, built with the Google Agent Development Kit (ADK). It functions as an "ethical AI CEO" layer, facilitating value-aligned, decentralized team management. The system features a hierarchical architecture with a central `GovernanceOrchestrator` routing tasks to specialized `ContextOrchestrator` agents, which manage workflows involving specific agents like `BusinessAgent`, `ValueSoulAgent`, and `TeamSpiritAgent`.

## Vision & Goal: AI Governance Framework

The core vision is to provide a universal framework enabling:

*   **Decentralized team management** while preserving core values and mission integrity.
*   **Value-aligned decision making** through a constitution-based approach (using partnership/organizational documents).
*   **Holistic success** balancing business objectives, ethical principles, and team wellbeing.
*   **Enhanced psychological safety** and effective communication within teams.

This project serves as a foundational implementation, showcasing agent coordination, tool usage, and context-specific workflow management within the ADK framework, using a configurable setup suitable for open-source collaboration while protecting sensitive data.

## Key Features & Differentiators

*   **Value Constitution Integration:** Formalizes organizational values (from documents like `partnership_agreement.md`) as a "constitution" guiding agent evaluation and potentially decision-making.
*   **Context-Specific Workflows:** A central `GovernanceOrchestrator` directs requests to one of five specialized `ContextOrchestrators` (Planning, Execution, Evaluation, Reflection, Resolution), tailoring agent interactions to the specific governance need.
*   **Holistic Agent Perspective:** Specialized agents provide a balanced view:
    *   `BusinessAgent`: Focuses on operational excellence and project success.
    *   `ValueSoulAgent`: Ensures alignment with the organization's core principles.
    *   `TeamSpiritAgent`: Monitors and supports team health and psychological safety.
*   **Configurable & Secure Document Handling:** Uses `config.py` and the `DOCUMENTS_DIR` environment variable to manage paths to operational documents (tasks, profiles, meeting notes, agreements), allowing separation of sensitive data from the codebase.
*   **Template-Based Setup:** Provides templates in the `templates/` directory for easy setup and customization of required documents.
*   **Extensible Tools:** Leverages Python functions as tools with Pydantic models for structured input/output.
*   **(Placeholder) Human-in-the-Loop:** Includes stubs (`human_interaction_tools.py`) for HITL interactions like clarification and approval. **Note:** Currently, these interactions occur via `print`/`input` in the terminal where `adk web` is running, not directly within the ADK web interface itself.
*   **Adaptability:** Designed to be adaptable across different team structures while maintaining core principles.

## Architecture Overview

The system follows a hierarchical pattern:

1.  **User Request:** The process starts with a user submitting a request.
2.  **`GovernanceOrchestrator` (`root_agent`):** Receives the request, analyzes it to determine the relevant governance context (Planning, Execution, Evaluation, Reflection, or Resolution).
3.  **Context Routing:** Transfers control to the single appropriate `ContextOrchestrator` based on the identified context.
4.  **`ContextOrchestrator` (e.g., `PlanningOrchestrator`):**
    *   Receives the request from the `GovernanceOrchestrator`.
    *   Manages the specific workflow for its context.
    *   Sequentially calls its own instances of specialized agents and/or HITL tools as needed for the workflow. Example calls within a Planning context:
        *   `BusinessAgent`
        *   `ValueSoulAgent`
        *   `TeamSpiritAgent`
        *   HITL Tools (Placeholders)
5.  **Specialized Agents (e.g., `BusinessAgent`, `ValueSoulAgent`, `TeamSpiritAgent`):**
    *   Receive specific tasks from their parent `ContextOrchestrator`.
    *   Execute their specialized logic.
    *   Interact with specific tools to access or modify data.
6.  **Tools:**
    *   `Task Tools` (used by `BusinessAgent`) -> Interact with `documents/tasks_*.md`.
    *   `Partnership Doc Tools` (used by `ValueSoulAgent`) -> Interact with `documents/partnership_*.md`.
    *   `Meeting/Profile Tools` (used by `TeamSpiritAgent`) -> Interact with `documents/meetings/*.md` and `documents/profiles/*.md`.
7.  **Response:** The final result is consolidated and returned up the chain to the user.

*   **`GovernanceOrchestrator` (`test_agents/agent.py`):** The main entry point (`root_agent`). Analyzes user requests and transfers control to the appropriate `ContextOrchestrator`.
*   **`ContextOrchestrators` (`test_agents/context_orchestrators/`):** Five orchestrators, each managing workflows for a specific governance context (Planning, Execution, Evaluation, Reflection, Resolution). They call specialized agents and Human-in-the-Loop (HITL) tools sequentially based on the request variant.
*   **Specialized Agents (`test_agents/*.py`, `*_base.py`):** These agents execute specific tasks within a context workflow, each bringing a unique focus:
    *   `BusinessAgent`: Focuses on operational excellence, task management, and project success metrics. Reads/writes task lists.
    *   `ValueSoulAgent`: Acts as the guardian of the organization's "constitution" (values, principles). Ensures decisions and actions align with core values defined in partnership documents. Reads partnership agreement/companion docs.
    *   `TeamSpiritAgent`: Monitors and maintains team health, psychological safety, and effective communication. Manages meeting logs and team profiles.
*   **Tools (`test_agents/tools/`):** Python functions performing specific actions like file I/O (reading/writing tasks, profiles, meeting logs, partnership docs) or user interaction (currently placeholders for HITL). Document paths are managed centrally via `config.py`.
*   **Models (`test_agents/models.py`):** Pydantic models define the expected structure for data passed between agents and tools, ensuring consistency.
*   **Configuration (`test_agents/config.py`):** Defines paths for runtime documents and templates. Allows overriding the base document directory via the `DOCUMENTS_DIR` environment variable (see Setup). Automatically creates necessary runtime directories (`meetings/`, `profiles/`) within the configured base directory upon first import by a tool.
*   **Templates (`templates/`):** Contains template versions of the documents used by the agents (task lists, meeting logs, profiles, partnership agreements). These should be copied to the runtime document directory and customized. **Warning headers** are included in templates to prevent accidental commits of sensitive data.

## Setup (Security First)

1.  **Clone the repository (outside sensitive directories):**
    ```bash
    git clone <repository-url>
    # Example: Clone into a general 'projects' directory, not inside your secure documents folder
    cd <repository-directory>
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate # On Windows use `.venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables:**
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Edit the new `.env` file:
        *   **Required:** Replace the placeholder `OPENAI_API_KEY` with your actual key.
        *   **Optional (for private data):** Uncomment the `DOCUMENTS_DIR` line and set it to the **absolute path** of your secure directory where you will store the populated documents (e.g., `/Users/yourname/secure_project_docs`). If you leave this commented out, the system will use a `documents/` folder inside the project directory (which is gitignored).
        ```dotenv
        # Example .env file content
        OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        # DOCUMENTS_DIR="/path/to/your/secure/private/documents"
        ```
5.  **Prepare Runtime Documents:**
    *   Decide where your runtime documents will live (either the default `documents/` folder inside the project or the custom path set in `DOCUMENTS_DIR`).
    *   Copy the contents of the `templates/` directory into your chosen runtime document directory.
    *   Rename and customize the copied files (e.g., rename `tasks_user.template.md` to `tasks_Philipp.md`, `profile.template.md` to `profiles/Guillaume.md`, etc.) and fill them with your actual data.
    *   **Crucially:** Ensure your runtime document directory (whether the default `documents/` or a custom one) is **NOT** committed to Git if it contains sensitive information. The provided `.gitignore` excludes the default `documents/` directory.

## Running the Agent System

Use the ADK command-line interface to launch the web UI and interact with the agent system:

```bash
# Make sure your virtual environment is activated
adk web test_agents
```

This command specifically targets the `test_agents` package containing your `root_agent`. It will start a local web server (usually at `http://localhost:8080`). Open this URL in your browser to access the ADK web interface, where you can send requests to the `GovernanceOrchestrator`.

## Project Structure

```
.
├── .env                  # Environment variables (API Keys, optional DOCUMENTS_DIR) - GITIGNORED
├── .gitignore            # Files ignored by Git
├── PLANNING.md           # Detailed project planning document
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── LICENSE               # MIT License file
├── templates/            # Template versions of documents (with warnings)
│   ├── meeting_log.template.md
│   ├── partnership_agreement.template.md
│   ├── partnership_companion.template.md
│   ├── profile.template.md
│   └── tasks_user.template.md
├── test_agents/          # Main package for agents and tools
│   ├── __init__.py
│   ├── agent.py          # Defines the root_agent (GovernanceOrchestrator)
│   ├── config.py         # Configuration for document paths
│   ├── models.py         # Pydantic models
│   ├── business_agent.py
│   ├── value_soul_agent_base.py
│   ├── team_spirit_agent_base.py
│   ├── context_orchestrators/ # Context-specific orchestrators
│   │   ├── __init__.py
│   │   ├── planning_orchestrator.py
│   │   └── ... (other orchestrators)
│   └── tools/              # Tool implementations
│       ├── __init__.py
│       ├── task_tools.py
│       ├── value_soul_tools.py
│       ├── team_spirit_tools.py
│       └── human_interaction_tools.py # Placeholder HITL tools
└── documents/            # Default runtime document directory - GITIGNORED
    ├── meetings/         # Default location for meeting logs
    ├── profiles/         # Default location for user profiles
    ├── partnership_agreement.md # Default location for agreement
    ├── partnership_companion.md # Default location for companion doc
    ├── tasks_Philipp.md  # Example task file
    └── tasks_Guillaume.md # Example task file
```

*(Note: The `documents/` directory is listed for structure illustration but is excluded by `.gitignore`. If you use a custom `DOCUMENTS_DIR` outside the project, that path will be used instead.)*

## Contributing

Please see `CONTRIBUTING.md` for guidelines on how to contribute safely to this project, especially regarding the handling of templates vs. runtime documents.

## Future Enhancements / Roadmap

This project serves as a foundation. Planned future enhancements include:

*   **Time Awareness:** Integrating time-awareness into the agents (especially the `GovernanceOrchestrator`) to understand requests in the context of current time, project timelines, and roadmaps. This could enable:
    *   Scheduled routines (e.g., morning kickstart, evening reflection sessions).
    *   Proactive notifications and reminders.
*   **Improved Human Interaction:** Enhancing the HITL tools to integrate more smoothly, potentially directly with the web UI or other interfaces.
*   **Custom User Interface:** Developing a dedicated UI (beyond the basic `adk web` interface) to support:
    *   Multiple simultaneous users.
    *   User authentication/login to differentiate users for personalized interactions (e.g., accessing correct task lists).
*   **Alternative Interfaces:** Exploring integrations with other platforms, such as:
    *   A Telegram bot interface.
    *   Voice message interaction capabilities.
*   **Sequential Tool Execution:** Addressing an intermittent issue where agents might attempt parallel tool calls within a single turn, potentially causing hangs. This will likely be resolved either through stricter agent prompting or by potentially implementing more robust ADK workflow agents (e.g., `SequentialAgent` or custom logic) to enforce sequential execution where necessary.
