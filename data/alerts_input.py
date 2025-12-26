"""
Alert Input Dataset
Entry point for the Agentic Alert Resolution System
Each alert represents a triggered monitoring rule for a specific customer
"""

ALERTS = [
    {
        "alert_id": "A-001",
        "scenario_code": "VELOCITY_SPIKE",
        "subject_id": "CUST-101",
        "description": "Multiple high-value transactions in short time window"
    },
    {
        "alert_id": "A-002",
        "scenario_code": "STRUCTURING",
        "subject_id": "CUST-102",
        "description": "Repeated cash deposits just below reporting threshold"
    },
    {
        "alert_id": "A-003",
        "scenario_code": "KYC_INCONSISTENCY",
        "subject_id": "CUST-103",
        "description": "Transaction behavior inconsistent with declared profile"
    },
    {
        "alert_id": "A-004",
        "scenario_code": "SANCTIONS_MATCH",
        "subject_id": "CUST-104",
        "description": "Counterparty name fuzzy-matched with sanctions list"
    },
    {
        "alert_id": "A-005",
        "scenario_code": "DORMANT_ACCOUNT",
        "subject_id": "CUST-105",
        "description": "Dormant account suddenly reactivated with risky activity"
    }
    # {
    #     "alert_id": "A-006",
    #     "scenario_code": "DORMANT_ACCOUNT",
    #     "subject_id": "CUST-106",
    #     "description": "Dormant account suddenly reactivated with risky activity"
    # }
]