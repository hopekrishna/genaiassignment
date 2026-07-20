import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)