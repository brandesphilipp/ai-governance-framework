# Contributing Guidelines

Thank you for considering contributing to the ADK Multi-Agent System project!

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally: `git clone https://github.com/YOUR_USERNAME/ai-governance-framework.git` (Assuming the remote repo will also be renamed).
3.  **Set up your environment** as described in the `README.md` (create virtual environment, install requirements, set up `.env` with your API key).

## Development Workflow

1.  **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name` or `bugfix/issue-description`.
2.  **Make your changes.**
3.  **Test your changes** locally. (Consider adding unit/integration tests if applicable).
4.  **Commit your changes** with clear commit messages.
5.  **Push your branch** to your fork: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request** against the main repository's `main` branch.

## Important: Handling Documents and Sensitive Data

This project uses external documents (tasks, profiles, meeting notes, partnership agreements) for its operation. To enable collaboration without exposing sensitive runtime data, please adhere to the following:

*   **Templates vs. Runtime Data:**
    *   The `templates/` directory contains generic, non-sensitive templates for all required documents. **Contribute changes to these templates.**
    *   The actual runtime documents (by default in `documents/`, or a custom path set via `DOCUMENTS_DIR` in your `.env`) contain potentially sensitive operational data. **NEVER commit your runtime documents directory or files to Git.** The `.gitignore` file is configured to ignore the default `documents/` directory.
*   **Configuration:** All code accessing documents **MUST** use the paths defined in `test_agents/config.py`. Do not hardcode paths directly in agent or tool code.
*   **Placeholders:** When modifying templates or adding examples, use clear placeholders (like `[Your Name]`, `YYYY-MM-DD`, `sk-xxxxxxxx`) instead of real data.
*   **Testing:** When writing tests that require document interaction, consider creating mock documents within a dedicated test directory (e.g., `tests/mock_documents/`) and potentially using fixtures (like pytest's `monkeypatch`) to temporarily set the `DOCUMENTS_DIR` environment variable during test execution to point to your mock directory.

## Code Style

*   Follow PEP 8 guidelines for Python code.
*   Use clear variable and function names.
*   Add docstrings to new functions and classes.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub. Provide as much detail as possible.

Thank you for contributing!
