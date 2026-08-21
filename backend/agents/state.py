from typing import Annotated, TypedDict, Sequence
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    State representing the overall conversation and execution flow.
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    conversation_id: str
    user_intent: str  # e.g., "RTI", "Complaint", "Legal Advice", "Scheme Info"
    extracted_entities: dict  # specific details extracted (e.g. date, location, amount)
    retrieved_context: list[str]
    drafted_document: str | None
    next_action: str
