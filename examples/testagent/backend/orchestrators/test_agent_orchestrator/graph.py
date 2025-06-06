import os
import json
from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .state import TestAgentState
from mcp_use import MCPClient

# MCP Client Setup
math_tools_server_path = os.path.join(
    os.path.dirname(__file__),
    "..", 
    "..", 
    "mcp_servers",
    "math_tools",
    "server.py"
)

mcp_config = {
    "mcpServers": {
        "math_tools": {
            "command": "python3",
            "args": [math_tools_server_path],
        }
    }
}
mcp_client = MCPClient.from_dict(mcp_config)

# LLM Setup
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# System message to guide the LLM
MATH_SYSTEM_PROMPT = """You are a helpful math tutor that helps students solve mathematical problems step by step.
You have access to various math tools that can help with calculations. Here's how to use them:

1. For basic arithmetic (addition, subtraction, multiplication, division):
   - Use the appropriate tool (add, subtract, multiply, divide)
   
2. For exponents and roots:
   - Use 'power' for exponents (e.g., 2^3)
   - Use 'square_root' for square roots (e.g., √9)
   
3. For solving equations:
   - Use 'solve_equation' for linear equations (e.g., '2x + 3 = 7')

Always break down complex problems into smaller, manageable steps. Show your work and explain each step clearly.
When using tools, make sure to provide all required parameters with the correct types.
"""

# Define the tools for the LLM
llm_tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Adds two numbers and returns the result with steps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "Subtracts the second number from the first and returns the result with steps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The number to subtract"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiplies two numbers and returns the result with steps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "Divides the first number by the second and returns the result with steps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The numerator"},
                    "b": {"type": "number", "description": "The denominator (cannot be zero)"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "power",
            "description": "Raises a number to a power and returns the result with steps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base": {"type": "number", "description": "The base number"},
                    "exponent": {"type": "number", "description": "The exponent"}
                },
                "required": ["base", "exponent"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "square_root",
            "description": "Calculates the square root of a number and returns the result with steps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {"type": "number", "description": "The number to find the square root of (must be non-negative)"}
                },
                "required": ["number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "solve_equation",
            "description": "Solves a simple linear equation in the form 'ax + b = c' and returns the solution with steps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "equation": {"type": "string", "description": "The equation to solve, e.g., '2x + 3 = 7'"}
                },
                "required": ["equation"]
            }
        }
    }
]

# Bind tools to the LLM
llm_with_tools = llm.bind_tools(tools=llm_tools, tool_choice="auto")
llm_tools = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Adds two integers and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "The first number"},
                    "b": {"type": "integer", "description": "The second number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]
llm_with_tools = llm.bind_tools(tools=llm_tools, tool_choice="auto")

# Helper function to format tool response
def format_tool_response(tool_name: str, tool_result: Dict[str, Any]) -> str:
    """Format the tool response for display to the user."""
    if "error" in tool_result:
        return f"Error in {tool_name}: {tool_result.get('message', 'Unknown error')}"
    
    response = []
    operation = tool_result.get("operation", "calculation")
    expression = tool_result.get("expression", "")
    result = tool_result.get("result", "")
    steps = tool_result.get("steps", [])
    
    response.append(f"## {operation.capitalize()}: {expression}")
    
    if steps:
        response.append("### Steps:")
        for step in steps:
            if step:  # Skip empty steps
                response.append(f"- {step}")
    
    if result is not None and result != "":
        response.append(f"\n**Final Result:** {result}")
    
    return "\n".join(response)


# LangGraph Nodes
def call_llm(state: TestAgentState):
    print("--- TestAgent: Calling LLM ---")
    
    # Add system message if it's the first message
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=MATH_SYSTEM_PROMPT)] + list(messages)
    
    # Call the LLM with the current conversation history
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def call_tool(state: TestAgentState):
    print("--- TestAgent: Calling Tool ---")
    ai_message = state["messages"][-1]
    tool_messages = []

    for tool_call in getattr(ai_message, "tool_calls", []):
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        print(f"LLM requested tool: {tool_name} with args: {tool_args}")

        try:
            # Call the appropriate FastMCP tool
            result = mcp_client.call_tool(f"math_tools.{tool_name}", tool_args)
            
            # Parse the result
            try:
                tool_result = json.loads(result.text)
                formatted_response = format_tool_response(tool_name, tool_result)
                tool_messages.append(
                    ToolMessage(
                        content=formatted_response,
                        tool_call_id=tool_call["id"]
                    )
                )
            except json.JSONDecodeError:
                tool_messages.append(
                    ToolMessage(
                        content=f"Tool response could not be parsed: {result.text}",
                        tool_call_id=tool_call["id"]
                    )
                )
                
        except Exception as e:
            error_msg = f"Error calling tool {tool_name}: {str(e)}"
            print(error_msg)
            tool_messages.append(
                ToolMessage(
                    content=error_msg,
                    tool_call_id=tool_call.get("id", "unknown")
                )
            )
    
    return {"messages": tool_messages}

# --- Conditional Edge Logic ---
def should_call_tool(state: TestAgentState):
    last_message = state["messages"][-1]
    
    # If the last message has tool calls, route to the tool calling node
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "call_tool"
        
    # If we just received a tool response, go back to the LLM to process it
    if isinstance(last_message, ToolMessage):
        return "call_llm"
        
    # Otherwise, end the turn
    return END

# Create and compile the graph
workflow = StateGraph(TestAgentState)
workflow.add_node("call_llm_node", call_llm)
workflow.add_node("call_tool_node", call_tool)
workflow.add_edge(START, "call_llm_node")
workflow.add_conditional_edges(
    "call_llm_node",
    should_call_tool,
    {
        "call_tool": "call_tool_node",
        END: END
    }
)
workflow.add_edge("call_tool_node", "call_llm_node")

test_agent_graph = workflow.compile(checkpointer=MemorySaver())
print("TestAgent LangGraph compiled.")
