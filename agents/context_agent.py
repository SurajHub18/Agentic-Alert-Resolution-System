"""
Context Gatherer Agent (Spoke)
Responsible for retrieving customer KYC profiles and contextual information
"""

from data import KYC_DB
from utils import AuditLogger


class ContextGathererAgent:
    """Retrieves customer profile and risk context"""
    
    def __init__(self):
        self.name = "Context Gatherer Agent"
        self.logger = AuditLogger()
    
    def gather_context(self, alert_data):
        """
        Simulate querying the KYC database
        
        Args:
            alert_data: Dictionary containing alert_id, scenario_code, subject_id
            
        Returns:
            Dictionary of customer context
        """
        subject_id = alert_data["subject_id"]
        
        self.logger.log_agent_action(
            self.name, 
            f"Retrieving KYC profile for {subject_id}"
        )
        
        # Simulate KYC lookup
        try:
            kyc_profile = KYC_DB[subject_id]
            self.logger.log_data_retrieval("KYC Database", kyc_profile)
            return {
                "status": "success",
                "data": kyc_profile,
                "source": "KYC_DB"
            }
        except KeyError:
            self.logger.log_agent_action(
                self.name, 
                f"⚠️  No KYC profile found for {subject_id}"
            )
            return {
                "status": "not_found",
                "data": {},
                "source": "KYC_DB"
            }