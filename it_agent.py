from autogen_agentchat.agents import AssistantAgent
from config import model_client

it_agent = AssistantAgent(
    name="IT_Agent",
    model_client=model_client,
    system_message="""
You are an IT Support Engineer.

Answer ONLY IT-related questions.

If the question is not related to IT,
reply:

This question belongs to another department.
"""
)