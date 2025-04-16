import typing # Add missing import
from pydantic import BaseModel, Field

class GetCurrentTimeInput(BaseModel):
    """Input model for the get_current_time tool."""
    time_zone: str = Field(..., description="The time zone to get the current time for (e.g., 'America/New_York', 'Europe/London')")

class TimeResult(BaseModel):
    """Output model representing the time result."""
    time_zone: str = Field(..., description="The time zone used.")
    date_time: str = Field(..., description="The current date and time in the specified format.")
    is_daylight_savings_time: bool = Field(..., description="Indicates if daylight saving time is currently active for the zone.")


class PirateCodeContent(BaseModel):
    """Output model representing the content of the pirate code."""
    content: str = Field(..., description="The full text content of the pirate code document.")


class AddPirateArticleInput(BaseModel):
    """Input model for adding a new article to the pirate code."""
    article_title: str = Field(..., description="The title for the new article (e.g., 'Article VI: Keep Yer Ship Tidy').")
    article_text: str = Field(..., description="The text content of the new article.")

class WriteResult(BaseModel):
    """Output model representing the result of a write or edit operation."""
    message: str = Field(..., description="A confirmation or error message.")


class EditPirateArticleInput(BaseModel):
    """Input model for editing or deleting an article in the pirate code."""
    target_article_title: str = Field(..., description="The exact title of the article to edit or delete (e.g., 'Article I: Share the Booty').")
    action: str = Field(..., description="The action to perform: 'modify' or 'delete'.")
    new_article_text: str | None = Field(None, description="The new text content if action is 'modify'. Should start with '- '.")


# --- Task Management Models ---

class Task(BaseModel):
    """Represents a single task in the list."""
    task_id: int = Field(..., description="Unique identifier for the task")
    title: str = Field(..., description="The title of the task")
    assignee: str = Field(..., description="Who the task is assigned to (e.g., 'Philipp', 'Guillaume')")
    deadline: str = Field(..., description="Due date for the task (e.g., YYYY-MM-DD)")
    description: str = Field(..., description="Detailed description of the task")
    status: str = Field(default="Pending", description="Current status (e.g., Pending, In Progress, Done)")

class TaskListResult(BaseModel):
    """Structured result for reading the task list."""
    tasks: list[Task] = Field(..., description="List of tasks found in the document")
    raw_content: str = Field(..., description="The raw markdown content of the task list file")

class WriteTaskInput(BaseModel):
    """Input model for adding a new task."""
    task_title: str = Field(..., description="The title for the new task.")
    assignee: str = Field(..., description="Who the task should be assigned to.")
    deadline: str = Field(..., description="The deadline for the task (YYYY-MM-DD).")
    description: str = Field(..., description="A description of the task.")
    user_name: str = Field(..., description="The name of the user whose list to modify ('Philipp' or 'Guillaume').") # Added to specify target list

class EditTaskInput(BaseModel):
    """Input model for editing or deleting a task."""
    task_id: int = Field(..., description="The ID of the task to modify or delete.")
    action: str = Field(..., description="The action to perform: 'modify' or 'delete'.")
    user_name: str = Field(..., description="The name of the user whose list to modify ('Philipp' or 'Guillaume').") # Added to specify target list
    # Optional fields for modification
    title: typing.Optional[str] = Field(None, description="The new title if action is 'modify'.")
    assignee: typing.Optional[str] = Field(None, description="The new assignee if action is 'modify'.")
    deadline: typing.Optional[str] = Field(None, description="The new deadline if action is 'modify'.")
    description: typing.Optional[str] = Field(None, description="The new description if action is 'modify'.")
    status: typing.Optional[str] = Field(None, description="The new status if action is 'modify'.")

class TaskOperationResult(BaseModel):
    """Output model representing the result of a task write or edit operation."""
    status: str = Field(..., description="Indicates success or error.")
    message: str = Field(..., description="A confirmation or error message.")
    task_id: int | None = Field(None, description="The ID of the task affected (useful for creation).")


# --- Generic Tool Result Model ---

class ToolResult(BaseModel):
    """Generic output model for tools, indicating success or failure."""
    status: typing.Literal["success", "error"] = Field(..., description="Indicates if the operation was successful or encountered an error.")
    result: typing.Optional[dict] = Field(None, description="A dictionary containing the successful result data, if applicable.")
    error_message: typing.Optional[str] = Field(None, description="A message describing the error, if status is 'error'.")
