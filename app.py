from crewai import LLM
import os

import streamlit as st
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process,LLM

# Tool for web searching
from crewai_tools import SerperDevTool

# Load environment variables
load_dotenv()

llm = LLM(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)
# ----------------------------
# Web Search Tool
# ----------------------------

search_tool = SerperDevTool()
# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(
    page_title="AI Customer Support System",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Customer Support System")

st.write("Ask any customer support question.")

user_query = st.text_area(
    "Enter your question:",
    height=150,
    placeholder="Example: How can I reset my password?"
)

submit = st.button("Get Answer")
# ----------------------------
# Agent 1
# ----------------------------

support_agent = Agent(
    role="Customer Support Agent",
    goal="Answer customer questions clearly and accurately.",
    backstory=(
        "You are a helpful customer support representative. "
        "Provide clear, concise, and friendly answers."
    ),
    llm=llm,
    verbose=True,
    
)
# ----------------------------
# Agent 2
# ----------------------------

research_agent = Agent(
    role="Web Research Agent",
    goal="Search the web and provide the most accurate and up-to-date answer.",
    backstory=(
        "You are an expert web researcher. "
        "You search the internet for reliable information before answering."
    ),
    llm=llm,
    tools=[search_tool],
    verbose=True,
)
# ----------------------------
# Agent 3
# ----------------------------

save_agent = Agent(
    role="Save Results Agent",
    goal="Save the customer query and both answers into a text file.",
    backstory=(
        "You are responsible for saving the customer support conversation "
        "to a text file for future reference."
    ),
    llm=llm,
    verbose=True,
)
# ----------------------------
# Task 1
# ----------------------------

task1 = Task(
    description="""
    Answer the following customer question:

    {user_query}

    Give a clear, accurate, and friendly response.
    """,
    expected_output="A helpful answer to the customer's question.",
    agent=support_agent,
)
# ----------------------------
# Task 2
# ----------------------------

task2 = Task(
    description="""
    Search the web for the following customer question:

    {user_query}

    Use reliable and up-to-date sources to provide an accurate answer.
    """,
    expected_output="A well-researched answer based on web search.",
    agent=research_agent,
)
# ----------------------------
# Task 3
# ----------------------------

task3 = Task(
    description="""
    Create a final customer support report.

    Include:

    1. Customer Question
    2. Agent 1 Answer
    3. Agent 2 Answer

    Format the report clearly.
    """,
    expected_output="A well-formatted customer support report.",
    agent=save_agent,
)
# ----------------------------
# Crew
# ----------------------------

crew = Crew(
    agents=[
        support_agent,
        research_agent,
        save_agent
    ],
    tasks=[
        task1,
        task2,
        task3
    ],
    process=Process.sequential,
    verbose=True
)
# ----------------------------
# Run Crew
# ----------------------------

if submit:

    if user_query.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Generating answer..."):

            result = crew.kickoff(
                inputs={
                    "user_query": user_query
                }
            )

        st.success("Answers Generated!")

        if len(result.tasks_output) >= 1:
            st.subheader("Agent 1 Answer")
            st.markdown(result.tasks_output[0].raw)

        if len(result.tasks_output) >= 2:
            st.divider()
            st.subheader("Agent 2 Answer")
            st.markdown(result.tasks_output[1].raw)

        if len(result.tasks_output) >= 3:
            final_report = result.tasks_output[2].raw

            with open("output.txt", "w", encoding="utf-8") as file:
                file.write(final_report)

            st.divider()
            st.subheader("Final Report")
            st.markdown(final_report)

            st.success("Report saved to output.txt")