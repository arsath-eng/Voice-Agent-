import requests
import json
from datetime import datetime

# Assuming parse_datetime is available from your calendar_utils.py
# If it's in a different location, adjust the import.
# For this example, let's assume it's accessible or we define a simple version here.
# from .calendar_utils import parse_datetime # If in the same directory structure

NESTJS_BACKEND_URL = "http://localhost:3000" # CHANGE IF NEEDED

def parse_datetime_for_iso(datetime_str: str) -> datetime | None:
    """
    Parses a datetime string and returns a datetime object.
    You should reuse or enhance your existing parse_datetime from calendar_utils.
    This is a simplified placeholder.
    """
    if not datetime_str:
        return None
    # Example formats, your original parse_datetime is more comprehensive
    formats_to_try = [
        "%Y-%m-%d %H:%M", "%Y-%m-%d %I:%M %p", 
        "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"
    ] 
    for fmt in formats_to_try:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    try: # Try direct ISO format as well
        return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    except ValueError:
        return None


def create_event_nestjs(summary: str, start_time_str: str, end_time_str: str, time_zone: str = "Asia/Colombo") -> dict:
    """
    Creates a new event by calling the NestJS backend API.
    The NestJS backend will handle saving to its database and pushing to Google Calendar if connected.

    Args:
        summary (str): Event title/summary.
        start_time_str (str): Start time as a string (e.g., "tomorrow 2 PM", "2025-12-25 10:00").
        end_time_str (str): End time as a string.
        time_zone (str, optional): Timezone for the event. Defaults to "Asia/Colombo".

    Returns:
        dict: Response indicating success or failure.
    """
    # The agent will pass natural language times. We need to parse them.
    # Your parse_datetime from calendar_utils should be used here.
    # For now, this is a placeholder for robust parsing logic.
    start_dt = parse_datetime_for_iso(start_time_str)
    end_dt = parse_datetime_for_iso(end_time_str)

    if not start_dt or not end_dt:
        return {
            "status": "error",
            "message": f"Invalid start or end time format. Could not parse '{start_time_str}' or '{end_time_str}'. Please provide a clear date and time.",
        }

    # Convert to ISO format for NestJS DTO
    # Your NestJS CreateEventDto expects: title, start, end, backgroundColor, timeZone
    payload = {
        "title": summary,
        "start": start_dt.isoformat(),
        "end": end_dt.isoformat(),
        "timeZone": time_zone, # Your NestJS DTO includes this
        "backgroundColor": "#def5e6"  # Default or agent could provide
    }

    try:
        # print(f"Calling NestJS to create event: {payload}") # For debugging
        response = requests.post(f"{NESTJS_BACKEND_URL}/events", json=payload)
        response.raise_for_status()  # Raises an exception for 4XX/5XX status codes

        # The NestJS backend handles DB save and Google Calendar push
        return {
            "status": "success",
            "message": f"Event '{summary}' creation request sent to backend.",
            "details": response.json() # Return details from NestJS if needed
        }
    except requests.exceptions.HTTPError as http_err:
        error_content = http_err.response.json() if http_err.response else str(http_err)
        return {"status": "error", "message": f"NestJS API error: {error_content}"}
    except requests.exceptions.RequestException as req_err:
        return {"status": "error", "message": f"Failed to connect to NestJS backend: {str(req_err)}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}