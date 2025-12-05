# Jarvis Voice Agent

A voice-enabled AI agent that helps with scheduling and calendar operations using Google Calendar.

## Repository

[https://github.com/arsath-eng/Voice-Agent-](https://github.com/arsath-eng/Voice-Agent-)

## Prerequisites

- Python 3.10 or higher
- A Google Cloud Project.
- A Google Gemini API Key.

## Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/arsath-eng/Voice-Agent-.git adk-voice-agent
    cd adk-voice-agent
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
    - Create a `.env` file in the root directory.
    - Add your Gemini API key:
      ```env
      GOOGLE_API_KEY=your_api_key_here
      ```

5.  **Google Calendar Authentication Setup**:
    To allow the agent to access your calendar, you need to set up Google Cloud credentials:
    
    1.  **Create a Project**: Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
    2.  **Enable API**: 
        - Go to "APIs & Services" > "Library".
        - Search for **"Google Calendar API"** and enable it.
    3.  **Configure OAuth Consent Screen**:
        - Go to "APIs & Services" > "OAuth consent screen".
        - Choose **"External"** and click Create.
        - Fill in the required app information (App name, User support email, Developer contact information).
        - Click "Save and Continue".
        - **Scopes**: Add `.../auth/calendar` scope if you want, or just "Save and Continue" (the app requests it dynamically).
        - **Test Users**: Add your Google email address as a test user. This is crucial for testing without verification.
    4.  **Create Credentials**:
        - Go to "APIs & Services" > "Credentials".
        - Click "Create Credentials" > **"OAuth client ID"**.
        - Application type: **"Desktop app"**.
        - Name: "Jarvis Agent" (or any name).
        - Click "Create".
    5.  **Download Credentials**:
        - Download the JSON file for the created OAuth client.
        - Rename it to `credentials.json`.
        - Place it in the root directory of this project (`adk-voice-agent/`).

6.  **Authenticate**:
    - Run the setup script:
      ```bash
      python setup_calendar_auth.py
      ```
    - A browser window will open. Log in with the Google account you added as a test user.
    - Grant the requested permissions.
    - Once successful, a `token.json` (or similar token file) will be created in your user directory, and the script will confirm success.

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
