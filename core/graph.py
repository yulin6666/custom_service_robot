"""
LangGraph state graph definition
"""
from langgraph.graph import StateGraph, END

from .models import EnterpriseQueryState
from .nodes import (
    intent_recognition_node,
    router_node,
    greeting_handler_node,
    knowledge_retrieval_node,
    chitchat_handler_node,
    response_generation_node,
    transfer_to_human_node
)


def create_enterprise_query_graph():
    """
    Create the internal enterprise query assistant state graph
    """
    # Create state graph
    workflow = StateGraph(EnterpriseQueryState)

    # Add nodes
    workflow.add_node("intent_recognition", intent_recognition_node)
    workflow.add_node("greeting_handler", greeting_handler_node)
    workflow.add_node("knowledge_retrieval", knowledge_retrieval_node)
    workflow.add_node("chitchat_handler", chitchat_handler_node)
    workflow.add_node("response_generation", response_generation_node)
    workflow.add_node("transfer_to_human", transfer_to_human_node)

    # Set entry point
    workflow.set_entry_point("intent_recognition")

    # Add conditional routing edges (from intent recognition to each handler)
    workflow.add_conditional_edges(
        "intent_recognition",
        router_node,
        {
            "greeting_handler": "greeting_handler",
            "knowledge_retrieval": "knowledge_retrieval",
            "chitchat_handler": "chitchat_handler",
            "transfer_to_human": "transfer_to_human"
        }
    )

    # Each handler node to response generation or end
    workflow.add_edge("greeting_handler", END)
    workflow.add_edge("knowledge_retrieval", "response_generation")
    workflow.add_edge("chitchat_handler", END)
    workflow.add_edge("response_generation", END)
    workflow.add_edge("transfer_to_human", END)

    # Compile graph
    app = workflow.compile()

    return app


# Compatibility alias
create_customer_service_graph = create_enterprise_query_graph
