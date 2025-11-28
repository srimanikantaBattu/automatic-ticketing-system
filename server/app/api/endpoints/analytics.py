from fastapi import APIRouter
from app.db.mongodb import db

router = APIRouter()

@router.get("/summary")
async def get_analytics_summary():
    total = await db.get_db()["tickets"].count_documents({})
    
    # Aggregation for Priority
    priority_cursor = db.get_db()["tickets"].aggregate([
        {"$group": {"_id": "$priority", "count": {"$sum": 1}}}
    ])
    priority_counts = {doc["_id"]: doc["count"] for doc in await priority_cursor.to_list(None)}

    # Aggregation for Category
    category_cursor = db.get_db()["tickets"].aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ])
    category_counts = {doc["_id"]: doc["count"] for doc in await category_cursor.to_list(None)}

    return {
        "total_tickets": total,
        "priority_breakdown": priority_counts,
        "category_breakdown": category_counts
    }

@router.get("/overrides")
async def get_overrides_summary():
    # Count documents where overrides array is not empty
    total_overridden = await db.get_db()["tickets"].count_documents({"overrides": {"$ne": []}})
    
    # Aggregate overrides by field
    pipeline = [
        {"$unwind": "$overrides"},
        {"$group": {"_id": "$overrides.field", "count": {"$sum": 1}}}
    ]
    cursor = db.get_db()["tickets"].aggregate(pipeline)
    field_breakdown = {doc["_id"]: doc["count"] for doc in await cursor.to_list(None)}
    
    return {
        "total_tickets_with_overrides": total_overridden,
        "overrides_by_field": field_breakdown
    }
