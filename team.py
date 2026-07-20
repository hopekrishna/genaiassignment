from autogen_agentchat.conditions import (
    MaxMessageTermination,
    TextMentionTermination,
)

from autogen_agentchat.teams import SelectorGroupChat

from config import model_client

from agents.it_agent import it_agent
from agents.hr_agent import hr_agent
from agents.marketing_agent import marketing_agent
from agents.admin_agent import admin_agent


selector_prompt = """
You are the Manager Agent.

Choose ONLY ONE agent.

Available Agents

ITAgent
HRAgent
MarketingAgent
AdminAgent

Roles

{roles}

Conversation

{history}

Choose one agent from:

{participants}

Only output the agent name.
"""


def create_team():

    termination = (
        TextMentionTermination("TERMINATE")
        | MaxMessageTermination(max_messages=10)
    )

    return SelectorGroupChat(
        participants=[
            it_agent,
            hr_agent,
            marketing_agent,
            admin_agent,
        ],
        model_client=model_client,
        selector_prompt=selector_prompt,
        termination_condition=termination,
        allow_repeated_speaker=True,
    )