# test_agents/config.py (Revised)
"""
Configuration settings with environment overrides
"""
import os
from pathlib import Path

# Allow environment overrides for local development
# Default to 'documents' if DOCUMENTS_DIR environment variable is not set.
DOCUMENTS_BASE_DIR = os.getenv("DOCUMENTS_DIR", "documents")
# Define the templates directory name
TEMPLATES_DIR = "templates" # Renamed from documents_templates

# Runtime paths (using pathlib for robustness)
# Convert DOCUMENTS_BASE_DIR string to a Path object
_documents_base_path = Path(DOCUMENTS_BASE_DIR)
MEETINGS_DIR = _documents_base_path / "meetings"
PROFILES_DIR = _documents_base_path / "profiles"

# File patterns/names derived from the base path
TASKS_FILE_PATTERN = str(_documents_base_path / "tasks_{user_name}.md")
PARTNERSHIP_AGREEMENT_FILE = str(_documents_base_path / "partnership_agreement.md")
PARTNERSHIP_COMPANION_FILE = str(_documents_base_path / "partnership_companion.md")

# Ensure runtime directories exist on first import
# This code runs when the module is imported by the tools.
try:
    MEETINGS_DIR.mkdir(parents=True, exist_ok=True)
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    # Ensure the base directory also exists, especially if overridden via env var
    _documents_base_path.mkdir(parents=True, exist_ok=True)
except OSError as e:
    print(f"Warning: Could not create runtime directories under '{DOCUMENTS_BASE_DIR}': {e}")
