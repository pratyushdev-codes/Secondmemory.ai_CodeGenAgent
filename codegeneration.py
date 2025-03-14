from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Optional, Dict
from crewai import Crew, Process
from tasks import research_task, code_writer
from agents import code_researcher, code_generator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Code Generation Agentic AI")

# Pydantic models for request validation
class CodeAnalysisRequest(BaseModel):
    code: str
    query: str

class DetailedOutput(BaseModel):
    final_answer: str
    thoughts: Optional[str]
    tool_input: Optional[str]

class AgentResponse(BaseModel):
    status: str
    message: str
    details: DetailedOutput

def parse_crew_output(crew_output: Any) -> DetailedOutput:
    """
    Parse the CrewOutput object from CrewAI
    """
    try:
        # Access the attributes directly from the CrewOutput object
        return DetailedOutput(
            final_answer=str(getattr(crew_output, 'final_answer', str(crew_output))),
            thoughts=str(getattr(crew_output, 'thoughts', '')),
            tool_input=str(getattr(crew_output, 'tool_input', ''))
        )
    except Exception as e:
        # Fallback if we can't access the attributes
        return DetailedOutput(
            final_answer=str(crew_output),
            thoughts=None,
            tool_input=None
        )

def run_crew_ai(query: str, code: str) -> DetailedOutput:
    """
    Run the CrewAI workflow with the given query and code
    """
    try:
        crew = Crew(
            agents=[code_researcher, code_generator],
            tasks=[research_task, code_writer],
            process=Process.sequential,
        )
        
        result = crew.kickoff(inputs={
            'query': query,
            'code': code
        })
        
        return parse_crew_output(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CrewAI Error: {str(e)}")
    
    
    
    
