# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Any, Optional, Dict
# from crewai import Crew, Process
# from tasks import research_task, code_writer
# from agents import code_researcher, code_generator
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Initialize FastAPI
# app = FastAPI(title="Code Generation Agentic AI")

# # Pydantic models for request validation
# class CodeAnalysisRequest(BaseModel):
#     code: str
#     query: str

# class DetailedOutput(BaseModel):
#     final_answer: str
#     thoughts: Optional[str]
#     tool_input: Optional[str]

# class AgentResponse(BaseModel):
#     status: str
#     message: str
#     details: DetailedOutput

# def parse_crew_output(crew_output: Any) -> DetailedOutput:
#     """
#     Parse the CrewOutput object from CrewAI
#     """
#     try:
#         # Access the attributes directly from the CrewOutput object
#         return DetailedOutput(
#             final_answer=str(getattr(crew_output, 'final_answer', str(crew_output))),
#             thoughts=str(getattr(crew_output, 'thoughts', '')),
#             tool_input=str(getattr(crew_output, 'tool_input', ''))
#         )
#     except Exception as e:
#         # Fallback if we can't access the attributes
#         return DetailedOutput(
#             final_answer=str(crew_output),
#             thoughts=None,
#             tool_input=None
#         )

# def run_crew_ai(query: str, code: str) -> DetailedOutput:
#     """
#     Run the CrewAI workflow with the given query and code
#     """
#     try:
#         crew = Crew(
#             agents=[code_researcher, code_generator],
#             tasks=[research_task, code_writer],
#             process=Process.sequential,
#         )
        
#         result = crew.kickoff(inputs={
#             'query': query,
#             'code': code
#         })
        
#         return parse_crew_output(result)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"CrewAI Error: {str(e)}")
    
    
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Optional, Dict, List
from crewai import Crew, Process
from tasks import research_task, code_writer
from agents import code_researcher, code_generator
from dotenv import load_dotenv
import os
import re
import json

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
    thoughts: Optional[str] = None
    tool_input: Optional[str] = None

class AgentResponse(BaseModel):
    status: str
    message: str
    details: DetailedOutput

def parse_crew_output(crew_output: Any) -> DetailedOutput:
    """
    Parse the CrewOutput object from CrewAI and extract the structured data
    """
    try:
        # Convert the crew output to string if it's not already
        output_str = str(getattr(crew_output, 'final_answer', str(crew_output)))
        
        # Extract thoughts using regex
        thoughts_match = re.search(r'##\s*Thoughts:\s*(.*?)(?=##|$)', output_str, re.DOTALL)
        thoughts = thoughts_match.group(1).strip() if thoughts_match else None
        
        # Extract tool input using regex
        tool_input_match = re.search(r'tool input\s*(.*?)(?=##|$)', output_str, re.DOTALL)
        tool_input = tool_input_match.group(1).strip() if tool_input_match else None
        
        # Extract final answer - this is typically after "Final Thought"
        final_answer_match = re.search(r'Final Thought\s*:?\s*(.*?)$', output_str, re.DOTALL)
        final_answer = final_answer_match.group(1).strip() if final_answer_match else output_str
        
        # If no final answer was found, use the entire output as the final answer
        if not final_answer:
            final_answer = output_str
            
        return DetailedOutput(
            final_answer=final_answer,
            thoughts=thoughts,
            tool_input=tool_input
        )
    except Exception as e:
        # Fallback if we can't parse the output
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
    
