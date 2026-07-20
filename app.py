import asyncio
import streamlit as st

from team import create_team

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="Multi-Agent Customer Support",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent Customer Support System")
st.write("Select a department and ask your question.")

# ---------------------------------
# Session State
# ---------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "department" not in st.session_state:
    st.session_state.department = None

# ---------------------------------
# Department Selection Function
# ---------------------------------
def select_department(dept):
    if st.session_state.department != dept:
        st.session_state.department = dept
        st.session_state.messages = []
        st.rerun()

# ---------------------------------
# Department Buttons
# ---------------------------------
st.subheader("Choose Department")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💻 IT Department", use_container_width=True):
        select_department("IT")

with col2:
    if st.button("👨‍💼 HR Department", use_container_width=True):
        select_department("HR")

with col3:
    if st.button("📢 Marketing Department", use_container_width=True):
        select_department("Marketing")

with col4:
    if st.button("🏢 Admin Department", use_container_width=True):
        select_department("Admin")

# ---------------------------------
# Selected Department
# ---------------------------------
if st.session_state.department:
    st.success(f"Selected Department: {st.session_state.department}")

# ---------------------------------
# Display Chat History
# ---------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------
# Chat Input
# ---------------------------------
prompt = st.chat_input("Type your question...")

if prompt:

    if st.session_state.department is None:
        st.warning("⚠️ Please select a department first.")
        st.stop()

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # AutoGen Response
    async def get_response():
        team = create_team()

        full_prompt = f"""
Department: {st.session_state.department}

User Question:
{prompt}
"""

        result = await team.run(task=full_prompt)

        return result.messages[-1].content

    response = asyncio.run(get_response())

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )