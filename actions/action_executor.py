"""
Action Execution Module (AEM)
Simulates the execution of resolution actions based on adjudicator decisions

"""

from utils import AuditLogger
from data import KYC_DB


class ActionExecutor:
    """Executes actions based on adjudication decisions"""
    
    def __init__(self):
        self.logger = AuditLogger()
    
    def execute(self, decision, alert_data):
        """
        Execute the appropriate action based on the decision
        
        Args:
            decision: Decision dictionary from Adjudicator
            alert_data: Original alert information
        """
        recommendation = decision["recommendation"]
        alert_id = decision["alert_id"]
        subject_id = alert_data["subject_id"]
        scenario_code = alert_data["scenario_code"]
        
        # Get customer name for personalization
        customer_name = KYC_DB.get(subject_id, {}).get("name", subject_id)
        risk = KYC_DB.get(subject_id, {}).get("risk_rating", "LOW")
        # Route to appropriate action simulator
        if recommendation == "ESCALATE_FOR_SAR":
            self._execute_sar_prep(alert_id, customer_name, decision)
        elif recommendation == "REQUEST_INFORMATION":
            # IVR is specifically for dormant account verification (A-005)
            if risk == "LOW" or risk == "MEDIUM":
                self._execute_rfi(alert_id, customer_name, decision)
            else:
                self._execute_ivr(alert_id, customer_name, decision)
        elif recommendation == "CLOSE_FALSE_POSITIVE":
            self._execute_close(alert_id, customer_name, decision)
    
    def _execute_sar_prep(self, alert_id, customer_name, decision):
        """Simulate SAR (Suspicious Activity Report) preparation"""
        print("\n" + "="*70)
        print("ACTION EXECUTION")
        print("="*70)
        print(f"Action Executed: SAR Preparer Module Activated.")
        print(f"Case [{alert_id}] pre-populated and routed to Human Queue.")
        print(f"Rationale: {decision['rationale']}")
        print("="*70 + "\n")
    
    def _execute_rfi(self, alert_id, customer_name, decision):
        """Simulate Request for Information (RFI) via email"""
        print("\n" + "="*70)
        print("ACTION EXECUTION")
        print("="*70)
        print(f"Action Executed: RFI via Email.")
        print(f"Drafted message for Customer: {customer_name} requesting Source of Funds.")
        print("="*70 + "\n")
    
    def _execute_ivr(self, alert_id, customer_name, decision):
        """Simulate IVR (Interactive Voice Response) call for verification"""
        print("\n" + "="*70)
        print("ACTION EXECUTION")
        print("="*70)
        print(f"Action Executed: IVR Call Initiated.")
        print(f"Script ID 3 used for simple verification.")
        print(f"Awaiting Customer Response...")
        print("="*70 + "\n")
    
    def _execute_close(self, alert_id, customer_name, decision):
        """Simulate closing alert as false positive"""
        print("\n" + "="*70)
        print("ACTION EXECUTION")
        print("="*70)
        print(f"Action Executed: Alert [{alert_id}] Closed as False Positive.")
        print(f"Customer: {customer_name}")
        print(f"Reason: {decision['rationale']}")
        print("="*70 + "\n")
    
