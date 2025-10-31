import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise Exception(f"Database connection failed: {str(e)}")

# Routes
@app.route('/')
def read_root():
    return jsonify({
        "status": "online",
        "service": "Argus Cloud API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "ask": "/api/ask",
            "memory": "/api/memory"
        }
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "openai": "configured" if openai_client else "not configured",
            "message": "Argus Cloud is running successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Ask a question and get an intelligent answer"""
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        if not openai_client:
            return jsonify({"error": "OpenAI API is not configured"}), 500
        
        # Get relevant memories from database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT content, metadata, timestamp
            FROM memory
            ORDER BY timestamp DESC
            LIMIT 10
        """)
        memories = cur.fetchall()
        cur.close()
        conn.close()
        
        # Build context from memories
        context = "Previous memories:\n"
        for mem in memories:
            context += f"- {mem['content']}\n"
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are Argus, an intelligent AI agent with memory. You have access to previous memories. Answer questions intelligently and remember context.\n\n{context}"
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        
        # Save the Q&A to memory
        metadata_json = json.dumps({
            "type": "qa",
            "question": question,
            "model": "gpt-4.1-mini"
        })
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO memory (content, metadata)
            VALUES (%s, %s)
            RETURNING id
        """, (f"Q: {question}\nA: {answer}", metadata_json))
        memory_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "question": question,
            "answer": answer,
            "memory_id": memory_id,
            "timestamp": response.created
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/memory', methods=['GET'])
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
        
        return jsonify({
            "status": "success",
            "count": len(memories),
            "data": memories
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/memory', methods=['POST'])
def create_memory():
    """Create a new memory"""
    try:
        data = request.get_json()
        content = data.get('content')
        metadata = data.get('metadata', {})
        
        if not content:
            return jsonify({"error": "Content is required"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Convert metadata dict to JSON string
        metadata_json = json.dumps(metadata)
        
        cur.execute("""
            INSERT INTO memory (content, metadata)
            VALUES (%s, %s)
            RETURNING id, content, metadata, timestamp
        """, (content, metadata_json))
        
        new_memory = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "Memory created successfully",
            "data": new_memory
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/memory/<int:memory_id>', methods=['DELETE'])
def delete_memory(memory_id):
    """Delete a memory by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM memory WHERE id = %s RETURNING id", (memory_id,))
        deleted = cur.fetchone()
        
        if not deleted:
            return jsonify({"error": "Memory not found"}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "Memory deleted successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel handler
if __name__ == '__main__':
    app.run(debug=True)
