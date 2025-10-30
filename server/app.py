import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Argus Cloud API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Initialize database
def init_db():
    """Initialize database tables"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create memory table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB
            )
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization error: {e}")

# Models
class MemoryItem(BaseModel):
    content: str
    metadata: Optional[dict] = None

class MemoryResponse(BaseModel):
    id: int
    content: str
    timestamp: str
    metadata: Optional[dict] = None

# Mount static files
client_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "client")
if os.path.exists(client_path):
    app.mount("/static", StaticFiles(directory=client_path), name="static")

# Routes
@app.get("/")
async def root():
    """Root endpoint - serve the client HTML"""
    html_path = os.path.join(client_path, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {
        "status": "online",
        "service": "Argus Cloud API",
        "version": "1.0.0",
        "endpoints": {
            "memory": "/api/memory",
            "health": "/api/health"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Argus Cloud is running successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/api/memory")
async def get_memories():
    """Get all memories"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM memory ORDER BY timestamp DESC")
        memories = cur.fetchall()
        cur.close()
        conn.close()
        return {
            "status": "success",
            "count": len(memories),
            "data": memories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch memories: {str(e)}")

@app.post("/api/memory")
async def create_memory(item: MemoryItem):
    """Create a new memory"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        metadata_json = json.dumps(item.metadata) if item.metadata else None
        cur.execute(
            "INSERT INTO memory (content, metadata) VALUES (%s, %s::jsonb) RETURNING *",
            (item.content, metadata_json)
        )
        memory = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {
            "status": "success",
            "message": "Memory created successfully",
            "data": memory
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create memory: {str(e)}")

@app.delete("/api/memory/{memory_id}")
async def delete_memory(memory_id: int):
    """Delete a memory"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM memory WHERE id = %s RETURNING *", (memory_id,))
        memory = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        
        return {
            "status": "success",
            "message": "Memory deleted successfully",
            "data": memory
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete memory: {str(e)}")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# For Vercel
app = app
