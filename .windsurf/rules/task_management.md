# Windsurf Rule: Task Generation and Execution

## Purpose
This document defines rules and best practices for generating new tasks and for agents executing those tasks. These guidelines aim to ensure clarity, efficiency, and reliability in task management within the AI system.

---

## 1. Task Generation

These rules apply when an agent (or a human user interacting with an agent) defines a new task for an AI agent or a multi-agent system.

### 1.1. Clarity and Specificity
- **Rule:** Tasks must be clearly defined, unambiguous, and specific. Avoid vague language.
- **Guideline:** State the desired outcome or goal of the task explicitly.
- **Example (Bad):** "Improve the system."
- **Example (Good):** "Refactor the `user_authentication` module to use OAuth 2.0 for Google Sign-In."

### 1.2. Actionability
- **Rule:** Tasks must describe an action or a series of actions that can be performed.
- **Guideline:** Use action verbs to describe what needs to be done.
- **Example:** "Analyze user feedback from the last 7 days and categorize common issues."

### 1.3. Atomicity and Decomposition
- **Rule:** Prefer atomic tasks that represent a single unit of work. Complex tasks should be broken down into smaller, manageable sub-tasks.
- **Guideline:** If a task requires multiple distinct steps or involves different specialized agents, consider creating separate sub-tasks for each.
- **Example (Complex):** "Build and deploy the new reporting feature."
- **Example (Decomposed):
    - "Design the database schema for the reporting feature."
    - "Implement the backend API endpoints for report generation."
    - "Develop the frontend UI for displaying reports."
    - "Write integration tests for the reporting feature."
    - "Deploy the reporting feature to the staging environment."

### 1.4. Context and Dependencies
- **Rule:** Tasks must include all necessary context, inputs, and prerequisite information or clearly state their dependencies.
- **Guideline:** If a task depends on the completion of another task or specific data, this must be noted.
- **Example:** "Generate a sales report for Q3, using the `final_sales_data_q3.csv` file (dependency: `data_processing_pipeline_q3` task must be complete)."

### 1.5. Acceptance Criteria
- **Rule:** Each task should have clear, measurable acceptance criteria that define what constitutes successful completion.
- **Guideline:** How will the agent (or a reviewer) know the task is done correctly?
- **Example:** "Acceptance Criteria for 'Implement OAuth 2.0': Users can successfully sign in with their Google accounts; existing username/password login remains functional."

### 1.6. Prioritization (Optional)
- **Guideline:** If applicable, assign a priority level (e.g., High, Medium, Low) to tasks to guide execution order.

### 1.7. Assignee/Agent Type (For Multi-Agent Systems)
- **Guideline:** If the task is intended for a specific type of specialized agent, indicate this. If for the master orchestrator, it can decide the routing.
- **Example:** "Task: Summarize recent news articles on AI. (Assignee Type: `NewsAnalysisAgent`)"

---

## 2. Task Execution

These rules apply when an AI agent receives a task and begins working on it.

### 2.1. Understanding and Clarification
- **Rule:** Before starting, the agent must ensure it fully understands the task, its goals, context, and acceptance criteria.
- **Guideline:** If the task is ambiguous or lacks information, the agent should seek clarification (e.g., from the originating agent, user, or by consulting knowledge bases).

### 2.2. Planning and Decomposition (If Necessary)
- **Rule:** For complex tasks not already decomposed, the agent must create an internal plan, breaking the task into smaller, logical steps.
- **Guideline:** This plan should outline the sequence of actions, tool usage, and knowledge retrieval needed.

### 2.3. Resource Utilization
- **Rule:** Agents must efficiently utilize available resources, including:
    - **Tools (FastMCP):** Select and use the most appropriate tools for sub-steps.
    - **Knowledge (LightRAG):** Query general and session-specific knowledge bases for relevant information.
    - **Other Agents:** If part of a multi-agent system, delegate sub-tasks to other specialized agents as needed (via the master orchestrator or direct interaction if allowed).

### 2.4. Error Handling and Retries
- **Rule:** Agents must have robust error handling mechanisms.
- **Guideline:** Implement retry logic for transient errors (e.g., network issues when calling a tool). For persistent errors, log the error and report failure gracefully, providing diagnostic information.

### 2.5. Progress Reporting and Logging
- **Rule:** Agents should log key actions, decisions, tool invocations, and errors encountered during task execution.
- **Guideline:** For long-running tasks, provide periodic progress updates if the architecture supports it (e.g., via AG-UI streaming events).

### 2.6. Verification Against Acceptance Criteria
- **Rule:** Upon completing the planned steps, the agent must verify its work against the task's acceptance criteria.
- **Guideline:** If possible, perform self-checks or use validation tools/logic.

### 2.7. Completion and Handoff
- **Rule:** Once a task is successfully completed and verified, the agent must report completion status and provide any outputs or results.
- **Guideline:** If the task was part of a larger workflow, notify the orchestrating agent or user.

### 2.8. State Management
- **Rule:** Agents must manage their internal state and the state of the task (e.g., pending, in-progress, completed, failed) consistent with the LangGraph checkpointer and overall session management.
