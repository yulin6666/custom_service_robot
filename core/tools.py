"""
Simulated tool calls (enterprise information queries, etc.)
"""
import random
from datetime import datetime, timedelta


def query_employee_info(employee_id: str = None, name: str = None) -> dict:
    """
    Simulated employee information query tool
    """
    # Simulated employee data
    mock_employees = {
        "EMP001": {
            "employee_id": "EMP001",
            "name": "Zhang San",
            "department": "Technology Department",
            "position": "Senior Engineer",
            "email": "zhangsan@company.com",
            "extension": "6688",
            "join_date": "2020-03-15"
        },
        "EMP002": {
            "employee_id": "EMP002",
            "name": "Li Si",
            "department": "Human Resources Department",
            "position": "HR Manager",
            "email": "lisi@company.com",
            "extension": "8899",
            "join_date": "2018-06-01"
        }
    }

    if employee_id and employee_id in mock_employees:
        return mock_employees[employee_id]
    else:
        return {
            "message": "Employee information not found. Please contact the Human Resources Department.",
            "hr_contact": "Extension 8899 | hr@company.com"
        }


def query_department_info(department_name: str) -> dict:
    """
    Simulated department information query tool
    """
    # Simulated department data
    departments = {
        "Administration Department": {
            "name": "Administration Department",
            "extension": "8888",
            "email": "admin@company.com",
            "location": "3F Room 301",
            "manager": "Manager Wang",
            "services": ["Office supplies request", "Meeting room booking", "Courier service", "Badge processing"]
        },
        "Human Resources Department": {
            "name": "Human Resources Department",
            "extension": "8899",
            "email": "hr@company.com",
            "location": "3F Room 302",
            "manager": "Manager Li",
            "services": ["Recruitment", "Training", "Compensation & Benefits", "Employee Relations"]
        },
        "IT Department": {
            "name": "IT Department",
            "extension": "6666",
            "email": "it@company.com",
            "location": "4F Room 401",
            "manager": "Manager Zhao",
            "services": ["OA system", "Software permissions", "Computer repair", "Network support"]
        },
        "Finance Department": {
            "name": "Finance Department",
            "extension": "8866",
            "email": "finance@company.com",
            "location": "3F Room 303",
            "manager": "Manager Liu",
            "services": ["Expense reimbursement", "Invoice management", "Payroll", "Budget management"]
        }
    }

    if department_name in departments:
        return departments[department_name]
    else:
        return {
            "message": f"No information found for department '{department_name}'",
            "suggestion": "Please verify the department name or contact the Administration Department"
        }


# Kept for backward compatibility (no longer in use)
def query_order(order_id: str) -> dict:
    """Deprecated: Order query tool (not needed for internal enterprise queries)"""
    return {"message": "This feature is no longer in use. For internal enterprise queries, please use the knowledge base search."}


def process_payment(order_id: str, amount: float) -> dict:
    """Deprecated: Payment processing tool (not needed for internal enterprise queries)"""
    return {"message": "This feature is no longer in use. For internal enterprise queries, please use the knowledge base search."}


def process_refund(order_id: str, reason: str = "") -> dict:
    """Deprecated: Refund processing tool (not needed for internal enterprise queries)"""
    return {"message": "This feature is no longer in use. For internal enterprise queries, please use the knowledge base search."}


def query_logistics(tracking_number: str) -> dict:
    """Deprecated: Logistics query tool (not needed for internal enterprise queries)"""
    return {"message": "This feature is no longer in use. For internal enterprise queries, please use the knowledge base search."}


def get_available_tools():
    """
    Get descriptions of all available tools
    """
    return {
        "query_employee_info": "Query employee information by employee ID or name",
        "query_department_info": "Query department information by department name"
    }
