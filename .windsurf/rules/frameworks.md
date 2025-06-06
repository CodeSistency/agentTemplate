# Windsurf Rule: Framework Usage (Short)

## Purpose
Defines essential rules and minimal code for each core framework.

---

## 1. AG-UI (CopilotKit)
- Use `@copilotkit/react-core` and `@copilotkit/react-ui` for frontend agent UIs.
- Wrap app with `<CopilotKit runtimeUrl="/api/copilotkit">` and use `<CopilotChat agent="..." />`.
- Pass agent/LLM selection and `threadId` to backend.

```tsx
<CopilotKit runtimeUrl="/api/copilotkit">
  <CopilotChat agent="multi_agent_orchestrator" />
</CopilotKit>
```

---

## 2. FastMCP
- Expose backend tools as FastMCP servers with `@tool`.

```python
from fastmcp import FastMCP, tool
mcp = FastMCP(name="Tools")
@tool
def upper(text: str) -> str:
    return text.upper()
mcp.serve()
```

---

## 3. langchain-mcp-adapters
- Integrate MCP tools using `MultiServerMCPClient` and `get_tools()`.

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
mcp_client = MultiServerMCPClient({...})
tools = await mcp_client.get_tools()
```

---

## 4. LangGraph
- Use LangGraph StateGraphs and `MemorySaver` for orchestration/state.

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
graph = StateGraph(dict)
graph.add_node("llm", call_model)
graph.set_entry_point("llm")
checkpointer = MemorySaver()
```

---

## 5. LightRAG
- Use LightRAG for all knowledge retrieval. Tag with session/thread.

```python
from lightrag import LightRAG
rag = LightRAG()
rag.insert(["doc"], session_id="thread_123")
results = rag.query("question", session_id="thread_123")
```

---

## Patterns
- Always send `threadId`, agent, LLM in AG-UI payloads.
- Test and document each tool/agent/knowledge path.
- Handle errors with actionable messages.

---

## References
- [CopilotKit](https://docs.copilotkit.ai/)
- [FastMCP](https://github.com/ContextualAI/fastmcp)
- [langchain-mcp-adapters](https://github.com/ContextualAI/langchain-mcp-adapters)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LightRAG](https://github.com/HKUDS/LightRAG)
