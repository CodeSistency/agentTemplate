# Agents
Source: https://docs.ag-ui.com/concepts/agents

Learn about agents in the Agent User Interaction Protocol

# Agents

Agents are the core components in the AG-UI protocol that process requests and
generate responses. They establish a standardized way for front-end applications
to communicate with AI services through a consistent interface, regardless of
the underlying implementation.

## What is an Agent?

In AG-UI, an agent is a class that:

1. Manages conversation state and message history
2. Processes incoming messages and context
3. Generates responses through an event-driven streaming interface
4. Follows a standardized protocol for communication

Agents can be implemented to connect with any AI service, including:

* Large language models (LLMs) like GPT-4 or Claude
* Custom AI systems
* Retrieval augmented generation (RAG) systems
* Multi-agent systems

## Agent Architecture

All agents in AG-UI extend the `AbstractAgent` class, which provides the
foundation for:

* State management
* Message history tracking
* Event stream processing
* Tool usage

```typescript
import { AbstractAgent } from "@ag-ui/client"

class MyAgent extends AbstractAgent {
  protected run(input: RunAgentInput): RunAgent {
    // Implementation details
  }
}
```

### Core Components

AG-UI agents have several key components:

1. **Configuration**: Agent ID, thread ID, and initial state
2. **Messages**: Conversation history with user and assistant messages
3. **State**: Structured data that persists across interactions
4. **Events**: Standardized messages for communication with clients
5. **Tools**: Functions that agents can use to interact with external systems

## Agent Types

AG-UI provides different agent implementations to suit various needs:

### AbstractAgent

The base class that all agents extend. It handles core event processing, state
management, and message history.

### HttpAgent

A concrete implementation that connects to remote AI services via HTTP:

```typescript
import { HttpAgent } from "@ag-ui/client"

const agent = new HttpAgent({
  url: "https://your-agent-endpoint.com/agent",
  headers: {
    Authorization: "Bearer your-api-key",
  },
})
```

### Custom Agents

You can create custom agents to integrate with any AI service by extending
`AbstractAgent`:

```typescript
class CustomAgent extends AbstractAgent {
  // Custom properties and methods

  protected run(input: RunAgentInput): RunAgent {
    // Implement the agent's logic
  }
}
```

## Implementing Agents

### Basic Implementation

To create a custom agent, extend the `AbstractAgent` class and implement the
required `run` method:

```typescript
import {
  AbstractAgent,
  RunAgent,
  RunAgentInput,
  EventType,
  BaseEvent,
} from "@ag-ui/client"
import { Observable } from "rxjs"

class SimpleAgent extends AbstractAgent {
  protected run(input: RunAgentInput): RunAgent {
    const { threadId, runId } = input

    return () =>
      new Observable<BaseEvent>((observer) => {
        // Emit RUN_STARTED event
        observer.next({
          type: EventType.RUN_STARTED,
          threadId,
          runId,
        })

        // Send a message
        const messageId = Date.now().toString()

        // Message start
        observer.next({
          type: EventType.TEXT_MESSAGE_START,
          messageId,
          role: "assistant",
        })

        // Message content
        observer.next({
          type: EventType.TEXT_MESSAGE_CONTENT,
          messageId,
          delta: "Hello, world!",
        })

        // Message end
        observer.next({
          type: EventType.TEXT_MESSAGE_END,
          messageId,
        })

        // Emit RUN_FINISHED event
        observer.next({
          type: EventType.RUN_FINISHED,
          threadId,
          runId,
        })

        // Complete the observable
        observer.complete()
      })
  }
}
```

## Agent Capabilities

Agents in the AG-UI protocol provide a rich set of capabilities that enable
sophisticated AI interactions:

### Interactive Communication

Agents establish bi-directional communication channels with front-end
applications through event streams. This enables:

* Real-time streaming responses character-by-character
* Immediate feedback loops between user and AI
* Progress indicators for long-running operations
* Structured data exchange in both directions

### Tool Usage

Agents can use tools to perform actions and access external resources.
Importantly, tools are defined and passed in from the front-end application to
the agent, allowing for a flexible and extensible system:

```typescript
// Tool definition
const confirmAction = {
  name: "confirmAction",
  description: "Ask the user to confirm a specific action before proceeding",
  parameters: {
    type: "object",
    properties: {
      action: {
        type: "string",
        description: "The action that needs user confirmation",
      },
      importance: {
        type: "string",
        enum: ["low", "medium", "high", "critical"],
        description: "The importance level of the action",
      },
      details: {
        type: "string",
        description: "Additional details about the action",
      },
    },
    required: ["action"],
  },
}

// Running an agent with tools from the frontend
agent.runAgent({
  tools: [confirmAction], // Frontend-defined tools passed to the agent
  // other parameters
})
```

Tools are invoked through a sequence of events:

1. `TOOL_CALL_START`: Indicates the beginning of a tool call
2. `TOOL_CALL_ARGS`: Streams the arguments for the tool call
3. `TOOL_CALL_END`: Marks the completion of the tool call

Front-end applications can then execute the tool and provide results back to the
agent. This bidirectional flow enables sophisticated human-in-the-loop workflows
where:

* The agent can request specific actions be performed
* Humans can execute those actions with appropriate judgment
* Results are fed back to the agent for continued reasoning
* The agent maintains awareness of all decisions made in the process

This mechanism is particularly powerful for implementing interfaces where AI and
humans collaborate. For example, [CopilotKit](https://docs.copilotkit.ai/)
leverages this exact pattern with their
[`useCopilotAction`](https://docs.copilotkit.ai/guides/frontend-actions) hook,
which provides a simplified way to define and handle tools in React
applications.

By keeping the AI informed about human decisions through the tool mechanism,
applications can maintain context and create more natural collaborative
experiences between users and AI assistants.

### State Management

Agents maintain a structured state that persists across interactions. This state
can be:

* Updated incrementally through `STATE_DELTA` events
* Completely refreshed with `STATE_SNAPSHOT` events
* Accessed by both the agent and front-end
* Used to store user preferences, conversation context, or application state

```typescript
// Accessing agent state
console.log(agent.state.preferences)

// State is automatically updated during agent runs
agent.runAgent().subscribe((event) => {
  if (event.type === EventType.STATE_DELTA) {
    // State has been updated
    console.log("New state:", agent.state)
  }
})
```

### Multi-Agent Collaboration

AG-UI supports agent-to-agent handoff and collaboration:

* Agents can delegate tasks to other specialized agents
* Multiple agents can work together in a coordinated workflow
* State and context can be transferred between agents
* The front-end maintains a consistent experience across agent transitions

For example, a general assistant agent might hand off to a specialized coding
agent when programming help is needed, passing along the conversation context
and specific requirements.

### Human-in-the-Loop Workflows

Agents support human intervention and assistance:

* Agents can request human input on specific decisions
* Front-ends can pause agent execution and resume it after human feedback
* Human experts can review and modify agent outputs before they're finalized
* Hybrid workflows combine AI efficiency with human judgment

This enables applications where the agent acts as a collaborative partner rather
than an autonomous system.

### Conversational Memory

Agents maintain a complete history of conversation messages:

* Past interactions inform future responses
* Message history is synchronized between client and server
* Messages can include rich content (text, structured data, references)
* The context window can be managed to focus on relevant information

```typescript
// Accessing message history
console.log(agent.messages)

// Adding a new user message
agent.messages.push({
  id: "msg_123",
  role: "user",
  content: "Can you explain that in more detail?",
})
```

### Metadata and Instrumentation

Agents can emit metadata about their internal processes:

* Reasoning steps through custom events
* Performance metrics and timing information
* Source citations and reference tracking
* Confidence scores for different response options

This allows front-ends to provide transparency into the agent's decision-making
process and help users understand how conclusions were reached.

## Using Agents

Once you've implemented or instantiated an agent, you can use it like this:

```typescript
// Create an agent instance
const agent = new HttpAgent({
  url: "https://your-agent-endpoint.com/agent",
})

// Add initial messages if needed
agent.messages = [
  {
    id: "1",
    role: "user",
    content: "Hello, how can you help me today?",
  },
]

// Run the agent
agent
  .runAgent({
    runId: "run_123",
    tools: [], // Optional tools
    context: [], // Optional context
  })
  .subscribe({
    next: (event) => {
      // Handle different event types
      switch (event.type) {
        case EventType.TEXT_MESSAGE_CONTENT:
          console.log("Content:", event.delta)
          break
        // Handle other events
      }
    },
    error: (error) => console.error("Error:", error),
    complete: () => console.log("Run complete"),
  })
```

## Agent Configuration

Agents accept configuration through the constructor:

```typescript
interface AgentConfig {
  agentId?: string // Unique identifier for the agent
  description?: string // Human-readable description
  threadId?: string // Conversation thread identifier
  initialMessages?: Message[] // Initial messages
  initialState?: State // Initial state object
}

// Using the configuration
const agent = new HttpAgent({
  agentId: "my-agent-123",
  description: "A helpful assistant",
  threadId: "thread-456",
  initialMessages: [
    { id: "1", role: "system", content: "You are a helpful assistant." },
  ],
  initialState: { preferredLanguage: "English" },
})
```

## Agent State Management

AG-UI agents maintain state across interactions:

```typescript
// Access current state
console.log(agent.state)

// Access messages
console.log(agent.messages)

// Clone an agent with its state
const clonedAgent = agent.clone()
```

## Conclusion

Agents are the foundation of the AG-UI protocol, providing a standardized way to
connect front-end applications with AI services. By implementing the
`AbstractAgent` class, you can create custom integrations with any AI service
while maintaining a consistent interface for your applications.

The event-driven architecture enables real-time, streaming interactions that are
essential for modern AI applications, and the standardized protocol ensures
compatibility across different implementations.


# Core architecture
Source: https://docs.ag-ui.com/concepts/architecture

Understand how AG-UI connects front-end applications to AI agents

Agent User Interaction Protocol (AG-UI) is built on a flexible, event-driven
architecture that enables seamless, efficient communication between front-end
applications and AI agents. This document covers the core architectural
components and concepts.

## Overview

AG-UI follows a client-server architecture that standardizes communication
between agents and applications:

```mermaid
flowchart LR
    subgraph "Frontend"
        App["Application"]
        Client["AG-UI Client"]
    end

    subgraph "Backend"
        A1["AI Agent A"]
        P["Secure Proxy"]
        A2["AI Agent B"]
        A3["AI Agent C"]
    end

    App <--> Client
    Client <-->|"AG-UI Protocol"| A1
    Client <-->|"AG-UI Protocol"| P
    P <-->|"AG-UI Protocol"| A2
    P <-->|"AG-UI Protocol"| A3

    class P mintStyle;
    classDef mintStyle fill:#E0F7E9,stroke:#66BB6A,stroke-width:2px,color:#000000;

    style App rx:5, ry:5;
    style Client rx:5, ry:5;
    style A1 rx:5, ry:5;
    style P rx:5, ry:5;
    style A2 rx:5, ry:5;
    style A3 rx:5, ry:5;
```

* **Application**: User-facing apps (i.e. chat or any AI-enabled application).
* **AG-UI Client**: Generic communication clients like `HttpAgent` or
  specialized clients for connecting to existing protocols.
* **Agents**: Backend AI agents that process requests and generate streaming
  responses.
* **Secure Proxy**: Backend services that provide additional capabilities and
  act as a secure proxy.

## Core components

### Protocol layer

AG-UI's protocol layer provides a flexible foundation for agent communication.

* **Universal compatibility**: Connect to any protocol by implementing
  `run(input: RunAgentInput) -> Observable<BaseEvent>`

The protocol's primary abstraction enables applications to run agents and
receive a stream of events:

{/* prettier-ignore */}

```typescript
// Core agent execution interface
type RunAgent = () => Observable<BaseEvent>

class MyAgent extends AbstractAgent {
  run(input: RunAgentInput): RunAgent {
    const { threadId, runId } = input
    return () =>
      from([
        { type: EventType.RUN_STARTED, threadId, runId },
        {
          type: EventType.MESSAGES_SNAPSHOT,
          messages: [
            { id: "msg_1", role: "assistant", content: "Hello, world!" }
          ],
        },
        { type: EventType.RUN_FINISHED, threadId, runId },
      ])
  }
}
```

### Standard HTTP client

AG-UI offers a standard HTTP client `HttpAgent` that can be used to connect to
any endpoint that accepts POST requests with a body of type `RunAgentInput` and
sends a stream of `BaseEvent` objects.

`HttpAgent` supports the following transports:

* **HTTP SSE (Server-Sent Events)**

  * Text-based streaming for wide compatibility
  * Easy to read and debug

* **HTTP binary protocol**
  * Highly performant and space-efficient custom transport
  * Robust binary serialization for production environments

### Message types

AG-UI defines several event categories for different aspects of agent
communication:

* **Lifecycle events**

  * `RUN_STARTED`, `RUN_FINISHED`, `RUN_ERROR`
  * `STEP_STARTED`, `STEP_FINISHED`

* **Text message events**

  * `TEXT_MESSAGE_START`, `TEXT_MESSAGE_CONTENT`, `TEXT_MESSAGE_END`

* **Tool call events**

  * `TOOL_CALL_START`, `TOOL_CALL_ARGS`, `TOOL_CALL_END`

* **State management events**

  * `STATE_SNAPSHOT`, `STATE_DELTA`, `MESSAGES_SNAPSHOT`

* **Special events**
  * `RAW`, `CUSTOM`

## Running Agents

To run an agent, you create a client instance and execute it:

```typescript
// Create an HTTP agent client
const agent = new HttpAgent({
  url: "https://your-agent-endpoint.com/agent",
  agentId: "unique-agent-id",
  threadId: "conversation-thread"
});

// Start the agent and handle events
agent.runAgent({
  tools: [...],
  context: [...]
}).subscribe({
  next: (event) => {
    // Handle different event types
    switch(event.type) {
      case EventType.TEXT_MESSAGE_CONTENT:
        // Update UI with new content
        break;
      // Handle other event types
    }
  },
  error: (error) => console.error("Agent error:", error),
  complete: () => console.log("Agent run complete")
});
```

## State Management

AG-UI provides efficient state management through specialized events:

* `STATE_SNAPSHOT`: Complete state representation at a point in time
* `STATE_DELTA`: Incremental state changes using JSON Patch format (RFC 6902)
* `MESSAGES_SNAPSHOT`: Complete conversation history

These events enable efficient client-side state management with minimal data
transfer.

## Tools and Handoff

AG-UI supports agent-to-agent handoff and tool usage through standardized
events:

* Tool definitions are passed in the `runAgent` parameters
* Tool calls are streamed as sequences of `TOOL_CALL_START` → `TOOL_CALL_ARGS` →
  `TOOL_CALL_END` events
* Agents can hand off to other agents, maintaining context continuity

## Events

All communication in AG-UI is based on typed events. Every event inherits from
`BaseEvent`:

```typescript
interface BaseEvent {
  type: EventType
  timestamp?: number
  rawEvent?: any
}
```

Events are strictly typed and validated, ensuring reliable communication between
components.


# Events
Source: https://docs.ag-ui.com/concepts/events

Understanding events in the Agent User Interaction Protocol

# Events

The Agent User Interaction Protocol uses a streaming event-based architecture.
Events are the fundamental units of communication between agents and frontends,
enabling real-time, structured interaction.

## Event Types Overview

Events in the protocol are categorized by their purpose:

| Category                | Description                             |
| ----------------------- | --------------------------------------- |
| Lifecycle Events        | Monitor the progression of agent runs   |
| Text Message Events     | Handle streaming textual content        |
| Tool Call Events        | Manage tool executions by agents        |
| State Management Events | Synchronize state between agents and UI |
| Special Events          | Support custom functionality            |

## Base Event Properties

All events share a common set of base properties:

| Property    | Description                                                      |
| ----------- | ---------------------------------------------------------------- |
| `type`      | The specific event type identifier                               |
| `timestamp` | Optional timestamp indicating when the event was created         |
| `rawEvent`  | Optional field containing the original event data if transformed |

## Lifecycle Events

These events represent the lifecycle of an agent run. A typical agent run
follows a predictable pattern: it begins with a `RunStarted` event, may contain
multiple optional `StepStarted`/`StepFinished` pairs, and concludes with either
a `RunFinished` event (success) or a `RunError` event (failure).

Lifecycle events provide crucial structure to agent runs, enabling frontends to
track progress, manage UI states appropriately, and handle errors gracefully.
They create a consistent framework for understanding when operations begin and
end, making it possible to implement features like loading indicators, progress
tracking, and error recovery mechanisms.

```mermaid
sequenceDiagram
    participant Agent
    participant Client

    Note over Agent,Client: Run begins
    Agent->>Client: RunStarted

    opt Sending steps is optional
        Note over Agent,Client: Step execution
        Agent->>Client: StepStarted
        Agent->>Client: StepFinished
    end

    Note over Agent,Client: Run completes
    alt
        Agent->>Client: RunFinished
    else
        Agent->>Client: RunError
    end
```

The `RunStarted` and either `RunFinished` or `RunError` events are mandatory,
forming the boundaries of an agent run. Step events are optional and may occur
multiple times within a run, allowing for structured, observable progress
tracking.

### RunStarted

Signals the start of an agent run.

The `RunStarted` event is the first event emitted when an agent begins
processing a request. It establishes a new execution context identified by a
unique `runId`. This event serves as a marker for frontends to initialize UI
elements such as progress indicators or loading states. It also provides crucial
identifiers that can be used to associate subsequent events with this specific
run.

| Property   | Description                   |
| ---------- | ----------------------------- |
| `threadId` | ID of the conversation thread |
| `runId`    | ID of the agent run           |

### RunFinished

Signals the successful completion of an agent run.

The `RunFinished` event indicates that an agent has successfully completed all
its work for the current run. Upon receiving this event, frontends should
finalize any UI states that were waiting on the agent's completion. This event
marks a clean termination point and indicates that no further processing will
occur in this run unless explicitly requested.

| Property   | Description                   |
| ---------- | ----------------------------- |
| `threadId` | ID of the conversation thread |
| `runId`    | ID of the agent run           |

### RunError

Signals an error during an agent run.

The `RunError` event indicates that the agent encountered an error it could not
recover from, causing the run to terminate prematurely. This event provides
information about what went wrong, allowing frontends to display appropriate
error messages and potentially offer recovery options. After a `RunError` event,
no further processing will occur in this run.

| Property  | Description         |
| --------- | ------------------- |
| `message` | Error message       |
| `code`    | Optional error code |

### StepStarted

Signals the start of a step within an agent run.

The `StepStarted` event indicates that the agent is beginning a specific subtask
or phase of its processing. Steps provide granular visibility into the agent's
progress, enabling more precise tracking and feedback in the UI. Steps are
optional but highly recommended for complex operations that benefit from being
broken down into observable stages. The `stepName` could be the name of a node
or function that is currently executing.

| Property   | Description      |
| ---------- | ---------------- |
| `stepName` | Name of the step |

### StepFinished

Signals the completion of a step within an agent run.

The `StepFinished` event indicates that the agent has completed a specific
subtask or phase. When paired with a corresponding `StepStarted` event, it
creates a bounded context for a discrete unit of work. Frontends can use these
events to update progress indicators, show completion animations, or reveal
results specific to that step. The `stepName` must match the corresponding
`StepStarted` event to properly pair the beginning and end of the step.

| Property   | Description      |
| ---------- | ---------------- |
| `stepName` | Name of the step |

## Text Message Events

These events represent the lifecycle of text messages in a conversation. Text
message events follow a streaming pattern, where content is delivered
incrementally. A message begins with a `TextMessageStart` event, followed by one
or more `TextMessageContent` events that deliver chunks of text as they become
available, and concludes with a `TextMessageEnd` event.

This streaming approach enables real-time display of message content as it's
generated, creating a more responsive user experience compared to waiting for
the entire message to be complete before showing anything.

```mermaid
sequenceDiagram
    participant Agent
    participant Client

    Note over Agent,Client: Message begins
    Agent->>Client: TextMessageStart

    loop Content streaming
        Agent->>Client: TextMessageContent
    end

    Note over Agent,Client: Message completes
    Agent->>Client: TextMessageEnd
```

The `TextMessageContent` events each contain a `delta` field with a chunk of
text. Frontends should concatenate these deltas in the order received to
construct the complete message. The `messageId` property links all related
events, allowing the frontend to associate content chunks with the correct
message.

### TextMessageStart

Signals the start of a text message.

The `TextMessageStart` event initializes a new text message in the conversation.
It establishes a unique `messageId` that will be referenced by subsequent
content chunks and the end event. This event allows frontends to prepare the UI
for an incoming message, such as creating a new message bubble with a loading
indicator. The `role` property identifies whether the message is coming from the
assistant or potentially another participant in the conversation.

| Property    | Description                                    |
| ----------- | ---------------------------------------------- |
| `messageId` | Unique identifier for the message              |
| `role`      | Role of the message sender (e.g., "assistant") |

### TextMessageContent

Represents a chunk of content in a streaming text message.

The `TextMessageContent` event delivers incremental parts of the message text as
they become available. Each event contains a small chunk of text in the `delta`
property that should be appended to previously received chunks. The streaming
nature of these events enables real-time display of content, creating a more
responsive and engaging user experience. Implementations should handle these
events efficiently to ensure smooth text rendering without visible delays or
flickering.

| Property    | Description                            |
| ----------- | -------------------------------------- |
| `messageId` | Matches the ID from `TextMessageStart` |
| `delta`     | Text content chunk (non-empty)         |

### TextMessageEnd

Signals the end of a text message.

The `TextMessageEnd` event marks the completion of a streaming text message.
After receiving this event, the frontend knows that the message is complete and
no further content will be added. This allows the UI to finalize rendering,
remove any loading indicators, and potentially trigger actions that should occur
after message completion, such as enabling reply controls or performing
automatic scrolling to ensure the full message is visible.

| Property    | Description                            |
| ----------- | -------------------------------------- |
| `messageId` | Matches the ID from `TextMessageStart` |

## Tool Call Events

These events represent the lifecycle of tool calls made by agents. Tool calls
follow a streaming pattern similar to text messages. When an agent needs to use
a tool, it emits a `ToolCallStart` event, followed by one or more `ToolCallArgs`
events that stream the arguments being passed to the tool, and concludes with a
`ToolCallEnd` event.

This streaming approach allows frontends to show tool executions in real-time,
making the agent's actions transparent and providing immediate feedback about
what tools are being invoked and with what parameters.

```mermaid
sequenceDiagram
    participant Agent
    participant Client

    Note over Agent,Client: Tool call begins
    Agent->>Client: ToolCallStart

    loop Arguments streaming
        Agent->>Client: ToolCallArgs
    end

    Note over Agent,Client: Tool call completes
    Agent->>Client: ToolCallEnd
```

The `ToolCallArgs` events each contain a `delta` field with a chunk of the
arguments. Frontends should concatenate these deltas in the order received to
construct the complete arguments object. The `toolCallId` property links all
related events, allowing the frontend to associate argument chunks with the
correct tool call.

### ToolCallStart

Signals the start of a tool call.

The `ToolCallStart` event indicates that the agent is invoking a tool to perform
a specific function. This event provides the name of the tool being called and
establishes a unique `toolCallId` that will be referenced by subsequent events
in this tool call. Frontends can use this event to display tool usage to users,
such as showing a notification that a specific operation is in progress. The
optional `parentMessageId` allows linking the tool call to a specific message in
the conversation, providing context for why the tool is being used.

| Property          | Description                         |
| ----------------- | ----------------------------------- |
| `toolCallId`      | Unique identifier for the tool call |
| `toolCallName`    | Name of the tool being called       |
| `parentMessageId` | Optional ID of the parent message   |

### ToolCallArgs

Represents a chunk of argument data for a tool call.

The `ToolCallArgs` event delivers incremental parts of the tool's arguments as
they become available. Each event contains a segment of the argument data in the
`delta` property. These deltas are often JSON fragments that, when combined,
form the complete arguments object for the tool. Streaming the arguments is
particularly valuable for complex tool calls where constructing the full
arguments may take time. Frontends can progressively reveal these arguments to
users, providing insight into exactly what parameters are being passed to tools.

| Property     | Description                         |
| ------------ | ----------------------------------- |
| `toolCallId` | Matches the ID from `ToolCallStart` |
| `delta`      | Argument data chunk                 |

### ToolCallEnd

Signals the end of a tool call.

The `ToolCallEnd` event marks the completion of a tool call. After receiving
this event, the frontend knows that all arguments have been transmitted and the
tool execution is underway or completed. This allows the UI to finalize the tool
call display and prepare for potential results. In systems where tool execution
results are returned separately, this event indicates that the agent has
finished specifying the tool and its arguments, and is now waiting for or has
received the results.

| Property     | Description                         |
| ------------ | ----------------------------------- |
| `toolCallId` | Matches the ID from `ToolCallStart` |

## State Management Events

These events are used to manage and synchronize the agent's state with the
frontend. State management in the protocol follows an efficient snapshot-delta
pattern where complete state snapshots are sent initially or infrequently, while
incremental updates (deltas) are used for ongoing changes.

This approach optimizes for both completeness and efficiency: snapshots ensure
the frontend has the full state context, while deltas minimize data transfer for
frequent updates. Together, they enable frontends to maintain an accurate
representation of agent state without unnecessary data transmission.

```mermaid
sequenceDiagram
    participant Agent
    participant Client

    Note over Agent,Client: Initial state transfer
    Agent->>Client: StateSnapshot

    Note over Agent,Client: Incremental updates
    loop State changes over time
        Agent->>Client: StateDelta
        Agent->>Client: StateDelta
    end

    Note over Agent,Client: Occasional full refresh
    Agent->>Client: StateSnapshot

    loop More incremental updates
        Agent->>Client: StateDelta
    end

    Note over Agent,Client: Message history update
    Agent->>Client: MessagesSnapshot
```

The combination of snapshots and deltas allows frontends to efficiently track
changes to agent state while ensuring consistency. Snapshots serve as
synchronization points that reset the state to a known baseline, while deltas
provide lightweight updates between snapshots.

### StateSnapshot

Provides a complete snapshot of an agent's state.

The `StateSnapshot` event delivers a comprehensive representation of the agent's
current state. This event is typically sent at the beginning of an interaction
or when synchronization is needed. It contains all state variables relevant to
the frontend, allowing it to completely rebuild its internal representation.
Frontends should replace their existing state model with the contents of this
snapshot rather than trying to merge it with previous state.

| Property   | Description             |
| ---------- | ----------------------- |
| `snapshot` | Complete state snapshot |

### StateDelta

Provides a partial update to an agent's state using JSON Patch.

The `StateDelta` event contains incremental updates to the agent's state in the
form of JSON Patch operations (as defined in RFC 6902). Each delta represents
specific changes to apply to the current state model. This approach is
bandwidth-efficient, sending only what has changed rather than the entire state.
Frontends should apply these patches in sequence to maintain an accurate state
representation. If a frontend detects inconsistencies after applying patches, it
may request a fresh `StateSnapshot`.

| Property | Description                               |
| -------- | ----------------------------------------- |
| `delta`  | Array of JSON Patch operations (RFC 6902) |

### MessagesSnapshot

Provides a snapshot of all messages in a conversation.

The `MessagesSnapshot` event delivers a complete history of messages in the
current conversation. Unlike the general state snapshot, this focuses
specifically on the conversation transcript. This event is useful for
initializing the chat history, synchronizing after connection interruptions, or
providing a comprehensive view when a user joins an ongoing conversation.
Frontends should use this to establish or refresh the conversational context
displayed to users.

| Property   | Description              |
| ---------- | ------------------------ |
| `messages` | Array of message objects |

## Special Events

Special events provide flexibility in the protocol by allowing for
system-specific functionality and integration with external systems. These
events don't follow the standard lifecycle or streaming patterns of other event
types but instead serve specialized purposes.

### Raw

Used to pass through events from external systems.

The `Raw` event acts as a container for events originating from external systems
or sources that don't natively follow the Agent UI Protocol. This event type
enables interoperability with other event-based systems by wrapping their events
in a standardized format. The enclosed event data is preserved in its original
form inside the `event` property, while the optional `source` property
identifies the system it came from. Frontends can use this information to handle
external events appropriately, either by processing them directly or by
delegating them to system-specific handlers.

| Property | Description                |
| -------- | -------------------------- |
| `event`  | Original event data        |
| `source` | Optional source identifier |

### Custom

Used for application-specific custom events.

The `Custom` event provides an extension mechanism for implementing features not
covered by the standard event types. Unlike `Raw` events which act as
passthrough containers, `Custom` events are explicitly part of the protocol but
with application-defined semantics. The `name` property identifies the specific
custom event type, while the `value` property contains the associated data. This
mechanism allows for protocol extensions without requiring formal specification
changes. Teams should document their custom events to ensure consistent
implementation across frontends and agents.

| Property | Description                     |
| -------- | ------------------------------- |
| `name`   | Name of the custom event        |
| `value`  | Value associated with the event |

## Event Flow Patterns

Events in the protocol typically follow specific patterns:

1. **Start-Content-End Pattern**: Used for streaming content (text messages,
   tool calls)

   * `Start` event initiates the stream
   * `Content` events deliver data chunks
   * `End` event signals completion

2. **Snapshot-Delta Pattern**: Used for state synchronization

   * `Snapshot` provides complete state
   * `Delta` events provide incremental updates

3. **Lifecycle Pattern**: Used for monitoring agent runs
   * `Started` events signal beginnings
   * `Finished`/`Error` events signal endings

## Implementation Considerations

When implementing event handlers:

* Events should be processed in the order they are received
* Events with the same ID (e.g., `messageId`, `toolCallId`) belong to the same
  logical stream
* Implementations should be resilient to out-of-order delivery
* Custom events should follow the established patterns for consistency


# Messages
Source: https://docs.ag-ui.com/concepts/messages

Understanding message structure and communication in AG-UI

# Messages

Messages form the backbone of communication in the AG-UI protocol. They
represent the conversation history between users and AI agents, and provide a
standardized way to exchange information regardless of the underlying AI service
being used.

## Message Structure

AG-UI messages follow a vendor-neutral format, ensuring compatibility across
different AI providers while maintaining a consistent structure. This allows
applications to switch between AI services (like OpenAI, Anthropic, or custom
models) without changing the client-side implementation.

The basic message structure includes:

```typescript
interface BaseMessage {
  id: string // Unique identifier for the message
  role: string // The role of the sender (user, assistant, system, tool)
  content?: string // Optional text content of the message
  name?: string // Optional name of the sender
}
```

## Message Types

AG-UI supports several message types to accommodate different participants in a
conversation:

### User Messages

Messages from the end user to the agent:

```typescript
interface UserMessage {
  id: string
  role: "user"
  content: string // Text input from the user
  name?: string // Optional user identifier
}
```

### Assistant Messages

Messages from the AI assistant to the user:

```typescript
interface AssistantMessage {
  id: string
  role: "assistant"
  content?: string // Text response from the assistant (optional if using tool calls)
  name?: string // Optional assistant identifier
  toolCalls?: ToolCall[] // Optional tool calls made by the assistant
}
```

### System Messages

Instructions or context provided to the agent:

```typescript
interface SystemMessage {
  id: string
  role: "system"
  content: string // Instructions or context for the agent
  name?: string // Optional identifier
}
```

### Tool Messages

Results from tool executions:

```typescript
interface ToolMessage {
  id: string
  role: "tool"
  content: string // Result from the tool execution
  toolCallId: string // ID of the tool call this message responds to
}
```

### Developer Messages

Internal messages used for development or debugging:

```typescript
interface DeveloperMessage {
  id: string
  role: "developer"
  content: string
  name?: string
}
```

## Vendor Neutrality

AG-UI messages are designed to be vendor-neutral, meaning they can be easily
mapped to and from proprietary formats used by various AI providers:

```typescript
// Example: Converting AG-UI messages to OpenAI format
const openaiMessages = agUiMessages
  .filter((msg) => ["user", "system", "assistant"].includes(msg.role))
  .map((msg) => ({
    role: msg.role as "user" | "system" | "assistant",
    content: msg.content || "",
    // Map tool calls if present
    ...(msg.role === "assistant" && msg.toolCalls
      ? {
          tool_calls: msg.toolCalls.map((tc) => ({
            id: tc.id,
            type: tc.type,
            function: {
              name: tc.function.name,
              arguments: tc.function.arguments,
            },
          })),
        }
      : {}),
  }))
```

This abstraction allows AG-UI to serve as a common interface regardless of the
underlying AI service.

## Message Synchronization

Messages can be synchronized between client and server through two primary
mechanisms:

### Complete Snapshots

The `MESSAGES_SNAPSHOT` event provides a complete view of all messages in a
conversation:

```typescript
interface MessagesSnapshotEvent {
  type: EventType.MESSAGES_SNAPSHOT
  messages: Message[] // Complete array of all messages
}
```

This is typically used:

* When initializing a conversation
* After connection interruptions
* When major state changes occur
* To ensure client-server synchronization

### Streaming Messages

For real-time interactions, new messages can be streamed as they're generated:

1. **Start a message**: Indicate a new message is being created

   ```typescript
   interface TextMessageStartEvent {
     type: EventType.TEXT_MESSAGE_START
     messageId: string
     role: string
   }
   ```

2. **Stream content**: Send content chunks as they become available

   ```typescript
   interface TextMessageContentEvent {
     type: EventType.TEXT_MESSAGE_CONTENT
     messageId: string
     delta: string // Text chunk to append
   }
   ```

3. **End a message**: Signal the message is complete
   ```typescript
   interface TextMessageEndEvent {
     type: EventType.TEXT_MESSAGE_END
     messageId: string
   }
   ```

This streaming approach provides a responsive user experience with immediate
feedback.

## Tool Integration in Messages

AG-UI messages elegantly integrate tool usage, allowing agents to perform
actions and process their results:

### Tool Calls

Tool calls are embedded within assistant messages:

```typescript
interface ToolCall {
  id: string // Unique ID for this tool call
  type: "function" // Type of tool call
  function: {
    name: string // Name of the function to call
    arguments: string // JSON-encoded string of arguments
  }
}
```

Example assistant message with tool calls:

```typescript
{
  id: "msg_123",
  role: "assistant",
  content: "I'll help you with that calculation.",
  toolCalls: [
    {
      id: "call_456",
      type: "function",
      function: {
        name: "calculate",
        arguments: '{"expression": "24 * 7"}'
      }
    }
  ]
}
```

### Tool Results

Results from tool executions are represented as tool messages:

```typescript
{
  id: "result_789",
  role: "tool",
  content: "168",
  toolCallId: "call_456" // References the original tool call
}
```

This creates a clear chain of tool usage:

1. Assistant requests a tool call
2. Tool executes and returns a result
3. Assistant can reference and respond to the result

## Streaming Tool Calls

Similar to text messages, tool calls can be streamed to provide real-time
visibility into the agent's actions:

1. **Start a tool call**:

   ```typescript
   interface ToolCallStartEvent {
     type: EventType.TOOL_CALL_START
     toolCallId: string
     toolCallName: string
     parentMessageId?: string // Optional link to parent message
   }
   ```

2. **Stream arguments**:

   ```typescript
   interface ToolCallArgsEvent {
     type: EventType.TOOL_CALL_ARGS
     toolCallId: string
     delta: string // JSON fragment to append to arguments
   }
   ```

3. **End a tool call**:
   ```typescript
   interface ToolCallEndEvent {
     type: EventType.TOOL_CALL_END
     toolCallId: string
   }
   ```

This allows frontends to show tools being invoked progressively as the agent
constructs its reasoning.

## Practical Example

Here's a complete example of a conversation with tool usage:

```typescript
// Conversation history
;[
  // User query
  {
    id: "msg_1",
    role: "user",
    content: "What's the weather in New York?",
  },

  // Assistant response with tool call
  {
    id: "msg_2",
    role: "assistant",
    content: "Let me check the weather for you.",
    toolCalls: [
      {
        id: "call_1",
        type: "function",
        function: {
          name: "get_weather",
          arguments: '{"location": "New York", "unit": "celsius"}',
        },
      },
    ],
  },

  // Tool result
  {
    id: "result_1",
    role: "tool",
    content:
      '{"temperature": 22, "condition": "Partly Cloudy", "humidity": 65}',
    toolCallId: "call_1",
  },

  // Assistant's final response using tool results
  {
    id: "msg_3",
    role: "assistant",
    content:
      "The weather in New York is partly cloudy with a temperature of 22°C and 65% humidity.",
  },
]
```

## Conclusion

The message structure in AG-UI enables sophisticated conversational AI
experiences while maintaining vendor neutrality. By standardizing how messages
are represented, synchronized, and streamed, AG-UI provides a consistent way to
implement interactive human-agent communication regardless of the underlying AI
service.

This system supports everything from simple text exchanges to complex tool-based
workflows, all while optimizing for both real-time responsiveness and efficient
data transfer.


# State Management
Source: https://docs.ag-ui.com/concepts/state

Understanding state synchronization between agents and frontends in AG-UI

# State Management

State management is a core feature of the AG-UI protocol that enables real-time
synchronization between agents and frontend applications. By providing efficient
mechanisms for sharing and updating state, AG-UI creates a foundation for
collaborative experiences where both AI agents and human users can work together
seamlessly.

## Shared State Architecture

In AG-UI, state is a structured data object that:

1. Persists across interactions with an agent
2. Can be accessed by both the agent and the frontend
3. Updates in real-time as the interaction progresses
4. Provides context for decision-making on both sides

This shared state architecture creates a bidirectional communication channel
where:

* Agents can access the application's current state to make informed decisions
* Frontends can observe and react to changes in the agent's internal state
* Both sides can modify the state, creating a collaborative workflow

## State Synchronization Methods

AG-UI provides two complementary methods for state synchronization:

### State Snapshots

The `STATE_SNAPSHOT` event delivers a complete representation of an agent's
current state:

```typescript
interface StateSnapshotEvent {
  type: EventType.STATE_SNAPSHOT
  snapshot: any // Complete state object
}
```

Snapshots are typically used:

* At the beginning of an interaction to establish the initial state
* After connection interruptions to ensure synchronization
* When major state changes occur that require a complete refresh
* To establish a new baseline for future delta updates

When a frontend receives a `STATE_SNAPSHOT` event, it should replace its
existing state model entirely with the contents of the snapshot.

### State Deltas

The `STATE_DELTA` event delivers incremental updates to the state using JSON
Patch format (RFC 6902):

```typescript
interface StateDeltaEvent {
  type: EventType.STATE_DELTA
  delta: JsonPatchOperation[] // Array of JSON Patch operations
}
```

Deltas are bandwidth-efficient, sending only what has changed rather than the
entire state. This approach is particularly valuable for:

* Frequent small updates during streaming interactions
* Large state objects where most properties remain unchanged
* High-frequency updates that would be inefficient to send as full snapshots

## JSON Patch Format

AG-UI uses the JSON Patch format (RFC 6902) for state deltas, which defines a
standardized way to express changes to a JSON document:

```typescript
interface JsonPatchOperation {
  op: "add" | "remove" | "replace" | "move" | "copy" | "test"
  path: string // JSON Pointer (RFC 6901) to the target location
  value?: any // The value to apply (for add, replace)
  from?: string // Source path (for move, copy)
}
```

Common operations include:

1. **add**: Adds a value to an object or array

   ```json
   { "op": "add", "path": "/user/preferences", "value": { "theme": "dark" } }
   ```

2. **replace**: Replaces a value

   ```json
   { "op": "replace", "path": "/conversation_state", "value": "paused" }
   ```

3. **remove**: Removes a value

   ```json
   { "op": "remove", "path": "/temporary_data" }
   ```

4. **move**: Moves a value from one location to another
   ```json
   { "op": "move", "path": "/completed_items", "from": "/pending_items/0" }
   ```

Frontends should apply these patches in sequence to maintain an accurate state
representation. If inconsistencies are detected after applying patches, the
frontend can request a fresh `STATE_SNAPSHOT`.

## State Processing in AG-UI

In the AG-UI implementation, state deltas are applied using the
`fast-json-patch` library:

```typescript
case EventType.STATE_DELTA: {
  const { delta } = event as StateDeltaEvent;

  try {
    // Apply the JSON Patch operations to the current state without mutating the original
    const result = applyPatch(state, delta, true, false);
    state = result.newDocument;
    return emitUpdate({ state });
  } catch (error: unknown) {
    console.warn(
      `Failed to apply state patch:\n` +
      `Current state: ${JSON.stringify(state, null, 2)}\n` +
      `Patch operations: ${JSON.stringify(delta, null, 2)}\n` +
      `Error: ${errorMessage}`
    );
    return emitNoUpdate();
  }
}
```

This implementation ensures that:

* Patches are applied atomically (all or none)
* The original state is not mutated during the application process
* Errors are caught and handled gracefully

## Human-in-the-Loop Collaboration

The shared state system is fundamental to human-in-the-loop workflows in AG-UI.
It enables:

1. **Real-time visibility**: Users can observe the agent's thought process and
   current status
2. **Contextual awareness**: The agent can access user actions, preferences, and
   application state
3. **Collaborative decision-making**: Both human and AI can contribute to the
   evolving state
4. **Feedback loops**: Humans can correct or guide the agent by modifying state
   properties

For example, an agent might update its state with a proposed action:

```json
{
  "proposal": {
    "action": "send_email",
    "recipient": "client@example.com",
    "content": "Draft email content..."
  }
}
```

The frontend can display this proposal to the user, who can then approve,
reject, or modify it before execution.

## CopilotKit Implementation

[CopilotKit](https://docs.copilotkit.ai), a popular framework for building AI
assistants, leverages AG-UI's state management system through its "shared state"
feature. This implementation enables bidirectional state synchronization between
agents (particularly LangGraph agents) and frontend applications.

CopilotKit's shared state system is implemented through:

```jsx
// In the frontend React application
const { state: agentState, setState: setAgentState } = useCoAgent({
  name: "agent",
  initialState: { someProperty: "initialValue" },
})
```

This hook creates a real-time connection to the agent's state, allowing:

1. Reading the agent's current state in the frontend
2. Updating the agent's state from the frontend
3. Rendering UI components based on the agent's state

On the backend, LangGraph agents can emit state updates using:

```python
# In the LangGraph agent
async def tool_node(self, state: ResearchState, config: RunnableConfig):
    # Update state with new information
    tool_state = {
        "title": new_state.get("title", ""),
        "outline": new_state.get("outline", {}),
        "sections": new_state.get("sections", []),
        # Other state properties...
    }

    # Emit updated state to frontend
    await copilotkit_emit_state(config, tool_state)

    return tool_state
```

These state updates are transmitted using AG-UI's state snapshot and delta
mechanisms, creating a seamless shared context between agent and frontend.

## Best Practices

When implementing state management in AG-UI:

1. **Use snapshots judiciously**: Full snapshots should be sent only when
   necessary to establish a baseline.
2. **Prefer deltas for incremental changes**: Small state updates should use
   deltas to minimize data transfer.
3. **Structure state thoughtfully**: Design state objects to support partial
   updates and minimize patch complexity.
4. **Handle state conflicts**: Implement strategies for resolving conflicting
   updates from agent and frontend.
5. **Include error recovery**: Provide mechanisms to resynchronize state if
   inconsistencies are detected.
6. **Consider security implications**: Avoid storing sensitive information in
   shared state.

## Conclusion

AG-UI's state management system provides a powerful foundation for building
collaborative applications where humans and AI agents work together. By
efficiently synchronizing state between frontend and backend through snapshots
and JSON Patch deltas, AG-UI enables sophisticated human-in-the-loop workflows
that combine the strengths of both human intuition and AI capabilities.

The implementation in frameworks like CopilotKit demonstrates how this shared
state approach can create collaborative experiences that are more effective than
either fully autonomous systems or traditional user interfaces.


# Tools
Source: https://docs.ag-ui.com/concepts/tools

Understanding tools and how they enable human-in-the-loop AI workflows

# Tools

Tools are a fundamental concept in the AG-UI protocol that enable AI agents to
interact with external systems and incorporate human judgment into their
workflows. By defining tools in the frontend and passing them to agents,
developers can create sophisticated human-in-the-loop experiences that combine
AI capabilities with human expertise.

## What Are Tools?

In AG-UI, tools are functions that agents can call to:

1. Request specific information
2. Perform actions in external systems
3. Ask for human input or confirmation
4. Access specialized capabilities

Tools bridge the gap between AI reasoning and real-world actions, allowing
agents to accomplish tasks that would be impossible through conversation alone.

## Tool Structure

Tools follow a consistent structure that defines their name, purpose, and
expected parameters:

```typescript
interface Tool {
  name: string // Unique identifier for the tool
  description: string // Human-readable explanation of what the tool does
  parameters: {
    // JSON Schema defining the tool's parameters
    type: "object"
    properties: {
      // Tool-specific parameters
    }
    required: string[] // Array of required parameter names
  }
}
```

The `parameters` field uses [JSON Schema](https://json-schema.org/) to define
the structure of arguments that the tool accepts. This schema is used by both
the agent (to generate valid tool calls) and the frontend (to validate and parse
tool arguments).

## Frontend-Defined Tools

A key aspect of AG-UI's tool system is that tools are defined in the frontend
and passed to the agent during execution:

```typescript
// Define tools in the frontend
const userConfirmationTool = {
  name: "confirmAction",
  description: "Ask the user to confirm a specific action before proceeding",
  parameters: {
    type: "object",
    properties: {
      action: {
        type: "string",
        description: "The action that needs user confirmation",
      },
      importance: {
        type: "string",
        enum: ["low", "medium", "high", "critical"],
        description: "The importance level of the action",
      },
    },
    required: ["action"],
  },
}

// Pass tools to the agent during execution
agent.runAgent({
  tools: [userConfirmationTool],
  // Other parameters...
})
```

This approach has several advantages:

1. **Frontend control**: The frontend determines what capabilities are available
   to the agent
2. **Dynamic capabilities**: Tools can be added or removed based on user
   permissions, context, or application state
3. **Separation of concerns**: Agents focus on reasoning while frontends handle
   tool implementation
4. **Security**: Sensitive operations are controlled by the application, not the
   agent

## Tool Call Lifecycle

When an agent needs to use a tool, it follows a standardized sequence of events:

1. **ToolCallStart**: Indicates the beginning of a tool call with a unique ID
   and tool name

   ```typescript
   {
     type: EventType.TOOL_CALL_START,
     toolCallId: "tool-123",
     toolCallName: "confirmAction",
     parentMessageId: "msg-456" // Optional reference to a message
   }
   ```

2. **ToolCallArgs**: Streams the tool arguments as they're generated

   ```typescript
   {
     type: EventType.TOOL_CALL_ARGS,
     toolCallId: "tool-123",
     delta: '{"act' // Partial JSON being streamed
   }
   ```

   ```typescript
   {
     type: EventType.TOOL_CALL_ARGS,
     toolCallId: "tool-123",
     delta: 'ion":"Depl' // More JSON being streamed
   }
   ```

   ```typescript
   {
     type: EventType.TOOL_CALL_ARGS,
     toolCallId: "tool-123",
     delta: 'oy the application to production"}' // Final JSON fragment
   }
   ```

3. **ToolCallEnd**: Marks the completion of the tool call
   ```typescript
   {
     type: EventType.TOOL_CALL_END,
     toolCallId: "tool-123"
   }
   ```

The frontend accumulates these deltas to construct the complete tool call
arguments. Once the tool call is complete, the frontend can execute the tool and
provide results back to the agent.

## Tool Results

After a tool has been executed, the result is sent back to the agent as a "tool
message":

```typescript
{
  id: "result-789",
  role: "tool",
  content: "true", // Tool result as a string
  toolCallId: "tool-123" // References the original tool call
}
```

This message becomes part of the conversation history, allowing the agent to
reference and incorporate the tool's result in subsequent responses.

## Human-in-the-Loop Workflows

The AG-UI tool system is especially powerful for implementing human-in-the-loop
workflows. By defining tools that request human input or confirmation,
developers can create AI experiences that seamlessly blend autonomous operation
with human judgment.

For example:

1. Agent needs to make an important decision
2. Agent calls the `confirmAction` tool with details about the decision
3. Frontend displays a confirmation dialog to the user
4. User provides their input
5. Frontend sends the user's decision back to the agent
6. Agent continues processing with awareness of the user's choice

This pattern enables use cases like:

* **Approval workflows**: AI suggests actions that require human approval
* **Data verification**: Humans verify or correct AI-generated data
* **Collaborative decision-making**: AI and humans jointly solve complex
  problems
* **Supervised learning**: Human feedback improves future AI decisions

## CopilotKit Integration

[CopilotKit](https://docs.copilotkit.ai/) provides a simplified way to work with
AG-UI tools in React applications through its
[`useCopilotAction`](https://docs.copilotkit.ai/guides/frontend-actions) hook:

```tsx
import { useCopilotAction } from "@copilotkit/react-core"

// Define a tool for user confirmation
useCopilotAction({
  name: "confirmAction",
  description: "Ask the user to confirm an action",
  parameters: {
    type: "object",
    properties: {
      action: {
        type: "string",
        description: "The action to confirm",
      },
    },
    required: ["action"],
  },
  handler: async ({ action }) => {
    // Show a confirmation dialog
    const confirmed = await showConfirmDialog(action)
    return confirmed ? "approved" : "rejected"
  },
})
```

This approach makes it easy to define tools that integrate with your React
components and handle the tool execution logic in a clean, declarative way.

## Tool Examples

Here are some common types of tools used in AG-UI applications:

### User Confirmation

```typescript
{
  name: "confirmAction",
  description: "Ask the user to confirm an action",
  parameters: {
    type: "object",
    properties: {
      action: {
        type: "string",
        description: "The action to confirm"
      },
      importance: {
        type: "string",
        enum: ["low", "medium", "high", "critical"],
        description: "The importance level"
      }
    },
    required: ["action"]
  }
}
```

### Data Retrieval

```typescript
{
  name: "fetchUserData",
  description: "Retrieve data about a specific user",
  parameters: {
    type: "object",
    properties: {
      userId: {
        type: "string",
        description: "ID of the user"
      },
      fields: {
        type: "array",
        items: {
          type: "string"
        },
        description: "Fields to retrieve"
      }
    },
    required: ["userId"]
  }
}
```

### User Interface Control

```typescript
{
  name: "navigateTo",
  description: "Navigate to a different page or view",
  parameters: {
    type: "object",
    properties: {
      destination: {
        type: "string",
        description: "Destination page or view"
      },
      params: {
        type: "object",
        description: "Optional parameters for the navigation"
      }
    },
    required: ["destination"]
  }
}
```

### Content Generation

```typescript
{
  name: "generateImage",
  description: "Generate an image based on a description",
  parameters: {
    type: "object",
    properties: {
      prompt: {
        type: "string",
        description: "Description of the image to generate"
      },
      style: {
        type: "string",
        description: "Visual style for the image"
      },
      dimensions: {
        type: "object",
        properties: {
          width: { type: "number" },
          height: { type: "number" }
        },
        description: "Dimensions of the image"
      }
    },
    required: ["prompt"]
  }
}
```

## Best Practices

When designing tools for AG-UI:

1. **Clear naming**: Use descriptive, action-oriented names
2. **Detailed descriptions**: Include thorough descriptions to help the agent
   understand when and how to use the tool
3. **Structured parameters**: Define precise parameter schemas with descriptive
   field names and constraints
4. **Required fields**: Only mark parameters as required if they're truly
   necessary
5. **Error handling**: Implement robust error handling in tool execution code
6. **User experience**: Design tool UIs that provide appropriate context for
   human decision-making

## Conclusion

Tools in AG-UI bridge the gap between AI reasoning and real-world actions,
enabling sophisticated workflows that combine the strengths of AI and human
intelligence. By defining tools in the frontend and passing them to agents,
developers can create interactive experiences where AI and humans collaborate
efficiently.

The tool system is particularly powerful for implementing human-in-the-loop
workflows, where AI can suggest actions but defer critical decisions to humans.
This balances automation with human judgment, creating AI experiences that are
both powerful and trustworthy.


# Contributing
Source: https://docs.ag-ui.com/development/contributing

How to participate in Agent User Interaction Protocol development

For questions and discussions, please use
[GitHub Discussions](https://github.com/orgs/ag-ui-protocol/discussions).


# Roadmap
Source: https://docs.ag-ui.com/development/roadmap

Our plans for evolving Agent User Interaction Protocol

The Agent User Interaction Protocol is rapidly evolving. This page outlines our
current thinking on key priorities and future direction.

<Note>
  The ideas presented here are not commitments—we may solve these challenges
  differently than described, or some may not materialize at all. This is also
  not an *exhaustive* list; we may incorporate work that isn't mentioned here.
</Note>

## Get Involved

We welcome community participation in shaping AG-UI's future. Visit our
[GitHub Discussions](https://github.com/orgs/ag-ui-protocol/discussions) to join
the conversation and contribute your ideas.


# What's New
Source: https://docs.ag-ui.com/development/updates

The latest updates and improvements to AG-UI

<Update label="2025-04-09" description="AG-UI repositories are now public">
  * Initial release of the Agent User Interaction Protocol
</Update>


# Integrations
Source: https://docs.ag-ui.com/integrations

A list of AG-UI integrations

This page showcases various Agent User Interaction Protocol (AG-UI) integrations
that demonstrate the protocol's capabilities and versatility.

## Frontend Integrations

* **[CopilotKit](https://copilotkit.ai)** - AI Copilots for your product.

## Agent Frameworks

* **[Mastra](https://mastra.ai)** - The TypeScript Agent Framework
* **[LangGraph](https://www.langchain.com/langgraph)** - Balance agent control
  with agency
* **[CrewAI](https://crewai.com)** - Streamline workflows across industries with
  powerful AI agents.
* **[AG2](https://ag2.ai)** - The Open-Source AgentOS

Visit our
[GitHub Discussions](https://github.com/orgs/ag-ui-protocol/discussions) to
engage with the AG-UI community.


# Introduction
Source: https://docs.ag-ui.com/introduction

Get started with the Agent User Interaction Protocol (AG-UI)

**AG-UI** standardizes how **front-end applications connect to AI agents**
through an open protocol. Think of it as a universal translator for AI-driven
systems- no matter what language an agent speaks: **AG-UI ensures fluent
communication**.

## Why AG-UI?

AG-UI helps developers build next-generation AI workflows that need **real-time
interactivity**, **live state streaming** and **human-in-the-loop
collaboration**.

AG-UI provides:

* **A straightforward approach** to integrating AI agents with the front-end
  through frameworks such as
  [CopilotKit 🪁](https://github.com/CopilotKit/CopilotKit)
* **Building blocks** for an efficient wire protocol for human⚡️agent
  communication
* **Best practices** for chat, streaming state updates, human-in-the-loop and
  shared state

## Existing Integrations

AG-UI has been integrated with several popular agent frameworks, making it easy
to adopt regardless of your preferred tooling:

* **[LangGraph](https://docs.copilotkit.ai/coagents)**: Build agent-native
  applications with shared state and human-in-the-loop workflows using
  LangGraph's powerful orchestration capabilities.
* **[CrewAI Flows](https://docs.copilotkit.ai/crewai-flows)**: Create sequential
  multi-agent workflows with well-defined stages and process control.
* **[CrewAI Crews](https://docs.copilotkit.ai/crewai-crews)**: Design
  collaborative agent teams with specialized roles and inter-agent
  communication.
* **[Mastra](/mastra)**: Leverage TypeScript for building strongly-typed agent
  implementations with enhanced developer experience.
* **[AG2](/ag2)**: Utilize the open-source AgentOS for scalable,
  production-ready agent deployments.

These integrations make it straightforward to connect your preferred agent
framework with frontend applications through the AG-UI protocol.

### Architecture

At its core, AG-UI bridges AI agents and front-end applications using a
lightweight, event-driven protocol:

```mermaid
flowchart LR
    subgraph "Frontend"
        FE["Front-end"]
    end

    subgraph "Backend"
        A1["AI Agent A"]
        P["Secure Proxy"]
        A2["AI Agent B"]
        A3["AI Agent C"]
    end

    FE <-->|"AG-UI Protocol"| A1
    FE <-->|"AG-UI Protocol"| P
    P <-->|"AG-UI Protocol"| A2
    P <-->|"AG-UI Protocol"| A3

    class P mintStyle;
    classDef mintStyle fill:#E0F7E9,stroke:#66BB6A,stroke-width:2px,color:#000000;

    %% Apply slight border radius to each node
    style FE rx:5, ry:5;
    style A1 rx:5, ry:5;
    style P rx:5, ry:5;
    style A2 rx:5, ry:5;
    style A3 rx:5, ry:5;
```

* **Front-end**: The application (chat or any AI-enabled app) that communicates
  over AG-UI
* **AI Agent A**: An agent that the front-end can connect to directly without
  going through the proxy
* **Secure Proxy**: An intermediary proxy that securely routes requests from the
  front-end to multiple AI agents
* **Agents B and C**: Agents managed by the proxy service

## Technical Overview

AG-UI is designed to be lightweight and minimally opinionated, making it easy to
integrate with a wide range of agent implementations. The protocol's flexibility
comes from its simple requirements:

1. **Event-Driven Communication**: Agents need to emit any of the 16
   standardized event types during execution, creating a stream of updates that
   clients can process.

2. **Bidirectional Interaction**: Agents accept input from users, enabling
   collaborative workflows where humans and AI work together seamlessly.

The protocol includes a built-in middleware layer that maximizes compatibility
in two key ways:

* **Flexible Event Structure**: Events don't need to match AG-UI's format
  exactly—they just need to be AG-UI-compatible. This allows existing agent
  frameworks to adapt their native event formats with minimal effort.

* **Transport Agnostic**: AG-UI doesn't mandate how events are delivered,
  supporting various transport mechanisms including Server-Sent Events (SSE),
  webhooks, WebSockets, and more. This flexibility lets developers choose the
  transport that best fits their architecture.

This pragmatic approach makes AG-UI easy to adopt without requiring major
changes to existing agent implementations or frontend applications.

## Comparison with other protocols

AG-UI focuses explicitly and specifically on the agent-user interactivity layer.
It does not compete with protocols such as A2A (Agent-to-Agent protocol) and MCP
(Model Context Protocol).

For example, the same agent may communicate with another agent via A2A while
communicating with the user via AG-UI, and while calling tools provided by an
MCP server.

These protocols serve complementary purposes in the agent ecosystem:

* **AG-UI**: Handles human-in-the-loop interaction and streaming UI updates
* **A2A**: Facilitates agent-to-agent communication and collaboration
* **MCP**: Standardizes tool calls and context handling across different models

## Quick Start

Choose the path that fits your needs:

<CardGroup cols={2}>
  <Card title="AG-UI Middleware Connectors" icon="bolt" href="/quickstart/middleware" color="#3B82F6" iconType="solid">
    Connect AG-UI with existing protocols, in process agents or custom solutions
    **using TypeScript**
  </Card>

  <Card title="AG-UI Compatible Servers" icon="wrench" href="/quickstart/server" color="#3B82F6" iconType="solid">
    Implement AG-UI compatible servers **using Python or TypeScript**
  </Card>
</CardGroup>

## Resources

Explore guides, tools, and integrations to help you build, optimize, and extend
your AG-UI implementation. These resources cover everything from practical
development workflows to debugging techniques.

<CardGroup cols={2}>
  <Card title="Explore Integrations" icon="cubes" iconType="light" color="#3B82F6" href="/integrations">
    Discover ready-to-use AG-UI integrations across popular agent frameworks and
    platforms
  </Card>

  <Card title="Developing with Cursor" icon="rocket" iconType="light" color="#3B82F6" href="/tutorials/cursor">
    Use Cursor to build AG-UI implementations faster
  </Card>

  <Card title="Troubleshooting AG-UI" icon="bug" iconType="light" color="#3B82F6" href="/tutorials/debugging">
    Fix common issues when working with AG-UI servers and clients
  </Card>
</CardGroup>

## Explore AG-UI

Dive deeper into AG-UI's core concepts and capabilities:

<CardGroup cols={2}>
  <Card title="Core architecture" icon="sitemap" iconType="light" color="#3B82F6" href="/docs/concepts/architecture">
    Understand how AG-UI connects agents, protocols, and front-ends
  </Card>

  <Card title="Transports" icon="network-wired" iconType="light" color="#3B82F6" href="/docs/concepts/transports">
    Learn about AG-UI's communication mechanism
  </Card>
</CardGroup>

## Contributing

Want to contribute? Check out our
[Contributing Guide](/development/contributing) to learn how you can help
improve AG-UI.

## Support and Feedback

Here's how to get help or provide feedback:

* For bug reports and feature requests related to the AG-UI specification, SDKs,
  or documentation (open source), please
  [create a GitHub issue](https://github.com/ag-ui-protocol)
* For discussions or Q\&A about the AG-UI specification, use the
  [specification discussions](https://github.com/ag-ui-protocol/specification/discussions)
* For discussions or Q\&A about other AG-UI open source components, use the
  [organization discussions](https://github.com/orgs/ag-ui-protocol/discussions)


# AG-UI Middleware Connectors
Source: https://docs.ag-ui.com/quickstart/middleware

Connect AG-UI with existing protocols, in process agents or custom solutions using TypeScript

# Getting Started with AG-UI

AG-UI provides a concise, event-driven protocol that lets any agent stream rich,
structured output to any client. In this quick-start guide, we'll walk through:

1. Scaffolding a new AG-UI integration that wraps **OpenAI's GPT-4o** model
2. Registering your integration with the **dojo**, our local web playground
3. Streaming responses from OpenAI through AG-UI's unified interface

## Prerequisites

Before we begin, make sure you have:

* [Node.js](https://nodejs.org/) **v16 or later**
* An **OpenAI API key**

### 1. Provide your OpenAI API key

First, let's set up your API key:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your-api-key-here
```

### 2. Install build utilities

Install the following tools:

```bash
brew install protobuf
```

```bash
npm i turbo
```

```bash
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

## Step 1 – Scaffold your integration

Start by cloning the repo and navigating to the TypeScript SDK:

```bash
git clone git@github.com:ag-ui-protocol/ag-ui.git
cd ag-ui/typescript-sdk
```

Copy the middleware-starter template to create your OpenAI integration:

```bash
cp -r integrations/middleware-starter integrations/openai
```

### Update metadata

Open `integrations/openai/package.json` and update the fields to match your new
folder:

```json
{
  "name": "@ag-ui/openai",
  "author": "Your Name <your-email@example.com>",
  "version": "0.0.1",

  ... rest of package.json
}
```

Next, update the class name inside `integrations/openai/src/index.ts`:

```ts
// change the name to OpenAIAgent
export class OpenAIAgent extends AbstractAgent {}
```

Finally, introduce your integration to the dojo by adding it to
`apps/dojo/src/menu.ts`:

```ts
// ...
export const menuIntegrations: MenuIntegrationConfig[] = [
  // ...

  configureIntegration({
    id: "openai",
    name: "OpenAI",
    features: ["agentic_chat"],
  }),
]
```

And `apps/dojo/src/agents.ts`:

```ts
// ...
import { OpenAIAgent } from "@ag-ui/openai"

export const agentsIntegrations: AgentIntegrationConfig[] = [
  // ...

  {
    id: "openai",
    agents: async () => {
      return {
        agentic_chat: new OpenAIAgent(),
      }
    },
  },
]
```

## Step 2 – Start the dojo

Now let's see your work in action:

```bash
# Install dependencies
pnpm install

# Compile the project and run the dojo
turbo run dev
```

Head over to [http://localhost:3000](http://localhost:3000) and choose
**OpenAI** from the drop-down. You'll see the stub agent replies with **Hello
world!** for now.

Here's what's happening with that stub agent:

```ts
// integrations/openai/src/index.ts
import {
  AbstractAgent,
  BaseEvent,
  EventType,
  RunAgentInput,
} from "@ag-ui/client"
import { Observable } from "rxjs"

export class OpenAIAgent extends AbstractAgent {
  protected run(input: RunAgentInput): Observable<BaseEvent> {
    const messageId = Date.now().toString()
    return new Observable<BaseEvent>((observer) => {
      observer.next({
        type: EventType.RUN_STARTED,
        threadId: input.threadId,
        runId: input.runId,
      } as any)

      observer.next({
        type: EventType.TEXT_MESSAGE_START,
        messageId,
      } as any)

      observer.next({
        type: EventType.TEXT_MESSAGE_CONTENT,
        messageId,
        delta: "Hello world!",
      } as any)

      observer.next({
        type: EventType.TEXT_MESSAGE_END,
        messageId,
      } as any)

      observer.next({
        type: EventType.RUN_FINISHED,
        threadId: input.threadId,
        runId: input.runId,
      } as any)

      observer.complete()
    })
  }
}
```

## Step 3 – Bridge OpenAI with AG-UI

Let's transform our stub into a real agent that streams completions from OpenAI.

### Install the OpenAI SDK

First, we need the OpenAI SDK:

```bash
cd integrations/openai
pnpm install openai
```

### AG-UI recap

An AG-UI agent extends `AbstractAgent` and emits a sequence of events to signal:

* lifecycle events (`RUN_STARTED`, `RUN_FINISHED`, `RUN_ERROR`)
* content events (`TEXT_MESSAGE_*`, `TOOL_CALL_*`, and more)

### Implement the streaming agent

Now we'll transform our stub agent into a real OpenAI integration. The key
difference is that instead of sending a hardcoded "Hello world!" message, we'll
connect to OpenAI's API and stream the response back through AG-UI events.

The implementation follows the same event flow as our stub, but we'll add the
OpenAI client initialization in the constructor and replace our mock response
with actual API calls. We'll also handle tool calls if they're present in the
response, making our agent fully capable of using functions when needed.

```typescript
// integrations/openai/src/index.ts
import {
  AbstractAgent,
  RunAgentInput,
  EventType,
  BaseEvent,
} from "@ag-ui/client"
import { Observable } from "rxjs"

import { OpenAI } from "openai"

export class OpenAIAgent extends AbstractAgent {
  private openai: OpenAI

  constructor(openai?: OpenAI) {
    super()
    // Initialize OpenAI client - uses OPENAI_API_KEY from environment if not provided
    this.openai = openai ?? new OpenAI()
  }

  protected run(input: RunAgentInput): Observable<BaseEvent> {
    return new Observable<BaseEvent>((observer) => {
      // Same as before - emit RUN_STARTED to begin
      observer.next({
        type: EventType.RUN_STARTED,
        threadId: input.threadId,
        runId: input.runId,
      } as any)

      // NEW: Instead of hardcoded response, call OpenAI's API
      this.openai.chat.completions
        .create({
          model: "gpt-4o",
          stream: true, // Enable streaming for real-time responses
          // Convert AG-UI tools format to OpenAI's expected format
          tools: input.tools.map((tool) => ({
            type: "function",
            function: {
              name: tool.name,
              description: tool.description,
              parameters: tool.parameters,
            },
          })),
          // Transform AG-UI messages to OpenAI's message format
          messages: input.messages.map((message) => ({
            role: message.role as any,
            content: message.content ?? "",
            // Include tool calls if this is an assistant message with tools
            ...(message.role === "assistant" && message.toolCalls
              ? {
                  tool_calls: message.toolCalls,
                }
              : {}),
            // Include tool call ID if this is a tool result message
            ...(message.role === "tool"
              ? { tool_call_id: message.toolCallId }
              : {}),
          })),
        })
        .then(async (response) => {
          const messageId = Date.now().toString()

          // NEW: Stream each chunk from OpenAI's response
          for await (const chunk of response) {
            // Handle text content chunks
            if (chunk.choices[0].delta.content) {
              observer.next({
                type: EventType.TEXT_MESSAGE_CHUNK, // Chunk events open and close messages automatically
                messageId,
                delta: chunk.choices[0].delta.content,
              } as any)
            }
            // Handle tool call chunks (when the model wants to use a function)
            else if (chunk.choices[0].delta.tool_calls) {
              let toolCall = chunk.choices[0].delta.tool_calls[0]

              observer.next({
                type: EventType.TOOL_CALL_CHUNK,
                toolCallId: toolCall.id,
                toolCallName: toolCall.function?.name,
                parentMessageId: messageId,
                delta: toolCall.function?.arguments,
              } as any)
            }
          }

          // Same as before - emit RUN_FINISHED when complete
          observer.next({
            type: EventType.RUN_FINISHED,
            threadId: input.threadId,
            runId: input.runId,
          } as any)

          observer.complete()
        })
        // NEW: Handle errors from the API
        .catch((error) => {
          observer.next({
            type: EventType.RUN_ERROR,
            message: error.message,
          } as any)

          observer.error(error)
        })
    })
  }
}
```

### What happens under the hood?

Let's break down what your agent is doing:

1. **Setup** – We create an OpenAI client and emit `RUN_STARTED`
2. **Request** – We send the user's messages to `chat.completions` with
   `stream: true`
3. **Streaming** – We forward each chunk as either `TEXT_MESSAGE_CHUNK` or
   `TOOL_CALL_CHUNK`
4. **Finish** – We emit `RUN_FINISHED` (or `RUN_ERROR` if something goes wrong)
   and complete the observable

## Step 4 – Chat with your agent

Reload the dojo page and start typing. You'll see GPT-4o streaming its answer in
real-time, word by word.

## Bridging AG-UI to any protocol

The pattern you just implemented—translate inputs, forward streaming chunks,
emit AG-UI events—works for virtually any backend:

* REST or GraphQL APIs
* WebSockets
* IoT protocols such as MQTT

## Connect your agent to a frontend

Tools like [CopilotKit](https://docs.copilotkit.ai) already understand AG-UI and
provide plug-and-play React components. Point them at your agent endpoint and
you get a full-featured chat UI out of the box.

## Share your integration

Did you build a custom adapter that others could reuse? We welcome community
contributions!

1. Fork the [AG-UI repository](https://github.com/ag-ui-protocol/ag-ui)
2. Add your package under `integrations/` with docs and tests
3. Open a pull request describing your use-case and design decisions

If you have questions, need feedback, or want to validate an idea first, start a
thread in the GitHub Discussions board:
[AG-UI GitHub Discussions board](https://github.com/orgs/ag-ui-protocol/discussions).

Your integration might ship in the next release and help the entire AG-UI
ecosystem grow.

## Conclusion

You now have a fully-functional AG-UI adapter for OpenAI and a local playground
to test it. From here you can:

* Add tool calls to enhance your agent
* Publish your integration to npm
* Bridge AG-UI to any other model or service

Happy building!


# AG-UI Compatible Servers
Source: https://docs.ag-ui.com/quickstart/server

Implement AG-UI compatible servers

In this tutorial, you'll learn how to build an HTTP endpoint that is compatible
with the [AG-UI protocol](https://github.com/ag-ui-protocol).

<Tabs>
  <Tab title="Python">
    ## Prerequisites

    Make sure to have [Python](https://www.python.org/downloads/) and
    [Poetry](https://python-poetry.org/docs/#installation) installed.

    ## Setup a New Project with Poetry

    First, let's create a new project and set up Poetry for dependency management:

    ```bash
    poetry new my-endpoint --python=">=3.12,<4.0" && cd my-endpoint
    ```

    ## Install Dependencies

    Now, let's install the necessary packages:

    ```bash
    poetry add ag-ui-protocol openai fastapi uvicorn
    ```

    ## Create a Basic Endpoint with FastAPI

    Create a new file called `my_endpoint/main.py` with the following code:

    ```python
    from fastapi import FastAPI, Request
    import json
    from ag_ui.core.types import RunAgentInput

    app = FastAPI(title="AG-UI Endpoint")

    @app.post("/awp")
    async def my_endpoint():
        return { "message": "Hello World" }

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    ```

    ## Run and Test Your Endpoint

    Start the server with:

    ```bash
    poetry run uvicorn my_endpoint.main:app --reload
    ```

    In another terminal, test your endpoint is running using curl:

    ```bash
    curl -X POST http://localhost:8000/awp
    ```

    You should see the following response:

    ```json
    { "message": "Hello World" }
    ```

    ## Parsing AG-UI Input

    Next let's update our endpoint to properly parse the incoming AG-UI request
    using the `RunAgentInput` Pydantic model:

    ```python
    from fastapi import FastAPI, Request, HTTPException
    from ag_ui.core import RunAgentInput, Message

    app = FastAPI(title="AG-UI Endpoint")

    @app.post("/awp")
    async def my_endpoint(input_data: RunAgentInput):
        thread_id = input_data.thread_id

        return { "message": "Hello World from " + thread_id }
    ```

    FastAPI automatically validates the incoming request against the RunAgentInput
    schema. If the request doesn't match the expected format, it will return a 422
    Validation Error with details about what went wrong.

    ## Add Event Streaming

    AG-UI supports streaming events using Server-Sent Events (SSE). Let's modify our
    `/awp` endpoint to stream events back to the client:

    ```python
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.responses import StreamingResponse
    from ag_ui.core import RunAgentInput, Message, EventType, RunStartedEvent, RunFinishedEvent
    from ag_ui.encoder import EventEncoder

    app = FastAPI(title="AG-UI Endpoint")

    @app.post("/awp")
    async def my_endpoint(input_data: RunAgentInput):
        async def event_generator():
            # Create an event encoder to properly format SSE events
            encoder = EventEncoder()

            # Send run started event
            yield encoder.encode(
              RunStartedEvent(
                type=EventType.RUN_STARTED,
                thread_id=input_data.thread_id,
                run_id=input_data.run_id
              )
            )

            # Send run finished event
            yield encoder.encode(
              RunFinishedEvent(
                type=EventType.RUN_FINISHED,
                thread_id=input_data.thread_id,
                run_id=input_data.run_id
              )
            )

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream"
        )

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    ```

    Awesome! We are already sending `RunStartedEvent` and `RunFinishedEvent` events,
    which gives us a basic AG-UI compliant endpoint. Now let's make it do something
    useful.

    ## Implementing Basic Chat

    Let's enhance our endpoint to call OpenAI's API and stream the responses back as
    AG-UI events:

    ```python
    from fastapi import FastAPI, Request
    from fastapi.responses import StreamingResponse
    from ag_ui.core import (
      RunAgentInput,
      Message,
      EventType,
      RunStartedEvent,
      RunFinishedEvent,
      TextMessageStartEvent,
      TextMessageContentEvent,
      TextMessageEndEvent
    )
    from ag_ui.encoder import EventEncoder
    import uuid
    from openai import OpenAI

    app = FastAPI(title="AG-UI Endpoint")

    @app.post("/awp")
    async def my_endpoint(input_data: RunAgentInput):
        async def event_generator():
            # Create an event encoder to properly format SSE events
            encoder = EventEncoder()

            # Send run started event
            yield encoder.encode(
              RunStartedEvent(
                type=EventType.RUN_STARTED,
                thread_id=input_data.thread_id,
                run_id=input_data.run_id
              )
            )

            # Initialize OpenAI client
            client = OpenAI()

            # Generate a message ID for the assistant's response
            message_id = uuid.uuid4()

            # Send text message start event
            yield encoder.encode(
                TextMessageStartEvent(
                    type=EventType.TEXT_MESSAGE_START,
                    message_id=message_id,
                    role="assistant"
                )
            )

            # Create a streaming completion request
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=openai_messages,
                stream=True
            )

            # Process the streaming response and send content events
            for chunk in stream:
                if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    yield encoder.encode(
                        TextMessageContentEvent(
                            type=EventType.TEXT_MESSAGE_CONTENT,
                            message_id=message_id,
                            delta=content
                        )
                    )

            # Send text message end event
            yield encoder.encode(
                TextMessageEndEvent(
                    type=EventType.TEXT_MESSAGE_END,
                    message_id=message_id
                )
            )

            # Send run finished event
            yield encoder.encode(
              RunFinishedEvent(
                type=EventType.RUN_FINISHED,
                thread_id=input_data.thread_id,
                run_id=input_data.run_id
              )
            )

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream"
        )

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    ```

    You'll need to set your OpenAI API key as an environment variable and then
    restart the server:

    ```bash
    export OPENAI_API_KEY=your-api-key
    poetry run uvicorn my_endpoint.main:app --reload
    ```

    This implementation creates a fully functional AG-UI endpoint that processes
    messages and streams back the responses in real-time.
  </Tab>

  <Tab title="Node">
    ## Prerequisites

    Make sure to have [Node.js](https://nodejs.org/) (v16 or later) and
    [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/) installed.

    ## Setup a New Project

    First, let's create a new project and set up npm with TypeScript:

    ```bash
    mkdir awp-endpoint && cd awp-endpoint
    npm init -y
    npm install typescript ts-node @types/node @types/express --save-dev
    npx tsc --init
    ```

    ## Install Dependencies

    Install the necessary packages:

    ```bash
    npm install express openai @ag-ui/core @ag-ui/encoder uuid
    npm install @types/uuid --save-dev
    ```

    ## Create a Basic Endpoint with Express

    Create a new file called `src/server.ts` with the following code:

    ```typescript
    import express from "express"
    import { Request, Response } from "express"

    const app = express()

    app.use(express.json())

    app.post("/awp", (req: Request, res: Response) => {
      res.json({ message: "Hello World" })
    })

    app.listen(8000, () => {
      console.log("Server running on http://localhost:8000")
    })
    ```

    ## Run and Test Your Endpoint

    Start the server with:

    ```bash
    npx ts-node src/server.ts
    ```

    In another terminal, test your endpoint is running using curl:

    ```bash
    curl -X POST http://localhost:8000/awp
    ```

    You should see the following response:

    ```json
    { "message": "Hello World" }
    ```

    ## Parsing AG-UI Input

    Next let's update our endpoint to properly parse the incoming AG-UI request
    using the `RunAgentInput` schema:

    ```typescript
    import express, { Request, Response } from "express"
    import { RunAgentInputSchema, RunAgentInput } from "@ag-ui/core"

    const app = express()

    app.use(express.json())

    app.post("/awp", (req: Request, res: Response) => {
      try {
        // Parse and validate the request body
        const input: RunAgentInput = RunAgentInputSchema.parse(req.body)
        res.json({ message: `Hello World from ${input.threadId}` })
      } catch (error) {
        res.status(422).json({ error: (error as Error).message })
      }
    })

    app.listen(8000, () => {
      console.log("Server running on http://localhost:8000")
    })
    ```

    Express with zod validation ensures the incoming request conforms to the AG-UI
    protocol format. If the request doesn't match the expected format, it will
    return a 422 Validation Error with details about what went wrong.

    ## Add Event Streaming

    AG-UI supports streaming events using Server-Sent Events (SSE). Let's modify our
    `/awp` endpoint to stream events back to the client:

    ```typescript
    import express, { Request, Response } from "express"
    import { RunAgentInputSchema, RunAgentInput, EventType } from "@ag-ui/core"
    import { EventEncoder } from "@ag-ui/encoder"

    const app = express()

    app.use(express.json())

    app.post("/awp", async (req: Request, res: Response) => {
      try {
        // Parse and validate the request body
        const input: RunAgentInput = RunAgentInputSchema.parse(req.body)

        // Set up SSE headers
        res.setHeader("Content-Type", "text/event-stream")
        res.setHeader("Cache-Control", "no-cache")
        res.setHeader("Connection", "keep-alive")

        // Create an event encoder
        const encoder = new EventEncoder()

        // Send run started event
        const runStarted = {
          type: EventType.RUN_STARTED,
          threadId: input.threadId,
          runId: input.runId,
        }
        res.write(encoder.encode(runStarted))

        // Send run finished event
        const runFinished = {
          type: EventType.RUN_FINISHED,
          threadId: input.threadId,
          runId: input.runId,
        }
        res.write(encoder.encode(runFinished))

        // End the response
        res.end()
      } catch (error) {
        res.status(422).json({ error: (error as Error).message })
      }
    })

    app.listen(8000, () => {
      console.log("Server running on http://localhost:8000")
    })
    ```

    ## Implementing Basic Chat

    Let's enhance our endpoint to call OpenAI's API and stream the responses back as
    AG-UI events:

    ```typescript
    import express, { Request, Response } from "express"
    import {
      RunAgentInputSchema,
      RunAgentInput,
      EventType,
      Message,
    } from "@ag-ui/core"
    import { EventEncoder } from "@ag-ui/encoder"
    import { OpenAI } from "openai"
    import { v4 as uuidv4 } from "uuid"

    const app = express()

    app.use(express.json())

    app.post("/awp", async (req: Request, res: Response) => {
      try {
        // Parse and validate the request body
        const input: RunAgentInput = RunAgentInputSchema.parse(req.body)

        // Set up SSE headers
        res.setHeader("Content-Type", "text/event-stream")
        res.setHeader("Cache-Control", "no-cache")
        res.setHeader("Connection", "keep-alive")

        // Create an event encoder
        const encoder = new EventEncoder()

        // Send run started event
        const runStarted = {
          type: EventType.RUN_STARTED,
          threadId: input.threadId,
          runId: input.runId,
        }
        res.write(encoder.encode(runStarted))

        // Initialize OpenAI client
        const client = new OpenAI()

        // Convert AG-UI messages to OpenAI messages format
        const openaiMessages = input.messages
          .filter((msg: Message) =>
            ["user", "system", "assistant"].includes(msg.role)
          )
          .map((msg: Message) => ({
            role: msg.role as "user" | "system" | "assistant",
            content: msg.content || "",
          }))

        // Generate a message ID for the assistant's response
        const messageId = uuidv4()

        // Send text message start event
        const textMessageStart = {
          type: EventType.TEXT_MESSAGE_START,
          messageId,
          role: "assistant",
        }
        res.write(encoder.encode(textMessageStart))

        // Create a streaming completion request
        const stream = await client.chat.completions.create({
          model: "gpt-3.5-turbo",
          messages: openaiMessages,
          stream: true,
        })

        // Process the streaming response and send content events
        for await (const chunk of stream) {
          if (chunk.choices[0]?.delta?.content) {
            const content = chunk.choices[0].delta.content
            const textMessageContent = {
              type: EventType.TEXT_MESSAGE_CONTENT,
              messageId,
              delta: content,
            }
            res.write(encoder.encode(textMessageContent))
          }
        }

        // Send text message end event
        const textMessageEnd = {
          type: EventType.TEXT_MESSAGE_END,
          messageId,
        }
        res.write(encoder.encode(textMessageEnd))

        // Send run finished event
        const runFinished = {
          type: EventType.RUN_FINISHED,
          threadId: input.threadId,
          runId: input.runId,
        }
        res.write(encoder.encode(runFinished))

        // End the response
        res.end()
      } catch (error) {
        res.status(422).json({ error: (error as Error).message })
      }
    })

    app.listen(8000, () => {
      console.log("Server running on http://localhost:8000")
    })
    ```

    You'll need to set your OpenAI API key as an environment variable and then start
    the server:

    ```bash
    export OPENAI_API_KEY=your-api-key
    npx ts-node src/server.ts
    ```

    This implementation creates a fully functional AG-UI endpoint that processes
    messages and streams back the responses in real-time.
  </Tab>
</Tabs>

## Connect Your Agent to a Frontend

Now that you've built your AG-UI compatible agent, it's ready to be connected to
any frontend that supports the AG-UI protocol. One such frontend is
[CopilotKit](https://docs.copilotkit.ai), which provides a rich set of UI
components designed to work seamlessly with AG-UI agents.

To connect your agent to CopilotKit:

1. Follow the [CopilotKit documentation](https://docs.copilotkit.ai) to set up
   your frontend
2. Configure CopilotKit to connect to your agent using the AG-UI protocol
3. Enjoy a fully functioning chat UI with streaming responses!

With this setup, you can focus on building powerful agent capabilities while
leveraging existing UI components that understand the AG-UI protocol,
significantly reducing development time and effort.


# Overview
Source: https://docs.ag-ui.com/sdk/js/client/overview

Client package overview

# @ag-ui/client

The Agent User Interaction Protocol Client SDK provides agent connectivity
options for AI systems. This package builds on the core types and events to
deliver flexible connection methods to agent implementations.

```bash
npm install @ag-ui/client
```

## AbstractAgent

`AbstractAgent` is the base agent class for implementing custom agent
connectivity. Extending this class and implementing `run()` lets you bridge your
own service or agent implementation to AG-UI.

* [Configuration](/sdk/js/client/abstract-agent#configuration) - Setup with
  agent ID, messages, and state
* [Core Methods](/sdk/js/client/abstract-agent#core-methods) - Run, abort, and
  clone functionality
* [Protected Methods](/sdk/js/client/abstract-agent#protected-methods) -
  Extensible hooks for custom implementations
* [Properties](/sdk/js/client/abstract-agent#properties) - State and message
  tracking

<Card title="AbstractAgent Reference" icon="cube" href="/sdk/js/client/abstract-agent" color="#3B82F6" iconType="solid">
  Base class for creating custom agent connections
</Card>

## HttpAgent

Concrete implementation for HTTP-based agent connectivity:

* [Configuration](/sdk/js/client/http-agent#configuration) - URL and header
  setup
* [Methods](/sdk/js/client/http-agent#methods) - HTTP-specific execution and
  cancellation
* [Protected Methods](/sdk/js/client/http-agent#protected-methods) -
  Customizable HTTP request handling
* [Properties](/sdk/js/client/http-agent#properties) - Connection management

<Card title="HttpAgent Reference" icon="cube" href="/sdk/js/client/http-agent" color="#3B82F6" iconType="solid">
  Ready-to-use HTTP implementation for agent connectivity, using a highly
  efficient event encoding format
</Card>


# Events
Source: https://docs.ag-ui.com/sdk/js/core/events

Documentation for the events used in the Agent User Interaction Protocol SDK

# Events

The Agent User Interaction Protocol SDK uses a streaming event-based
architecture. Events are the fundamental units of communication between agents
and the frontend. This section documents the event types and their properties.

## EventType Enum

The `EventType` enum defines all possible event types in the system:

```typescript
enum EventType {
  TEXT_MESSAGE_START = "TEXT_MESSAGE_START",
  TEXT_MESSAGE_CONTENT = "TEXT_MESSAGE_CONTENT",
  TEXT_MESSAGE_END = "TEXT_MESSAGE_END",
  TOOL_CALL_START = "TOOL_CALL_START",
  TOOL_CALL_ARGS = "TOOL_CALL_ARGS",
  TOOL_CALL_END = "TOOL_CALL_END",
  STATE_SNAPSHOT = "STATE_SNAPSHOT",
  STATE_DELTA = "STATE_DELTA",
  MESSAGES_SNAPSHOT = "MESSAGES_SNAPSHOT",
  RAW = "RAW",
  CUSTOM = "CUSTOM",
  RUN_STARTED = "RUN_STARTED",
  RUN_FINISHED = "RUN_FINISHED",
  RUN_ERROR = "RUN_ERROR",
  STEP_STARTED = "STEP_STARTED",
  STEP_FINISHED = "STEP_FINISHED",
}
```

## BaseEvent

All events inherit from the `BaseEvent` type, which provides common properties
shared across all event types.

```typescript
type BaseEvent = {
  type: EventType // Discriminator field
  timestamp?: number
  rawEvent?: any
}
```

| Property    | Type                | Description                                           |
| ----------- | ------------------- | ----------------------------------------------------- |
| `type`      | `EventType`         | The type of event (discriminator field for the union) |
| `timestamp` | `number` (optional) | Timestamp when the event was created                  |
| `rawEvent`  | `any` (optional)    | Original event data if this event was transformed     |

## Lifecycle Events

These events represent the lifecycle of an agent run.

### RunStartedEvent

Signals the start of an agent run.

```typescript
type RunStartedEvent = BaseEvent & {
  type: EventType.RUN_STARTED
  threadId: string
  runId: string
}
```

| Property   | Type     | Description                   |
| ---------- | -------- | ----------------------------- |
| `threadId` | `string` | ID of the conversation thread |
| `runId`    | `string` | ID of the agent run           |

### RunFinishedEvent

Signals the successful completion of an agent run.

```typescript
type RunFinishedEvent = BaseEvent & {
  type: EventType.RUN_FINISHED
  threadId: string
  runId: string
}
```

| Property   | Type     | Description                   |
| ---------- | -------- | ----------------------------- |
| `threadId` | `string` | ID of the conversation thread |
| `runId`    | `string` | ID of the agent run           |

### RunErrorEvent

Signals an error during an agent run.

```typescript
type RunErrorEvent = BaseEvent & {
  type: EventType.RUN_ERROR
  message: string
  code?: string
}
```

| Property  | Type                | Description   |
| --------- | ------------------- | ------------- |
| `message` | `string`            | Error message |
| `code`    | `string` (optional) | Error code    |

### StepStartedEvent

Signals the start of a step within an agent run.

```typescript
type StepStartedEvent = BaseEvent & {
  type: EventType.STEP_STARTED
  stepName: string
}
```

| Property   | Type     | Description      |
| ---------- | -------- | ---------------- |
| `stepName` | `string` | Name of the step |

### StepFinishedEvent

Signals the completion of a step within an agent run.

```typescript
type StepFinishedEvent = BaseEvent & {
  type: EventType.STEP_FINISHED
  stepName: string
}
```

| Property   | Type     | Description      |
| ---------- | -------- | ---------------- |
| `stepName` | `string` | Name of the step |

## Text Message Events

These events represent the lifecycle of text messages in a conversation.

### TextMessageStartEvent

Signals the start of a text message.

```typescript
type TextMessageStartEvent = BaseEvent & {
  type: EventType.TEXT_MESSAGE_START
  messageId: string
  role: "assistant"
}
```

| Property    | Type          | Description                       |
| ----------- | ------------- | --------------------------------- |
| `messageId` | `string`      | Unique identifier for the message |
| `role`      | `"assistant"` | Role is always "assistant"        |

### TextMessageContentEvent

Represents a chunk of content in a streaming text message.

```typescript
type TextMessageContentEvent = BaseEvent & {
  type: EventType.TEXT_MESSAGE_CONTENT
  messageId: string
  delta: string // Non-empty string
}
```

| Property    | Type     | Description                               |
| ----------- | -------- | ----------------------------------------- |
| `messageId` | `string` | Matches the ID from TextMessageStartEvent |
| `delta`     | `string` | Text content chunk (non-empty)            |

### TextMessageEndEvent

Signals the end of a text message.

```typescript
type TextMessageEndEvent = BaseEvent & {
  type: EventType.TEXT_MESSAGE_END
  messageId: string
}
```

| Property    | Type     | Description                               |
| ----------- | -------- | ----------------------------------------- |
| `messageId` | `string` | Matches the ID from TextMessageStartEvent |

## Tool Call Events

These events represent the lifecycle of tool calls made by agents.

### ToolCallStartEvent

Signals the start of a tool call.

```typescript
type ToolCallStartEvent = BaseEvent & {
  type: EventType.TOOL_CALL_START
  toolCallId: string
  toolCallName: string
  parentMessageId?: string
}
```

| Property          | Type                | Description                         |
| ----------------- | ------------------- | ----------------------------------- |
| `toolCallId`      | `string`            | Unique identifier for the tool call |
| `toolCallName`    | `string`            | Name of the tool being called       |
| `parentMessageId` | `string` (optional) | ID of the parent message            |

### ToolCallArgsEvent

Represents a chunk of argument data for a tool call.

```typescript
type ToolCallArgsEvent = BaseEvent & {
  type: EventType.TOOL_CALL_ARGS
  toolCallId: string
  delta: string
}
```

| Property     | Type     | Description                            |
| ------------ | -------- | -------------------------------------- |
| `toolCallId` | `string` | Matches the ID from ToolCallStartEvent |
| `delta`      | `string` | Argument data chunk                    |

### ToolCallEndEvent

Signals the end of a tool call.

```typescript
type ToolCallEndEvent = BaseEvent & {
  type: EventType.TOOL_CALL_END
  toolCallId: string
}
```

| Property     | Type     | Description                            |
| ------------ | -------- | -------------------------------------- |
| `toolCallId` | `string` | Matches the ID from ToolCallStartEvent |

## State Management Events

These events are used to manage agent state.

### StateSnapshotEvent

Provides a complete snapshot of an agent's state.

```typescript
type StateSnapshotEvent = BaseEvent & {
  type: EventType.STATE_SNAPSHOT
  snapshot: any // StateSchema
}
```

| Property   | Type  | Description             |
| ---------- | ----- | ----------------------- |
| `snapshot` | `any` | Complete state snapshot |

### StateDeltaEvent

Provides a partial update to an agent's state using JSON Patch.

```typescript
type StateDeltaEvent = BaseEvent & {
  type: EventType.STATE_DELTA
  delta: any[] // JSON Patch operations (RFC 6902)
}
```

| Property | Type    | Description                    |
| -------- | ------- | ------------------------------ |
| `delta`  | `any[]` | Array of JSON Patch operations |

### MessagesSnapshotEvent

Provides a snapshot of all messages in a conversation.

```typescript
type MessagesSnapshotEvent = BaseEvent & {
  type: EventType.MESSAGES_SNAPSHOT
  messages: Message[]
}
```

| Property   | Type        | Description              |
| ---------- | ----------- | ------------------------ |
| `messages` | `Message[]` | Array of message objects |

## Special Events

### RawEvent

Used to pass through events from external systems.

```typescript
type RawEvent = BaseEvent & {
  type: EventType.RAW
  event: any
  source?: string
}
```

| Property | Type                | Description         |
| -------- | ------------------- | ------------------- |
| `event`  | `any`               | Original event data |
| `source` | `string` (optional) | Source of the event |

### CustomEvent

Used for application-specific custom events.

```typescript
type CustomEvent = BaseEvent & {
  type: EventType.CUSTOM
  name: string
  value: any
}
```

| Property | Type     | Description                     |
| -------- | -------- | ------------------------------- |
| `name`   | `string` | Name of the custom event        |
| `value`  | `any`    | Value associated with the event |

## Event Schemas

The SDK uses Zod schemas to validate events:

```typescript
const EventSchemas = z.discriminatedUnion("type", [
  TextMessageStartEventSchema,
  TextMessageContentEventSchema,
  TextMessageEndEventSchema,
  ToolCallStartEventSchema,
  ToolCallArgsEventSchema,
  ToolCallEndEventSchema,
  StateSnapshotEventSchema,
  StateDeltaEventSchema,
  MessagesSnapshotEventSchema,
  RawEventSchema,
  CustomEventSchema,
  RunStartedEventSchema,
  RunFinishedEventSchema,
  RunErrorEventSchema,
  StepStartedEventSchema,
  StepFinishedEventSchema,
])
```

This allows for runtime validation of events and provides TypeScript type
inference.


# Overview
Source: https://docs.ag-ui.com/sdk/js/core/overview

Core concepts in the Agent User Interaction Protocol SDK

# @ag-ui/core

The Agent User Interaction Protocol SDK uses a streaming event-based
architecture with strongly typed data structures. This package provides the
foundation for connecting to agent systems.

```bash
npm install @ag-ui/core
```

## Types

Core data structures that represent the building blocks of the system:

* [RunAgentInput](/sdk/js/core/types#runagentinput) - Input parameters for
  running agents
* [Message](/sdk/js/core/types#message-types) - User assistant communication and
  tool usage
* [Context](/sdk/js/core/types#context) - Contextual information provided to
  agents
* [Tool](/sdk/js/core/types#tool) - Defines functions that agents can call
* [State](/sdk/js/core/types#state) - Agent state management

<Card title="Types Reference" icon="cube" href="/sdk/js/core/types" color="#3B82F6" iconType="solid">
  Complete documentation of all types in the @ag-ui/core package
</Card>

## Events

Events that power communication between agents and frontends:

* [Lifecycle Events](/sdk/js/core/events#lifecycle-events) - Run and step
  tracking
* [Text Message Events](/sdk/js/core/events#text-message-events) - Assistant
  message streaming
* [Tool Call Events](/sdk/js/core/events#tool-call-events) - Function call
  lifecycle
* [State Management Events](/sdk/js/core/events#state-management-events) - Agent
  state updates
* [Special Events](/sdk/js/core/events#special-events) - Raw and custom events

<Card title="Events Reference" icon="cube" href="/sdk/js/core/events" color="#3B82F6" iconType="solid">
  Complete documentation of all events in the @ag-ui/core package
</Card>


# Types
Source: https://docs.ag-ui.com/sdk/js/core/types

Documentation for the core types used in the Agent User Interaction Protocol SDK

# Core Types

The Agent User Interaction Protocol SDK is built on a set of core types that
represent the fundamental structures used throughout the system. This page
documents these types and their properties.

## RunAgentInput

Input parameters for running an agent. In the HTTP API, this is the body of the
`POST` request.

```typescript
type RunAgentInput = {
  threadId: string
  runId: string
  state: any
  messages: Message[]
  tools: Tool[]
  context: Context[]
  forwardedProps: any
}
```

| Property         | Type        | Description                                    |
| ---------------- | ----------- | ---------------------------------------------- |
| `threadId`       | `string`    | ID of the conversation thread                  |
| `runId`          | `string`    | ID of the current run                          |
| `state`          | `any`       | Current state of the agent                     |
| `messages`       | `Message[]` | Array of messages in the conversation          |
| `tools`          | `Tool[]`    | Array of tools available to the agent          |
| `context`        | `Context[]` | Array of context objects provided to the agent |
| `forwardedProps` | `any`       | Additional properties forwarded to the agent   |

## Message Types

The SDK includes several message types that represent different kinds of
messages in the system.

### Role

Represents the possible roles a message sender can have.

```typescript
type Role = "developer" | "system" | "assistant" | "user" | "tool"
```

### DeveloperMessage

Represents a message from a developer.

```typescript
type DeveloperMessage = {
  id: string
  role: "developer"
  content: string
  name?: string
}
```

| Property  | Type          | Description                                      |
| --------- | ------------- | ------------------------------------------------ |
| `id`      | `string`      | Unique identifier for the message                |
| `role`    | `"developer"` | Role of the message sender, fixed as "developer" |
| `content` | `string`      | Text content of the message (required)           |
| `name`    | `string`      | Optional name of the sender                      |

### SystemMessage

Represents a system message.

```typescript
type SystemMessage = {
  id: string
  role: "system"
  content: string
  name?: string
}
```

| Property  | Type       | Description                                   |
| --------- | ---------- | --------------------------------------------- |
| `id`      | `string`   | Unique identifier for the message             |
| `role`    | `"system"` | Role of the message sender, fixed as "system" |
| `content` | `string`   | Text content of the message (required)        |
| `name`    | `string`   | Optional name of the sender                   |

### AssistantMessage

Represents a message from an assistant.

```typescript
type AssistantMessage = {
  id: string
  role: "assistant"
  content?: string
  name?: string
  toolCalls?: ToolCall[]
}
```

| Property    | Type                    | Description                                      |
| ----------- | ----------------------- | ------------------------------------------------ |
| `id`        | `string`                | Unique identifier for the message                |
| `role`      | `"assistant"`           | Role of the message sender, fixed as "assistant" |
| `content`   | `string` (optional)     | Text content of the message                      |
| `name`      | `string` (optional)     | Name of the sender                               |
| `toolCalls` | `ToolCall[]` (optional) | Tool calls made in this message                  |

### UserMessage

Represents a message from a user.

```typescript
type UserMessage = {
  id: string
  role: "user"
  content: string
  name?: string
}
```

| Property  | Type     | Description                                 |
| --------- | -------- | ------------------------------------------- |
| `id`      | `string` | Unique identifier for the message           |
| `role`    | `"user"` | Role of the message sender, fixed as "user" |
| `content` | `string` | Text content of the message (required)      |
| `name`    | `string` | Optional name of the sender                 |

### ToolMessage

Represents a message from a tool.

```typescript
type ToolMessage = {
  id: string
  content: string
  role: "tool"
  toolCallId: string
}
```

| Property     | Type     | Description                                  |
| ------------ | -------- | -------------------------------------------- |
| `id`         | `string` | Unique identifier for the message            |
| `content`    | `string` | Text content of the message                  |
| `role`       | `"tool"` | Role of the message sender, fixed as "tool"  |
| `toolCallId` | `string` | ID of the tool call this message responds to |

### Message

A union type representing any type of message in the system.

```typescript
type Message =
  | DeveloperMessage
  | SystemMessage
  | AssistantMessage
  | UserMessage
  | ToolMessage
```

### ToolCall

Represents a tool call made by an agent.

```typescript
type ToolCall = {
  id: string
  type: "function"
  function: FunctionCall
}
```

| Property   | Type           | Description                              |
| ---------- | -------------- | ---------------------------------------- |
| `id`       | `string`       | Unique identifier for the tool call      |
| `type`     | `"function"`   | Type of the tool call, always "function" |
| `function` | `FunctionCall` | Details about the function being called  |

#### FunctionCall

Represents function name and arguments in a tool call.

```typescript
type FunctionCall = {
  name: string
  arguments: string
}
```

| Property    | Type     | Description                                      |
| ----------- | -------- | ------------------------------------------------ |
| `name`      | `string` | Name of the function to call                     |
| `arguments` | `string` | JSON-encoded string of arguments to the function |

## Context

Represents a piece of contextual information provided to an agent.

```typescript
type Context = {
  description: string
  value: string
}
```

| Property      | Type     | Description                                 |
| ------------- | -------- | ------------------------------------------- |
| `description` | `string` | Description of what this context represents |
| `value`       | `string` | The actual context value                    |

## Tool

Defines a tool that can be called by an agent.

```typescript
type Tool = {
  name: string
  description: string
  parameters: any // JSON Schema
}
```

| Property      | Type     | Description                                      |
| ------------- | -------- | ------------------------------------------------ |
| `name`        | `string` | Name of the tool                                 |
| `description` | `string` | Description of what the tool does                |
| `parameters`  | `any`    | JSON Schema defining the parameters for the tool |

## State

Represents the state of an agent during execution.

```typescript
type State = any
```

The state type is flexible and can hold any data structure needed by the agent
implementation.


# @ag-ui/encoder
Source: https://docs.ag-ui.com/sdk/js/encoder





# @ag-ui/proto
Source: https://docs.ag-ui.com/sdk/js/proto





# Events
Source: https://docs.ag-ui.com/sdk/python/core/events

Documentation for the events used in the Agent User Interaction Protocol Python SDK

# Events

The Agent User Interaction Protocol Python SDK uses a streaming event-based
architecture. Events are the fundamental units of communication between agents
and the frontend. This section documents the event types and their properties.

## EventType Enum

`from ag_ui.core import EventType`

The `EventType` enum defines all possible event types in the system:

```python
class EventType(str, Enum):
    TEXT_MESSAGE_START = "TEXT_MESSAGE_START"
    TEXT_MESSAGE_CONTENT = "TEXT_MESSAGE_CONTENT"
    TEXT_MESSAGE_END = "TEXT_MESSAGE_END"
    TOOL_CALL_START = "TOOL_CALL_START"
    TOOL_CALL_ARGS = "TOOL_CALL_ARGS"
    TOOL_CALL_END = "TOOL_CALL_END"
    STATE_SNAPSHOT = "STATE_SNAPSHOT"
    STATE_DELTA = "STATE_DELTA"
    MESSAGES_SNAPSHOT = "MESSAGES_SNAPSHOT"
    RAW = "RAW"
    CUSTOM = "CUSTOM"
    RUN_STARTED = "RUN_STARTED"
    RUN_FINISHED = "RUN_FINISHED"
    RUN_ERROR = "RUN_ERROR"
    STEP_STARTED = "STEP_STARTED"
    STEP_FINISHED = "STEP_FINISHED"
```

## BaseEvent

`from ag_ui.core import BaseEvent`

All events inherit from the `BaseEvent` class, which provides common properties
shared across all event types.

```python
class BaseEvent(ConfiguredBaseModel):
    type: EventType
    timestamp: Optional[int] = None
    raw_event: Optional[Any] = None
```

| Property    | Type            | Description                                           |
| ----------- | --------------- | ----------------------------------------------------- |
| `type`      | `EventType`     | The type of event (discriminator field for the union) |
| `timestamp` | `Optional[int]` | Timestamp when the event was created                  |
| `raw_event` | `Optional[Any]` | Original event data if this event was transformed     |

## Lifecycle Events

These events represent the lifecycle of an agent run.

### RunStartedEvent

`from ag_ui.core import RunStartedEvent`

Signals the start of an agent run.

```python
class RunStartedEvent(BaseEvent):
    type: Literal[EventType.RUN_STARTED]
    thread_id: str
    run_id: str
```

| Property    | Type  | Description                   |
| ----------- | ----- | ----------------------------- |
| `thread_id` | `str` | ID of the conversation thread |
| `run_id`    | `str` | ID of the agent run           |

### RunFinishedEvent

`from ag_ui.core import RunFinishedEvent`

Signals the successful completion of an agent run.

```python
class RunFinishedEvent(BaseEvent):
    type: Literal[EventType.RUN_FINISHED]
    thread_id: str
    run_id: str
```

| Property    | Type  | Description                   |
| ----------- | ----- | ----------------------------- |
| `thread_id` | `str` | ID of the conversation thread |
| `run_id`    | `str` | ID of the agent run           |

### RunErrorEvent

`from ag_ui.core import RunErrorEvent`

Signals an error during an agent run.

```python
class RunErrorEvent(BaseEvent):
    type: Literal[EventType.RUN_ERROR]
    message: str
    code: Optional[str] = None
```

| Property  | Type            | Description   |
| --------- | --------------- | ------------- |
| `message` | `str`           | Error message |
| `code`    | `Optional[str]` | Error code    |

### StepStartedEvent

`from ag_ui.core import StepStartedEvent`

Signals the start of a step within an agent run.

```python
class StepStartedEvent(BaseEvent):
    type: Literal[EventType.STEP_STARTED]
    step_name: str
```

| Property    | Type  | Description      |
| ----------- | ----- | ---------------- |
| `step_name` | `str` | Name of the step |

### StepFinishedEvent

`from ag_ui.core import StepFinishedEvent`

Signals the completion of a step within an agent run.

```python
class StepFinishedEvent(BaseEvent):
    type: Literal[EventType.STEP_FINISHED]
    step_name: str
```

| Property    | Type  | Description      |
| ----------- | ----- | ---------------- |
| `step_name` | `str` | Name of the step |

## Text Message Events

These events represent the lifecycle of text messages in a conversation.

### TextMessageStartEvent

`from ag_ui.core import TextMessageStartEvent`

Signals the start of a text message.

```python
class TextMessageStartEvent(BaseEvent):
    type: Literal[EventType.TEXT_MESSAGE_START]
    message_id: str
    role: Literal["assistant"]
```

| Property     | Type                   | Description                       |
| ------------ | ---------------------- | --------------------------------- |
| `message_id` | `str`                  | Unique identifier for the message |
| `role`       | `Literal["assistant"]` | Role is always "assistant"        |

### TextMessageContentEvent

`from ag_ui.core import TextMessageContentEvent`

Represents a chunk of content in a streaming text message.

```python
class TextMessageContentEvent(BaseEvent):
    type: Literal[EventType.TEXT_MESSAGE_CONTENT]
    message_id: str
    delta: str  # Non-empty string

    def model_post_init(self, __context):
        if len(self.delta) == 0:
            raise ValueError("Delta must not be an empty string")
```

| Property     | Type  | Description                               |
| ------------ | ----- | ----------------------------------------- |
| `message_id` | `str` | Matches the ID from TextMessageStartEvent |
| `delta`      | `str` | Text content chunk (non-empty)            |

### TextMessageEndEvent

`from ag_ui.core import TextMessageEndEvent`

Signals the end of a text message.

```python
class TextMessageEndEvent(BaseEvent):
    type: Literal[EventType.TEXT_MESSAGE_END]
    message_id: str
```

| Property     | Type  | Description                               |
| ------------ | ----- | ----------------------------------------- |
| `message_id` | `str` | Matches the ID from TextMessageStartEvent |

## Tool Call Events

These events represent the lifecycle of tool calls made by agents.

### ToolCallStartEvent

`from ag_ui.core import ToolCallStartEvent`

Signals the start of a tool call.

```python
class ToolCallStartEvent(BaseEvent):
    type: Literal[EventType.TOOL_CALL_START]
    tool_call_id: str
    tool_call_name: str
    parent_message_id: Optional[str] = None
```

| Property            | Type            | Description                         |
| ------------------- | --------------- | ----------------------------------- |
| `tool_call_id`      | `str`           | Unique identifier for the tool call |
| `tool_call_name`    | `str`           | Name of the tool being called       |
| `parent_message_id` | `Optional[str]` | ID of the parent message            |

### ToolCallArgsEvent

`from ag_ui.core import ToolCallArgsEvent`

Represents a chunk of argument data for a tool call.

```python
class ToolCallArgsEvent(BaseEvent):
    type: Literal[EventType.TOOL_CALL_ARGS]
    tool_call_id: str
    delta: str
```

| Property       | Type  | Description                            |
| -------------- | ----- | -------------------------------------- |
| `tool_call_id` | `str` | Matches the ID from ToolCallStartEvent |
| `delta`        | `str` | Argument data chunk                    |

### ToolCallEndEvent

`from ag_ui.core import ToolCallEndEvent`

Signals the end of a tool call.

```python
class ToolCallEndEvent(BaseEvent):
    type: Literal[EventType.TOOL_CALL_END]
    tool_call_id: str
```

| Property       | Type  | Description                            |
| -------------- | ----- | -------------------------------------- |
| `tool_call_id` | `str` | Matches the ID from ToolCallStartEvent |

## State Management Events

These events are used to manage agent state.

### StateSnapshotEvent

`from ag_ui.core import StateSnapshotEvent`

Provides a complete snapshot of an agent's state.

```python
class StateSnapshotEvent(BaseEvent):
    type: Literal[EventType.STATE_SNAPSHOT]
    snapshot: State
```

| Property   | Type    | Description             |
| ---------- | ------- | ----------------------- |
| `snapshot` | `State` | Complete state snapshot |

### StateDeltaEvent

`from ag_ui.core import StateDeltaEvent`

Provides a partial update to an agent's state using JSON Patch.

```python
class StateDeltaEvent(BaseEvent):
    type: Literal[EventType.STATE_DELTA]
    delta: List[Any]  # JSON Patch (RFC 6902)
```

| Property | Type        | Description                    |
| -------- | ----------- | ------------------------------ |
| `delta`  | `List[Any]` | Array of JSON Patch operations |

### MessagesSnapshotEvent

`from ag_ui.core import MessagesSnapshotEvent`

Provides a snapshot of all messages in a conversation.

```python
class MessagesSnapshotEvent(BaseEvent):
    type: Literal[EventType.MESSAGES_SNAPSHOT]
    messages: List[Message]
```

| Property   | Type            | Description              |
| ---------- | --------------- | ------------------------ |
| `messages` | `List[Message]` | Array of message objects |

## Special Events

### RawEvent

`from ag_ui.core import RawEvent`

Used to pass through events from external systems.

```python
class RawEvent(BaseEvent):
    type: Literal[EventType.RAW]
    event: Any
    source: Optional[str] = None
```

| Property | Type            | Description         |
| -------- | --------------- | ------------------- |
| `event`  | `Any`           | Original event data |
| `source` | `Optional[str]` | Source of the event |

### CustomEvent

`from ag_ui.core import CustomEvent`

Used for application-specific custom events.

```python
class CustomEvent(BaseEvent):
    type: Literal[EventType.CUSTOM]
    name: str
    value: Any
```

| Property | Type  | Description                     |
| -------- | ----- | ------------------------------- |
| `name`   | `str` | Name of the custom event        |
| `value`  | `Any` | Value associated with the event |

## Event Discrimination

`from ag_ui.core import Event`

The SDK uses Pydantic's discriminated unions for event validation:

```python
Event = Annotated[
    Union[
        TextMessageStartEvent,
        TextMessageContentEvent,
        TextMessageEndEvent,
        ToolCallStartEvent,
        ToolCallArgsEvent,
        ToolCallEndEvent,
        StateSnapshotEvent,
        StateDeltaEvent,
        MessagesSnapshotEvent,
        RawEvent,
        CustomEvent,
        RunStartedEvent,
        RunFinishedEvent,
        RunErrorEvent,
        StepStartedEvent,
        StepFinishedEvent,
    ],
    Field(discriminator="type")
]
```

This allows for runtime validation of events and type checking at development
time.


# Overview
Source: https://docs.ag-ui.com/sdk/python/core/overview

Core concepts in the Agent User Interaction Protocol SDK

```bash
pip install ag-ui-protocol
```

# ag\_ui.core

The Agent User Interaction Protocol SDK uses a streaming event-based
architecture with strongly typed data structures. This package provides the
foundation for connecting to agent systems.

```python
from ag_ui.core import ...
```

## Types

Core data structures that represent the building blocks of the system:

* [RunAgentInput](/sdk/python/core/types#runagentinput) - Input parameters for
  running agents
* [Message](/sdk/python/core/types#message-types) - User assistant communication
  and tool usage
* [Context](/sdk/python/core/types#context) - Contextual information provided to
  agents
* [Tool](/sdk/python/core/types#tool) - Defines functions that agents can call
* [State](/sdk/python/core/types#state) - Agent state management

<Card title="Types Reference" icon="cube" href="/sdk/python/core/types" color="#3B82F6" iconType="solid">
  Complete documentation of all types in the ag\_ui.core package
</Card>

## Events

Events that power communication between agents and frontends:

* [Lifecycle Events](/sdk/python/core/events#lifecycle-events) - Run and step
  tracking
* [Text Message Events](/sdk/python/core/events#text-message-events) - Assistant
  message streaming
* [Tool Call Events](/sdk/python/core/events#tool-call-events) - Function call
  lifecycle
* [State Management Events](/sdk/python/core/events#state-management-events) -
  Agent state updates
* [Special Events](/sdk/python/core/events#special-events) - Raw and custom
  events

<Card title="Events Reference" icon="cube" href="/sdk/python/core/events" color="#3B82F6" iconType="solid">
  Complete documentation of all events in the ag\_ui.core package
</Card>


# Types
Source: https://docs.ag-ui.com/sdk/python/core/types

Documentation for the core types used in the Agent User Interaction Protocol Python SDK

# Core Types

The Agent User Interaction Protocol Python SDK is built on a set of core types
that represent the fundamental structures used throughout the system. This page
documents these types and their properties.

## RunAgentInput

`from ag_ui.core import RunAgentInput`

Input parameters for running an agent. In the HTTP API, this is the body of the
`POST` request.

```python
class RunAgentInput(ConfiguredBaseModel):
    thread_id: str
    run_id: str
    state: Any
    messages: List[Message]
    tools: List[Tool]
    context: List[Context]
    forwarded_props: Any
```

| Property          | Type            | Description                                   |
| ----------------- | --------------- | --------------------------------------------- |
| `thread_id`       | `str`           | ID of the conversation thread                 |
| `run_id`          | `str`           | ID of the current run                         |
| `state`           | `Any`           | Current state of the agent                    |
| `messages`        | `List[Message]` | List of messages in the conversation          |
| `tools`           | `List[Tool]`    | List of tools available to the agent          |
| `context`         | `List[Context]` | List of context objects provided to the agent |
| `forwarded_props` | `Any`           | Additional properties forwarded to the agent  |

## Message Types

The SDK includes several message types that represent different kinds of
messages in the system.

### Role

`from ag_ui.core import Role`

Represents the possible roles a message sender can have.

```python
Role = Literal["developer", "system", "assistant", "user", "tool"]
```

### DeveloperMessage

`from ag_ui.core import DeveloperMessage`

Represents a message from a developer.

```python
class DeveloperMessage(BaseMessage):
    role: Literal["developer"]
    content: str
```

| Property  | Type                   | Description                                      |
| --------- | ---------------------- | ------------------------------------------------ |
| `id`      | `str`                  | Unique identifier for the message                |
| `role`    | `Literal["developer"]` | Role of the message sender, fixed as "developer" |
| `content` | `str`                  | Text content of the message (required)           |
| `name`    | `Optional[str]`        | Optional name of the sender                      |

### SystemMessage

`from ag_ui.core import SystemMessage`

Represents a system message.

```python
class SystemMessage(BaseMessage):
    role: Literal["system"]
    content: str
```

| Property  | Type                | Description                                   |
| --------- | ------------------- | --------------------------------------------- |
| `id`      | `str`               | Unique identifier for the message             |
| `role`    | `Literal["system"]` | Role of the message sender, fixed as "system" |
| `content` | `str`               | Text content of the message (required)        |
| `name`    | `Optional[str]`     | Optional name of the sender                   |

### AssistantMessage

`from ag_ui.core import AssistantMessage`

Represents a message from an assistant.

```python
class AssistantMessage(BaseMessage):
    role: Literal["assistant"]
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
```

| Property     | Type                       | Description                                      |
| ------------ | -------------------------- | ------------------------------------------------ |
| `id`         | `str`                      | Unique identifier for the message                |
| `role`       | `Literal["assistant"]`     | Role of the message sender, fixed as "assistant" |
| `content`    | `Optional[str]`            | Text content of the message                      |
| `name`       | `Optional[str]`            | Name of the sender                               |
| `tool_calls` | `Optional[List[ToolCall]]` | Tool calls made in this message                  |

### UserMessage

`from ag_ui.core import UserMessage`

Represents a message from a user.

```python
class UserMessage(BaseMessage):
    role: Literal["user"]
    content: str
```

| Property  | Type              | Description                                 |
| --------- | ----------------- | ------------------------------------------- |
| `id`      | `str`             | Unique identifier for the message           |
| `role`    | `Literal["user"]` | Role of the message sender, fixed as "user" |
| `content` | `str`             | Text content of the message (required)      |
| `name`    | `Optional[str]`   | Optional name of the sender                 |

### ToolMessage

`from ag_ui.core import ToolMessage`

Represents a message from a tool.

```python
class ToolMessage(ConfiguredBaseModel):
    id: str
    role: Literal["tool"]
    content: str
    tool_call_id: str
```

| Property       | Type              | Description                                  |
| -------------- | ----------------- | -------------------------------------------- |
| `id`           | `str`             | Unique identifier for the message            |
| `content`      | `str`             | Text content of the message                  |
| `role`         | `Literal["tool"]` | Role of the message sender, fixed as "tool"  |
| `tool_call_id` | `str`             | ID of the tool call this message responds to |

### Message

`from ag_ui.core import Message`

A union type representing any type of message in the system.

```python
Message = Annotated[
    Union[DeveloperMessage, SystemMessage, AssistantMessage, UserMessage, ToolMessage],
    Field(discriminator="role")
]
```

### ToolCall

`from ag_ui.core import ToolCall`

Represents a tool call made by an agent.

```python
class ToolCall(ConfiguredBaseModel):
    id: str
    type: Literal["function"]
    function: FunctionCall
```

| Property   | Type                  | Description                              |
| ---------- | --------------------- | ---------------------------------------- |
| `id`       | `str`                 | Unique identifier for the tool call      |
| `type`     | `Literal["function"]` | Type of the tool call, always "function" |
| `function` | `FunctionCall`        | Details about the function being called  |

#### FunctionCall

`from ag_ui.core import FunctionCall`

Represents function name and arguments in a tool call.

```python
class FunctionCall(ConfiguredBaseModel):
    name: str
    arguments: str
```

| Property    | Type  | Description                                      |
| ----------- | ----- | ------------------------------------------------ |
| `name`      | `str` | Name of the function to call                     |
| `arguments` | `str` | JSON-encoded string of arguments to the function |

## Context

`from ag_ui.core import Context`

Represents a piece of contextual information provided to an agent.

```python
class Context(ConfiguredBaseModel):
    description: str
    value: str
```

| Property      | Type  | Description                                 |
| ------------- | ----- | ------------------------------------------- |
| `description` | `str` | Description of what this context represents |
| `value`       | `str` | The actual context value                    |

## Tool

`from ag_ui.core import Tool`

Defines a tool that can be called by an agent.

```python
class Tool(ConfiguredBaseModel):
    name: str
    description: str
    parameters: Any  # JSON Schema
```

| Property      | Type  | Description                                      |
| ------------- | ----- | ------------------------------------------------ |
| `name`        | `str` | Name of the tool                                 |
| `description` | `str` | Description of what the tool does                |
| `parameters`  | `Any` | JSON Schema defining the parameters for the tool |

## State

`from ag_ui.core import State`

Represents the state of an agent during execution.

```python
State = Any
```

The state type is flexible and can hold any data structure needed by the agent
implementation.


# Overview
Source: https://docs.ag-ui.com/sdk/python/encoder/overview

Documentation for encoding Agent User Interaction Protocol events

```bash
pip install ag-ui-protocol
```

# Event Encoder

The Agent User Interaction Protocol uses a streaming approach to send events
from agents to clients. The `EventEncoder` class provides the functionality to
encode events into a format that can be sent over HTTP.

## EventEncoder

`from ag_ui.encoder import EventEncoder`

The `EventEncoder` class is responsible for encoding `BaseEvent` objects into
string representations that can be transmitted to clients.

```python
from ag_ui.core import BaseEvent
from ag_ui.encoder import EventEncoder

# Initialize the encoder
encoder = EventEncoder()

# Encode an event
encoded_event = encoder.encode(event)
```

### Usage

The `EventEncoder` is typically used in HTTP handlers to convert event objects
into a stream of data. The current implementation encodes events as Server-Sent
Events (SSE), which can be consumed by clients using the EventSource API.

### Methods

#### `__init__(accept: str = None)`

Creates a new encoder instance.

| Parameter | Type             | Description                         |
| --------- | ---------------- | ----------------------------------- |
| `accept`  | `str` (optional) | Content type accepted by the client |

#### `encode(event: BaseEvent) -> str`

Encodes an event into a string representation.

| Parameter | Type        | Description         |
| --------- | ----------- | ------------------- |
| `event`   | `BaseEvent` | The event to encode |

**Returns**: A string representation of the event in SSE format.

### Example

```python
from ag_ui.core import TextMessageContentEvent, EventType
from ag_ui.encoder import EventEncoder

# Create an event
event = TextMessageContentEvent(
    type=EventType.TEXT_MESSAGE_CONTENT,
    message_id="msg_123",
    delta="Hello, world!"
)

# Initialize the encoder
encoder = EventEncoder()

# Encode the event
encoded_event = encoder.encode(event)
print(encoded_event)
# Output: data: {"type":"TEXT_MESSAGE_CONTENT","messageId":"msg_123","delta":"Hello, world!"}\n\n
```

### Implementation Details

Internally, the encoder converts events to JSON and formats them as Server-Sent
Events with the following structure:

```
data: {json-serialized event}\n\n
```

This format allows clients to receive a continuous stream of events and process
them as they arrive.


# Developing with Cursor
Source: https://docs.ag-ui.com/tutorials/cursor

Use Cursor to build AG-UI implementations faster

This guide will help you set up Cursor to help you build custom Agent User
Interaction Protocol (AG-UI) servers and clients faster. The same principles
apply to other IDE's like Windsurf, VSCode, etc.

## Adding the documentation to Cursor

1. Open up the Cursor settings
2. Go to Features > Docs and click "+ Add new Doc"
3. Paste in the following URL: [https://docs.ag-ui.com/llms-full.txt](https://docs.ag-ui.com/llms-full.txt)
4. Click "Add"

## Using the documentation

Now you can use the documentation to help you build your AG-UI project. Load the
docs into the current prompt by typing the `@` symbol, selecting "Docs" and then
selecting "Agent User Interaction Protocol" from the list. Happy coding!

## Best practices

When building AG-UI servers with Cursor:

* Break down complex problems into smaller steps
* Have a look at what the agent was doing by checking which files it edited
  (above the chat input)
* Let the agent write unit tests to verify your implementation
* Follow AG-UI protocol specifications carefully


# Debugging
Source: https://docs.ag-ui.com/tutorials/debugging

A comprehensive guide to debugging Agent User Interaction Protocol (AG-UI) integrations

# Debugging AG-UI Integrations

Debugging agent-based applications can be challenging, especially when working
with real-time, event-driven protocols like AG-UI. This guide introduces you to
the AG-UI Dojo, a powerful tool for learning, testing, and debugging your AG-UI
implementations.

## The AG-UI Dojo

The AG-UI Dojo is the best way to bring AG-UI to a new surface, and is also an
excellent resource for learning about the protocol's basic capabilities. It
provides a structured environment where you can test and validate each component
of the AG-UI protocol.

### What is the Dojo?

The Dojo consists of a series of "hello world"-sized demonstrations for the
different building blocks available via AG-UI. Each demonstration:

1. Shows a specific AG-UI capability in action
2. Presents both the user-visible interaction and the underlying code side by
   side
3. Allows you to test and verify your implementation

### Using the Dojo as an Implementation Checklist

When working on bringing AG-UI to a new surface or platform, you can use the
Dojo as a comprehensive "todo list":

1. Work through each demonstration one by one
2. Implement and test each AG-UI building block in your environment
3. When all demonstrations work correctly in your implementation, you can be
   confident that full-featured copilots and agent-native applications can be
   built on your new surface

This methodical approach ensures you've covered all the necessary functionality
required for a complete AG-UI implementation.

### Using the Dojo as a Learning Resource

For developers new to AG-UI, the Dojo serves as an interactive learning
resource:

* Each item demonstrates a specific AG-UI capability
* You can see both what the interaction looks like from a user perspective
* The underlying code is shown alongside, helping you understand how it works
* The incremental complexity helps build understanding from basics to advanced
  features

### Common Debugging Patterns

When using the Dojo for debugging your AG-UI implementation, keep these patterns
in mind:

1. **Event Sequence Issues**: Verify that events are being emitted in the
   correct order and with proper nesting (e.g., `TEXT_MESSAGE_START` before
   `TEXT_MESSAGE_CONTENT`)

2. **Data Format Problems**: Ensure your event payloads match the expected
   structure for each event type

3. **Transport Layer Debugging**: Check that your chosen transport mechanism
   (SSE, WebSockets, etc.) is correctly delivering events

4. **State Synchronization**: Confirm that state updates are correctly applied
   using snapshots and deltas

5. **Tool Execution**: Verify that tool calls and responses are properly
   formatted and processed

## Getting Started with the Dojo

To start using the AG-UI Dojo:

1. Clone the repository from
   [github.com/ag-ui-protocol/dojo](https://github.com/ag-ui-protocol/dojo)
2. Follow the setup instructions in the README
3. Start working through the demonstrations in order
4. Use the provided test cases to validate your implementation

The Dojo's structured approach makes it an invaluable resource for both learning
AG-UI and ensuring your implementation meets all requirements.


