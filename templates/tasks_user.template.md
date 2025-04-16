<!-- 
**WARNING:** This is a template file. Copy it to your runtime documents directory 
(configured via DOCUMENTS_DIR environment variable, defaults to 'documents/') 
and rename it (e.g., tasks_Philipp.md). Populate it with actual user tasks. 
DO NOT commit sensitive task information from your populated version to version control.
-->

# Task List Template for [User Name]

<!-- 
This file tracks tasks assigned to a specific user. It's managed by the BusinessAgent.
The agent expects a Markdown table with the following columns: ID, Task, Status, Priority, Due Date, Notes.
The 'ID' should be a unique integer for each task within this user's list.
-->

| ID  | Task                 | Status      | Priority | Due Date   | Notes                       |
| --- | -------------------- | ----------- | -------- | ---------- | --------------------------- |
| 1   | [Example Task Title] | To Do       | High     | YYYY-MM-DD | [Optional details or links] |
| 2   | [Another Task]       | In Progress | Medium   | YYYY-MM-DD |                             |
| 3   | [Completed Task]     | Done        | Low      | YYYY-MM-DD |                             |

<!-- 
Instructions for the BusinessAgent:
- When writing a new task (`write_task`), append a new row with the next available ID.
- When editing a task (`edit_task`), find the row by ID and modify the specified fields or delete the row if the action is 'delete'.
- When reading tasks (`read_task_list`), parse this table.
-->

---
*Last Updated: [Date]*
