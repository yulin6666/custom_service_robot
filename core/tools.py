"""
模拟工具调用（订单查询、支付等）
"""
import random
from datetime import datetime, timedelta


def query_order(order_id: str) -> dict:
    """
    模拟订单查询工具
    """
    # 模拟订单数据
    mock_orders = {
        "ORD001": {
            "order_id": "ORD001",
            "status": "已发货",
            "products": ["商品A", "商品B"],
            "total_amount": 299.00,
            "create_time": "2024-12-01 10:30:00",
            "logistics": "圆通快递",
            "tracking_number": "YT1234567890"
        },
        "ORD002": {
            "order_id": "ORD002",
            "status": "待支付",
            "products": ["商品C"],
            "total_amount": 99.00,
            "create_time": "2024-12-03 09:15:00",
            "logistics": None,
            "tracking_number": None
        }
    }

    # 如果订单存在，返回数据，否则返回空
    if order_id in mock_orders:
        return mock_orders[order_id]
    else:
        # 生成随机模拟订单
        return {
            "order_id": order_id,
            "status": random.choice(["已发货", "待发货", "已完成"]),
            "products": [f"商品{random.randint(1, 10)}"],
            "total_amount": round(random.uniform(50, 500), 2),
            "create_time": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S"),
            "logistics": random.choice(["顺丰快递", "圆通快递", "中通快递"]),
            "tracking_number": f"SF{random.randint(1000000000, 9999999999)}"
        }


def process_payment(order_id: str, amount: float) -> dict:
    """
    模拟支付处理
    返回支付链接
    """
    payment_link = f"https://pay.example.com/pay?order_id={order_id}&amount={amount}"

    return {
        "success": True,
        "payment_link": payment_link,
        "message": f"请点击链接完成支付: {payment_link}",
        "qr_code": f"https://pay.example.com/qrcode/{order_id}"
    }


def process_refund(order_id: str, reason: str = "") -> dict:
    """
    模拟退款申请
    """
    refund_id = f"REF{random.randint(100000, 999999)}"

    return {
        "success": True,
        "refund_id": refund_id,
        "message": f"退款申请已提交，退款单号: {refund_id}",
        "estimated_time": "3-5个工作日",
        "status_link": f"https://service.example.com/refund/{refund_id}"
    }


def query_logistics(tracking_number: str) -> dict:
    """
    模拟物流查询
    """
    # 模拟物流信息
    logistics_info = [
        {"time": "2024-12-03 10:00:00", "status": "已签收", "location": "北京市朝阳区"},
        {"time": "2024-12-03 08:30:00", "status": "派送中", "location": "北京市朝阳区"},
        {"time": "2024-12-02 15:20:00", "status": "到达北京转运中心", "location": "北京市"},
        {"time": "2024-12-01 20:00:00", "status": "已发货", "location": "上海市"},
    ]

    return {
        "tracking_number": tracking_number,
        "current_status": logistics_info[0]["status"],
        "history": logistics_info,
        "track_link": f"https://express.example.com/track/{tracking_number}"
    }


def get_available_tools():
    """
    获取所有可用工具的描述
    """
    return {
        "query_order": "查询订单信息，需要订单号",
        "process_payment": "处理支付，需要订单号和金额",
        "process_refund": "申请退款，需要订单号和退款原因",
        "query_logistics": "查询物流信息，需要快递单号"
    }
