# 🏦 Agentic Alert Resolution System (AARS)

A multi-agent system for automated investigation and resolution of banking transaction monitoring alerts. Built using a **Hub-and-Spoke architecture** where specialized agents collaborate to analyze alerts based on Standard Operating Procedures (SOPs).

---

## 📁 Project Structure

```
├── main.py                          # Entry point - orchestrates alert processing
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py              # Hub Agent - routes alerts to 
│   ├── investigator.py              # Spoke - queries transaction 
│   ├── context_agent.py             # Spoke - retrieves KYC profiles
│   └── adjudicator.py               # Spoke - applies SOP rules & makes decisions
├── actions/
│   ├── __init__.py
│   └── action_executor.py           # Executes resolution actions (SAR,RFI, IVR, Close)
├── config/
│   ├── __init__.py
│   └── sop_rules.py                 # SOP definitions for each alert 
├── data/
│   ├── __init__.py
│   ├── alerts_input.py              # 5 pre-generated alert scenarios
│   ├── kyc_db.py                    # Mock KYC database
│   └── historic_transactions_db.py  # Mock transaction history
├── utils/
│   ├── __init__.py
│   └── logger.py                    # Audit trail logging

```

---

## 🤖 Agent Architecture

### Hub Agent
| Agent | Responsibility |
|-------|----------------|
| **Orchestrator** | Routes alerts to appropriate spoke agents, coordinates investigation workflow |

### Spoke Agents
| Agent | Responsibility |
|-------|----------------|
| **Investigator** | Queries historical transaction data (90-day lookback) |
| **Context Gatherer** | Retrieves customer KYC profiles and risk ratings |
| **Adjudicator** | Applies if/then/else SOP logic to make resolution decisions |

### Action Execution Module (AEM)
Simulates tool execution based on adjudicator decisions:
- **SAR Preparer**: Escalates suspicious cases to human analysts
- **RFI (Email)**: Requests information from customers
- **IVR (Phone)**: Initiates verification calls
- **Close**: Marks alerts as false positives

---

## 📊 Mock Data

### Alert Scenarios (5 Types)
```python
    {
        "alert_id": "A-001",
        "scenario_code": "VELOCITY_SPIKE",
        "subject_id": "CUST-101",
        "description": "Multiple high-value transactions in short time window"
    }
    # ... more alerts
```
### KYC Database
```python
KYC_DB = {
    "CUST-101": {
        "name": "Anuj Kumar",
        "occupation": "Teacher",
        "declared_income": 50000,
        "source_of_funds": "Salary",
        "risk_rating": "LOW",
        "account_age_months": 36
    }
    # ... more customers
}
```

### Historic Transactions Database
```python

HISTORIC_TRANSACTIONS_DB = {
    # A-001: Velocity Spike
    "VELOCITY_SPIKE": {
        "CUST-101": {
            "historical_max_txn_90d": 1500,
            "txn_count_last_48h": 6,
            "prior_velocity_spike": False,
            "avg_txns_per_month": 3
        }
    }
    # ... more Transaction Scenarios
}
```
---

## 📋 SOP Rules

```python
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
    }
    # ... more rules
}
```

All 5 scenarios have defined decision paths in `config/sop_rules.py`.

---

## 🔄 Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         ALERT INPUT                             │
│              (alert_id, scenario_code, subject_id)              │
└─────────────────────┬───────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (Hub)                           │
│                  Routes to Spoke Agents                         │
└─────────────────────┬───────────────────────────────────────────┘
                      ▼
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│  INVESTIGATOR │           │    CONTEXT    │
│    (Spoke)    │           │   GATHERER    │
│               │           │    (Spoke)    │
│ Query Txn DB  │           │ Query KYC DB  │
└───────┬───────┘           └───────┬───────┘
        │                           │
        └───────────┬───────────────┘
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ADJUDICATOR (Spoke)                          │
│              Apply SOP Rules → Make Decision                    │
│    (ESCALATE_FOR_SAR | REQUEST_INFORMATION | CLOSE)             │
└─────────────────────┬───────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│               ACTION EXECUTION MODULE (AEM)                     │
│         Execute: SAR Prep | RFI Email | IVR Call | Close        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📤 Sample Output

```
======================================================================
 PROCESSING ALERT: A-001 | Scenario: VELOCITY_SPIKE
======================================================================
[10:35:41] [Orchestrator Agent] Routing alert A-001 to Investigator and Context Gatherer agents
[10:35:41] [Investigator Agent] Querying transaction history for CUST-101 (Scenario: VELOCITY_SPIKE)
    └─  Data Retrieved from Historic Transactions DB:
       • historical_max_txn_90d: 1500
       • txn_count_last_48h: 6
       • prior_velocity_spike: False
       • avg_txns_per_month: 3
[10:35:41] [Context Gatherer Agent] Retrieving KYC profile for CUST-101
    └─  Data Retrieved from KYC Database:
       • name: John Doe
       • occupation: Teacher
       • declared_income: 50000
       • source_of_funds: Salary
       • risk_rating: LOW
       • account_age_months: 36
[10:35:41] [Orchestrator Agent] All data gathered. Forwarding to Adjudicator for decision...
[10:35:41] [Adjudicator Agent] Applying SOP rule RUL-A001 for VELOCITY_SPIKE

----------------------------------------------------------------------
ADJUDICATION DECISION
----------------------------------------------------------------------
Recommendation: ESCALATE_FOR_SAR
Confidence: 95.0%
Rationale: Velocity spike detected: 6 transactions in 48 hours with no prior high-velocity behavior. Estimated transaction volume ($9,000) is inconsistent with declared income ($50,000) and source of funds ('Salary'), indicating unexplained activity.
----------------------------------------------------------------------

======================================================================
ACTION EXECUTION
======================================================================
Action Executed: SAR Preparer Module Activated.
Case [A-001] pre-populated and routed to Human Queue.
Rationale: Velocity spike detected: 6 transactions in 48 hours with no prior high-velocity behavior. Estimated transaction volume ($9,000) is inconsistent with declared income ($50,000) and source of funds ('Salary'), indicating unexplained activity.
======================================================================

Alert A-001 processing complete.
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/aars-fintech.git

```

### Run the System
```bash
python main.py
```

### Output
All 5 alerts will be processed with decisions:
| Alert | Decision |
|-------|-------------------|
| A-001 | ESCALATE_FOR_SAR |
| A-002 | REQUEST_INFORMATION |
| A-003 | CLOSE_FALSE_POSITIVE |
| A-004 | ESCALATE_FOR_SAR |
| A-005 | ESCALATE_FOR_SAR |

---

## 📝 Key Features

- ✅ **Hub-and-Spoke Architecture**: Clear separation of concerns
- ✅ **5 Alert Scenarios**: Complete coverage of banking AML use cases
- ✅ **SOP-Driven Decisions**: Configurable rule-based logic
- ✅ **Tool Simulation**: SAR, RFI, IVR, and Close actions
- ✅ **Audit Trail**: Timestamped logging of all agent actions
- ✅ **Extensible Design**: Easy to add new scenarios or rules

---

