import typing
import os
import csv
import io
from pathlib import Path
from pydantic import ValidationError

# Import required models and configuration
from ..models import Task, TaskListResult, WriteTaskInput, EditTaskInput, TaskOperationResult
from ..config import TASKS_FILE_PATTERN # Import the configured path pattern

# Define the table header structure (remains constant)
TASK_TABLE_HEADER = "| ID | Title | Assignee | Deadline | Description | Status |\n|---|---|---|---|---|---|\n"

def _get_task_file_path(user_name: str) -> Path:
    """Constructs the path to the user's task file using the configured pattern."""
    # Basic validation, could be expanded if needed
    if not user_name or not isinstance(user_name, str):
        raise ValueError("Invalid user name provided.")
    # Use the configured pattern directly
    return Path(TASKS_FILE_PATTERN.format(user_name=user_name))

def _read_tasks_from_file(file_path: Path, user_name: str) -> tuple[list[Task], str]:
    """Reads tasks from the markdown file, returning Task objects and raw content."""
    tasks = []
    # Use the user_name passed to the function for the header
    default_header = f"# Task List for {user_name}\n\n{TASK_TABLE_HEADER}"
    raw_content = default_header # Default content if file doesn't exist

    # Use the file_path directly as it's now correctly constructed by _get_task_file_path
    if not file_path.exists():
        return tasks, raw_content # Return empty list and default header

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
            # Find the table content after the header and separator
            table_start = raw_content.find(TASK_TABLE_HEADER)
            if table_start == -1:
                 return tasks, raw_content # Header not found, return raw content

            table_content_start = table_start + len(TASK_TABLE_HEADER)
            table_lines = raw_content[table_content_start:].strip().splitlines()

            cleaned_lines = [line.strip().strip('|').strip() for line in table_lines if line.strip()]
            if not cleaned_lines:
                 return tasks, raw_content # No task rows

            csv_data = io.StringIO("\n".join(cleaned_lines))
            reader = csv.reader(csv_data, delimiter='|', skipinitialspace=True)

            for row in reader:
                cleaned_row = [cell.strip() for cell in row]
                if len(cleaned_row) == 6:
                    try:
                        task = Task(
                            task_id=int(cleaned_row[0]),
                            title=cleaned_row[1],
                            assignee=cleaned_row[2],
                            deadline=cleaned_row[3],
                            description=cleaned_row[4],
                            status=cleaned_row[5]
                        )
                        tasks.append(task)
                    except (ValueError, IndexError) as e:
                        print(f"Skipping invalid task row: {row} - Error: {e}")
                        continue
                else:
                     print(f"Skipping row with incorrect column count: {row}")
    except Exception as e:
        print(f"Error reading task file {file_path}: {e}")
        # Return potentially partial raw_content read before error, or default header
        return tasks, raw_content

    return tasks, raw_content


def _write_tasks_to_file(file_path: Path, tasks: list[Task], user_name: str):
    """Writes the list of tasks back to the markdown file."""
    # Directory creation is handled in config.py on import
    # Use file_path directly
    tasks.sort(key=lambda t: t.task_id)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# Task List for {user_name}\n\n")
        f.write(TASK_TABLE_HEADER)
        for task in tasks:
            f.write(f"| {task.task_id} | {task.title} | {task.assignee} | {task.deadline} | {task.description} | {task.status} |\n")

# Removed incorrect @tool decorator
def read_task_list(user_name: str):
    """
    Reads the task list for the specified user.

    Args:
        user_name (str): The name of the user whose list to read ('Philipp' or 'Guillaume').

    Returns:
        dict: A dictionary with status and result (TaskListResult) or error_message.
    """
    try:
        file_path = _get_task_file_path(user_name)
        # Pass user_name to _read_tasks_from_file for correct header generation if file is new/empty
        tasks, raw_content = _read_tasks_from_file(file_path, user_name)
        result_model = TaskListResult(tasks=tasks, raw_content=raw_content)
        return {
            "status": "success",
            "result": result_model.model_dump()
        }
    except ValueError as e: # Catch specific error from _get_task_file_path
         return {"status": "error", "error_message": str(e)}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to read task list for {user_name}: {str(e)}"
        }

# Removed incorrect @tool decorator
def write_task(task_title: str, assignee: str, deadline: str, description: str, user_name: str):
    """
    Adds a new task to the specified user's task list.

    Args:
        task_title (str): The title for the new task.
        assignee (str): Who the task should be assigned to.
        deadline (str): The deadline for the task (YYYY-MM-DD).
        description (str): A description of the task.
        user_name (str): The name of the user whose list to modify ('Philipp' or 'Guillaume').

    Returns:
        dict: A dictionary representing TaskOperationResult.
    """
    try:
        validated_input = WriteTaskInput(
            task_title=task_title,
            assignee=assignee,
            deadline=deadline,
            description=description,
            user_name=user_name
        )

        file_path = _get_task_file_path(validated_input.user_name)
        # Pass user_name to _read_tasks_from_file
        tasks, _ = _read_tasks_from_file(file_path, validated_input.user_name)

        next_id = (max(task.task_id for task in tasks) + 1) if tasks else 1

        new_task = Task(
            task_id=next_id,
            title=validated_input.task_title,
            assignee=validated_input.assignee,
            deadline=validated_input.deadline,
            description=validated_input.description,
            status="Pending"
        )
        tasks.append(new_task)

        _write_tasks_to_file(file_path, tasks, validated_input.user_name)

        result_model = TaskOperationResult(
            status="success",
            message=f"Successfully added task '{new_task.title}' (ID: {new_task.task_id}) to {validated_input.user_name}'s list.",
            task_id=new_task.task_id
        )
        return result_model.model_dump()

    except (ValidationError, ValueError) as e:
         return TaskOperationResult(status="error", message=f"Invalid input: {str(e)}", task_id=None).model_dump()
    except Exception as e:
        return TaskOperationResult(status="error", message=f"Failed to write task for {user_name}: {str(e)}", task_id=None).model_dump()

# Removed incorrect @tool decorator
def edit_task(task_id: int, action: str, user_name: str, updates: typing.Optional[dict] = None):
    """
    Modifies or deletes an existing task in the specified user's list.

    Args:
        task_id (int): The ID of the task to modify or delete.
        action (str): The action to perform: 'modify' or 'delete'.
        user_name (str): The name of the user whose list to modify ('Philipp' or 'Guillaume').
        updates (typing.Optional[dict]): A dictionary containing fields to modify
            (e.g., {'title': 'New Title', 'status': 'In Progress'}).
            Required if action is 'modify', ignored if action is 'delete'.
            Valid keys: 'title', 'assignee', 'deadline', 'description', 'status'.

    Returns:
        dict: A dictionary representing TaskOperationResult.
    """
    try:
        # --- Input Validation ---
        if action not in ['modify', 'delete']:
            raise ValueError("Invalid action specified. Must be 'modify' or 'delete'.")
        if action == 'modify':
            if updates is None or not isinstance(updates, dict) or not updates:
                 raise ValueError("Modification action requires a non-empty 'updates' dictionary.")
            valid_keys = {'title', 'assignee', 'deadline', 'description', 'status'}
            invalid_keys = set(updates.keys()) - valid_keys
            if invalid_keys:
                 raise ValueError(f"Invalid keys found in 'updates' dictionary: {', '.join(invalid_keys)}")

        file_path = _get_task_file_path(user_name)
        # Pass user_name to _read_tasks_from_file
        tasks, _ = _read_tasks_from_file(file_path, user_name)

        task_found = False
        updated_tasks = []
        affected_task_title = ""

        for task in tasks:
            if task.task_id == task_id:
                task_found = True
                affected_task_title = task.title
                if action == 'modify':
                    for key, value in updates.items():
                         if hasattr(task, key) and value is not None:
                             setattr(task, key, value)
                    updated_tasks.append(task)
                elif action == 'delete':
                    pass # Skip task
            else:
                updated_tasks.append(task)

        if not task_found:
            return TaskOperationResult(status="error", message=f"Task with ID {task_id} not found in {user_name}'s list.", task_id=task_id).model_dump()

        _write_tasks_to_file(file_path, updated_tasks, user_name)

        action_verb = "modified" if action == 'modify' else "deleted"
        result_model = TaskOperationResult(
            status="success",
            message=f"Successfully {action_verb} task '{affected_task_title}' (ID: {task_id}) in {user_name}'s list.",
            task_id=task_id
        )
        return result_model.model_dump()

    except ValueError as e:
         return TaskOperationResult(status="error", message=f"Operation error: {str(e)}", task_id=task_id).model_dump()
    except Exception as e:
        return TaskOperationResult(status="error", message=f"Failed to {action} task {task_id} for {user_name}: {str(e)}", task_id=task_id).model_dump()
