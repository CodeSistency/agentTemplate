---
description: Implementation
---

## AI Agent Workflow: Continue Project Implementation

This workflow guides the AI assistant in contributing to the ongoing development of the modular multi-agent AI architecture. It ensures consistency, adherence to project standards, and leverages previously established knowledge and rules.

### Phase 1: Contextual Grounding & Understanding

1.  **Review Latest State & User Request:**
    *   Carefully analyze the last interaction, checkpoint summary, and the current USER request to understand the immediate objective.
    *   If the request is broad (e.g., "continue working"), identify the most logical next task based on previous discussions or outstanding items from the architecture documents.

2.  **Consult Architectural Blueprints:**
    *   Re-familiarize yourself with the primary architecture document being implemented or extended (e.g., `multi_agent_architecture.md` or `generic_agent_architecture.md`).
    *   Pay attention to the defined layers (Presentation, Gateway, Orchestration, Tooling & Knowledge) and their responsibilities.

3.  **Internalize Project Rules:**
    *   **Crucial:** Review the following Windsurf rules located in `.windsurf/rules/` before proceeding:
        *   `generic_agent_architecture.md` (if relevant to the current task context)
        *   `multi_agent_architecture.md` (if relevant to the current task context)
        *   `frameworks.md` (for correct usage of AG-UI, FastMCP, LangGraph, LightRAG, etc.)
        *   `task_management.md` (for defining and executing sub-tasks)
        *   `project-structure.md` (if it exists, otherwise adhere to the structure in the main architecture documents).
    *   Ensure all subsequent actions strictly adhere to these rules.

### Phase 2: Planning & Design

1.  **Task Decomposition (Adhering to `task_management.md`):
    *   Break down the USER's request or the identified next objective into clear, specific, and actionable sub-tasks.
    *   For each sub-task, define:
        *   A clear goal/outcome.
        *   Necessary inputs and expected outputs.
        *   Acceptance criteria (how to verify completion).
        *   Potential dependencies on other sub-tasks or existing components.
        *   Relevant architectural layers and components involved.

2.  **Framework & Tool Selection (Adhering to `frameworks.md`):
    *   For each sub-task, identify the appropriate frameworks, libraries, and tools required (e.g., LangGraph for an orchestrator, FastMCP for a new tool, LightRAG for knowledge access).
    *   Plan how these will be integrated, following the patterns in `frameworks.md`.

3.  **File and Code Structure Planning:
    *   Determine which existing files need modification or what new files need to be created.
    *   Ensure new files are placed in the correct directories as per the project's defined folder structure (see architecture documents or `project-structure.md`).

### Phase 3: Implementation & Execution

1.  **Iterative Development:**
    *   Implement the planned sub-tasks one by one, or in a logical sequence.
    *   Write clean, well-documented code.
    *   **Strictly follow coding examples and best practices outlined in `.windsurf/rules/frameworks.md`** for each technology used.

2.  **Tool & Service Integration:**
    *   When creating new tools, ensure they are exposed via FastMCP.
    *   Integrate tools into LangGraph agents using `langchain-mcp-adapters`.
    *   Interface with LightRAG for knowledge operations as per its defined patterns.

3.  **Adherence to Architectural Layers:**
    *   Ensure that logic remains within its designated architectural layer (e.g., no direct calls from frontend to deep backend services, bypassing the gateway or orchestrators).

### Phase 4: Verification & Documentation

1.  **Self-Correction & Review:**
    *   Review the implemented code against the sub-task's acceptance criteria and the overall USER request.
    *   Check for adherence to all project rules (architecture, frameworks, task management).

2.  **Update Documentation (As Needed):
    *   If the changes introduce new components, modify existing ones significantly, or alter workflows, update relevant sections of `generic_agent_architecture.md`, `multi_agent_architecture.md`, or other project documentation.
    *   Ensure code comments are clear and explain complex logic.

### Phase 5: Reporting & Next Steps

1.  **Summarize Work Done:**
    *   Provide a concise summary of the tasks completed and the changes made.
    *   List all new files created and key files modified.
    *   Explain how the implementation addresses the USER's request or moves the project forward.

2.  **Propose Next Steps or Seek Clarification:**
    *   If further steps are obvious, suggest them.
    *   If ambiguities were encountered or decisions made that require USER validation, ask for clarification.
    *   Indicate readiness for the next task.

--- 
*This workflow is a living document and can be updated as the project evolves.*