import google.generativeai as genai
import json
from typing import Dict, Any
from app.core.config import settings

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

def analyze_ticket(subject: str, description: str, user_urgency: str) -> Dict[str, Any]:
    if not settings.GEMINI_API_KEY:
        # Rule-based Fallback
        return _rule_based_analysis(subject, description)

    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""
    You are an intelligent IT support automation agent. Analyze the following support ticket and provide a structured JSON response.
    
    Ticket Details:
    - Subject: {subject}
    - Description: {description}
    - User Reported Urgency: {user_urgency}

    Task:
    1. Categorize the issue (e.g., Hardware, Software, Network, Access, Security, Billing, etc.).
    2. Assign a Priority level (Critical, High, Medium, Low) based on the actual impact described.
    3. Suggest the best resolution team.
    4. Generate a polite, professional automated first response with 2-3 troubleshooting steps.
    5. Provide a confidence score (0.0 to 1.0).

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
        text_response = response.text.strip()
        if text_response.startswith("```json"):
            text_response = text_response[7:-3]
        elif text_response.startswith("```"):
            text_response = text_response[3:-3]
        
        return json.loads(text_response)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return _rule_based_analysis(subject, description)

def _rule_based_analysis(subject: str, description: str) -> Dict[str, Any]:
    """Simple keyword-based fallback analysis"""
    text = (subject + " " + description).lower()
    
    category = "General"
    priority = "Medium"
    team = "Support"
    
    if any(w in text for w in ["password", "login", "access", "account"]):
        category = "Access"
        team = "Identity Management"
    elif any(w in text for w in ["wifi", "internet", "slow", "connect"]):
        category = "Network"
        team = "Network Ops"
    elif any(w in text for w in ["crash", "error", "bug", "fail"]):
        category = "Software"
        team = "App Support"
    elif any(w in text for w in ["printer", "laptop", "screen", "mouse"]):
        category = "Hardware"
        team = "IT Helpdesk"
        
    if "urgent" in text or "critical" in text or "immediately" in text:
        priority = "High"
        
    return {
        "category": category,
        "priority": priority,
        "suggested_team": team,
        "auto_response": f"Thank you for your ticket regarding {category}. We have assigned it to {team}.",
        "confidence_score": 0.5
    }
