"""
Historic Transactions Database (Simulated)
Provides pre-computed analytics and facts about customer transaction behavior
Organized by scenario for efficient lookup
"""

HISTORIC_TRANSACTIONS_DB = {
    # A-001: Velocity Spike
    "VELOCITY_SPIKE": {
        "CUST-101": {
            "historical_max_txn_90d": 1500,
            "txn_count_last_48h": 6,
            "prior_velocity_spike": False,
            "avg_txns_per_month": 3
        }
    },

    # A-002: Structuring
    "STRUCTURING": {
        "CUST-102": {
            "cash_deposits_7d": [9800, 9500, 9700],
            "linked_accounts_total": 29500,
            "geographically_diverse": True,
            "branches_used": ["NYC_001", "NYC_002", "LA_001"]
        }
    },

    # A-003: KYC Inconsistency
    "KYC_INCONSISTENCY": {
        "CUST-103": {
            "wire_amount": 20000,
            "merchant_category": "Precious Metals Trading",
            "transaction_type": "International Wire"
        }
    },

    # A-004: Sanctions Match
    "SANCTIONS_MATCH": {
        "CUST-104": {
            "counterparty_name": "AL QUDS TRADING",
            "similarity_score": 0.80,
            "bank_jurisdiction": "High Risk",
            "previous_relationship": False
        }
    },

    # A-005: Dormant Account
    "DORMANT_ACCOUNT": {
        "CUST-105": {
            "months_inactive": 14,
            "recent_inbound_amount": 15000,
            "followed_by_atm_withdrawal": True,
            "international_withdrawal": True
        }
        }

    # # A-006: Dormant Account
    # "DORMANT_ACCOUNT": {
    #     "CUST-106": {
    #         "months_inactive": 18,
    #         "recent_inbound_amount": 15000,
    #         "followed_by_atm_withdrawal": True,
    #         "international_withdrawal": False
    #     }
    # }
}