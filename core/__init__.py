"""
企业内部查询助手核心模块
"""
from .main import EnterpriseQueryBot

# 为了向后兼容，保留旧名称的别名
CustomerServiceBot = EnterpriseQueryBot

__version__ = "1.0.0"
__all__ = ["EnterpriseQueryBot", "CustomerServiceBot"]
