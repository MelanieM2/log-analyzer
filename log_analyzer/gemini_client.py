"""
gemini_client.py

Sends structured log analysis summaries to the Gemini API and returns
a natural language interpretation of what the logs are telling us.
"""

import os
import sys #  for sys.exit() if the key is missing
from google import genai
# from google.genai.errors import APIError

def check_api_key() -> str:
    """Verify the Gemini API key is present in the environment. Returns the key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("CRITICAL ERROR: GEMINI_API_KEY is missing from system RAM!", file=sys.stderr)
        print("Please verify your ~/.bashrc configuration and run 'source ~/.bashrc'.", file=sys.stderr)
        sys.exit(1)
    return api_key


def analyze_logs(summary: dict) -> str:
    """Send log summary to Gemini and return a natural language analysis."""
    api_key = check_api_key()
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a systems reliability engineer analyzing application logs.
Here is a structured summary of a log file:

- Total entries: {summary['total']}
- Entries by level: {summary['by_level']}
- Entries by module: {summary['by_module']}
- Error messages: {summary['errors']}

Please provide:
1. A plain English summary of what these logs are telling us
2. Any concerns or patterns worth investigating
3. Suggested next steps if there are errors or warnings
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    result = response.text
    if result is None:
        return "No response received from Gemini API."
    return result