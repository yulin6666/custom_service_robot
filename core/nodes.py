"""
LangGraph节点定义
"""
import json
from typing import Any
from langchain_core.messages import HumanMessage, AIMessage

from .models import EnterpriseQueryState
from .config import llm, INTENT_CONFIDENCE_THRESHOLD
from .knowledge_base import knowledge_base
from .tools import query_employee_info, query_department_info


def intent_recognition_node(state: EnterpriseQueryState) -> dict:
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

【咨询类】- 用户在询问政策、规则、流程、如何操作等企业内部信息
- greeting: 问候、打招呼（你好、在吗）
- admin_inquiry: 行政管理咨询（如何申请办公用品、会议室预订、班车时刻、工牌补办、快递寄送等）
- hr_inquiry: 人力资源咨询（如何申请年假、工资发放、社保公积金、内部转岗、培训报名、离职流程等）
- it_inquiry: IT办公咨询（OA密码、软件权限、电脑故障、VPN连接、企业邮箱、Wi-Fi等）
- legal_inquiry: 法务合规咨询（合同审核、保密协议、知识产权、投诉举报等）
- finance_inquiry: 财务报销咨询（差旅费报销、日常报销、发票查验、个税、备用金等）
- procurement_inquiry: 采购管理咨询（采购申请、供应商选择、货物验收、采购纠纷等）
- general_inquiry: 通用咨询（无法明确分类的企业信息查询）
- chitchat: 闲聊（天气、笑话等非业务话题）

【特殊类】
- transfer_human: 明确要求转人工（转人工、找人工客服、联系HR、联系行政等）

重要提示：
- 仔细识别问题所属的部门领域（行政、人力、IT、法务、财务、采购）
- 如果是询问"如何"、"什么情况"、"怎么办"、"流程"、"政策"等，选择对应部门的 inquiry 类型
- 如果无法明确分类，选择 general_inquiry

返回格式：
{{"intent": "意图类型", "confidence": 0.95, "entities": {{"部门": "行政部", "关键词": "会议室"}}}}

只返回JSON，不要其他内容。
"""

    try:
        response = llm.invoke(intent_prompt)
        result = json.loads(response.content)
        intent = result.get("intent", "general_inquiry")
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
            "intent": "general_inquiry",
            "intent_confidence": 0.3,
            "entities": {},
            "next_step": "router"
        }


def router_node(state: EnterpriseQueryState) -> str:
    """
    路由分发节点 - 根据意图决定下一步
    """
    intent = state.get("intent", "general_inquiry")
    confidence = state.get("intent_confidence", 0.0)

    print(f"\n[路由] 进入路由节点")
    print(f"[路由] 意图: {intent}, 置信度: {confidence:.2f}")

    # 低置信度或明确要求转人工
    if confidence < INTENT_CONFIDENCE_THRESHOLD or intent == "transfer_human":
        route = "transfer_to_human"
        print(f"[路由] 决策: 转人工 (置信度过低或用户请求)")
        return route

    # 根据意图路由 - 所有企业查询都走知识库检索
    intent_routes = {
        "greeting": "greeting_handler",
        "admin_inquiry": "knowledge_retrieval",
        "hr_inquiry": "knowledge_retrieval",
        "it_inquiry": "knowledge_retrieval",
        "legal_inquiry": "knowledge_retrieval",
        "finance_inquiry": "knowledge_retrieval",
        "procurement_inquiry": "knowledge_retrieval",
        "general_inquiry": "knowledge_retrieval",
        "chitchat": "chitchat_handler"
    }

    route = intent_routes.get(intent, "knowledge_retrieval")
    print(f"[路由] 决策: 路由到 {route}\n")
    return route


def greeting_handler_node(state: EnterpriseQueryState) -> dict:
    """
    问候处理节点
    """
    greeting_response = """您好！我是企业内部查询助手，很高兴为您服务！

我可以帮您查询：
- 📋 行政管理：办公用品、会议室、班车、工牌等
- 👥 人力资源：年假、工资、社保、培训、离职等
- 💻 IT办公：OA系统、软件权限、电脑故障、VPN等
- ⚖️ 法务合规：合同审核、保密协议、知识产权等
- 💰 财务报销：差旅费、日常报销、发票、备用金等
- 🛒 采购管理：采购申请、供应商、验收流程等

请问有什么可以帮到您的吗？"""

    return {
        "final_response": greeting_response,
        "next_step": "end"
    }


def knowledge_retrieval_node(state: EnterpriseQueryState) -> dict:
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


def order_handler_node(state: EnterpriseQueryState) -> dict:
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


def payment_handler_node(state: EnterpriseQueryState) -> dict:
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


def refund_handler_node(state: EnterpriseQueryState) -> dict:
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


def logistics_handler_node(state: EnterpriseQueryState) -> dict:
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


def complaint_handler_node(state: EnterpriseQueryState) -> dict:
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


def chitchat_handler_node(state: EnterpriseQueryState) -> dict:
    """
    闲聊处理节点
    """
    messages = state["messages"]
    user_message = messages[-1].content

    chitchat_prompt = f"""
你是一个友好的企业内部查询助手。用户说：{user_message}

请给出简短友好的回复，然后引导用户提出企业相关的问题（如行政、人力、IT、法务、财务、采购等）。回复要简洁（不超过50字）。
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


def response_generation_node(state: EnterpriseQueryState) -> dict:
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
        context += "参考企业知识库：\n"
        for doc in retrieved_docs:
            context += f"- {doc.page_content}\n"
    else:
        print(f"[响应生成] 没有RAG文档，将直接使用LLM生成响应")

    if tool_results:
        print(f"[响应生成] 使用工具调用结果: {list(tool_results.keys())}")
        context += f"\n查询结果：\n{json.dumps(tool_results, ensure_ascii=False, indent=2)}"

    # 生成响应
    prompt = f"""
你是一个专业的企业内部查询助手，根据以下信息回答员工的问题。

员工问题：{messages[-1].content}

{context}

要求：
- 语气友好专业
- 回答准确简洁
- 如果信息充足，直接给出答案
- 如果信息不足，礼貌地建议员工联系相关部门（行政、人力、IT、法务、财务、采购等）
- 不要编造信息，严格基于知识库内容回答
- 如果知识库中有联系方式或流程步骤，请详细列出
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


def transfer_to_human_node(state: EnterpriseQueryState) -> dict:
    """
    转接人工节点
    """
    return {
        "need_human": True,
        "final_response": """正在为您转接相关部门，请稍候...

您可以直接联系：
📋 行政部：分机8888 | admin@company.com
👥 人力资源部：分机8899 | hr@company.com
💻 IT部：分机6666 | it@company.com
⚖️ 法务部：分机7777 | legal@company.com
💰 财务部：分机8866 | finance@company.com
🛒 采购部：分机8855 | purchase@company.com

总机：010-XXXX-XXXX（工作时间：9:00-18:00）""",
        "next_step": "end"
    }
