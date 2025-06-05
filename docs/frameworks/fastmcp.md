Beyond the Protocol
FastMCP is the standard framework for working with the Model Context Protocol. FastMCP 1.0 was incorporated into the official low-level Python SDK, and FastMCP 2.0 (this project) provides a complete toolkit for working with the MCP ecosystem.

FastMCP has a comprehensive set of features that go far beyond the core MCP specification, all in service of providing the simplest path to production. These include client support, server composition, auth, automatic generation from OpenAPI specs, remote server proxying, built-in testing tools, integrations, and more.

Ready to upgrade or get started? Follow the installation instructions, which include specific steps for upgrading from the official MCP SDK.

The Model Context Protocol (MCP) is a new, standardized way to provide context and tools to your LLMs, and FastMCP makes building MCP servers and clients simple and intuitive. Create tools, expose resources, define prompts, and connect components with clean, Pythonic code.

# server.py
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
Run the server locally:

fastmcp run server.py
📚 Documentation
FastMCP's complete documentation is available at gofastmcp.com, including detailed guides, API references, and advanced patterns. This readme provides only a high-level overview.

Documentation is also available in llms.txt format, which is a simple markdown standard that LLMs can consume easily.

There are two ways to access the LLM-friendly documentation:

llms.txt is essentially a sitemap, listing all the pages in the documentation.
llms-full.txt contains the entire documentation. Note this may exceed the context window of your LLM.
Table of Contents
What is MCP?
Why FastMCP?
Installation
Core Concepts
The FastMCP Server
Tools
Resources & Templates
Prompts
Context
MCP Clients
Advanced Features
Proxy Servers
Composing MCP Servers
OpenAPI & FastAPI Generation
Authentication & Security
Running Your Server
Contributing
Prerequisites
Setup
Unit Tests
Static Checks
Pull Requests
What is MCP?
The Model Context Protocol (MCP) lets you build servers that expose data and functionality to LLM applications in a secure, standardized way. It is often described as "the USB-C port for AI", providing a uniform way to connect LLMs to resources they can use. It may be easier to think of it as an API, but specifically designed for LLM interactions. MCP servers can:

Expose data through Resources (think of these sort of like GET endpoints; they are used to load information into the LLM's context)
Provide functionality through Tools (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
Define interaction patterns through Prompts (reusable templates for LLM interactions)
And more!
FastMCP provides a high-level, Pythonic interface for building, managing, and interacting with these servers.

Why FastMCP?
The MCP protocol is powerful but implementing it involves a lot of boilerplate - server setup, protocol handlers, content types, error management. FastMCP handles all the complex protocol details and server management, so you can focus on building great tools. It's designed to be high-level and Pythonic; in most cases, decorating a function is all you need.

FastMCP 2.0 has evolved into a comprehensive platform that goes far beyond basic protocol implementation. While 1.0 provided server-building capabilities (and is now part of the official MCP SDK), 2.0 offers a complete ecosystem including client libraries, authentication systems, deployment tools, integrations with major AI platforms, testing frameworks, and production-ready infrastructure patterns.

FastMCP aims to be:

🚀 Fast: High-level interface means less code and faster development

🍀 Simple: Build MCP servers with minimal boilerplate

🐍 Pythonic: Feels natural to Python developers

🔍 Complete: A comprehensive platform for all MCP use cases, from dev to prod

Installation
We recommend installing FastMCP with uv:

uv pip install fastmcp
For full installation instructions, including verification, upgrading from the official MCPSDK, and developer setup, see the Installation Guide.

Core Concepts
These are the building blocks for creating MCP servers and clients with FastMCP.

The FastMCP Server
The central object representing your MCP application. It holds your tools, resources, and prompts, manages connections, and can be configured with settings like authentication.

from fastmcp import FastMCP

# Create a server instance
mcp = FastMCP(name="MyAssistantServer")
Learn more in the FastMCP Server Documentation.

Tools
Tools allow LLMs to perform actions by executing your Python functions (sync or async). Ideal for computations, API calls, or side effects (like POST/PUT). FastMCP handles schema generation from type hints and docstrings. Tools can return various types, including text, JSON-serializable objects, and even images using the fastmcp.Image helper.

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b
Learn more in the Tools Documentation.

Resources & Templates
Resources expose read-only data sources (like GET requests). Use @mcp.resource("your://uri"). Use {placeholders} in the URI to create dynamic templates that accept parameters, allowing clients to request specific data subsets.

# Static resource
@mcp.resource("config://version")
def get_version(): 
    return "2.0.1"

# Dynamic resource template
@mcp.resource("users://{user_id}/profile")
def get_profile(user_id: int):
    # Fetch profile for user_id...
    return {"name": f"User {user_id}", "status": "active"}
Learn more in the Resources & Templates Documentation.

Prompts
Prompts define reusable message templates to guide LLM interactions. Decorate functions with @mcp.prompt. Return strings or Message objects.

@mcp.prompt()
def summarize_request(text: str) -> str:
    """Generate a prompt asking for a summary."""
    return f"Please summarize the following text:\n\n{text}"
Learn more in the Prompts Documentation.

Context
Access MCP session capabilities within your tools, resources, or prompts by adding a ctx: Context parameter. Context provides methods for:

Logging: Log messages to MCP clients with ctx.info(), ctx.error(), etc.
LLM Sampling: Use ctx.sample() to request completions from the client's LLM.
HTTP Request: Use ctx.http_request() to make HTTP requests to other servers.
Resource Access: Use ctx.read_resource() to access resources on the server
Progress Reporting: Use ctx.report_progress() to report progress to the client.
and more...
To access the context, add a parameter annotated as Context to any mcp-decorated function. FastMCP will automatically inject the correct context object when the function is called.

from fastmcp import FastMCP, Context

mcp = FastMCP("My MCP Server")

@mcp.tool()
async def process_data(uri: str, ctx: Context):
    # Log a message to the client
    await ctx.info(f"Processing {uri}...")

    # Read a resource from the server
    data = await ctx.read_resource(uri)

    # Ask client LLM to summarize the data
    summary = await ctx.sample(f"Summarize: {data.content[:500]}")

    # Return the summary
    return summary.text
Learn more in the Context Documentation.

MCP Clients
Interact with any MCP server programmatically using the fastmcp.Client. It supports various transports (Stdio, SSE, In-Memory) and often auto-detects the correct one. The client can also handle advanced patterns like server-initiated LLM sampling requests if you provide an appropriate handler.

Critically, the client allows for efficient in-memory testing of your servers by connecting directly to a FastMCP server instance via the FastMCPTransport, eliminating the need for process management or network calls during tests.

from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("my_server.py") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"Result: {result.text}")

    # Connect via SSE
    async with Client("http://localhost:8000/sse") as client:
        # ... use the client
        pass
To use clients to test servers, use the following pattern:

from fastmcp import FastMCP, Client

mcp = FastMCP("My MCP Server")

async def main():
    # Connect via in-memory transport
    async with Client(mcp) as client:
        # ... use the client
FastMCP also supports connecting to multiple servers through a single unified client using the standard MCP configuration format:

from fastmcp import Client

# Standard MCP configuration with multiple servers
config = {
    "mcpServers": {
        "weather": {"url": "https://weather-api.example.com/mcp"},
        "assistant": {"command": "python", "args": ["./assistant_server.py"]}
    }
}

# Create a client that connects to all servers
client = Client(config)

async def main():
    async with client:
        # Access tools and resources with server prefixes
        forecast = await client.call_tool("weather_get_forecast", {"city": "London"})
        answer = await client.call_tool("assistant_answer_question", {"query": "What is MCP?"})
Learn more in the Client Documentation and Transports Documentation.

Advanced Features
FastMCP introduces powerful ways to structure and deploy your MCP applications.

Proxy Servers
Create a FastMCP server that acts as an intermediary for another local or remote MCP server using FastMCP.as_proxy(). This is especially useful for bridging transports (e.g., remote SSE to local Stdio) or adding a layer of logic to a server you don't control.

Learn more in the Proxying Documentation.

Composing MCP Servers
Build modular applications by mounting multiple FastMCP instances onto a parent server using mcp.mount() (live link) or mcp.import_server() (static copy).

Learn more in the Composition Documentation.

OpenAPI & FastAPI Generation
Automatically generate FastMCP servers from existing OpenAPI specifications (FastMCP.from_openapi()) or FastAPI applications (FastMCP.from_fastapi()), instantly bringing your web APIs to the MCP ecosystem.

Learn more: OpenAPI Integration | FastAPI Integration.

Authentication & Security
FastMCP provides built-in authentication support to secure both your MCP servers and clients in production environments. Protect your server endpoints from unauthorized access and authenticate your clients against secured MCP servers using industry-standard protocols.

Server Protection: Secure your FastMCP server endpoints with configurable authentication providers
Client Authentication: Connect to authenticated MCP servers with automatic credential management
Production Ready: Support for common authentication patterns used in enterprise environments
Learn more in the Authentication Documentation for servers and clients.

Running Your Server
The main way to run a FastMCP server is by calling the run() method on your server instance:

# server.py
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()  # Default: uses STDIO transport
FastMCP supports three transport protocols:

STDIO (Default): Best for local tools and command-line scripts.

mcp.run(transport="stdio")  # Default, so transport argument is optional
Streamable HTTP: Recommended for web deployments.

mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/mcp")
SSE: For compatibility with existing SSE clients.

mcp.run(transport="sse", host="127.0.0.1", port=8000)
See the Running Server Documentation for more details.

Contributing
Contributions are the core of open source! We welcome improvements and features.

Prerequisites
Python 3.10+
uv (Recommended for environment management)
Setup
Clone the repository:

git clone https://github.com/jlowin/fastmcp.git 
cd fastmcp
Create and sync the environment:

uv sync
This installs all dependencies, including dev tools.

Activate the virtual environment (e.g., source .venv/bin/activate or via your IDE).

Unit Tests
FastMCP has a comprehensive unit test suite. All PRs must introduce or update tests as appropriate and pass the full suite.

Run tests using pytest:

pytest
or if you want an overview of the code coverage

uv run pytest --cov=src --cov=examples --cov-report=html
Static Checks
FastMCP uses pre-commit for code formatting, linting, and type-checking. All PRs must pass these checks (they run automatically in CI).

Install the hooks locally:

uv run pre-commit install
The hooks will now run automatically on git commit. You can also run them manually at any time:

pre-commit run --all-files
# or via uv
uv run pre-commit run --all-files
Pull Requests
Fork the repository on GitHub.
Create a feature branch from main.
Make your changes, including tests and documentation updates.
Ensure tests and pre-commit hooks pass.
Commit your changes and push to your fork.
Open a pull request against the main branch of jlowin/fastmcp.
Please open an issue or discussion for questions or suggestions before starting significant work!