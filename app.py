from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from codegeneration import AgentResponse, run_crew_ai
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create a new request model that matches your frontend
class CodeRequest(BaseModel):
    code: str
    syntax: Optional[str] = None

# Keep your original model for backward compatibility
class CodeAnalysisRequest(BaseModel):
    query: str
    code: str

app = FastAPI(title="Code Generation Agentic AI")

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
async def process_code(request: CodeRequest):
    """
    Process code with syntax specification using CrewAI
    """
    try:
        # Use the syntax field as the query if provided, otherwise use a default
        query = request.syntax if request.syntax else "Analyze this code"
        result = run_crew_ai(query, request.code)
        
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
