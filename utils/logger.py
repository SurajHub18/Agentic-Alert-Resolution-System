"""
Audit Trail Logger
Provides formatted console output for tracking agent actions and decisions
"""

from datetime import datetime


class AuditLogger:
    """Centralized logger for audit trail and console output"""
    
    @staticmethod
    def log_alert_start(alert_id, scenario_code):
        """Log the beginning of alert processing"""
        print("\n" + "=" * 70)
        print(f" PROCESSING ALERT: {alert_id} | Scenario: {scenario_code}")
        print("=" * 70)
    
    @staticmethod
    def log_agent_action(agent_name, message):
        """Log an agent's action or decision"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{agent_name}] {message}")
    
    @staticmethod
    def log_data_retrieval(source, data_summary):
        """Log data retrieved from mock databases"""
        print(f"    └─  Data Retrieved from {source}:")
        for key, value in data_summary.items():
            print(f"       • {key}: {value}")
    
    @staticmethod
    def log_decision(decision_data):
        """Log the adjudicator's final decision"""
        print("\n" + "-" * 70)
        print("ADJUDICATION DECISION")
        print("-" * 70)
        print(f"Recommendation: {decision_data['recommendation']}")
        print(f"Confidence: {decision_data['confidence'] * 100:.1f}%")
        print(f"Rationale: {decision_data['rationale']}")
        print("-" * 70)
    
    @staticmethod
    def log_action_execution(action_type, details):
        """Log simulated action execution"""
        print("\n" + "ACTION EXECUTION" + "\n" + "=" * 70)
        print(f"Action Type: {action_type}")
        print(f"Details:\n{details}")
        print("=" * 70 + "\n")
    
    @staticmethod
    def log_alert_complete(alert_id):
        """Log completion of alert processing"""
        print(f"Alert {alert_id} processing complete.\n")