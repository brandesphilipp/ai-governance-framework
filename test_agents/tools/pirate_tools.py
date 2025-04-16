import typing
import re
from pydantic import ValidationError
# Removed incorrect import: from google.adk.tools import tool

# Import required models - adjust path relative to this new location
from ..models import AddPirateArticleInput, EditPirateArticleInput, WriteResult

PIRATE_CODE_PATH = "documents/pirate_code_101.md"

# Removed incorrect @tool decorator
def read_pirate_code():
    """
    Reads the content of the pirate code document (pirate_code_101.md).

    Returns:
        dict: A dictionary with status and result (content) or error_message.
    """
    try:
        with open(PIRATE_CODE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        return {
            "status": "success",
            "result": {"content": content}
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "error_message": f"File not found: {PIRATE_CODE_PATH}",
            "pirate_message": "Shiver me timbers! The pirate code file be missin'."
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to read file {PIRATE_CODE_PATH}: {str(e)}",
            "pirate_message": "Blast! Couldn't read the pirate code."
        }

# Removed incorrect @tool decorator
def write_pirate_code(article_title: str, article_text: str):
    """
    Appends a new article to the pirate code document (pirate_code_101.md).

    Args:
        article_title (str): The title for the new article (e.g., 'Article VI: Keep Yer Ship Tidy').
        article_text (str): The text content of the new article.

    Returns:
        dict: A dictionary with status and result (message) or error_message.
    """
    try:
        # Validate input using Pydantic model
        try:
            validated_input = AddPirateArticleInput(article_title=article_title, article_text=article_text)
        except ValidationError as e:
             return {
                "status": "error",
                "error_message": f"Input validation failed: {str(e)}"
            }

        # Format the new article
        formatted_title = validated_input.article_title
        if not formatted_title.startswith("## "):
             formatted_title = f"## {formatted_title}"

        formatted_text = validated_input.article_text
        if not formatted_text.startswith("- "):
            formatted_text = f"- {formatted_text}"
        if not formatted_text.endswith("\n"):
            formatted_text += "\n"

        new_article_content = f"\n\n{formatted_title}\n{formatted_text}"

        # Append to the file
        with open(PIRATE_CODE_PATH, 'a', encoding='utf-8') as f:
            f.write(new_article_content)

        result_model = WriteResult(message=f"Success! Added '{validated_input.article_title}' to the Pirate Code.")
        return {
            "status": "success",
            "result": result_model.model_dump()
        }

    except FileNotFoundError:
         return {
            "status": "error",
            "error_message": f"File not found: {PIRATE_CODE_PATH}. Cannot add article.",
            "pirate_message": "Shiver me timbers! The pirate code file be missin'."
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to write to file {PIRATE_CODE_PATH}: {str(e)}",
            "pirate_message": "Arrr! Failed to add article to the pirate code."
        }

# Removed incorrect @tool decorator
def edit_pirate_code(target_article_title: str, action: str, new_article_text: typing.Optional[str] = None):
    """
    Edits or deletes an existing article in the pirate code document (pirate_code_101.md).

    Args:
        target_article_title (str): The exact title of the article to edit or delete (e.g., 'Article I: Share the Booty'). Must include the '## '.
        action (str): The action to perform: 'modify' or 'delete'.
        new_article_text (typing.Optional[str]): The new text content if action is 'modify'. Should start with '- '. Required for 'modify', ignored for 'delete'.

    Returns:
        dict: A dictionary with status and result (message) or error_message.
    """
    try:
        # --- Input Validation ---
        try:
            # Ensure target title starts correctly for matching
            if not target_article_title.startswith("## "):
                 target_article_title = f"## {target_article_title}"

            validated_input = EditPirateArticleInput(
                target_article_title=target_article_title,
                action=action,
                new_article_text=new_article_text
            )
        except ValidationError as e:
             return {
                "status": "error",
                "error_message": f"Input validation failed: {str(e)}"
            }

        # Internal logic check
        if validated_input.action == 'modify' and validated_input.new_article_text is None:
            raise ValueError("Modification action requires 'new_article_text'.")

        # Prepare new text if modifying
        current_new_text = validated_input.new_article_text
        if validated_input.action == 'modify' and current_new_text:
             if not current_new_text.startswith("- "):
                 current_new_text = f"- {current_new_text}"
             if not current_new_text.endswith("\n"):
                 current_new_text += "\n"

    except ValueError as e: # Catch specific validation error
         return {
            "status": "error",
            "error_message": f"Invalid input: {str(e)}"
        }

    # --- File Processing ---
    try:
        with open(PIRATE_CODE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        sections = re.split(r'(\n*\#\#\s)', content)
        processed_sections = []
        article_found = False

        if sections[0].strip():
             processed_sections.append(sections[0])

        for i in range(1, len(sections), 2):
            delimiter = sections[i]
            section_content = sections[i+1]
            full_title_line = section_content.split('\n', 1)[0].strip()
            current_title = f"## {full_title_line}"

            if current_title == validated_input.target_article_title:
                article_found = True
                if validated_input.action == 'modify':
                    modified_section = f"{delimiter}{full_title_line}\n{current_new_text}"
                    processed_sections.append(modified_section)
                elif validated_input.action == 'delete':
                    pass # Skip section
            else:
                processed_sections.append(delimiter + section_content)

        if not article_found:
            return {
                "status": "error",
                "error_message": f"Article not found: '{validated_input.target_article_title}'.",
                "pirate_message": "Blast it! Couldn't find the article."
            }

        new_content = "".join(processed_sections)

        with open(PIRATE_CODE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)

        # --- Return Success ---
        action_verb = "modified" if validated_input.action == 'modify' else "deleted"
        result_model = WriteResult(message=f"Success! {action_verb.capitalize()} article '{validated_input.target_article_title}'.")
        return {
            "status": "success",
            "result": result_model.model_dump()
        }

    except FileNotFoundError:
         return {
            "status": "error",
            "error_message": f"File not found: {PIRATE_CODE_PATH}. Cannot edit article.",
            "pirate_message": "Shiver me timbers! The pirate code file be missin'."
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to edit file {PIRATE_CODE_PATH}: {str(e)}",
            "pirate_message": "Arrr! Failed to edit the pirate code."
        }
