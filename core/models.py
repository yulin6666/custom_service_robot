"""
State definitions
"""
from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
import operator


class EnterpriseQueryState(TypedDict):
    """Enterprise query conversation state"""
    # Message history
    messages: Annotated[Sequence[BaseMessage], operator.add]

    # Session information
    session_id: str
    user_id: Optional[str]

    # Intent recognition
    intent: Optional[str]  # greeting/inquiry/admin/hr/it/legal/finance/procurement/chitchat
    intent_confidence: Optional[float]

    # Context information
    entities: Optional[dict]  # Extracted entities (departments, employee info, etc.)

    # Knowledge base retrieval
    retrieved_docs: Optional[list]

    # Tool calls
    tool_results: Optional[dict]

    # Human transfer
    need_human: bool

    # Response generation
    final_response: Optional[str]

    # Flow control
    next_step: Optional[str]


# Compatibility alias
CustomerServiceState = EnterpriseQueryState
