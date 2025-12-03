"""
LangGraph状态图定义
"""
from langgraph.graph import StateGraph, END

from .models import CustomerServiceState
from .nodes import (
    intent_recognition_node,
    router_node,
    greeting_handler_node,
    knowledge_retrieval_node,
    order_handler_node,
    payment_handler_node,
    refund_handler_node,
    logistics_handler_node,
    complaint_handler_node,
    chitchat_handler_node,
    response_generation_node,
    transfer_to_human_node
)


def create_customer_service_graph():
    """
    创建客服机器人状态图
    """
    # 创建状态图
    workflow = StateGraph(CustomerServiceState)

    # 添加节点
    workflow.add_node("intent_recognition", intent_recognition_node)
    workflow.add_node("greeting_handler", greeting_handler_node)
    workflow.add_node("knowledge_retrieval", knowledge_retrieval_node)
    workflow.add_node("order_handler", order_handler_node)
    workflow.add_node("payment_handler", payment_handler_node)
    workflow.add_node("refund_handler", refund_handler_node)
    workflow.add_node("logistics_handler", logistics_handler_node)
    workflow.add_node("complaint_handler", complaint_handler_node)
    workflow.add_node("chitchat_handler", chitchat_handler_node)
    workflow.add_node("response_generation", response_generation_node)
    workflow.add_node("transfer_to_human", transfer_to_human_node)

    # 设置入口点
    workflow.set_entry_point("intent_recognition")

    # 添加条件路由边（从意图识别到各个处理器）
    workflow.add_conditional_edges(
        "intent_recognition",
        router_node,
        {
            "greeting_handler": "greeting_handler",
            "knowledge_retrieval": "knowledge_retrieval",
            "order_handler": "order_handler",
            "payment_handler": "payment_handler",
            "refund_handler": "refund_handler",
            "logistics_handler": "logistics_handler",
            "complaint_handler": "complaint_handler",
            "chitchat_handler": "chitchat_handler",
            "transfer_to_human": "transfer_to_human"
        }
    )

    # 各处理节点到响应生成或结束
    workflow.add_edge("greeting_handler", END)
    workflow.add_edge("knowledge_retrieval", "response_generation")
    workflow.add_edge("order_handler", "response_generation")
    workflow.add_edge("payment_handler", "response_generation")
    workflow.add_edge("refund_handler", "response_generation")
    workflow.add_edge("logistics_handler", "response_generation")
    workflow.add_edge("complaint_handler", END)
    workflow.add_edge("chitchat_handler", END)
    workflow.add_edge("response_generation", END)
    workflow.add_edge("transfer_to_human", END)

    # 编译图
    app = workflow.compile()

    return app
