import datetime
import typing
from zoneinfo import ZoneInfo
from pydantic import ValidationError
# Removed incorrect import: from google.adk.tools import tool

# Import required models - adjust path relative to this new location
from ..models import GetCurrentTimeInput, TimeResult

# Removed incorrect @tool decorator
def get_current_time(time_zone: str):
    """
    Get current time in a specified time zone.

    Args:
        time_zone (str): The time zone to get the current time for (e.g., 'America/New_York', 'Europe/London')

    Returns:
        dict: A dictionary with status, result/error_message
    """
    try:
        # Validate input using Pydantic model
        validated_input = GetCurrentTimeInput(time_zone=time_zone)

        # Get time zone
        try:
            tz = ZoneInfo(validated_input.time_zone)
        except Exception as e:
            # Standardized error message
            return {
                "status": "error",
                "error_message": f"Invalid or unknown time zone specified: {validated_input.time_zone}"
            }

        # Get current time in the specified timezone
        current_time = datetime.datetime.now(tz)

        # Create result using Pydantic model
        time_result = TimeResult(
            time_zone=validated_input.time_zone,
            date_time=current_time.strftime("%I:%M %p on %B %d, %Y"),
            is_daylight_savings_time=current_time.dst() != datetime.timedelta(0)
        )

        return {
            "status": "success",
            "result": time_result.model_dump()
        }

    except ValidationError as e:
        # Standardized error message
        return {
            "status": "error",
            "error_message": f"Input validation failed: {str(e)}"
        }
    except Exception as e:
        # Standardized error message
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred while getting the time: {str(e)}"
        }
