import requests
import json
from datetime import datetime, timedelta


NESTJS_BACKEND_URL = "http://localhost:3000" # CHANGE IF NEEDED
# You'd reuse parse_datetime_for_iso or your more robust parse_datetime here
# from .create_event_nestjs import parse_datetime_for_iso # Example if it's in another file

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

def list_events_nestjs(start_date_str: str  , days: int) -> dict:
    """
    Lists events by fetching them from the NestJS backend.
    The NestJS backend provides events from its own database.
    Note: Currently fetches all events and filters locally if a start date is provided.
          For efficiency, the NestJS backend should ideally support date range filtering.

    Args:
        start_date_str (str | None, optional): Start date string (e.g., "today", "next Monday"). 
                                               If None, defaults to today.
        days (int, optional): Number of days to look ahead from the start_date. Defaults to 7.

    Returns:
        dict: Response with list of events or error.
    """
    if start_date_str:
        # Robust date parsing needed here (e.g., from calendar_utils.py)
        # This is a simplified placeholder
        start_dt_filter = parse_datetime_for_iso(start_date_str)
        if not start_dt_filter:
             # Default to today if parsing fails but a string was given
            start_dt_filter = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # Default to today if no start_date_str is provided
        start_dt_filter = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    end_dt_filter = start_dt_filter + timedelta(days=days)

    try:
        response = requests.get(f"{NESTJS_BACKEND_URL}/events")
        response.raise_for_status()
        all_events_from_nestjs = response.json() # Expects a list of event objects

        # Filter events locally based on the date range
        # NestJS event structure from your entity: id, title, start, end, backgroundColor, timeZone
        filtered_events = []
        for event_data in all_events_from_nestjs:
            event_start_str = event_data.get("start")
            if event_start_str:
                try:
                    # NestJS stores dates as ISO strings, convert them to datetime
                    event_start_dt = datetime.fromisoformat(event_start_str.replace('Z', '+00:00'))
                    # Make event_start_dt timezone-aware if start_dt_filter is, or compare naively
                    # For simplicity, assuming naive comparison or that both are UTC after parsing
                    if start_dt_filter.tzinfo is None and event_start_dt.tzinfo is not None:
                        event_start_dt = event_start_dt.replace(tzinfo=None)
                    
                    if start_dt_filter <= event_start_dt < end_dt_filter:
                        filtered_events.append({
                            "id": event_data.get("id"),
                            "summary": event_data.get("title"),
                            "start": event_start_str, # Keep original string for display consistency
                            "end": event_data.get("end"),
                            "timeZone": event_data.get("timeZone"),
                            "backgroundColor": event_data.get("backgroundColor")
                        })
                except ValueError:
                    print(f"Warning: Could not parse date for event: {event_data.get('title')}")
                    continue # Skip event if date is unparseable
        
        if not filtered_events:
            return {"status": "success", "message": "No events found in the specified range.", "events": []}

        return {
            "status": "success",
            "message": f"Found {len(filtered_events)} event(s).",
            "events": filtered_events
        }
    except requests.exceptions.HTTPError as http_err:
        error_content = http_err.response.json() if http_err.response else str(http_err)
        return {"status": "error", "message": f"NestJS API error: {error_content}", "events": []}
    except requests.exceptions.RequestException as req_err:
        return {"status": "error", "message": f"Failed to connect to NestJS backend: {str(req_err)}", "events": []}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}", "events": []}