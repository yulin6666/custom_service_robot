"""
LangGraph节点定义
"""
import json
from typing import Any
from langchain_core.messages import HumanMessage, AIMessage

from .models import CustomerServiceState
from .config import llm, INTENT_CONFIDENCE_THRESHOLD
from .knowledge_base import knowledge_base
from .tools import query_order, process_payment, process_refund, query_logistics


def intent_recognition_node(state: CustomerServiceState) -> dict:
    """
    意图识别节点
    """
    messages = state["messages"]
    last_message = messages[-1].content

    print(f"\n[节点] 进入意图识别节点 (intent_recognition_node)")
    print(f"[节点] 用户消息: {last_message}")

    # 使用LLM进行意图分类
    intent_prompt = f"""
分析以下用户消息的意图，返回JSON格式。

用户消息：{last_message}

请识别用户意图，从以下类型中选择一个：

【咨询类】- 用户在询问政策、规则、流程、如何操作等
- greeting: 问候、打招呼（你好、在吗）
- inquiry: 咨询问题（如何退货、什么情况可以退款、退货流程是什么、支持哪些支付方式、多久发货等）
- chitchat: 闲聊（天气、笑话等非业务话题）

【操作类】- 用户要执行具体操作，通常会提供订单号或明确说"我要..."
- order_query: 查询具体订单（我的订单、查询订单ORD001）
- payment: 要支付订单（帮我支付、支付链接）
- refund: 要申请退款退货（我要退货、帮我退款、申请退款，通常有订单号）
- logistics: 查询物流（快递到哪了、物流信息）

【特殊类】
- complaint: 投诉抱怨（态度差、质量太烂、要投诉）
- transfer_human: 明确要求转人工（转人工、找客服）

重要：
- 如果是询问"如何"、"什么情况"、"怎么办"、"流程"、"政策"等，选择 inquiry
- 如果是要执行操作且提供了订单号等信息，才选择对应的操作类型

返回格式：
{{"intent": "意图类型", "confidence": 0.95, "entities": {{"订单号": "ORD001"}}}}

只返回JSON，不要其他内容。
"""

    try:
        response = llm.invoke(intent_prompt)
        result = json.loads(response.content)
        intent = result.get("intent", "inquiry")
        confidence = result.get("confidence", 0.5)

        print(f"[节点] 识别意图: {intent} (置信度: {confidence:.2f})")

        return {
            "intent": intent,
            "intent_confidence": confidence,
            "entities": result.get("entities", {}),
            "next_step": "router"
        }
    except Exception as e:
        print(f"意图识别失败: {e}")
        return {
            "intent": "inquiry",
            "intent_confidence": 0.3,
            "entities": {},
            "next_step": "router"
        }


def router_node(state: CustomerServiceState) -> str:
    """
    路由分发节点 - 根据意图决定下一步
    """
    intent = state.get("intent", "inquiry")
    confidence = state.get("intent_confidence", 0.0)

    print(f"\n[路由] 进入路由节点")
    print(f"[路由] 意图: {intent}, 置信度: {confidence:.2f}")

    # 低置信度或明确要求转人工
    if confidence < INTENT_CONFIDENCE_THRESHOLD or intent == "transfer_human":
        route = "transfer_to_human"
        print(f"[路由] 决策: 转人工 (置信度过低或用户请求)")
        return route

    # 根据意图路由
    intent_routes = {
        "greeting": "greeting_handler",
        "inquiry": "knowledge_retrieval",
        "order_query": "order_handler",
        "payment": "payment_handler",
        "refund": "refund_handler",
        "logistics": "logistics_handler",
        "complaint": "complaint_handler",
        "chitchat": "chitchat_handler"
    }

    route = intent_routes.get(intent, "knowledge_retrieval")
    print(f"[路由] 决策: 路由到 {route}\n")
    return route


def greeting_handler_node(state: CustomerServiceState) -> dict:
    """
    问候处理节点
    """
    greeting_response = """您好！我是智能客服助手，很高兴为您服务！

我可以帮您：
- 查询订单状态
- 处理退换货
- 解答常见问题
- 查询物流信息

请问有什么可以帮到您的吗？"""

    return {
        "final_response": greeting_response,
        "next_step": "end"
    }


def knowledge_retrieval_node(state: CustomerServiceState) -> dict:
    """
    知识库检索节点（RAG）
    """
    print("\n[节点] 进入知识库检索节点 (knowledge_retrieval_node)")

    messages = state["messages"]
    query = messages[-1].content

    # 从知识库检索
    docs = knowledge_base.search(query, k=3)

    if not docs:
        print("[节点] 未检索到相关文档，将使用空上下文生成响应\n")
        return {
            "retrieved_docs": [],
            "next_step": "response_generation"
        }

    print(f"[节点] 成功检索到 {len(docs)} 个文档，准备生成响应\n")
    return {
        "retrieved_docs": docs,
        "next_step": "response_generation"
    }


def order_handler_node(state: CustomerServiceState) -> dict:
    """
    订单查询处理节点
    """
    entities = state.get("entities", {})
    order_id = entities.get("订单号") or entities.get("order_id")

    if not order_id:
        return {
            "final_response": "请提供您的订单号，格式如：ORD001",
            "next_step": "end"
        }

    # 调用订单查询工具
    order_info = query_order(order_id)

    tool_result = {
        "order": order_info
    }

    return {
        "tool_results": tool_result,
        "next_step": "response_generation"
    }


def payment_handler_node(state: CustomerServiceState) -> dict:
    """
    支付处理节点
    """
    entities = state.get("entities", {})
    order_id = entities.get("订单号") or entities.get("order_id")

    if not order_id:
        return {
            "final_response": "请提供需要支付的订单号",
            "next_step": "end"
        }

    # 模拟调用支付工具
    payment_info = process_payment(order_id, 299.00)

    return {
        "tool_results": {"payment": payment_info},
        "next_step": "response_generation"
    }


def refund_handler_node(state: CustomerServiceState) -> dict:
    """
    退款处理节点
    """
    entities = state.get("entities", {})
    order_id = entities.get("订单号") or entities.get("order_id")
    messages = state["messages"]
    reason = messages[-1].content

    if not order_id:
        return {
            "final_response": "请提供需要退款的订单号",
            "next_step": "end"
        }

    # 调用退款工具
    refund_info = process_refund(order_id, reason)

    return {
        "tool_results": {"refund": refund_info},
        "next_step": "response_generation"
    }


def logistics_handler_node(state: CustomerServiceState) -> dict:
    """
    物流查询节点
    """
    entities = state.get("entities", {})
    tracking_number = entities.get("快递单号") or entities.get("tracking_number")

    if not tracking_number:
        # 尝试通过订单号查询
        order_id = entities.get("订单号") or entities.get("order_id")
        if order_id:
            order_info = query_order(order_id)
            tracking_number = order_info.get("tracking_number")

    if not tracking_number:
        return {
            "final_response": "请提供您的快递单号或订单号",
            "next_step": "end"
        }

    # 查询物流
    logistics_info = query_logistics(tracking_number)

    return {
        "tool_results": {"logistics": logistics_info},
        "next_step": "response_generation"
    }


def complaint_handler_node(state: CustomerServiceState) -> dict:
    """
    投诉处理节点
    """
    messages = state["messages"]
    complaint_content = messages[-1].content

    response = f"""非常抱歉给您带来了不好的体验。我们已经记录了您的反馈：

"{complaint_content}"

我们会尽快处理您的投诉，并在24小时内给您回复。如需紧急处理，建议您转接人工客服。

是否需要为您转接人工客服？"""

    return {
        "final_response": response,
        "next_step": "end"
    }


def chitchat_handler_node(state: CustomerServiceState) -> dict:
    """
    闲聊处理节点
    """
    messages = state["messages"]
    user_message = messages[-1].content

    chitchat_prompt = f"""
你是一个友好的客服助手。用户说：{user_message}

请给出简短友好的回复，然后引导用户提出实际问题。回复要简洁（不超过50字）。
"""

    try:
        response = llm.invoke(chitchat_prompt)
        return {
            "final_response": response.content,
            "next_step": "end"
        }
    except Exception as e:
        return {
            "final_response": "感谢您的留言！请问有什么可以帮到您的吗？",
            "next_step": "end"
        }


def response_generation_node(state: CustomerServiceState) -> dict:
    """
    响应生成节点
    """
    print("\n[节点] 进入响应生成节点 (response_generation_node)")

    messages = state["messages"]
    retrieved_docs = state.get("retrieved_docs", [])
    tool_results = state.get("tool_results", {})

    # 构建上下文
    context = ""

    if retrieved_docs:
        print(f"[响应生成] 使用RAG检索到的 {len(retrieved_docs)} 个文档作为上下文")
        context += "参考知识库：\n"
        for doc in retrieved_docs:
            context += f"- {doc.page_content}\n"
    else:
        print(f"[响应生成] 没有RAG文档，将直接使用LLM生成响应")

    if tool_results:
        print(f"[响应生成] 使用工具调用结果: {list(tool_results.keys())}")
        context += f"\n查询结果：\n{json.dumps(tool_results, ensure_ascii=False, indent=2)}"

    # 生成响应
    prompt = f"""
你是一个专业的客服助手，根据以下信息回答用户问题。

用户问题：{messages[-1].content}

{context}

要求：
- 语气友好专业
- 回答准确简洁
- 如果信息充足，直接给出答案
- 如果信息不足，礼貌地请求补充
- 不要编造信息
"""

    try:
        print("[响应生成] 正在调用LLM生成最终响应...")
        response = llm.invoke(prompt)
        print("[响应生成] 响应生成成功\n")
        return {
            "final_response": response.content,
            "next_step": "end"
        }
    except Exception as e:
        print(f"生成响应失败: {e}")
        return {
            "final_response": "抱歉，我遇到了一些问题。请稍后再试或转接人工客服。",
            "next_step": "end"
        }


def transfer_to_human_node(state: CustomerServiceState) -> dict:
    """
    转接人工节点
    """
    return {
        "need_human": True,
        "final_response": "正在为您转接人工客服，请稍候...\n\n在线客服工作时间：9:00-18:00\n客服热线：400-XXX-XXXX",
        "next_step": "end"
    }
