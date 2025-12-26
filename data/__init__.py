"""
Data module initialization
Exports all mock databases and alert inputs
"""

from .alerts_input import ALERTS
from .historic_transactions_db import HISTORIC_TRANSACTIONS_DB
from .kyc_db import KYC_DB

__all__ = ['ALERTS', 'HISTORIC_TRANSACTIONS_DB', 'KYC_DB']