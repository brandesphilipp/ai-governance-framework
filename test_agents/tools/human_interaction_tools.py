# Human-in-the-Loop (HITL) Tools
# Implementations will be added in Task 1.3

from typing import Dict, Any
from typing import Dict, Any, Optional
from ..models import ToolResult
import time

def request_user_clarification(question: str, context_info: Optional[Dict[str, Any]] = None) -> ToolResult:
    """Pauses execution and asks the user a specific question for clarification.

    This tool is intended to interact with an external system (e.g., a web UI)
    to present a question and optional context to the user, wait for their
    textual response, and return it.

    (Placeholder implementation uses print/input for simulation).

    Args:
        question: The specific question to ask the user.
        context_info: A dictionary containing relevant context to display
                      alongside the question (optional).

    Returns:
        A ToolResult object. On success, the 'result' dictionary contains:
            {'user_response': str} - The text response provided by the user.
        On failure, 'status' is 'error' and 'error_message' provides details.
    """
    print(f"\n--- Asking User for Clarification ---")
    print(f"Question: {question}")
    if context_info:
        print(f"Context: {context_info}")
    print("------------------------------------")

    # Placeholder for actual interaction with UI/external system
    try:
        user_response = input("Your response: ")
        return ToolResult(status="success", result={"user_response": user_response})
    except Exception as e:
        print(f"Error during placeholder user input: {e}")
        return ToolResult(status="error", error_message=f"Failed to get user clarification: {e}")


def present_for_review_and_approval(item_type: str, item_content: Dict[str, Any], proposed_action: str) -> ToolResult:
    """Presents an item to the user for review and approval before proceeding.

    This tool simulates presenting structured information (e.g., a draft plan,
    an evaluation summary) to the user via an external UI and capturing their
    decision and optional comments.

    (Placeholder implementation uses print/input for simulation).

    Args:
        item_type: A string describing the type of item being presented
                   (e.g., "Draft Plan", "Evaluation Summary").
        item_content: A dictionary containing the details of the item to be
                      reviewed by the user.
        proposed_action: A string describing what will happen if approved
                         (e.g., "Finalize plan", "Save evaluation").

    Returns:
        A ToolResult object. On success, the 'result' dictionary contains:
            {'decision': str} - The user's decision ('approved', 'rejected',
                               or 'approved_with_comments').
            {'comments': str} - Any comments provided by the user (empty string
                                if none).
        On failure, 'status' is 'error' and 'error_message' provides details.
    """
    print(f"\n--- User Review Request ---")
    print(f"Item Type: {item_type}")
    print(f"Content: {item_content}")
    print(f"Proposed Action: {proposed_action}")
    print("---------------------------")

    # Placeholder for actual interaction
    while True:
        decision = input("Decision (approved / rejected / approved_with_comments): ").lower().strip()
        if decision in ["approved", "rejected", "approved_with_comments"]:
            break
        else:
            print("Invalid input. Please enter 'approved', 'rejected', or 'approved_with_comments'.")

    comments = ""
    if decision in ["rejected", "approved_with_comments"]:
        comments = input("Comments (optional): ")

    try:
        return ToolResult(status="success", result={"decision": decision, "comments": comments})
    except Exception as e:
        print(f"Error during placeholder user input: {e}")
        return ToolResult(status="error", error_message=f"Failed to get user review/approval: {e}")


def ask_user_to_choose_option(prompt: str, options: list[str]) -> ToolResult:
    """Asks the user to select one option from a provided list.

    This tool simulates presenting a prompt and a list of choices to the user
    via an external UI and returning the selected option.

    (Placeholder implementation uses print/input for simulation).

    Args:
        prompt: The question or instruction prompting the user to choose.
        options: A list of strings representing the available choices.

    Returns:
        A ToolResult object. On success, the 'result' dictionary contains:
            {'selected_option': str} - The option chosen by the user.
        On failure (e.g., no options provided), 'status' is 'error' and
        'error_message' provides details.
    """
    print(f"\n--- User Choice Request ---")
    print(prompt)
    if not options:
        return ToolResult(status="error", error_message="No options provided for user choice.")

    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    print("-------------------------")

    # Placeholder for actual interaction
    while True:
        try:
            choice_input = input(f"Enter choice number (1-{len(options)}): ")
            choice_idx = int(choice_input) - 1
            if 0 <= choice_idx < len(options):
                selected_option = options[choice_idx]
                return ToolResult(status="success", result={"selected_option": selected_option})
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"Error during placeholder user input: {e}")
            return ToolResult(status="error", error_message=f"Failed to get user choice: {e}")
