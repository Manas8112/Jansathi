from typing import Annotated, TypedDict, Sequence, Optional
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    State representing the overall conversation and execution flow.
    
    New fields added for the 4-differentiator architecture:
    - jurisdiction_data: output from the deterministic jurisdiction engine
    - confidence_score: verifier score (0-10) after reflexion check
    - citations: specific law sections cited in the response
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    conversation_id: str
    user_intent: str          # "RTI", "Complaint", "Legal Advice", "Scheme Info", "General"
    extracted_entities: dict  # specific details extracted (date, location, amount, state)
    retrieved_context: list[str]  # RAG + Knowledge Graph + Jurisdiction Engine context
    drafted_document: str | None
    next_action: str
    jurisdiction_data: Optional[dict]   # Output from JurisdictionEngine
    confidence_score: Optional[float]   # Verifier score (0-10)
    citations: Optional[list[str]]      # Law sections cited in the final response
