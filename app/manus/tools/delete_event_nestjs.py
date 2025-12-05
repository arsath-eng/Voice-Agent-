import requests
import json

NESTJS_BACKEND_URL = "http://localhost:3000" # CHANGE IF NEEDED

def delete_event_nestjs(event_id: str, confirm: bool = False) -> dict:
    """
    Deletes an event by calling the NestJS backend API.
    Requires confirmation.

    Args:
        event_id (str): The ID of the event to delete.
        confirm (bool, optional): Must be True to proceed with deletion. Defaults to False.

    Returns:
        dict: Response indicating success or failure.
    """
    if not confirm:
        return {
            "status": "confirmation_required",
            "message": "Deletion not confirmed. Please confirm you want to delete this event."
        }
    if not event_id:
        return {"status": "error", "message": "Event ID is required to delete an event."}

    try:
        response = requests.delete(f"{NESTJS_BACKEND_URL}/events/{event_id}")
        response.raise_for_status() # DELETE might return 204 No Content on success
        
        # For DELETE, a successful response might not have a JSON body (e.g., 204 No Content)
        if response.status_code == 200 or response.status_code == 204:
             message = f"Event '{event_id}' successfully deleted via backend."
        else:
             message = f"Event '{event_id}' deletion request sent to backend with status {response.status_code}."

        return {
            "status": "success",
            "message": message
        }
    except requests.exceptions.HTTPError as http_err:
        error_message = str(http_err)
        if http_err.response is not None:
            try:
                error_content = http_err.response.json()
                error_message = error_content.get('message', str(error_content))
            except ValueError: # Not JSON
                error_message = http_err.response.text if http_err.response.text else str(http_err)
        return {"status": "error", "message": f"NestJS API error deleting event {event_id}: {error_message}"}
    except requests.exceptions.RequestException as req_err:
        return {"status": "error", "message": f"Failed to connect to NestJS backend: {str(req_err)}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}