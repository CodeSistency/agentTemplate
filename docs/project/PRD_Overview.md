Product Requirements Document: Petroleum AI Agent Platform
Version: 3.0
Date: June 5, 2025
1. Introduction
The Petroleum AI Agent Platform is a versatile, AI-powered application designed to assist professionals across the entire petroleum lifecycle. It functions as an intelligent assistant, accessible via a chatbot interface. Users can create projects or chats, and interact with a variety of specialized AI agents.
A core capability of the platform is its flexible knowledge management. Users can upload general knowledge resources (e.g., textbooks, industry standards, extensive public datasets) that can serve as a foundational knowledge base, potentially for enhancing or fine-tuning the underlying Large Language Models (LLMs). Separately, within individual projects or chats, users can upload specific files (data, documents) to provide immediate context for the ongoing interaction with an agent.
The platform allows users to select from different underlying LLMs, including prominent commercial models and locally deployable open-source options. A key feature is the ability to choose a specific petroleum domain agent (e.g., Reservoir Engineering, Drilling, Production) tailored for certain tasks, or a multi-agent system that automatically orchestrates and delegates tasks among the specialized agents to achieve complex goals.
This document outlines the overall platform vision and provides detailed requirements for an initial cornerstone agent: the Reservoir Engineering Agent Consultant. This agent will focus on analyzing user-provided data files and documents, leveraging chat-specific knowledge and specialized calculation tools.
2. Goals
Platform Goals:
To provide a unified, chat-based interface for accessing a suite of AI agents specialized in various petroleum domains.
To empower users with the flexibility to choose from a range of LLMs, balancing performance, cost, and data privacy needs (including local model support).
To enable efficient knowledge sharing with AI agents through easy resource uploading, both for general platform knowledge and for specific chat contexts.
To streamline complex workflows through intelligent multi-agent orchestration.
To create an extensible platform where new specialized petroleum agents can be readily integrated.
Reservoir Engineering Agent Goals (Illustrative for a specialized agent):
To significantly reduce the manual effort required for routine reservoir data analysis and reporting.
To provide Reservoir Engineers with quick access to synthesized information from their project-specific documents and data.
To generate standard reservoir engineering metrics and plots accurately and efficiently.
To offer data-driven insights and flag potential anomalies based on uploaded data.
To serve as a valuable "consultant" by explaining data, analyses, and relevant concepts based on project documentation.
3. Target Audience
Petroleum Engineers (Reservoir, Drilling, Production, etc.)
Geoscientists
Data Analysts in the energy sector
Project Managers and Decision-Makers in oil and gas operations.
(The audience will expand as more specialized agents are developed.)
4. Scope
Platform Scope (In Scope for V1):
User account management (basic login).
Project/Chat creation and organization for managing interactions.
Uploading of general knowledge resources to a central repository accessible by the platform, intended for broader AI model enhancement or reference.
Uploading of chat-specific resources (files) directly within a project/chat to provide immediate context to agents for that conversation.
Selection mechanism for choosing the underlying LLM.
Selection mechanism for choosing the active agent (e.g., "Reservoir Agent," "Multi-Agent Orchestrator").
A multi-agent orchestration capability that can understand a task and delegate sub-tasks to appropriate specialized agents.
Chat interface for user interaction, querying data, requesting analyses, and receiving insights.
Storing uploaded general and chat-specific resources and chat history persistently.
Reservoir Engineering Agent Scope (In Scope for V1 - as an example of a specialized agent):
Analysis of user-provided structured data files (e.g., CSV, Excel) and unstructured/semi-structured documents (e.g., PDF, Word, text) uploaded as chat-specific knowledge.
Basic data validation suggestions upon resource upload.
Agentic core for interpreting user requests and orchestrating internal tools, using the provided chat-specific knowledge.
Access to specialized reservoir engineering calculation tools for:
Decline Curve Analysis (DCA)
Material Balance (MB) Analysis (basic)
Basic Volumetric Calculations
Basic Pressure Data Analysis
Basic Fluid Property Estimation (using correlations)
Basic Well Log Analysis
Generation of standard reservoir engineering plots.
Generation of summary reports based on analyses.
Ability for the agent to explain its findings and the basis of its analysis from the provided chat-specific resources.
Out of Scope for V1 (Platform & Initial Reservoir Agent):
Automated fine-tuning of LLMs using the uploaded general knowledge resources (though the resources will be available for such processes to be developed later).
Direct, real-time integration with external company-wide data platforms.
Advanced autonomous control of any field operations or critical systems.
For the Reservoir Agent: Advanced reservoir simulation setup/interaction, complex well test analysis, complex geomechanical analysis, advanced uncertainty analysis.
Multi-user real-time collaboration features within the same project/chat.
5. User Stories / Use Cases
Platform Use Cases:
As an Administrator, I want to upload a collection of industry-standard petroleum engineering textbooks as "general knowledge" so that all agents can potentially benefit from this information base.
As a User, I want to create a new project for my "Field Alpha Study."
As a User, I want to upload several PDF reports and CSV production data files into my "Field Alpha Study" project so the AI can use this information for our current discussion.
As a User, I want to select the "Gemini Pro" model for my current chat session.
As a User, I want to select the "Reservoir Engineering Agent" to ask questions about oil in place.
As a User, I want to use the "Multi-Agent Orchestrator" to plan a field development strategy, so it can leverage insights from Reservoir, Drilling, and Production agents using the context I've provided in this chat.
Reservoir Engineering Agent Use Cases (Illustrative):
As a Reservoir Engineer, I want to upload my well production data to the Reservoir Agent (within my current chat) so it can analyze decline trends and estimate reserves based on that data.
Scenario: Upload a CSV file into the chat. Ask the agent: "Using the Reservoir Agent and the production data I just uploaded, analyze the decline for Well ABC and estimate its remaining oil reserves based on a 5 STB/day economic limit."
As a Reservoir Engineer, I want to upload a core analysis report (into my current chat) so the Reservoir Agent can extract key properties and make them searchable for this session.
Scenario: Upload a PDF into the chat. Ask the agent: "Reservoir Agent, what was the average matrix permeability reported in the core study for Well DEF from the document I just provided?"
(Other Reservoir Engineering Agent use cases from the original PRD, Section 5, remain relevant here, with the understanding that resources are chat-specific.)
6. Functional Requirements
6.1 Platform Core Functionality
REQ-P.1.1: The system shall allow users to create, manage, and switch between "Projects" or "Chats".
REQ-P.1.2: The system shall provide a mechanism for authorized users (e.g., administrators) to upload general knowledge resources (documents, datasets) to a central platform repository.
REQ-P.1.3: Within an active project/chat, the system shall allow users to upload chat-specific resources (files) that provide context solely for that specific interaction.
REQ-P.1.4: The system shall provide a clear mechanism for users to select the primary LLM to be used.
REQ-P.1.5: The system shall provide a clear mechanism for users to select a specialized AI agent or the "Multi-Agent Orchestrator".
REQ-P.1.6: The system's chat interface shall allow users to input natural language queries or commands.
REQ-P.1.7: The system shall maintain conversation history within a project/chat.
REQ-P.1.8: Uploaded general and chat-specific resources shall be securely stored and appropriately associated.
REQ-P.1.9: The system shall include basic user authentication and authorization, including role differentiation for managing general knowledge resources.
6.2 Multi-Agent Orchestration
REQ-P.2.1: When the "Multi-Agent Orchestrator" is selected, the system shall analyze the user's request, utilizing chat-specific context.
REQ-P.2.2: The orchestrator shall be capable of decomposing complex requests into sub-tasks suitable for individual specialized agents.
REQ-P.2.3: The orchestrator shall route sub-tasks to appropriate agents and synthesize their outputs.
REQ-P.2.4: The orchestrator shall manage the flow of information between agents as needed.
6.3 Specialized Agent Core Functionality (General for any agent, exemplified by Reservoir Agent)
REQ-A.1.1: Each specialized agent shall be able to interpret user queries relevant to its domain.
REQ-A.1.2: Agents shall primarily utilize the chat-specific resources uploaded by the user within the active project/chat to inform their responses and analyses. They may also draw upon the general knowledge base if designed to do so for broader context.
REQ-A.1.3: Agents shall be able to identify when a query requires performing a specialized calculation or data analysis using its internal tools.
REQ-A.1.4: Agents shall manage the conversation history to maintain context.
REQ-A.1.5: Agents shall be able to explain the source of their information (from uploaded chat-specific documents) or the general method used for an analysis.
6.4 Data Ingestion and Management (for chat-specific resources used by agents like Reservoir Engineering)
REQ-RE.1.1: The Reservoir Engineering Agent shall support ingestion of structured data files uploaded as chat-specific resources.
REQ-RE.1.2: The Reservoir Engineering Agent shall support ingestion of unstructured/semi-structured documents uploaded as chat-specific resources.
REQ-RE.1.3: The system shall attempt to automatically identify common data patterns in structured files uploaded to a chat.
REQ-RE.1.4: The system shall perform basic data validation suggestions upon chat-specific resource upload.
6.5 Reservoir Engineering Agent Tooling & Analysis (Specific to this agent, using chat-specific context)
REQ-RE.2.1: The Reservoir Engineering Agent shall include tools for Decline Curve Analysis (DCA), Material Balance (MB) analysis, Volumetric calculations, Pressure Data Analysis, fluid property estimation, and basic Well Log Analysis, operating on the data provided within the chat.
(Detailed sub-requirements for each tool from v2.0, e.g., REQ-RE.2.1.1, REQ-RE.2.1.2, etc., apply here but are consolidated for brevity, with the understanding they use chat-specific context.)
REQ-RE.2.2: The Reservoir Engineering Agent shall synthesize information and analysis tool outputs to provide insights relevant to the chat context.
REQ-RE.2.3: The Reservoir Engineering Agent shall be able to flag potential anomalies in data based on observed trends within the chat-specific data.
6.6 Visualization and Reporting (Behavior of agents providing outputs based on chat context)
REQ-A.2.1: Agents capable of data analysis shall generate relevant plots and visualizations based on chat-specific data.
REQ-A.2.2: Plots shall be displayed within the UI.
REQ-A.2.3: Users shall be able to export generated plots and reports.
REQ-A.2.4: Agents shall generate summary reports of analyses performed on chat-specific data.
6.7 User Interface (Platform Level)
REQ-P.3.1: The system shall have an intuitive web-based user interface.
REQ-P.3.2: The UI shall provide distinct areas or mechanisms for managing/uploading general knowledge resources (e.g., an admin panel) versus chat-specific resources (within the chat interface).
REQ-P.3.3: The Interaction Interface shall feature a main area for displaying agent responses and a chat window for user input and uploading chat-specific files.
REQ-P.3.4: The UI shall provide clear feedback on the system's status.
REQ-P.3.5: The UI shall provide mechanisms for managing projects/chats.
7. Key System Attributes (Non-Functional Requirements - Behavioral Focus)
Extensibility: The platform architecture should facilitate the addition of new specialized petroleum agents and LLMs.
Modularity: Specialized agents and core platform services should be relatively independent.
User-Friendliness: The interface should be intuitive. Interactions should primarily be through natural language.
Responsiveness: The system should provide timely feedback.
Contextual Awareness: Agents must effectively use chat-specific resources and history. The system should also be aware of available general knowledge resources.
Data Security & Privacy: User-uploaded data (both general and chat-specific) must be handled securely.
Configurability: Users should be able to select preferred models and agents.
9. Future Considerations (Beyond V1)
Automated LLM Fine-tuning: Developing processes to leverage the "general knowledge resources" for fine-tuning selected LLMs.
Advanced Knowledge Linking: Creating relationships between general knowledge and insights derived from chat-specific interactions.
(Other future considerations from v2.0 remain relevant.)
