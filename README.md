# Jarvis Voice Agent

A voice-enabled AI agent that helps with scheduling and calendar operations using Google Calendar.

## Prerequisites

- Python 3.10 or higher
- A Google Cloud Project with the **Google Calendar API** enabled.
- OAuth 2.0 Desktop App credentials (`credentials.json`).
- A Google Gemini API Key.

## Setup

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd bhancockio-adk-voice-agent
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration**:
    - Ensure you have a `.env` file in the root directory with your Gemini API key:
      ```env
      GOOGLE_API_KEY=your_api_key_here
      ```

5.  **Google Calendar Authentication**:
    - Place your downloaded `credentials.json` file in the root directory.
    - Run the setup script to authenticate:
      ```bash
      python setup_calendar_auth.py
      ```
    - Follow the on-screen instructions to log in and authorize the app.

## Running the Application

To start the Jarvis agent server:

```bash
uvicorn app.main:app --reload --port 8000
```

The application will be available at `http://localhost:8000`.

## Usage

- Open `http://localhost:8000` in your browser.
- Connect to the agent.
- You can interact with Jarvis via voice or text to manage your calendar events.
