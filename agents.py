from crewai import Agent, Task, Crew, Process , LLM
from crewai_tools import CodeDocsSearchTool, DirectorySearchTool, GithubSearchTool	
from tools import githubSearch_tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

import os
load_dotenv()

# call gemini model
# code_llm = ChatGoogleGenerativeAI(
#     model='gemini/gemini-1.5-flash',  # Correct model path
#     verbose=True,
#     temperature=0.5,
#     google_api_key=os.getenv('GOOGLE_API_KEY')  # Corrected the spelling from 'goggle_api_key'
# )

my_llm = LLM(
    api_key=os.getenv("AIzaSyCyqPIWLCb2U1kdmfzPtYV_eZIJ4F4vWDw"),
    model="gemini/gemini-1.5-flash",
    temperature=0.7,
    verbose= True,
    memory=True,
   
    
)


# Researcher Agent to analyze the code
code_researcher = Agent(
    role="Senior Software Engineer , Code researcher and Computer Scientist",
    goal="Research, analyze, and understand the given code {code} provided by the user.",
    verbose=True,
    memory=True,
    backstory=(
        "You are an expert AI code analyzer that analyzes and understands given code and helps the user with their demands and queries"
    ),
    llm=my_llm,
    tools=[githubSearch_tool],
    allow_delegation=False,
    allow_code_execution=False
)

# Writer Agent to generate or complete the code
code_generator = Agent(
    role="Senior Software Engineer that writes code, debugs code, helps in code completion and improves the quality of code",
    goal="Write and generate code keeping the context as {code} provided by the user according to their queries {query}",
    verbose=True,
    memory=True,
    backstory=(
        "Craft and generate code in an easily understandable manner answering the user query {query} and making necessary changes to their code {code}"
    ),
    llm=my_llm,
    tools=[githubSearch_tool],
    allow_delegation=False,
    allow_code_execution=False
)
