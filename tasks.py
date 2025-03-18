# from crewai import Task , LLM
# from tools import githubSearch_tool
# from  agents import code_researcher , code_generator


# ## Research Task
# research_task = Task(
#   description=(
#     "Analyze the given code {code} by the user."
#     "Understand the logic , syntax , libraries and the code."
#   ),
#   expected_output='A to-the point code report based on the {code} of user source code.',
#   tools=[githubSearch_tool],
#   agent=code_researcher,
# )

# # Writing task with language model configuration
# code_writer = Task(
#   description=(
#     "Get the info from code {code} and understand the user query{query} and generate code accordingly."
#   ),
#   expected_output='Generate the code according to the user queries {query} keeping in context the provided code by the user {code} and perform the tasks given by the user.It may be Code Generation , Code debugging , Code Completion or Code Completion',
#   tools=[githubSearch_tool],
#   agent=code_generator,
#   async_execution=False,
#   output_file='gen-code.md'  # Example of output customization
# )

from crewai import Task
from tools import githubSearch_tool
from agents import code_researcher, code_generator

## Research Task
research_task = Task(
  description=(
    "Analyze the given code {code} by the user."
    "Understand the logic, syntax, libraries and the code."
    "YOUR RESPONSE MUST FOLLOW THIS FORMAT:"
    "## Task: [description of what you are doing]"
    "## Thoughts: [your detailed analysis]"
    "tool input [any tool usage results]"
    "Final Thought: [your final answer]"
  ),
  expected_output='A to-the point code report in the EXACT format: "## Task: [task description] ## Thoughts: [analysis] tool input [tool usage] Final Thought: [conclusion]"',
  tools=[githubSearch_tool],
  agent=code_researcher,
)

# Writing task with language model configuration
code_writer = Task(
  description=(
    "Get the info from code {code} and understand the user query{query} and generate code accordingly."
    "YOUR RESPONSE MUST FOLLOW THIS FORMAT:"
    "## Task: [description of what you are doing]"
    "## Thoughts: [your detailed analysis]"
    "tool input [any tool usage results]"
    "Final Thought: [your final code or solution]"
  ),
  expected_output='Generate the code according to the user queries {query} in the EXACT format: "## Task: [task description] ## Thoughts: [analysis] tool input [tool usage] Final Thought: [code solution]"',
  tools=[githubSearch_tool],
  agent=code_generator,
  async_execution=False,
  output_file='gen-code.md'
)
