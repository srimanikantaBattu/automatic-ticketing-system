from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    submitter: str
    subject: str
    description: str
    urgency: str  # User's perception of urgency

class Ticket(TicketCreate):
    ticket_id: str
    timestamp: str
    status: str = "new"
    
    # AI Enriched Fields
    priority: Optional[str] = None  # AI determined priority
    category: Optional[str] = None
    suggested_team: Optional[str] = None
    auto_response: Optional[str] = None
    confidence_score: Optional[float] = None
