# Product Requirements Document: Petroleum AI Agent Platform

**Version:** 1.0
**Date:** June 5, 2025

## 1. Introduction

### 1.1. Problem Statement
Professionals across the petroleum lifecycle (exploration, drilling, production, reservoir management) face challenges in efficiently accessing and synthesizing vast amounts of specialized knowledge, performing rapid and accurate data analysis, and making timely, informed decisions. Existing tools are often siloed, require significant manual effort, and lack intelligent, context-aware assistance.

### 1.2. Proposed Solution
The Petroleum AI Agent Platform is a versatile, AI-powered application designed to address these challenges. It functions as an intelligent assistant, accessible via a modern chat-based interface. Users can create projects or chats, upload relevant data and documents, and interact with a variety of specialized AI agents tailored to specific petroleum domains. The platform emphasizes flexible knowledge management, choice of underlying Large Language Models (LLMs), and robust tool integration.

### 1.3. Vision
To empower petroleum professionals with a unified, intelligent, and extensible AI assistant that streamlines complex workflows, enhances data interpretation, provides actionable insights, and fosters innovation across all segments of the oil and gas industry.

### 1.4. Core Technologies & Frameworks
This platform will leverage a combination of cutting-edge AI technologies and robust software frameworks:

*   **Frontend Interaction & UI Protocol:** AG-UI will be used to ensure a responsive, event-driven, and standardized chat interface, facilitating rich interactions between the user and the AI agents.
*   **Backend Agent Logic & Orchestration:**
    *   **LangChain:** Will form the core for LLM interactions, prompt engineering, managing conversational memory, and basic agent capabilities.
    *   **LangGraph:** Will be employed for building stateful, multi-actor applications, enabling complex agent workflows, tool usage sequences, and sophisticated multi-agent orchestration.
*   **Tool & Service Exposure (Specialized Capabilities):** FastMCP will be used to create secure and standardized MCP (Model Context Protocol) servers. These servers will expose specialized petroleum engineering calculations, data processing utilities, and other functionalities as tools that AI agents can consume.
*   **Agent-Tool Communication:** `mcp-use` will bridge LangChain/LangGraph agents with the FastMCP tool servers, allowing agents to discover and utilize the exposed tools seamlessly.
*   **Knowledge Management (Retrieval Augmented Generation - RAG):** LightRAG will be implemented for comprehensive document ingestion (supporting multimodal content like PDF, DOCX, CSV, images, tables, and formulas), efficient chunking, state-of-the-art embedding generation, robust vector storage, and advanced semantic search capabilities. This includes providing citations for information retrieved from documents.

## 2. Goals

### 2.1. Platform Goals
*   **Unified Access:** Provide a single, intuitive chat-based interface (AG-UI) for accessing a suite of AI agents specialized in various petroleum domains.
*   **LLM Flexibility:** Empower users with the flexibility to choose from a range of LLMs (via LangChain), balancing performance, cost, and data privacy needs, including support for locally deployable open-source options where feasible.
*   **Efficient Knowledge Management:** Enable efficient knowledge sharing with AI agents through easy resource uploading (general platform knowledge and chat-specific context) and advanced RAG capabilities (LightRAG).
*   **Intelligent Orchestration:** Streamline complex workflows through intelligent multi-agent orchestration (LangGraph), allowing agents to collaborate and delegate tasks.
*   **Extensibility & Modularity:** Create an extensible platform where new specialized petroleum agents (LangGraph) and tools (FastMCP) can be readily integrated with minimal friction.

### 2.2. Initial Specialized Agent Goals (Reservoir Engineering Agent Consultant - V1)
*   **Reduce Manual Effort:** Significantly reduce the manual effort required for routine reservoir data analysis, interpretation, and reporting.
*   **Rapid Information Synthesis:** Provide Reservoir Engineers with quick access to synthesized information from their project-specific documents and data (LightRAG).
*   **Accurate Metrics & Plots:** Generate standard reservoir engineering metrics and plots accurately and efficiently using specialized tools (FastMCP) orchestrated by the agent (LangGraph).
*   **Data-Driven Insights:** Offer data-driven insights and flag potential anomalies based on uploaded data and performed analyses.
*   **Consultative Assistance:** Serve as a valuable "consultant" by explaining data, analyses, and relevant petroleum engineering concepts, sourcing information from provided project documentation (LightRAG with citations).

## 3. Target Audience

*   Petroleum Engineers (Reservoir, Drilling, Production, Completions, etc.)
*   Geoscientists (Geologists, Geophysicists)
*   Data Analysts and Data Scientists in the energy sector
*   Project Managers and Decision-Makers in oil and gas operations
*   (The audience will expand as more specialized agents are developed for other domains.)

## 4. Scope

### 4.1. Platform Scope (In Scope for V1)
*   **User Management:** Basic user account creation, login, and profile management.
*   **Project/Chat Management:** Ability for users to create, name, organize, and switch between different projects or chat sessions.
*   **General Knowledge Repository:**
    *   Mechanism for authorized users (e.g., administrators) to upload general knowledge resources (textbooks, standards, public datasets) to a central repository.
    *   Processing of these resources by LightRAG for platform-wide RAG capabilities.
*   **Chat-Specific Knowledge:**
    *   Mechanism for users to upload files (data, documents) directly within a project/chat to provide immediate context for that specific interaction.
    *   Processing of these resources by LightRAG for chat-specific RAG.
*   **LLM Selection:** UI and backend logic for users to select their preferred underlying LLM for a given chat session from a list of available models (integrated via LangChain).
*   **Agent Selection:** UI and backend logic for users to select the active AI agent (e.g., "Reservoir Engineering Agent," "Multi-Agent Orchestrator").
*   **Multi-Agent Orchestration Core:** A foundational multi-agent orchestration capability (LangGraph) that can understand a high-level task and delegate sub-tasks to appropriate specialized agents (initially, the Reservoir Agent).
*   **Chat Interface (AG-UI):** Interactive chat interface for user input (natural language, commands), displaying agent responses (text, plots, tables), and managing file uploads.
*   **Persistence:** Secure storage for user accounts, project/chat metadata, conversation history, and references to uploaded general and chat-specific resources (LightRAG will manage its own data stores for embeddings and processed documents).

### 4.2. Specialized Agent Scope

#### 4.2.1. Reservoir Engineering Agent Consultant (In Scope for Initial V1)
*   **Data Ingestion & Understanding (LightRAG):**
    *   Analysis of user-provided structured data files (e.g., CSV, Excel) and unstructured/semi-structured documents (e.g., PDF, Word, text, images with relevant data) uploaded as chat-specific knowledge.
    *   Basic data validation suggestions upon resource upload (e.g., missing columns, unexpected data types).
*   **Agentic Core (LangChain, LangGraph, `mcp-use`):**
    *   Interpretation of user requests relevant to reservoir engineering.
    *   Orchestration of internal tools and RAG capabilities using chat-specific knowledge.
*   **Specialized Calculation Tools (Exposed via FastMCP):**
    *   Decline Curve Analysis (DCA): Arps (Exponential, Hyperbolic, Harmonic), rate-time, cum-time plots, EUR estimation.
    *   Material Balance (MB) Analysis: Basic Havlena-Odeh for oil reservoirs (P/z for gas later).
    *   Basic Volumetric Calculations: OOIP/OGIP from maps or parameters.
    *   Basic Pressure Data Analysis: Simple pressure transient plot identification (e.g., IARF, PSF).
    *   Basic Fluid Property Estimation: Correlations for Bo, Bg, mu_o, mu_g, Z-factor.
    *   Basic Well Log Analysis: Porosity from Density/Neutron, Sw from Archie's.
*   **Output Generation:**
    *   Generation of standard reservoir engineering plots (e.g., DCA plots, P/z plots).
    *   Generation of summary reports based on analyses performed.
*   **Explainability & Sourcing:**
    *   Ability for the agent to explain its findings, the methods used, and the basis of its analysis, referencing specific information from the provided chat-specific resources (LightRAG citations).

#### 4.2.2. Drilling Engineering Agent (Future V1.x / V2 Scope)
*   **Core Functionalities:**
    *   **Basic Well Design Parameter Suggestions:** Provide guidance on parameters like casing seat depths based on user-provided pore pressure and fracture gradient data. Assist with basic directional drilling trajectory considerations.
    *   **Common Drilling Problem Diagnosis:** Help identify potential causes for common drilling issues (e.g., stuck pipe, lost circulation, kicks) based on described symptoms and operational parameters. Suggest initial diagnostic steps or relevant information to gather.
*   **Key Tools (FastMCP - Examples):**
    *   Casing seat depth estimator.
    *   Drilling problem diagnostic knowledge base/ruleset.
*   **RAG Integration (LightRAG - Examples):**
    *   Utilize drilling manuals, best practices documents, and case histories for problem diagnosis and parameter suggestions.
    *   Ingest user-provided drilling programs, daily drilling reports, and real-time data (if simplified and provided as context).

#### 4.2.3. Production Optimization Agent (Future V1.x / V2 Scope)
*   **Core Functionalities:**
    *   **Artificial Lift Method Selection Guidance:** Offer recommendations for suitable artificial lift methods (e.g., ESP, Gas Lift, PCP, Rod Pump) based on well conditions, fluid properties, and production targets provided by the user.
    *   **Basic Production Bottleneck Analysis:** Analyze production data (rates, pressures) and well configuration details (provided by user) to suggest potential areas of inflow or outflow restriction.
*   **Key Tools (FastMCP - Examples):**
    *   Artificial lift screening tool (based on criteria).
    *   Simple nodal analysis concepts (qualitative).
*   **RAG Integration (LightRAG - Examples):**
    *   Access production handbooks, artificial lift design guides, and field performance data.
    *   Ingest well test reports, production histories, and equipment specifications.

#### 4.2.4. Geology & Geophysics Agent (Future V1.x / V2 Scope)
*   **Core Functionalities:**
    *   **Formation Top Correlation Assistance:** Assist in correlating formation tops across multiple wells using uploaded well log data (e.g., LAS files, textual descriptions of picks).
    *   **Basic Seismic Attribute Analysis Guidance:** Provide information on common seismic attributes, their typical applications, and how they might relate to identifying specific geological features or reservoir properties based on user queries.
*   **Key Tools (FastMCP - Examples):**
    *   Log data visualizer/comparator (conceptual for V1, actual plotting if feasible).
    *   Seismic attribute knowledge base.
*   **RAG Integration (LightRAG - Examples):**
    *   Utilize geological textbooks, regional studies, and seismic interpretation guides.
    *   Ingest well completion reports, geological maps, and seismic survey parameters.

#### 4.2.5. Petrophysical Analysis Agent (Future V1.x / V2 Scope)
*   **Core Functionalities:**
    *   **Quick-Look Log Interpretation:** Identify potential pay zones, fluid contacts, and lithology from standard well log suites (GR, Resistivity, Neutron, Density) provided by the user.
    *   **Basic Petrophysical Parameter Calculation:** Calculate fundamental parameters like Vshale (from GR), Porosity (from Density/Neutron logs), and Water Saturation (e.g., Archie's equation with user-provided parameters).
*   **Key Tools (FastMCP - Examples):**
    *   Vshale calculator.
    *   Porosity calculator (Density, Neutron-Density methods).
    *   Sw calculator (Archie).
*   **RAG Integration (LightRAG - Examples):**
    *   Access petrophysics textbooks, log interpretation charts, and core analysis data.
    *   Ingest LAS files, core reports, and mud log data.

#### 4.2.6. Economics & Risk Assessment Agent (Future V1.x / V2 Scope)
*   **Core Functionalities:**
    *   **Simple Economic Indicator Calculation:** Calculate key economic metrics like Net Present Value (NPV), Internal Rate of Return (IRR), and Payback Period from user-provided cash flow projections or production forecasts and cost estimates.
    *   **Qualitative Risk Factor Identification:** Help identify and list potential technical and economic risk factors for a given petroleum project scenario described by the user.
*   **Key Tools (FastMCP - Examples):**
    *   NPV/IRR/Payback calculator.
    *   Risk factor checklist/database.
*   **RAG Integration (LightRAG - Examples):**
    *   Utilize economic evaluation handbooks, risk management frameworks, and commodity price forecasts.
    *   Ingest AFE documents, financial models, and project feasibility studies.

### 4.3. Out of Scope for V1 (Platform & Initial Reservoir Agent)
*   Automated fine-tuning of LLMs using the uploaded general knowledge resources (though resources will be available for future development).
*   Direct, real-time integration with external company-wide data platforms or SCADA systems.
*   Advanced autonomous control of any field operations or critical systems.
*   For the Reservoir Agent: Advanced reservoir simulation setup/interaction, complex well test analysis (e.g., deconvolution), complex geomechanical analysis, advanced uncertainty quantification workflows (e.g., Monte Carlo on full models).
*   Multi-user real-time collaboration features within the same project/chat (e.g., multiple users editing/chatting simultaneously).
*   Advanced administrative features beyond basic user and general knowledge management.

## 5. User Stories / Use Cases

### 5.1. Platform Use Cases
*   **As an Administrator,** I want to upload a collection of industry-standard petroleum engineering textbooks and SPE papers as "general knowledge" so that all agents can potentially benefit from this information base when answering broader questions.
*   **As a User,** I want to create a new project named "Field Alpha Study" to keep all my interactions and data related to this field organized.
*   **As a User,** I want to upload several PDF geological reports, CSV production data files, and LAS well log files into my "Field Alpha Study" project so the AI can use this specific information for our current discussion.
*   **As a User,** I want to select the "Claude 3.5 Sonnet" model for my current chat session because I prefer its analytical capabilities for this task.
*   **As a User,** I want to select the "Reservoir Engineering Agent" to ask specific questions about oil in place calculations for a particular zone in Field Alpha.
*   **As a User,** I want to use the "Multi-Agent Orchestrator" to ask, "Based on the production data and geological reports for Field Alpha, provide a preliminary assessment of infill drilling opportunities and suggest key data to acquire next," so it can leverage insights from Reservoir, (future) Drilling, and (future) Economic agents using the context I've provided in this chat.
*   **As a User,** I want to ask the agent a question and see the source document and page number for any factual claims it makes based on the documents I uploaded (enabled by LightRAG citation).

### 5.2. Reservoir Engineering Agent Use Cases (Illustrative)

### 5.3. Drilling Engineering Agent Use Cases (Illustrative - Future V1.x / V2)
*   **As a Drilling Engineer,** I want to provide the Drilling Agent with pore pressure and fracture gradient data for a planned well section, and ask for a suggested casing seat depth range and the reasoning behind it.
    *   *Scenario:* "Drilling Agent, for a vertical well section from 3000m to 4500m, the pore pressure gradient is 0.45 psi/ft and the minimum horizontal stress gradient (interpreted as frac gradient) is 0.7 psi/ft. What would be a reasonable depth to set the 9 5/8" casing?"
*   **As a Drilling Supervisor,** I'm experiencing intermittent high torque and drag while drilling the 8 1/2" hole section. I want to describe the symptoms and current drilling parameters to the Drilling Agent to get a list of potential causes and recommended immediate actions or data to check.
    *   *Scenario:* "Drilling Agent, we're seeing torque spikes from 15 kft-lbs to 25 kft-lbs and overpull of 30 klbs when making connections. We are drilling with WBM, 12 ppg, flow rate 600 gpm, RPM 120. What could be causing this and what should we check first?"

### 5.4. Production Optimization Agent Use Cases (Illustrative - Future V1.x / V2)
*   **As a Production Engineer,** I have a well (Well P-10) that has stopped flowing naturally. I want to provide its production history, fluid properties, and current reservoir pressure to the Production Optimization Agent to get a recommendation for the most suitable artificial lift methods to consider.
    *   *Scenario:* Upload `Well_P-10_Data.xlsx`. "Production Agent, based on the data for Well P-10, what artificial lift methods should I evaluate for restoring production? The well produces 35 API oil with a GOR of 800 scf/stb."
*   **As a Production Technologist,** I want to upload daily production data (oil rate, water cut, GOR, THP, FLP) for a group of ESP-lifted wells and ask the Production Optimization Agent to identify any wells that might be showing signs of suboptimal performance or potential pump issues.
    *   *Scenario:* Upload `ESP_Well_Group_Data.csv`. "Production Agent, review this data for my ESP wells. Are there any wells that appear to be underperforming or might need operational adjustments based on these trends?"

### 5.5. Geology & Geophysics Agent Use Cases (Illustrative - Future V1.x / V2)
*   **As a Geologist,** I have uploaded LAS files for three nearby wells. I want the Geology & Geophysics Agent to help me correlate the 'Top Sand C' marker across these wells based on GR and Resistivity logs.
    *   *Scenario:* Upload `WellA.las`, `WellB.las`, `WellC.las`. "G&G Agent, please display the GR and Deep Resistivity logs for Well A, B, and C between 2000m and 2500m. I've picked Top Sand C in Well A at 2250m. Can you suggest equivalent picks in Well B and C?"
*   **As a Geophysicist,** I am evaluating a prospect and have identified a seismic amplitude anomaly. I want to ask the Geology & Geophysics Agent what this type of anomaly could represent in a clastic depositional environment and what other seismic attributes might help differentiate the possibilities.
    *   *Scenario:* "G&G Agent, I see a strong negative amplitude anomaly (dim spot) on my 3D seismic in an area expected to be predominantly shales with interbedded sands. What could this indicate, and what other attributes like AVO or spectral decomposition might help clarify if it's a hydrocarbon accumulation versus a lithology change?"

### 5.6. Petrophysical Analysis Agent Use Cases (Illustrative - Future V1.x / V2)
*   **As a Petrophysicist,** I have an LAS file with standard logs (GR, NPHI, RHOB, RT). I want the Petrophysical Agent to perform a quick-look interpretation to identify potential reservoir zones and estimate Vshale and effective porosity for those zones.
    *   *Scenario:* Upload `Well_Z1_Logs.las`. "Petrophysics Agent, analyze these logs for Well Z1. Identify potential reservoir intervals, and for each, calculate Vshale using the linear method (GRmin=20, GRmax=120) and effective porosity using the Neutron-Density crossplot method (sandstone matrix)."
*   **As a Geologist,** I need a quick estimate of water saturation for a newly identified sand. I have log-derived porosity and resistivity, and I have estimates for Archie's parameters (a, m, n) and Rw from a nearby well. I want the Petrophysical Agent to calculate Sw.
    *   *Scenario:* "Petrophysics Agent, calculate Sw for a zone with 18% porosity and 25 ohm-m true resistivity. Use a=1, m=2, n=2, and Rw=0.05 ohm-m."

### 5.7. Economics & Risk Assessment Agent Use Cases (Illustrative - Future V1.x / V2)
*   **As an Asset Manager,** I have a production forecast and a set of capital and operating cost estimates for a new development project. I want the Economics Agent to calculate the project's NPV (at 10% discount rate) and IRR.
    *   *Scenario:* Upload `Project_Cashflow_Data.xlsx`. "Economics Agent, using the provided production forecast and cost data, calculate the NPV10 and IRR for this project."
*   **As a Project Lead,** we are considering a new exploration well. I want to discuss the main geological and operational risks with the Risk Assessment Agent to ensure we've considered key uncertainties.
    *   *Scenario:* "Risk Agent, we are planning to drill an exploration well in a new basin, targeting a sub-thrust play. What are the typical major geological risks (e.g., source, migration, reservoir presence/quality, trap/seal) and operational risks (e.g., drilling hazards, HSE) we should be evaluating in detail?"
*   **As a Reservoir Engineer,** I want to upload my well production data (CSV) to the Reservoir Agent (within my current chat) so it can analyze decline trends and estimate remaining reserves based on that data for Well X-1.
    *   *Scenario:* Upload `Well_X-1_Prod.csv`. Ask: "Using the Reservoir Agent and the production data I just uploaded, perform a hyperbolic decline curve analysis for Well X-1 and estimate its EUR based on a 5 STB/day economic limit. Plot the rate-time and rate-cumulative production data with the best-fit curve."
*   **As a Reservoir Engineer,** I want to upload a core analysis report (PDF) for Well Y-2 (into my current chat) so the Reservoir Agent can extract key properties like porosity and permeability and make them searchable for this session.
    *   *Scenario:* Upload `Well_Y-2_Core_Report.pdf`. Ask: "Reservoir Agent, what was the average matrix permeability and porosity reported in the core study for Well Y-2 from the document I just provided for the 'Sandstone A' formation?"
*   **As a Reservoir Engineer,** I want to upload a PVT report (PDF) and ask the agent to estimate oil formation volume factor (Bo) at a given pressure using a standard correlation, and then explain which correlation it used.
*   **As a Reservoir Engineer,** I want to provide basic reservoir parameters (area, thickness, porosity, Sw) and ask the agent to calculate OOIP, showing the formula used.

## 6. Functional Requirements

### 6.1. Platform Core Functionality
*   **REQ-P.1.1:** The system shall allow authenticated users to create, name, list, select, and delete Projects/Chats.
*   **REQ-P.1.2:** The system shall provide a secure mechanism for authorized users (e.g., administrators) to upload general knowledge resources (documents, datasets) to a central platform repository.
*   **REQ-P.1.3:** Within an active project/chat, the system shall allow users to upload chat-specific resources (files) that provide context solely for that specific interaction.
*   **REQ-P.1.4:** The system shall provide a clear UI mechanism for users to select the primary LLM (from a pre-configured list) to be used for the current chat session.
*   **REQ-P.1.5:** The system shall provide a clear UI mechanism for users to select a specialized AI agent or the "Multi-Agent Orchestrator" for the current chat session.
*   **REQ-P.1.6:** The system's chat interface shall allow users to input natural language queries or commands and receive streaming responses.
*   **REQ-P.1.7:** The system shall maintain and display conversation history within a project/chat, including user inputs and agent responses.
*   **REQ-P.1.8:** Uploaded general and chat-specific resources shall be securely stored and appropriately associated with their scope (platform-wide or chat-specific).
*   **REQ-P.1.9:** The system shall include basic user authentication (e.g., username/password) and authorization, including role differentiation (e.g., User, Administrator) for managing general knowledge resources.

### 6.2. Knowledge Management (LightRAG)
*   **REQ-KM.1:** The system, using LightRAG, shall support the ingestion and processing of the following file types for both general and chat-specific knowledge: PDF, TXT, DOCX, CSV, Excel. LightRAG's multimodal capabilities should be leveraged to extract text, tables, and potentially relevant information from images within these documents where applicable.
*   **REQ-KM.2:** Upon document upload, LightRAG shall automatically perform document parsing, text extraction, chunking, embedding generation (using a configurable embedding model), and indexing into a vector store.
*   **REQ-KM.3:** Agents shall be able to perform semantic search queries via LightRAG across the relevant knowledge base (chat-specific first, then general if specified or appropriate) to retrieve contextually relevant document chunks.
*   **REQ-KM.4:** Agent responses derived from information in uploaded documents shall, where possible, include citations (e.g., document name, page number/section) provided by LightRAG, visible to the user.
*   **REQ-KM.5:** Users shall be able to list and delete chat-specific documents they have uploaded. Administrators shall be able to manage (list, delete) general knowledge resources.
*   **REQ-KM.6:** LightRAG shall provide basic metadata for stored documents (e.g., filename, upload date, type).

### 6.3. Chat Interface (AG-UI, `mcp-use` for streaming)
*   **REQ-CI.1:** The chat interface shall support real-time, streaming of agent responses (character by character or token by token) to provide immediate feedback to the user, leveraging AG-UI event streams.
*   **REQ-CI.2:** The UI shall provide an intuitive mechanism for users to upload chat-specific files (e.g., drag-and-drop, file browser).
*   **REQ-CI.3:** The UI shall be capable of rendering rich content in agent responses, including formatted text (markdown), tables, and plots/images.
*   **REQ-CI.4:** The UI shall clearly distinguish between user messages and agent messages.
*   **REQ-CI.5:** The UI shall provide clear indicators of agent activity (e.g., "Agent is typing...", "Agent is using tool X...").

### 6.4. Specialized Agent Core Functionality (LangChain, LangGraph, FastMCP, `mcp-use`)
*   **REQ-A.1.1:** Each specialized agent shall be able to interpret user queries relevant to its domain using LLM capabilities managed by LangChain.
*   **REQ-A.1.2:** Agents shall primarily utilize the chat-specific resources (via LightRAG) uploaded by the user within the active project/chat to inform their responses and analyses. They may also draw upon the general knowledge base if designed to do so for broader context.
*   **REQ-A.1.3:** Agents, using LangGraph state management, shall be able to identify when a query requires performing a specialized calculation or data analysis using its internal tools (exposed via FastMCP and accessed via `mcp-use`).
*   **REQ-A.1.4:** Agents shall manage conversation history (via LangChain/LangGraph state) to maintain context throughout an interaction.
*   **REQ-A.1.5:** Agents shall be able to explain the source of their information (from uploaded chat-specific documents via LightRAG citations) or the general method/tool used for an analysis.
*   **REQ-A.1.6:** Agents shall use `mcp-use` to discover and call tools exposed by FastMCP servers, passing necessary parameters and receiving results.
*   **REQ-A.1.7:** Agent state, including conversation history, intermediate results from tool calls, and current operational context, shall be managed effectively by LangGraph.

### 6.5. Data Ingestion and Management (for chat-specific resources used by agents like Reservoir Engineering)
*   **REQ-RE.1.1:** The Reservoir Engineering Agent, through LightRAG, shall support ingestion of structured data files (CSV, Excel) uploaded as chat-specific resources, making their content accessible for analysis.
*   **REQ-RE.1.2:** The Reservoir Engineering Agent, through LightRAG, shall support ingestion of unstructured/semi-structured documents (PDF, Word, text, images with relevant data) uploaded as chat-specific resources.
*   **REQ-RE.1.3:** The system (potentially LightRAG or a pre-processing step) shall attempt to automatically identify common data patterns (e.g., headers, data types) in structured files uploaded to a chat to facilitate their use by tools.
*   **REQ-RE.1.4:** The system shall provide basic data validation suggestions upon chat-specific resource upload (e.g., "CSV file seems to be missing a 'Date' column typically used for production analysis").

### 6.6. Reservoir Engineering Agent Tooling & Analysis (FastMCP, LangGraph)
*   **REQ-RE.2.1:** The Reservoir Engineering Agent shall include, or have access via FastMCP to, tools for:
    *   Decline Curve Analysis (DCA)
    *   Material Balance (MB) Analysis (basic)
    *   Basic Volumetric Calculations
    *   Basic Pressure Data Analysis
    *   Basic Fluid Property Estimation (using correlations)
    *   Basic Well Log Analysis
    *   (Each tool will be a distinct function/module within a FastMCP server, with clearly defined inputs and outputs.)
*   **REQ-RE.2.2:** The Reservoir Engineering Agent (LangGraph) shall synthesize information from user queries, chat context (LightRAG), and analysis tool outputs (FastMCP) to provide comprehensive insights relevant to the chat context.
*   **REQ-RE.2.3:** The Reservoir Engineering Agent shall be able to flag potential anomalies or points of interest in data based on observed trends within the chat-specific data or deviations from typical patterns (as understood from general knowledge or tool logic).

### 6.7. Multi-Agent Orchestration (LangGraph)

### 6.8. Additional Specialized Agent Functional Requirements (Future V1.x / V2)

#### 6.8.1. Drilling Engineering Agent
*   **REQ-DRL.1.1 (Well Design Assistance):** The Drilling Engineering Agent shall provide suggestions for basic well design parameters (e.g., casing seat depth) based on user-provided inputs like pore pressure, fracture gradient, and relevant offset well data (if provided as context via LightRAG).
*   **REQ-DRL.1.2 (Problem Diagnosis):** The Drilling Engineering Agent shall assist in diagnosing common drilling problems (e.g., stuck pipe, lost circulation) by analyzing symptoms described by the user and relevant operational parameters, leveraging its knowledge base (potentially RAG-enhanced) and suggesting potential causes or data to verify.
*   **REQ-DRL.1.3 (Tooling):** The agent shall utilize FastMCP tools for calculations related to casing design, hydraulics (basic), and accessing drilling problem diagnostic guides.

#### 6.8.2. Production Optimization Agent
*   **REQ-PROD.1.1 (Artificial Lift Selection):** The Production Optimization Agent shall guide users in selecting appropriate artificial lift methods by evaluating well conditions, fluid properties, and production targets provided by the user, referencing best practices and equipment suitability (via RAG and internal logic).
*   **REQ-PROD.1.2 (Bottleneck Analysis):** The Production Optimization Agent shall perform basic analysis of production data and well configurations (provided by the user) to identify potential inflow or outflow bottlenecks, suggesting areas for further investigation.
*   **REQ-PROD.1.3 (Tooling):** The agent shall utilize FastMCP tools for artificial lift screening, basic nodal analysis concepts, and production data trend analysis.

#### 6.8.3. Geology & Geophysics (G&G) Agent
*   **REQ-GG.1.1 (Formation Correlation):** The G&G Agent shall assist in correlating formation tops across multiple wells using user-uploaded well log data (e.g., LAS files processed by LightRAG) and provide visual aids or suggestions for picks.
*   **REQ-GG.1.2 (Seismic Attribute Guidance):** The G&G Agent shall provide information on common seismic attributes, their geological significance, and potential application in identifying features or properties based on user queries and RAG from relevant literature.
*   **REQ-GG.1.3 (Tooling):** The agent shall utilize FastMCP tools for basic log data visualization/comparison (conceptual), accessing seismic attribute knowledge bases, and potentially simple map-based displays.

#### 6.8.4. Petrophysical Analysis Agent
*   **REQ-PETRO.1.1 (Quick-Look Interpretation):** The Petrophysical Analysis Agent shall perform quick-look interpretations of standard well log suites (provided via LightRAG from LAS files or user input) to identify potential reservoir zones, estimate lithology, and flag potential fluid contacts.
*   **REQ-PETRO.1.2 (Parameter Calculation):** The Petrophysical Analysis Agent shall calculate basic petrophysical parameters such as Vshale, porosity (e.g., from Density/Neutron), and water saturation (e.g., Archie's) using standard equations and user-provided or RAG-retrieved parameters.
*   **REQ-PETRO.1.3 (Tooling):** The agent shall utilize FastMCP tools for Vshale calculation, porosity estimation from different methods, and water saturation calculations (e.g., Archie, Simandoux).

#### 6.8.5. Economics & Risk Assessment Agent
*   **REQ-ECO.1.1 (Economic Indicator Calculation):** The Economics & Risk Assessment Agent shall calculate key economic indicators (e.g., NPV, IRR, Payout) based on user-provided cash flow data, production forecasts, and cost estimates.
*   **REQ-ECO.1.2 (Risk Factor Identification):** The Economics & Risk Assessment Agent shall assist in identifying qualitative technical and economic risk factors relevant to a petroleum project scenario described by the user, drawing from its knowledge base (RAG-enhanced).
*   **REQ-ECO.1.3 (Tooling):** The agent shall utilize FastMCP tools for NPV/IRR calculations and accessing/querying a risk factor database/checklist.
*   **REQ-P.2.1:** When the "Multi-Agent Orchestrator" is selected, the system (LangGraph) shall analyze the user's complex request, utilizing chat-specific context (LightRAG).
*   **REQ-P.2.2:** The orchestrator shall be capable of decomposing complex requests into sub-tasks suitable for individual specialized agents (e.g., a sub-task for the Reservoir Agent, another for a future Drilling Agent).
*   **REQ-P.2.3:** The orchestrator shall route sub-tasks to appropriate agents, manage the execution flow, and synthesize their outputs into a coherent final response for the user.
*   **REQ-P.2.4:** The orchestrator shall manage the flow of information and context between agents as needed to fulfill the user's request.

### 6.8. Visualization and Reporting (Behavior of agents providing outputs based on chat context)
*   **REQ-A.2.1:** Agents capable of data analysis (like the Reservoir Agent) shall generate relevant plots and visualizations (e.g., line charts, scatter plots) based on chat-specific data and tool outputs.
*   **REQ-A.2.2:** Plots shall be rendered and displayed within the AG-UI chat interface.
*   **REQ-A.2.3:** Users shall be able to export generated plots (e.g., as PNG, SVG) and summary reports (e.g., as Markdown, PDF).
*   **REQ-A.2.4:** Agents shall be able to generate concise summary reports of analyses performed on chat-specific data, presented in a readable format within the chat.

### 6.9. User Interface (Platform Level - AG-UI)
*   **REQ-P.3.1:** The system shall have an intuitive, modern, and responsive web-based user interface adhering to AG-UI principles.
*   **REQ-P.3.2:** The UI shall provide distinct areas or mechanisms for managing/uploading general knowledge resources (e.g., an admin panel or section) versus chat-specific resources (directly within the chat interface of a project).
*   **REQ-P.3.3:** The Interaction Interface shall feature a main area for displaying agent responses (supporting rich text, images, plots, tables) and a chat input window for user text input and uploading chat-specific files.
*   **REQ-P.3.4:** The UI shall provide clear feedback on the system's status (e.g., connecting, processing, agent thinking, tool in use) and any errors encountered.
*   **REQ-P.3.5:** The UI shall provide mechanisms for creating, selecting, and managing projects/chats (e.g., a sidebar listing projects).

## 7. Key System Attributes (Non-Functional Requirements)

*   **Extensibility:** The platform architecture must facilitate the straightforward addition of new specialized petroleum agents (LangGraph), new tools to FastMCP servers, new LLMs (LangChain), and updates/enhancements to LightRAG capabilities.
*   **Modularity:** Specialized agents, core platform services (auth, project management), FastMCP tool servers, and the LightRAG system should be developed as relatively independent, loosely coupled modules to promote maintainability and independent scaling.
*   **User-Friendliness:** The interface should be intuitive even for users not deeply familiar with AI. Interactions should primarily be through natural language, with clear guidance for complex operations.
*   **Responsiveness:** The system should provide timely feedback. Agent responses, especially for simple queries, should be quick. Streaming (AG-UI, `mcp-use`) should be used for longer computations or tool calls to keep the user informed.
*   **Contextual Awareness:** Agents must effectively use chat-specific resources (via LightRAG) and conversation history (LangGraph state) to provide relevant and coherent responses. The system should also be aware of available general knowledge resources.
*   **Data Security & Privacy:** User-uploaded data (both general and chat-specific) and conversation history must be handled securely, with appropriate access controls and encryption (at rest and in transit).
*   **Configurability:** Users should be able to select preferred LLMs. Administrators should have configuration options for managing general knowledge, users, and potentially agent settings.
*   **Reliability & Availability:** The platform should be reliable, with robust error handling and mechanisms to ensure high availability for critical functions.
*   **Scalability:** The architecture should be designed to scale to accommodate a growing number of users, documents, and agent interactions. Components like LightRAG and FastMCP servers should be scalable independently.
*   **Maintainability:** Code should be well-documented, follow consistent coding standards, and be covered by automated tests to facilitate easier maintenance and upgrades.

## 8. Technical Architecture Overview

*   **8.1. Frontend:**
    *   A web application (e.g., built with React, Vue, or Streamlit for rapid prototyping) that implements the client-side of the AG-UI protocol.
    *   Handles user input, displays agent responses (including rich media), manages file uploads to the backend.
*   **8.2. Backend Gateway / Agent Host:**
    *   A central backend service (e.g., Python with FastAPI or Flask).
    *   Implements the server-side of the AG-UI protocol, receiving requests from the frontend.
    *   Hosts and manages the lifecycle of LangChain/LangGraph agents.
    *   Uses `mcp-use` library to communicate with FastMCP tool servers based on agent decisions.
    *   Interfaces with the LightRAG system for document processing and retrieval requests.
    *   Manages user sessions, authentication, and authorization.
*   **8.3. Agent Core (LangChain & LangGraph):**
    *   **LangChain:** Provides fundamental building blocks for LLM interaction, prompt templates, output parsers, conversational memory management, and integration with various LLM providers.
    *   **LangGraph:** Defines the structure and flow of individual agents (e.g., Reservoir Agent) and the Multi-Agent Orchestrator as state graphs. Manages transitions between states (e.g., awaiting input, calling tool, processing RAG results, generating response).
*   **8.4. Tool Servers (FastMCP):**
    *   One or more separate Python applications, each running a FastMCP server.
    *   Example: A `ReservoirEngineeringToolsMCPServer` exposing functions for DCA, Volumetric Calculations, etc., decorated with `@mcp.tool()`.
    *   These servers are stateless or manage their own state if necessary for a specific tool.
*   **8.5. Knowledge Management System (LightRAG):**
    *   A dedicated service or set of services responsible for the RAG pipeline.
    *   Handles document ingestion API (called by Backend Gateway when users upload files).
    *   Performs parsing, chunking, embedding (using selected models like Sentence Transformers or OpenAI embeddings).
    *   Manages the vector database (e.g., FAISS, ChromaDB, Weaviate, PostgreSQL with pgvector).
    *   Exposes a semantic search API for agents to query for relevant document chunks.
    *   Manages document metadata and provides citation information.
*   **8.6. Data Stores:**
    *   **Primary Relational Database (e.g., PostgreSQL, MySQL):** Stores user accounts, project/chat metadata, conversation history (user prompts, agent final responses, key intermediate steps for auditability).
    *   **Vector Database:** Managed by or integrated with LightRAG (as mentioned above).
    *   **File Storage (e.g., S3, MinIO, local filesystem):** Stores raw uploaded documents (general and chat-specific).
*   **8.7. LLM Services:**
    *   External API calls to commercial LLMs (e.g., OpenAI, Anthropic, Google Gemini) via LangChain integrations.
    *   Potential for integration with locally hosted/open-source LLMs if they are compatible with LangChain and support tool calling (e.g., via Ollama).

## 9. Success Metrics

*   **User Adoption & Engagement:**
    *   Number of active users (daily, weekly, monthly).
    *   Average session duration.
    *   Number of projects/chats created per user.
    *   Frequency of feature usage (e.g., specific tools, RAG queries).
*   **Task Completion & Efficiency:**
    *   Task completion rates for key Reservoir Engineering use cases (e.g., successful DCA, OOIP calculation).
    *   Reduction in time spent by users on specific data analysis tasks compared to manual methods (survey-based or observational).
*   **Accuracy & Relevance:**
    *   User satisfaction ratings for agent responses and analyses (e.g., via in-app feedback).
    *   Accuracy of tool calculations (verified against benchmarks).
    *   Relevance of documents retrieved by RAG (measured by user feedback or click-through on citations).
*   **System Performance & Stability:**
    *   Average response time for queries.
    *   System uptime and availability.
    *   Error rates (application errors, tool failures).
*   **Knowledge Base Utility:**
    *   Number of documents uploaded to general and chat-specific repositories.
    *   Frequency of RAG system utilization by agents.

## 10. Future Considerations (Beyond V1)

*   **Automated LLM Fine-tuning:** Develop processes to leverage the "general knowledge resources" for fine-tuning selected open-source LLMs to improve domain specificity.
*   **Advanced RAG Techniques:** Explore and implement more advanced RAG strategies such as graph RAG (leveraging LightRAG's knowledge graph capabilities if applicable), re-ranking, and query transformation for better retrieval.
*   **Proactive Agent Suggestions:** Enable agents to proactively offer suggestions, insights, or next steps based on the ongoing conversation and context.
*   **Integration with More External Data Sources:** Develop connectors for real-time or batch data ingestion from common industry databases and platforms.
*   **Expanded Agent Ecosystem:** Develop and integrate more specialized agents for other petroleum domains, including but not limited to:
    *   Drilling Engineering Agent
    *   Production Optimization Agent
    *   Geology & Geophysics Agent
    *   Petrophysical Analysis Agent
    *   Economics & Risk Assessment Agent
*   **Advanced Visualization:** Integrate more sophisticated and interactive visualization tools beyond static plots.
*   **Multi-User Collaboration:** Implement features for multiple users to collaborate within the same project/chat in real-time.
*   **Workflow Automation:** Allow users to define and automate sequences of agent tasks or tool calls.
*   **Enhanced Security & Compliance:** Implement more granular access controls, audit trails, and features to support industry-specific compliance requirements.

