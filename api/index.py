import os
import sys
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

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

# Pydantic models
class Memory(BaseModel):
    content: str
    metadata: Optional[dict] = {}

# Routes
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Argus Cloud API",
        "version": "1.0.0"
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        conn.close()
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Argus Cloud is running successfully"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

@app.get("/api/memory")
def get_memories():
    """Get all memories"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, content, metadata, timestamp
            FROM memory
            ORDER BY timestamp DESC
        """)
        
        memories = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return {
            "status": "success",
            "count": len(memories),
            "data": memories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/memory")
def create_memory(memory: Memory):
    """Create a new memory"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Convert metadata dict to JSON string
        metadata_json = json.dumps(memory.metadata)
        
        cur.execute("""
            INSERT INTO memory (content, metadata)
            VALUES (%s, %s)
            RETURNING id, content, metadata, timestamp
        """, (memory.content, metadata_json))
        
        new_memory = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "status": "success",
            "message": "Memory created successfully",
            "data": new_memory
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/memory/{memory_id}")
def delete_memory(memory_id: int):
    """Delete a memory by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM memory WHERE id = %s RETURNING id", (memory_id,))
        deleted = cur.fetchone()
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Memory not found")
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "status": "success",
            "message": "Memory deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# This is required for Vercel
handler = app
