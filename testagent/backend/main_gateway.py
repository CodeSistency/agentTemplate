import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from copilotkit import CopilotKit
from copilotkit.adapters.langgraph import LangGraphAdapter
import json
import logging
from typing import AsyncGenerator, Dict, Any

from orchestrators.test_agent_orchestrator.graph import workflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TestAgent Gateway",
    description="A gateway for the TestAgent that provides advanced math capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize CopilotKit with LangGraph adapter
copilotkit = CopilotKit(
    adapters=[
        LangGraphAdapter(
            workflow=workflow,
            name="test_agent",
            description="An advanced math tutor agent that can solve complex problems step by step",
        )
    ]
)

# Mount CopilotKit endpoints
app.mount("/copilotkit", copilotkit.router)

# Add a simple HTML page for testing
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>TestAgent API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .endpoint { background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .method { font-weight: bold; color: #0366d6; }
        .path { font-family: monospace; }
        .description { margin: 10px 0; }
    </style>
</head>
<body>
    <h1>TestAgent API</h1>
    <p>Welcome to the TestAgent API. This service provides advanced math capabilities through an AI assistant.</p>
    
    <div class="endpoint">
        <div class="method">POST</div>
        <div class="path">/copilotkit/chat</div>
        <div class="description">Chat with the TestAgent. The agent can help with various math problems including arithmetic, algebra, and more.</div>
    </div>
    
    <div class="endpoint">
        <div class="method">GET</div>
        <div class="path">/health</div>
        <div class="description">Check if the service is running.</div>
    </div>
    
    <h2>Example Queries</h2>
    <ul>
        <li>"What is 123 * 456?"</li>
        <li>"Solve for x: 2x + 5 = 15"</li>
        <li>"What is the square root of 144?"</li>
        <li>"Calculate (5 + 3) * 2 - 10 / 2"</li>
    </ul>
</body>
</html>
"""

@app.get("/")
async def root():
    return HTML

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "TestAgent Gateway",
        "version": "1.0.0"
    }

# Error handling middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import socket
    
    # Get available port if 8080 is in use
    def find_available_port(start_port=8080, max_attempts=10):
        port = start_port
        for _ in range(max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('0.0.0.0', port))
                    return port
            except OSError:
                port += 1
        raise RuntimeError(f"Could not find available port in range {start_port}-{start_port + max_attempts - 1}")
    
    port = find_available_port()
    
    print(f"\n{'='*50}")
    print(f"Starting TestAgent Gateway on http://localhost:{port}")
    print("Available endpoints:")
    print(f"  - GET  /              - API documentation and test page")
    print(f"  - POST /copilotkit/chat - Chat with the TestAgent")
    print(f"  - GET  /health        - Health check endpoint")
    print(f"\nTry it out at: http://localhost:{port}")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
