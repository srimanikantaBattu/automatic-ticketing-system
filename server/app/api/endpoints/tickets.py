from fastapi import APIRouter, HTTPException, Body
from typing import List
from datetime import datetime
import uuid
from app.models.ticket import Ticket, TicketCreate, TicketUpdate
from app.db.mongodb import db
from app.ai.service import analyze_ticket

router = APIRouter()

@router.post("/", response_model=Ticket)
async def create_ticket(ticket_in: TicketCreate):
    # 1. Generate ID and Timestamp
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.now()

    # 2. Call AI Service
    ai_result = analyze_ticket(
        subject=ticket_in.subject,
        description=ticket_in.description,
        user_urgency=ticket_in.urgency
    )

    # 3. Create Ticket Document
    ticket_doc = ticket_in.model_dump()
    
    # Extract AI results
    ai_cat = ai_result.get("category", "Uncategorized")
    ai_pri = ai_result.get("priority", "Medium")
    ai_team = ai_result.get("suggested_team", "Support")
    ai_resp = ai_result.get("auto_response", "")
    ai_conf = ai_result.get("confidence_score", 0.0)

    ticket_doc.update({
        "ticket_id": ticket_id,
        "created_at": timestamp,
        "updated_at": timestamp,
        "status": "new",
        
        # Set initial values to AI predictions
        "category": ai_cat,
        "priority": ai_pri,
        "suggested_team": ai_team,
        "auto_response": ai_resp,
        "confidence_score": ai_conf,
        
        # Store original AI predictions separately
        "ai_category": ai_cat,
        "ai_priority": ai_pri,
        "ai_suggested_team": ai_team,
        "ai_suggested_response": ai_resp,
        "ai_confidence_score": ai_conf,
        
        "overrides": []
    })

    # 4. Save to DB
    new_ticket = await db.get_db()["tickets"].insert_one(ticket_doc)
    created_ticket = await db.get_db()["tickets"].find_one({"_id": new_ticket.inserted_id})
    return created_ticket

@router.get("/", response_model=List[Ticket])
async def get_tickets():
    tickets = await db.get_db()["tickets"].find().to_list(1000)
    return tickets

@router.get("/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: str):
    ticket = await db.get_db()["tickets"].find_one({"ticket_id": ticket_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.patch("/{ticket_id}", response_model=Ticket)
async def update_ticket(ticket_id: str, update_data: TicketUpdate):
    ticket = await db.get_db()["tickets"].find_one({"ticket_id": ticket_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    
    if not update_dict:
        return ticket

    # Track overrides
    overrides = ticket.get("overrides", [])
    for key, value in update_dict.items():
        if key in ticket and ticket[key] != value:
            overrides.append({
                "field": key,
                "old_value": ticket[key],
                "new_value": value,
                "timestamp": datetime.now().isoformat()
            })

    update_dict["updated_at"] = datetime.now()
    update_dict["overrides"] = overrides

    await db.get_db()["tickets"].update_one(
        {"ticket_id": ticket_id},
        {"$set": update_dict}
    )
    
    updated_ticket = await db.get_db()["tickets"].find_one({"ticket_id": ticket_id})
    return updated_ticket
