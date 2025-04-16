import typing
import datetime
from pathlib import Path # Use pathlib
from ..models import ToolResult
# Import configured directory paths
from ..config import MEETINGS_DIR, PROFILES_DIR

def _validate_date_format(date_str: str) -> bool:
    """Helper to validate YYYY-MM-DD format."""
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def read_meeting_log(meeting_date: str) -> dict:
    """
    Reads the content of a meeting log for a specific date.

    Args:
        meeting_date: The date of the meeting log to read (format: YYYY-MM-DD).

    Returns:
        A dictionary containing the status and the log content or an error message.
    """
    if not _validate_date_format(meeting_date):
        return ToolResult(
            status="error",
            error_message=f"Invalid date format for meeting_date: '{meeting_date}'. Please use YYYY-MM-DD."
        ).model_dump()

    # Construct path using configured directory
    file_path = MEETINGS_DIR / f"{meeting_date}.md"

    try:
        # Directory creation handled in config.py
        # Check if file exists before reading
        if not file_path.is_file():
            raise FileNotFoundError(f"Meeting log for date '{meeting_date}' not found at '{file_path}'.")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return ToolResult(
            status="success",
            result={"log_content": content}
        ).model_dump()
    except FileNotFoundError:
        return ToolResult(
            status="error",
            error_message=str(e) # Use error message from FileNotFoundError
        ).model_dump()
    except Exception as e:
        return ToolResult(
            status="error",
            error_message=f"An unexpected error occurred while reading meeting log '{file_path.name}': {str(e)}"
        ).model_dump()

def write_meeting_log(meeting_date: str, participants: list[str], content: str) -> dict:
    """
    Creates or overwrites a meeting log for a specific date.

    Args:
        meeting_date: The date of the meeting (format: YYYY-MM-DD).
        participants: A list of participant names.
        content: The main content/notes of the meeting log (Markdown format recommended).

    Returns:
        A dictionary containing the status and a success or error message.
    """
    if not _validate_date_format(meeting_date):
        return ToolResult(
            status="error",
            error_message=f"Invalid date format for meeting_date: '{meeting_date}'. Please use YYYY-MM-DD."
        ).model_dump()

    # Construct path using configured directory
    file_path = MEETINGS_DIR / f"{meeting_date}.md"

    # Format the content
    participant_list = "\n".join([f"- {p}" for p in participants])
    full_content = f"# Meeting Log: {meeting_date}\n\n" \
                   f"## Participants\n{participant_list}\n\n" \
                   f"## Notes\n{content}\n"

    try:
        # Directory creation handled in config.py
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        return ToolResult(
            status="success",
            result={"message": f"Meeting log for {meeting_date} saved successfully."}
        ).model_dump()
    except Exception as e:
        return ToolResult(
            status="error",
            error_message=f"An unexpected error occurred while writing meeting log '{file_path.name}': {str(e)}"
        ).model_dump()

def read_team_profile(member_name: typing.Literal["Philipp", "Guillaume"]) -> dict:
    """
    Reads the profile content for a specific team member using paths defined in config.py.

    Args:
        member_name: The name of the team member ('Philipp' or 'Guillaume').

    Returns:
        A dictionary containing the status and the profile content or an error message.
    """
    # Construct path using configured directory
    file_path = PROFILES_DIR / f"{member_name}.md"

    try:
        # Directory creation handled in config.py
        # Check if file exists before reading
        if not file_path.is_file():
             # If profile doesn't exist, return default content instead of error
             content = f"# Profile: {member_name}\n\n(No details added yet.)"
        else:
             with open(file_path, 'r', encoding='utf-8') as f:
                 content = f.read()
             # Add default content if file exists but is empty
             if not content.strip():
                 content = f"# Profile: {member_name}\n\n(No details added yet.)"

        return ToolResult(
            status="success",
            result={"profile_content": content}
        ).model_dump()
    except Exception as e: # Catch potential errors during file read if it exists
        return ToolResult(
            status="error",
            error_message=f"An unexpected error occurred while reading profile '{file_path.name}': {str(e)}"
        ).model_dump()
