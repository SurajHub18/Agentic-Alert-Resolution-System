"""
Orchestrator Agent (Hub)
Routes alerts to appropriate spoke agents and coordinates the investigation workflow
"""

from utils import AuditLogger
from .investigator import InvestigatorAgent
from .context_agent import ContextGathererAgent
from .adjudicator import AdjudicatorAgent


class OrchestratorAgent:
    """Central hub that coordinates multi-agent alert resolution workflow"""
    
    def __init__(self):
        self.name = "Orchestrator Agent"
        self.logger = AuditLogger()
        
        # Initialize spoke agents
        self.investigator = InvestigatorAgent()
        self.context_gatherer = ContextGathererAgent()
        self.adjudicator = AdjudicatorAgent()
    
    def process_alert(self, alert_data):
        """
        Main orchestration method - delegates to spokes and returns final decision
        
        Args:
            alert_data: Dictionary containing alert details
            
        Returns:
            Final adjudication decision
        """
        alert_id = alert_data["alert_id"]
        scenario_code = alert_data["scenario_code"]
        
        # Log alert processing start
        self.logger.log_alert_start(alert_id, scenario_code)
        
        # Step 1: Route to investigator
        self.logger.log_agent_action(
            self.name, 
            f"Routing alert {alert_id} to Investigator and Context Gatherer agents"
        )
        
        # Step 2: Execute parallel investigation (simulated as sequential for simplicity)
        investigation_result = self.investigator.investigate(alert_data)
        context_result = self.context_gatherer.gather_context(alert_data)
        
        # Step 3: Send findings to adjudicator
        self.logger.log_agent_action(
            self.name, 
            "All data gathered. Forwarding to Adjudicator for decision..."
        )
        
        decision = self.adjudicator.adjudicate(
            alert_data, 
            investigation_result, 
            context_result
        )
        
        # Step 4: Log decision
        self.logger.log_decision(decision)
        
        return decision