from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage, ToolCall
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
import os
from typing import Optional

from agents.tools.flights_searcher import flights_searcher
from agents.tools.hotels_searcher import hotels_searcher
 

load_dotenv()

class State(TypedDict):
  messages:Annotated[list,add_messages]


class Agent():
  def __init__(self, system_prompt):
    self.tools = [flights_searcher, hotels_searcher]
    self.system_prompt = system_prompt
    self.llm = ChatOpenAI(model='gpt-4o').bind_tools(self.tools)

  def handle_conversation_flow(self,state : State):
    messages = state['messages']
    messages = [SystemMessage(content = self.system_prompt)] + messages
    message = self.llm.invoke(messages)
    return {'messages': message}
  
  def tool_executor(self,state: State):
    last_message = state['messages'][-1]
    new_messages =[]
    for tool_call in getattr(last_message, 'tool_calls',[] ):
      tool_obj = next((t for t in self.tools if t.name == tool_call["name"]), None)
      if tool_obj:
        try:
          parsed_args = tool_obj.args_schema(**tool_call["args"])
          result = tool_obj.func(parsed_args)  # directly call the function
          new_messages.append(
                    ToolMessage(tool_call_id=tool_call["id"], content=str(result))
                )
        except Exception as e:
          new_messages.append(
                    ToolMessage(tool_call_id=tool_call["id"], content=f"Tool error: {e}")
                )
    return {'messages': new_messages}
  

  
  def graph_builder(self):
    builder=StateGraph(State)
    builder.add_node("handle_conversation_flow",self.handle_conversation_flow)
    builder.add_node("tool_executor", self.tool_executor)
    builder.set_entry_point("handle_conversation_flow")

    # Conditional edge depending on whether LLM calls a tool
    builder.add_conditional_edges(
        "handle_conversation_flow",
        lambda state: "tool_executor" if getattr(state["messages"][-1], "tool_calls", None) else END,
        {
            "tool_executor": "tool_executor",
            END: END
        }
    )

    builder.add_edge("tool_executor", "handle_conversation_flow")

    return builder.compile()
  
def main():
  system_prompt ="You are a smart travel agency, Use the tools to look up information. If you need to look up some information before asking a follow up question, you are allowed to do that! Also default trip is a round trip (1), while one way is 2 and multi-city is 3. DO NOT mention the raw search results or data to the user - instead, analyze the data and provide useful summaries and recommendations based on it."
  agent = Agent(system_prompt=system_prompt)

  return agent.graph_builder()






          
  
  










  


