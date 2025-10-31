from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.get("/")
@app.get("/api/health")
async def health():
    return JSONResponse({
        "status": "healthy",
        "message": "Argus Cloud is running!"
    })

# Vercel handler
from mangum import Mangum
handler = Mangum(app)
