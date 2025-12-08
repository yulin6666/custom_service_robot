"""
模拟工具调用（企业信息查询等）
"""
import random
from datetime import datetime, timedelta


def query_employee_info(employee_id: str = None, name: str = None) -> dict:
    """
    模拟员工信息查询工具
    """
    # 模拟员工数据
    mock_employees = {
        "EMP001": {
            "employee_id": "EMP001",
            "name": "张三",
            "department": "技术部",
            "position": "高级工程师",
            "email": "zhangsan@company.com",
            "extension": "6688",
            "join_date": "2020-03-15"
        },
        "EMP002": {
            "employee_id": "EMP002",
            "name": "李四",
            "department": "人力资源部",
            "position": "HR经理",
            "email": "lisi@company.com",
            "extension": "8899",
            "join_date": "2018-06-01"
        }
    }

    if employee_id and employee_id in mock_employees:
        return mock_employees[employee_id]
    else:
        return {
            "message": "未找到员工信息，请联系人力资源部查询",
            "hr_contact": "分机8899 | hr@company.com"
        }


def query_department_info(department_name: str) -> dict:
    """
    模拟部门信息查询工具
    """
    # 模拟部门数据
    departments = {
        "行政部": {
            "name": "行政部",
            "extension": "8888",
            "email": "admin@company.com",
            "location": "3楼301室",
            "manager": "王经理",
            "services": ["办公用品申请", "会议室预订", "快递寄送", "工牌办理"]
        },
        "人力资源部": {
            "name": "人力资源部",
            "extension": "8899",
            "email": "hr@company.com",
            "location": "3楼302室",
            "manager": "李经理",
            "services": ["招聘", "培训", "薪酬福利", "员工关系"]
        },
        "IT部": {
            "name": "IT部",
            "extension": "6666",
            "email": "it@company.com",
            "location": "4楼401室",
            "manager": "赵经理",
            "services": ["OA系统", "软件权限", "电脑维修", "网络支持"]
        },
        "财务部": {
            "name": "财务部",
            "extension": "8866",
            "email": "finance@company.com",
            "location": "3楼303室",
            "manager": "刘经理",
            "services": ["报销审核", "发票管理", "工资发放", "预算管理"]
        }
    }

    if department_name in departments:
        return departments[department_name]
    else:
        return {
            "message": f"未找到部门'{department_name}'的信息",
            "suggestion": "请确认部门名称或联系行政部查询"
        }


# 保留旧函数作为兼容性（但不再使用）
def query_order(order_id: str) -> dict:
    """已废弃：订单查询工具（企业内部查询不需要）"""
    return {"message": "此功能已不再使用，企业内部查询请使用知识库检索"}


def process_payment(order_id: str, amount: float) -> dict:
    """已废弃：支付处理工具（企业内部查询不需要）"""
    return {"message": "此功能已不再使用，企业内部查询请使用知识库检索"}


def process_refund(order_id: str, reason: str = "") -> dict:
    """已废弃：退款处理工具（企业内部查询不需要）"""
    return {"message": "此功能已不再使用，企业内部查询请使用知识库检索"}


def query_logistics(tracking_number: str) -> dict:
    """已废弃：物流查询工具（企业内部查询不需要）"""
    return {"message": "此功能已不再使用，企业内部查询请使用知识库检索"}


def get_available_tools():
    """
    获取所有可用工具的描述
    """
    return {
        "query_employee_info": "查询员工信息，需要工号或姓名",
        "query_department_info": "查询部门信息，需要部门名称"
    }
