from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, List, Dict, Any
from datetime import datetime
from typing_extensions import Annotated

# Helper for Mongo ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class TicketBase(BaseModel):
    submitter: str
    subject: str
    description: str
    urgency: str

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_team: Optional[str] = None
    human_response: Optional[str] = None

class Ticket(TicketBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    ticket_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    status: str = "new"
    
    # AI Fields (The original AI prediction)
    ai_category: Optional[str] = None
    ai_priority: Optional[str] = None
    ai_suggested_team: Optional[str] = None
    ai_suggested_response: Optional[str] = None
    ai_confidence_score: Optional[float] = None
    
    # Current Fields (Can be overridden by human)
    category: Optional[str] = None
    priority: Optional[str] = None
    suggested_team: Optional[str] = None
    auto_response: Optional[str] = None
    confidence_score: Optional[float] = None
    
    # Overrides
    overrides: List[Dict[str, Any]] = []

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
