"""
Agentic Alert Resolution System - Main Entry Point
Processes all 5 pre-generated alerts through the multi-agent workflow
"""

from data import ALERTS
from agents import OrchestratorAgent
from actions import ActionExecutor
from utils import AuditLogger


def main():
    """Main execution function"""
    # Initialize components
    orchestrator = OrchestratorAgent()
    action_executor = ActionExecutor()
    logger = AuditLogger()
    
    print("\n" + "="*70)
    print("AGENTIC ALERT RESOLUTION SYSTEM (AARS)")
    print("="*70)
    print(f"Total Alerts to Process: {len(ALERTS)}")
    print("="*70 + "\n")
    
    # Process each alert
    for alert in ALERTS:
        try:
            # Step 1: Orchestrator coordinates investigation
            decision = orchestrator.process_alert(alert)
            
            # Step 2: Execute action based on decision
            action_executor.execute(decision, alert)
            
            # Mark alert as complete
            logger.log_alert_complete(alert["alert_id"])
            
        except Exception as e:
            print(f"\n❌ ERROR processing alert {alert['alert_id']}: {str(e)}\n")
            continue
    

    print("\n" + "="*70)
    print("ALL ALERTS PROCESSED SUCCESSFULLY")
    print("="*70)


if __name__ == "__main__":
    main()