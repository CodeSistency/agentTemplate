from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage

class TestAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]
