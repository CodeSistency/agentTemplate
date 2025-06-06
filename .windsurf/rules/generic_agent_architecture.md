# Windsurf Rule: Generic Agent Architecture

## Purpose
This rule enforces best practices and standards for any project implementing the architecture described in `generic_agent_architecture.md`.

---

## 1. Architectural Principles
- **Layered Structure**: All code and services must adhere to the defined architectural layers: Presentation (Frontend), Agent Gateway/BFF, Agent Orchestration, Tooling & Knowledge. Cross-layer dependencies are prohibited except as explicitly defined in the architecture doc.
- **Separation of Concerns**: Each layer must have clear, documented responsibilities. Do not mix UI, orchestration, tool, or knowledge logic across layers.
- **Modularity**: Agents, tools, and knowledge services must be independently deployable, replaceable, and extensible.
- **Reusability**: Favor generic, reusable components (e.g., tool adapters, knowledge ingestion scripts, UI components) over one-off solutions.

## 2. Agent and Tool Integration
- **MCP Standard**: All tools must be exposed via the Model Context Protocol (MCP) and integrated using `langchain-mcp-adapters` (not `mcp-use`).
- **Agent Addition**: New agents must be added as independent orchestrators under `backend/orchestrators/`, each with its own `graph.py`, `state.py`, and `prompts.py`.
- **Tool Discovery**: The system must support dynamic discovery and registration of new MCP tools without requiring frontend or orchestrator code changes.

## 3. Knowledge Management
- **LightRAG Usage**: All long-term knowledge must be ingested and served via LightRAG. Session-specific knowledge must be handled using temporary or tagged indices, with proper cleanup after session end.
- **General vs. Session Knowledge**: General knowledge is persistent and available to all agents; session-specific knowledge is only accessible within the current chat/thread context.
- **Knowledge Ingestion**: Scripts for general knowledge ingestion must be located in `scripts/knowledge_ingestion/` and be idempotent and automatable.

## 4. Frontend/UX
- **LLM Selector**: The UI must allow users to select from available LLMs (OpenAI, Gemini, Ollama, etc.).
- **Chat Management**: The UI must support starting new chats, viewing chat history, and resetting conversations.
- **Knowledge Injection**: The UI must allow users to upload or input documents/text for session-specific knowledge grounding.

## 5. Backend/Orchestration
- **Session Management**: All chat and knowledge operations must be keyed by a unique `thread_id` for each session.
- **LLM Flexibility**: The orchestration layer must support dynamic LLM selection based on user preference.
- **Event Streaming**: All agent responses must be streamed to the frontend using the AG-UI protocol, supporting text, tool calls, and HITL events.

## 6. Coding and Documentation
- **Naming Conventions**: All files, classes, and functions must use clear, descriptive names matching their architectural role.
- **Documentation**: All new agents, tools, and knowledge ingestion scripts must be documented with purpose, usage, and integration points.
- **Testing**: All critical logic (routing, tool invocation, knowledge retrieval) must have automated tests.

## 7. Security and Privacy
- **Data Isolation**: Session-specific knowledge must not persist beyond the session unless explicitly promoted to general knowledge.
- **Access Control**: Only authorized users may ingest general knowledge or add new agents/tools.
- **Sensitive Data**: Uploaded documents and chat histories must be handled in accordance with privacy policies and not exposed to unauthorized agents or users.

## 8. Deployment and Operations
- **Environment Configuration**: All service endpoints, API keys, and model settings must be configurable via environment variables or config files.
- **Logging and Monitoring**: All agent and tool invocations, as well as knowledge queries, must be logged for traceability and debugging.
- **Graceful Degradation**: If a tool, agent, or knowledge service is unavailable, the system must provide a clear error message to the user and fallback if possible.
