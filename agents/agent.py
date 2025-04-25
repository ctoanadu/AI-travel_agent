import os
from typing import Annotated, Callable, Dict, List, Optional

from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import (AnyMessage, HumanMessage, SystemMessage,
                                     ToolCall, ToolMessage)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from agents.tools.flights_searcher import flights_searcher
from agents.tools.hotels_searcher import hotels_searcher

# Load environment variables from .env file
load_dotenv()


class State(TypedDict):
    """
    Represents the current state of the conversation, containing a list of messages.
    """

    messages: Annotated[list, add_messages]


class Agent:
    """
    An AI agent that handles conversational flow and executes tools such as flight and hotel search.

    Attributes:
        system_prompt (str): Prompt used to guide the system message behavior.
        tools (list): Tools available to the agent (flights, hotels).
        llm (ChatOpenAI): LLM instance with tools bound.
    """

    def __init__(self, system_prompt: str):
        """
         Initializes the Agent.

        Args:
            system_prompt (str): Instructional prompt for guiding assistant behavior.
        """
        self.tools = [flights_searcher, hotels_searcher]
        self.system_prompt = system_prompt
        self.llm = ChatOpenAI(model="gpt-4o").bind_tools(self.tools)

    def handle_conversation_flow(self, state: State) -> Dict[str, List[AnyMessage]]:
        """
        Processes the conversation state by invoking the LLM with the system message and user inputs.

        Args:
             state (State): Current conversation state.

        Returns:
            dict: A dictionary with a list of LLM-generated messages.
        """
        messages = state["messages"]
        messages = [SystemMessage(content=self.system_prompt)] + messages
        message = self.llm.invoke(messages)
        return {"messages": message}

    def tool_executor(self, state: State) -> Dict[str, List[ToolMessage]]:
        """
        Executes any tool calls found in the last message and returns their results as ToolMessages.

        Args:
            state (State): Current conversation state.

        Returns:
            dict: A dictionary with the new ToolMessages.
        """
        last_message = state["messages"][-1]
        new_messages = []
        for tool_call in getattr(last_message, "tool_calls", []):
            tool_obj = next(
                (t for t in self.tools if t.name == tool_call["name"]), None
            )
            if tool_obj:
                try:
                    parsed_args = tool_obj.args_schema(**tool_call["args"])
                    result = tool_obj.func(parsed_args)  # directly call the function
                    new_messages.append(
                        ToolMessage(tool_call_id=tool_call["id"], content=str(result))
                    )
                except Exception as e:
                    new_messages.append(
                        ToolMessage(
                            tool_call_id=tool_call["id"], content=f"Tool error: {e}"
                        )
                    )
        return {"messages": new_messages}

    def graph_builder(self) -> Callable:
        """
        Builds the conversation graph using LangGraph, defining interaction logic
        between the LLM and tool executions.

        Returns:
            Callable: A compiled graph function that handles conversation flow.
        """

        builder = StateGraph(State)
        builder.add_node("handle_conversation_flow", self.handle_conversation_flow)
        builder.add_node("tool_executor", self.tool_executor)
        builder.set_entry_point("handle_conversation_flow")

        # Conditional edge depending on whether LLM calls a tool
        builder.add_conditional_edges(
            "handle_conversation_flow",
            lambda state: (
                "tool_executor"
                if getattr(state["messages"][-1], "tool_calls", None)
                else END
            ),
            {"tool_executor": "tool_executor", END: END},
        )

        builder.add_edge("tool_executor", "handle_conversation_flow")

        return builder.compile()


def main():
    """
    Entry point to create and compile the travel assistant agent's graph.

    Returns:
        Callable: The compiled conversation flow graph ready for execution.
    """
    system_prompt = """
You are a highly capable travel assistant, equipped with the ability to search for up-to-date travel information. When necessary, use available tools to gather relevant data before making recommendations. Your goal is to provide insightful travel advice, including customized flight options and hotel recommendations.

- **Trip Types:**
  - **type=1 (Round Trip):** A round-trip flight, where the traveler departs and returns to the same location.
  - **type=2 (One-Way):** A one-way journey from one location to another without returning.
  - **type=3 (Multi-City):** A journey with multiple destinations or stopovers.

- **Recommendations:**
  For each travel inquiry, you should:
  1. **Provide a summary of the best flight options** based on user preferences, with flight logos where available.
  2. **Offer hotel suggestions** with direct booking links, tailored to the user’s destination and preferences.
  3. If additional research is required to provide relevant recommendations, you may gather that information before responding.

When a user provides a query, include the appropriate `type` value (1, 2, or 3) based on their request. Ensure that you customize the flight and hotel options based on the selected trip type.
"""

    agent = Agent(system_prompt=system_prompt)

    return agent.graph_builder()
