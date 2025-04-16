import typing
from pathlib import Path # Use pathlib for consistency, though config provides strings
from ..models import ToolResult
# Import the configured paths
from ..config import PARTNERSHIP_AGREEMENT_FILE, PARTNERSHIP_COMPANION_FILE

def read_partnership_documents(document_type: typing.Literal["agreement", "companion"]) -> dict:
    """
    Reads the content of either the Partnership Agreement or the Companion Document
    using paths defined in config.py.

    Args:
        document_type: Specifies which document to read ('agreement' or 'companion').

    Returns:
        A dictionary containing the status and the document content or an error message.
    """
    file_path_str = ""
    if document_type == "agreement":
        file_path_str = PARTNERSHIP_AGREEMENT_FILE
    elif document_type == "companion":
        file_path_str = PARTNERSHIP_COMPANION_FILE
    else:
        # This case should ideally be caught by ADK's type validation
        return ToolResult(
            status="error",
            error_message=f"Invalid document type specified: {document_type}. Must be 'agreement' or 'companion'."
        ).model_dump()

    file_path = Path(file_path_str) # Convert string from config to Path object

    try:
        # Check if file exists before attempting to open
        if not file_path.is_file():
             raise FileNotFoundError(f"The document '{file_path.name}' was not found at '{file_path}'.")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return ToolResult(
            status="success",
            result={"document_content": content}
        ).model_dump()
    except FileNotFoundError:
        return ToolResult(
            status="error",
            error_message=str(e) # Use the error message from FileNotFoundError
        ).model_dump()
    except Exception as e:
        return ToolResult(
            status="error",
            error_message=f"An unexpected error occurred while reading '{file_path.name}': {str(e)}"
        ).model_dump()
