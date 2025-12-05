import requests
import json
from datetime import datetime


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

def update_event_nestjs(event_id: str, summary: str  , start_time_str: str  , end_time_str: str  , time_zone: str  ) -> dict:
    """
    Updates an existing event by calling the NestJS backend API.
    Provide only the fields you want to change.

    Args:
        event_id (str): The ID of the event to update (obtained from list_events_nestjs).
        summary (str, optional): New event title/summary.
        start_time_str (str, optional): New start time string.
        end_time_str (str, optional): New end time string.
        time_zone (str, optional): New timezone for the event.

    Returns:
        dict: Response indicating success or failure.
    """
    if not event_id:
        return {"status": "error", "message": "Event ID is required to update an event."}

    payload = {}
    if summary is not None:
        payload["title"] = summary
    
    if start_time_str is not None:
        start_dt = parse_datetime_for_iso(start_time_str) # Assuming this function exists
        if not start_dt:
            return {"status": "error", "message": f"Invalid start time format: {start_time_str}"}
        payload["start"] = start_dt.isoformat()
        
    if end_time_str is not None:
        end_dt = parse_datetime_for_iso(end_time_str) # Assuming this function exists
        if not end_dt:
            return {"status": "error", "message": f"Invalid end time format: {end_time_str}"}
        payload["end"] = end_dt.isoformat()

    if time_zone is not None:
        payload["timeZone"] = time_zone
        
    if not payload:
        return {"status": "info", "message": "No changes provided to update the event."}

    try:
        response = requests.put(f"{NESTJS_BACKEND_URL}/events/{event_id}", json=payload)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Event '{event_id}' update request sent to backend.",
            "details": response.json()
        }
    except requests.exceptions.HTTPError as http_err:
        error_message = str(http_err)
        try:
            error_content = http_err.response.json()
            if isinstance(error_content, dict) and 'message' in error_content:
                error_message = error_content['message']
            else:
                error_message = str(error_content)
        except ValueError: # Not JSON
            pass # Keep original http_err string
        return {"status": "error", "message": f"NestJS API error updating event {event_id}: {error_message}"}
    except requests.exceptions.RequestException as req_err:
        return {"status": "error", "message": f"Failed to connect to NestJS backend: {str(req_err)}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}