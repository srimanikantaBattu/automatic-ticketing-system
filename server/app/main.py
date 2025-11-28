from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
from app.core.config import settings
from app.db.mongodb import db
from app.api.endpoints import tickets, analytics

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Events
@app.on_event("startup")
async def startup_db_client():
    logger.info("Connecting to MongoDB...")
    db.connect()
    logger.info("MongoDB connected.")

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Closing MongoDB connection...")
    db.close()
    logger.info("MongoDB connection closed.")

# Routers
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(analytics.router, prefix="/stats", tags=["analytics"])

@app.get("/")
def read_root():
    return {"message": "Smart Ticketing API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
