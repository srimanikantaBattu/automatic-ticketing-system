import os
import google.generativeai as genai
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def analyze_ticket(subject: str, description: str, user_urgency: str) -> Dict[str, Any]:
    if not API_KEY:
        return {
            "category": "Uncategorized (No API Key)",
            "priority": "Medium",
            "suggested_team": "General Support",
            "auto_response": "AI service is not configured. Please check the backend configuration.",
            "confidence_score": 0.0
        }

    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""
    You are an intelligent IT support automation agent. Analyze the following support ticket and provide a structured JSON response.
    
    Ticket Details:
    - Subject: {subject}
    - Description: {description}
    - User Reported Urgency: {user_urgency}

    Task:
    1. Categorize the issue (e.g., Hardware, Software, Network, Access, Security, Billing, etc.).
    2. Assign a Priority level (Critical, High, Medium, Low) based on the actual impact described, not just the user's urgency.
    3. Suggest the best resolution team (e.g., Network Ops, IT Support, Security Team, DevOps, Finance).
    4. Generate a polite, professional, and helpful automated first response. Include 2-3 troubleshooting steps if applicable.
    5. Provide a confidence score (0.0 to 1.0) for your classification.

    Output must be valid JSON strictly in this format:
    {{
        "category": "string",
        "priority": "string",
        "suggested_team": "string",
        "auto_response": "string",
        "confidence_score": float
    }}
    """

    try:
        response = model.generate_content(prompt)
        # Clean up the response to ensure it's valid JSON
        text_response = response.text.strip()
        if text_response.startswith("```json"):
            text_response = text_response[7:-3]
        elif text_response.startswith("```"):
            text_response = text_response[3:-3]
        
        return json.loads(text_response)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return {
            "category": "Error",
            "priority": "High",
            "suggested_team": "Human Review",
            "auto_response": "We are currently experiencing high load. A human agent will review your ticket shortly.",
            "confidence_score": 0.0
        }
