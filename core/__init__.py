"""
Internal enterprise query assistant core module
"""
from .main import EnterpriseQueryBot

# For backward compatibility, keep the old name as an alias
CustomerServiceBot = EnterpriseQueryBot

__version__ = "1.0.0"
__all__ = ["EnterpriseQueryBot", "CustomerServiceBot"]
