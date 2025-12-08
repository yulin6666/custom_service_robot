"""
状态定义
"""
from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
import operator


class EnterpriseQueryState(TypedDict):
    """企业查询对话状态"""
    # 消息历史
    messages: Annotated[Sequence[BaseMessage], operator.add]

    # 会话信息
    session_id: str
    user_id: Optional[str]

    # 意图识别
    intent: Optional[str]  # greeting/inquiry/admin/hr/it/legal/finance/procurement/chitchat
    intent_confidence: Optional[float]

    # 上下文信息
    entities: Optional[dict]  # 提取的实体（部门、员工信息等）

    # 知识库检索
    retrieved_docs: Optional[list]

    # 工具调用
    tool_results: Optional[dict]

    # 人工转接
    need_human: bool

    # 响应生成
    final_response: Optional[str]

    # 流程控制
    next_step: Optional[str]


# 兼容性别名
CustomerServiceState = EnterpriseQueryState
