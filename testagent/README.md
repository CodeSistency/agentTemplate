# TestAgent - A Simple AI Agent Example

This is a minimal implementation of an AI agent using the architecture described in `generic_agent_architecture.md`.

## Project Structure

```
testagent/
├── backend/                  # Python backend services
│   ├── mcp_servers/          # FastMCP tool servers
│   │   └── math_tools/       # Example math tools server
│   │       └── server.py
│   ├── orchestrators/        # LangGraph agent orchestrators
│   │   └── test_agent_orchestrator/
│   │       ├── graph.py
│   │       └── state.py
│   ├── main_gateway.py       # FastAPI gateway
│   └── requirements.txt
└── frontend/                 # Next.js frontend
    └── src/app/              # Next.js app directory
        ├── api/              # BFF API routes
        │   └── copilotkit/
        │       └── route.ts
        ├── globals.css
        ├── layout.tsx
        └── page.tsx
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd testagent/backend
   ```

2. Create a Python virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

5. Start the backend server:
   ```bash
   python main_gateway.py
   ```
   The server will start on http://localhost:8080

### Frontend Setup

1. In a new terminal, navigate to the frontend directory:
   ```bash
   cd testagent/frontend
   ```

2. Install the required Node.js packages:
   ```bash
   npm install
   ```

3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at http://localhost:3000

## Testing the Agent

1. Open http://localhost:3000 in your browser
2. Try asking the agent to add numbers, for example:
   - "What is 5 plus 3?"
   - "Add 10 and 20"
   - "Can you calculate 15 + 25?"

The agent will use the FastMCP math tool server to perform the calculations.

## How It Works

1. The frontend sends user messages to the Next.js API route (`/api/copilotkit`)
2. The API route forwards the request to the Python backend
3. The LangGraph agent processes the message and decides whether to use the math tool
4. If a tool is needed, it calls the FastMCP math tool server
5. The response is streamed back to the frontend

## Next Steps

- Add more tools to the FastMCP server
- Implement more complex agent logic in the LangGraph orchestrator
- Add authentication and user management
- Deploy the application to a hosting provider
