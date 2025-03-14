# from crewai_tools import GithubSearchTool

# # Initialize the tool with a specific Youtube channel handle to target your search
# githubSearch_tool = GithubSearchTool(
#     gh_token="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",
#     github_repo='https://github.com/pratyushdev-codes/Secondmemory.ai_GenAIRAG',
#     content_types=["code", "repositories"]  # Replace with appropriate content types
# )



# ##Create Custom tools for code generation


import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, WebsiteSearchTool
load_dotenv()
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')

# inititlaize the tool for internet searching capabilities
githubSearch_tool = SerperDevTool()   ##this is just names as github search tool but it is google search tool

web_search_tool=WebsiteSearchTool

