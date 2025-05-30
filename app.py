from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
from codegeneration import AgentResponse, CodeAnalysisRequest, run_crew_ai
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI(title="Code Generation Agentic AI")

# Configure CORS
origins = [
    "*"  # You can restrict this to your frontend domain, e.g., "https://yourdomain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],    # Allows all HTTP methods
    allow_headers=["*"],    # Allows all headers
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "active", "message": "Code Generation using AI Agents"}

@app.post("/syntax", response_model=AgentResponse)
async def analyze_syntax(request: CodeAnalysisRequest):
    """
    Analyze code syntax using CrewAI
    """
    try:
        result = run_crew_ai(request.query, request.code)
        return AgentResponse(
            status="success",
            message="Syntax analysis completed",
            details=result
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/code", response_model=AgentResponse)
async def process_code(request: CodeAnalysisRequest):
    """
    Process code with custom query using CrewAI
    """
    try:
        result = run_crew_ai(request.query, request.code)
        return AgentResponse(
            status="success",
            message="Code analysis completed",
            details=result
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "status": "error",
        "message": str(exc.detail),
        "details": None
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
