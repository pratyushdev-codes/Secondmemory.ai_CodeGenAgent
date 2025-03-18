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
        
        # Initialize variables
        task = None
        thoughts = None
        tool_input = None
        final_answer = None
        
        # Extract Task using regex
        task_match = re.search(r'##\s*Task:\s*(.*?)(?=##\s*Thoughts:|$)', output_str, re.DOTALL)
        if task_match:
            task = task_match.group(1).strip()
        
        # Extract Thoughts using regex
        thoughts_match = re.search(r'##\s*Thoughts:\s*(.*?)(?=tool input|Final Thought|$)', output_str, re.DOTALL)
        if thoughts_match:
            thoughts = thoughts_match.group(1).strip()
        
        # Extract tool input using regex
        tool_input_match = re.search(r'tool input\s*(.*?)(?=Final Thought|$)', output_str, re.DOTALL)
        if tool_input_match:
            tool_input = tool_input_match.group(1).strip()
        
        # Extract final answer - this is typically after "Final Thought"
        final_answer_match = re.search(r'Final Thought\s*:?\s*(.*?)$', output_str, re.DOTALL)
        if final_answer_match:
            final_answer = final_answer_match.group(1).strip()
        else:
            # If no final answer was found, use the entire output as the final answer
            final_answer = output_str
        
        # Create debugging output to verify extraction is working
        print(f"PARSED OUTPUT:\nTask: {task}\nThoughts: {thoughts}\nTool Input: {tool_input}\nFinal Answer: {final_answer}")
        
        return DetailedOutput(
            final_answer=final_answer if final_answer else output_str,
            thoughts=thoughts,
            tool_input=tool_input
        )
    except Exception as e:
        print(f"Error parsing output: {str(e)}")
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
        # Modify agent and task configuration to ensure standardized output format
        # Update the expected_output in your tasks to include the required format
        
        crew = Crew(
            agents=[code_researcher, code_generator],
            tasks=[research_task, code_writer],
            process=Process.sequential,
        )
        
        result = crew.kickoff(inputs={
            'query': query,
            'code': code
        })
        
        # Print raw output for debugging
        print(f"RAW OUTPUT: {result}")
        
        return parse_crew_output(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CrewAI Error: {str(e)}")

# Update response model for API endpoints
@app.post("/syntax", response_model=AgentResponse)
async def analyze_syntax(request: CodeAnalysisRequest):
    """
    Analyze code syntax using CrewAI
    """
    try:
        result = run_crew_ai(request.query, request.code)

        response = AgentResponse(
            status="success",
            message="Syntax analysis completed",
            details=result
        )
        
        # Print final response for debugging
        print(f"FINAL RESPONSE: {response.json()}")
        
        return response
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
        
        response = AgentResponse(
            status="success",
            message="Code analysis completed",
            details=result
        )
        
        # Print final response for debugging
        print(f"FINAL RESPONSE: {response.json()}")
        
        return response
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
