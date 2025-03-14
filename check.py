# Agentic AI code without streamlit app
from crewai import Crew, Process, LLM , Agent
from tasks import research_task , code_writer
from agents import code_researcher , code_generator
from crewai_tools import CodeDocsSearchTool, DirectorySearchTool, GithubSearchTool    
from tools import githubSearch_tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

# Initialize the Gemini model with the correct parameters
# code_llm = ChatGoogleGenerativeAI(
#     model='gemini/gemini-1.5-flash',
#     verbose=True,
#     temperature=0.5,
#     google_api_key=os.environ['GOOGLE_API_KEY']  # Corrected the spelling from 'goggle_api_key'
# )

# Creating the Crew with agents and tasks
crew = Crew(
    agents=[code_researcher, code_generator],
    tasks=[research_task, code_writer],
    process=Process.sequential,
)

## Start the task execution process with enhanced feedback
result = crew.kickoff(inputs={'query': 'Complete the given code for polymorphism in Python',
                              'code': 'dog = Dog() cat = Cat() animal_sound(dog) animal_sound(cat)'})
print(result)