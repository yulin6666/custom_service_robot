"""
LangGraph node definitions
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
    Intent recognition node
    """
    messages = state["messages"]
    last_message = messages[-1].content

    print(f"\n[Node] Enter intent recognition node (intent_recognition_node)")
    print(f"[Node] User message: {last_message}")

    # Use LLM for intent classification
    intent_prompt = f"""
Analyze the intent of the following user message and return JSON format.

User message: {last_message}

Please identify one intent from the following types:

[Inquiry]
- greeting: Greetings (hello, are you there)
- admin_inquiry: Administrative inquiries (how to request office supplies, meeting room booking, shuttle schedule, badge replacement, courier service, etc.)
- hr_inquiry: Human resources inquiries (how to apply for annual leave, salary payment, social insurance, internal transfer, training enrollment, resignation process, etc.)
- it_inquiry: IT office inquiries (OA password, software permission, computer issues, VPN connection, corporate email, Wi-Fi, etc.)
- legal_inquiry: Legal and compliance inquiries (contract review, NDA, intellectual property, complaints and reports, etc.)
- finance_inquiry: Finance reimbursement inquiries (travel reimbursement, daily reimbursement, invoice verification, personal income tax, petty cash, etc.)
- procurement_inquiry: Procurement management inquiries (procurement request, supplier selection, goods acceptance, procurement disputes, etc.)
- general_inquiry: General inquiries (enterprise information queries that cannot be clearly categorized)
- chitchat: Casual chat (weather, jokes, and other non-business topics)

[Special]
- transfer_human: Explicitly requests transfer to human support (transfer to human, find a human agent, contact HR, contact admin, etc.)

Important notes:
- Carefully identify which domain the question belongs to (administration, HR, IT, legal, finance, procurement)
- If the user asks "how", "under what circumstances", "what should I do", "process", or "policy", choose the corresponding department inquiry type
- If it cannot be clearly classified, choose general_inquiry

Return format:
{{"intent": "intent_type", "confidence": 0.95, "entities": {{"department": "Administration Department", "keyword": "meeting room"}}}}

Return JSON only, no other content.
"""

    try:
        response = llm.invoke(intent_prompt)
        result = json.loads(response.content)
        intent = result.get("intent", "general_inquiry")
        confidence = result.get("confidence", 0.5)

        print(f"[Node] Recognized intent: {intent} (confidence: {confidence:.2f})")

        return {
            "intent": intent,
            "intent_confidence": confidence,
            "entities": result.get("entities", {}),
            "next_step": "router"
        }
    except Exception as e:
        print(f"Intent recognition failed: {e}")
        return {
            "intent": "general_inquiry",
            "intent_confidence": 0.3,
            "entities": {},
            "next_step": "router"
        }


def router_node(state: EnterpriseQueryState) -> str:
    """
    Routing node - decides the next step based on intent
    """
    intent = state.get("intent", "general_inquiry")
    confidence = state.get("intent_confidence", 0.0)

    print(f"\n[Router] Enter routing node")
    print(f"[Router] Intent: {intent}, confidence: {confidence:.2f}")

    # Low confidence or explicit transfer-to-human request
    if confidence < INTENT_CONFIDENCE_THRESHOLD or intent == "transfer_human":
        route = "transfer_to_human"
        print(f"[Router] Decision: Transfer to human (low confidence or user request)")
        return route

    # Route by intent - all enterprise queries use knowledge base retrieval
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
    print(f"[Router] Decision: Route to {route}\n")
    return route


def greeting_handler_node(state: EnterpriseQueryState) -> dict:
    """
    Greeting handler node
    """
    greeting_response = """Hello! I am your internal enterprise query assistant. Glad to help!

I can help you with:
- Administration: office supplies, meeting rooms, shuttle service, badges, etc.
- Human Resources: annual leave, payroll, social insurance, training, resignation, etc.
- IT Office: OA system, software permissions, computer issues, VPN, etc.
- Legal & Compliance: contract review, NDA, intellectual property, etc.
- Financial Reimbursement: travel expenses, daily reimbursement, invoices, petty cash, etc.
- Procurement Management: procurement requests, suppliers, acceptance process, etc.

How can I help you today?"""

    return {
        "final_response": greeting_response,
        "next_step": "end"
    }


def knowledge_retrieval_node(state: EnterpriseQueryState) -> dict:
    """
    Knowledge base retrieval node (RAG)
    """
    print("\n[Node] Enter knowledge retrieval node (knowledge_retrieval_node)")

    messages = state["messages"]
    query = messages[-1].content

    # Retrieve from knowledge base
    docs = knowledge_base.search(query, k=3)

    if not docs:
        print("[Node] No relevant documents retrieved. Will generate response with empty context\n")
        return {
            "retrieved_docs": [],
            "next_step": "response_generation"
        }

    print(f"[Node] Successfully retrieved {len(docs)} documents. Preparing response generation\n")
    return {
        "retrieved_docs": docs,
        "next_step": "response_generation"
    }


def complaint_handler_node(state: EnterpriseQueryState) -> dict:
    """
    Complaint handler node
    """
    messages = state["messages"]
    complaint_content = messages[-1].content

    response = f"""We sincerely apologize for your unpleasant experience. We have recorded your feedback:

"{complaint_content}"

We will process your complaint as soon as possible and reply within 24 hours. For urgent cases, we recommend transferring to a human agent.

Would you like me to transfer you to a human agent?"""

    return {
        "final_response": response,
        "next_step": "end"
    }


def chitchat_handler_node(state: EnterpriseQueryState) -> dict:
    """
    Chitchat handler node
    """
    messages = state["messages"]
    user_message = messages[-1].content

    chitchat_prompt = f"""
You are a friendly internal enterprise query assistant. The user says: {user_message}

Please provide a short and friendly reply, then guide the user to ask enterprise-related questions (such as administration, HR, IT, legal, finance, procurement, etc.). Keep the reply concise (no more than 50 words).
"""

    try:
        response = llm.invoke(chitchat_prompt)
        return {
            "final_response": response.content,
            "next_step": "end"
        }
    except Exception:
        return {
            "final_response": "Thanks for your message! How can I assist you today?",
            "next_step": "end"
        }


def response_generation_node(state: EnterpriseQueryState) -> dict:
    """
    Response generation node
    """
    print("\n[Node] Enter response generation node (response_generation_node)")

    messages = state["messages"]
    retrieved_docs = state.get("retrieved_docs", [])
    tool_results = state.get("tool_results", {})

    # Build context
    context = ""

    if retrieved_docs:
        print(f"[Response Generation] Using {len(retrieved_docs)} RAG-retrieved documents as context")
        context += "Reference enterprise knowledge base:\n"
        for doc in retrieved_docs:
            context += f"- {doc.page_content}\n"
    else:
        print("[Response Generation] No RAG documents. Will directly use LLM to generate response")

    if tool_results:
        print(f"[Response Generation] Using tool call results: {list(tool_results.keys())}")
        context += f"\nQuery results:\n{json.dumps(tool_results, ensure_ascii=False, indent=2)}"

    # Generate response
    prompt = f"""
You are a professional internal enterprise query assistant. Answer employee questions based on the following information.

Employee question: {messages[-1].content}

{context}

Requirements:
- Friendly and professional tone
- Accurate and concise answer
- If information is sufficient, provide the direct answer
- If information is insufficient, politely suggest the employee contact the relevant department (administration, HR, IT, legal, finance, procurement, etc.)
- Do not fabricate information; strictly answer based on the knowledge base content
- If contact details or process steps are available in the knowledge base, list them in detail
"""

    try:
        print("[Response Generation] Calling LLM to generate final response...")
        response = llm.invoke(prompt)
        print("[Response Generation] Response generated successfully\n")
        return {
            "final_response": response.content,
            "next_step": "end"
        }
    except Exception as e:
        print(f"Response generation failed: {e}")
        return {
            "final_response": "Sorry, I encountered an issue. Please try again later or transfer to a human agent.",
            "next_step": "end"
        }


def transfer_to_human_node(state: EnterpriseQueryState) -> dict:
    """
    Transfer to human node
    """
    return {
        "need_human": True,
        "final_response": """Transferring you to the relevant department. Please wait...

You can directly contact:
Administration Department: Extension 8888 | admin@company.com
Human Resources Department: Extension 8899 | hr@company.com
IT Department: Extension 6666 | it@company.com
Legal Department: Extension 7777 | legal@company.com
Finance Department: Extension 8866 | finance@company.com
Procurement Department: Extension 8855 | purchase@company.com

Switchboard: 010-XXXX-XXXX (Business hours: 9:00-18:00)""",
        "next_step": "end"
    }
