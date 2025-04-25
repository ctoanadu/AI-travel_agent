import streamlit as st
from langchain_core.messages import HumanMessage, ToolMessage

from agents.agent import main


# Functions to format and display chat messages
def display_message(message: str, is_user: bool = False, is_tool: bool = False) -> None:
    """
    Renders a chat message on the Streamlit UI.

    Args:
        message (str): The message content.
        is_user (bool, optional): True if the message is from the user. Defaults to False.
        is_tool (bool, optional): True if the message is from a tool. Defaults to False.
    """
    if is_user:
        st.markdown(
            f'<div class="chat-message user-message"><div class="message-content">{message}</div></div>',
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            f'<div class="chat-message bot-message"><div class="message-content">{message}</div></div>',
            unsafe_allow_html=True,
        )


# -- Page configuration--
st.set_page_config(
    page_title="Travel Agent Chatbot", page_icon=":airplane:", layout="wide"
)

# -- Add custom CSS for better styling --
st.markdown(
    """
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left: 5px solid #4b70e2;
    }
    .bot-message {
        background-color: #f8f9fa;
        border-left: 5px solid #43b581;
    }
    
    .message-content {
        margin-top: 0.5rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -- Initialize session state for conversation history--
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# --Initialize session state for agent messages --
if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []


# Streamlit UI components
st.title("🧳 Travel Agent Chatbot")
st.markdown("Ask me about flights and hotels for your next trip!")

# Display chat history
for message in st.session_state.conversation_history:
    if message["type"] == "user":
        display_message(message["content"], is_user=True)
    elif message["type"] == "assistant":
        display_message(message["content"])


# -- Chat user input--
with st.container():
    user_input = st.chat_input("What's your travel plan?")

    if user_input:

        # Add user message to conversation history
        st.session_state.conversation_history.append(
            {"type": "user", "content": user_input}
        )
        human_message = HumanMessage(content=user_input)
        st.session_state.agent_messages.append(human_message)

        # Build the input state for the graph
        state = {"messages": st.session_state.agent_messages}

        with st.spinner("Searching..."):
            graph = main()
            result = graph.invoke(state)

            # Process only the new messages from this interaction
            new_messages = result["messages"]

            # Process and display results
            assistant_response = None
            for message in new_messages:
                if isinstance(message, ToolMessage):
                    st.session_state.agent_messages.append(message)
                elif not isinstance(message, HumanMessage):
                    assistant_response = message
                    st.session_state.agent_messages.append(message)
            # Only add the final assistant response to the conversation history
            if assistant_response:
                content = assistant_response.content
                st.session_state.conversation_history.append(
                    {"type": "assistant", "content": content}
                )

        # Force a rerun to update the UI with all new messages
        st.rerun()

# Add footer
st.markdown("---")
st.markdown("Powered by LangGraph and SerpAPI")
