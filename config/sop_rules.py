"""
SOP / Meta Configuration File
This file defines the Standard Operating Procedures (SOPs) for each alert scenario.
These rules are POLICY DEFINITIONS, not executable logic.
The actual rule enforcement is implemented in the Adjudicator Agent.
"""

SOP_RULES = {
    # ============================================================
    # RUL-A001 : Velocity Spike (Layering)
    # ============================================================
    "VELOCITY_SPIKE": {
        "rule_id": "RUL-A001",
        "scenario_code": "VELOCITY_SPIKE",
        "description": (
            "Escalate when a customer exhibits a first-time high transaction velocity "
            "that is not supported by declared income or business activity. "
            "Close the alert if the spike is consistent with a known business cycle."
    ),
        "conditions": [
            "Transaction_Count_Last_48h > 5",
            "Is_First_Velocity_Spike_90d == True",
            "Income_Match == False"
        ],
        "possible_actions": [
            "ESCALATE_FOR_SAR",
            "CLOSE_FALSE_POSITIVE"
        ]
    },

    
    # ============================================================
    # RUL-A002 : Below-Threshold Structuring
    # ============================================================
    "STRUCTURING": {
        "rule_id": "RUL-A002",
        "scenario_code": "STRUCTURING",
        "description": (
            "Evaluate repeated below-threshold cash deposits for potential structuring. "
            "If deposits across linked accounts exceed the aggregate threshold without "
            "legitimate business justification, escalate for SAR preparation. "
            "If deposits are geographically diverse and align with legitimate business "
            "receipts, request additional information from the customer."
        ),
        "decision_paths": [
            {
                "conditions": [
                    "Geographically_Diverse == True",
                    "Legitimate_Business == True"
                ],
                "action": "REQUEST_INFORMATION"
            },
            {
                "conditions": [
                    "Linked_Accounts_Total > 28000",
                    "Cash_Deposits_Below_Threshold == True"
                ],
                "action": "ESCALATE_FOR_SAR"
            }
        ]
    },

    
    # ============================================================
    # RUL-A003 : KYC Inconsistency (Profile vs Transaction)
    # ============================================================
    "KYC_INCONSISTENCY": {
        "rule_id": "RUL-A003",
        "scenario_code": "KYC_INCONSISTENCY",
        "description": (
            "IF transaction type or merchant category is inconsistent with "
            "customer's declared occupation THEN escalate for SAR."
        ),
        "conditions": [
            "Occupation_Match == False",
            "Transaction_Amount >= 20000"
        ],
        "intended_action": "ESCALATE_FOR_SAR"
    },
    
    # ============================================================
    # RUL-A004 : Sanctions List Hit (Minor Match)
    # ============================================================
    "SANCTIONS_MATCH": {
        "rule_id": "RUL-A004",
        "scenario_code": "SANCTIONS_MATCH",
        "description": (
            "IF counterparty name similarity to sanctions list is high "
            "OR transaction jurisdiction is high-risk THEN escalate."
        ),
        "conditions": [
            "Similarity_Score >= 0.80",
            "Jurisdiction == High_Risk"
        ],
        "intended_action": "ESCALATE_FOR_SAR"
    },
    
    # ============================================================
    # RUL-A005 : Dormant Account Activation
    # ============================================================
    "DORMANT_ACCOUNT": {
        "rule_id": "RUL-A005",
        "scenario_code": "DORMANT_ACCOUNT",
        "description": (
            "IF a dormant account (12+ months) is reactivated with inbound funds "
            "and immediate cash withdrawal, escalate when the customer risk is HIGH "
            "and withdrawal is international. Otherwise, request information from customer."
        ),
        "conditions": [
            "Months_Inactive > 12",
            "Immediate_Withdrawal == True"
        ],
        "intended_actions": {
        "HIGH_RISK + INTERNATIONAL": "ESCALATE_FOR_SAR",
        "LOW_RISK": "REQUEST_INFORMATION"
    }
    }
}