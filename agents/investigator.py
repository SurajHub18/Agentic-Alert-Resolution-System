"""
Investigator Agent (Spoke)
Responsible for querying historic transaction data and providing facts
"""

from data import HISTORIC_TRANSACTIONS_DB
from utils import AuditLogger


class InvestigatorAgent:
    """Queries and analyzes historic transaction patterns"""
    
    def __init__(self):
        self.name = "Investigator Agent"
        self.logger = AuditLogger()
    
    def investigate(self, alert_data):
        """
        Simulate querying the historic transactions database
        
        Args:
            alert_data: Dictionary containing alert_id, scenario_code, subject_id
            
        Returns:
            Dictionary of investigation findings
        """
        scenario_code = alert_data["scenario_code"]
        subject_id = alert_data["subject_id"]
        
        self.logger.log_agent_action(
            self.name, 
            f"Querying transaction history for {subject_id} (Scenario: {scenario_code})"
        )
        
        # Simulate database query
        try:
            findings = HISTORIC_TRANSACTIONS_DB[scenario_code][subject_id]
            self.logger.log_data_retrieval("Historic Transactions DB", findings)
            return {
                "status": "success",
                "data": findings,
                "source": "HISTORIC_TRANSACTIONS_DB"
            }
        except KeyError:
            self.logger.log_agent_action(
                self.name, 
                f"⚠️  No transaction history found for {subject_id}"
            )
            return {
                "status": "not_found",
                "data": {},
                "source": "HISTORIC_TRANSACTIONS_DB"
            }