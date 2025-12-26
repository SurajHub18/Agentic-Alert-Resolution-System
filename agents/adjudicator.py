"""
Adjudicator Agent (Spoke)
Applies SOP rules to investigation findings and makes resolution decisions
"""

from config import SOP_RULES
from utils import AuditLogger


class AdjudicatorAgent:
    """Makes resolution decisions based on gathered evidence and SOPs"""
    
    def __init__(self):
        self.name = "Adjudicator Agent"
        self.logger = AuditLogger()
    
    def adjudicate(self, alert_data, investigation_result, context_result):
        """
        Apply SOP logic to make a resolution decision
        
        Args:
            alert_data: Original alert information
            investigation_result: Findings from Investigator Agent
            context_result: Customer context from Context Gatherer Agent
            
        Returns:
            Decision dictionary with recommendation, rationale, and confidence
        """
        scenario_code = alert_data["scenario_code"]
        alert_id = alert_data["alert_id"]
        
        self.logger.log_agent_action(
            self.name, 
            f"Applying SOP rule {SOP_RULES[scenario_code]['rule_id']} for {scenario_code}"
        )
        
        # Route to scenario-specific logic
        if scenario_code == "VELOCITY_SPIKE":
            return self._adjudicate_velocity_spike(
                alert_id, investigation_result, context_result
            )
        elif scenario_code == "STRUCTURING":
            return self._adjudicate_structuring(
                alert_id, investigation_result, context_result
            )
        elif scenario_code == "KYC_INCONSISTENCY":
            return self._adjudicate_kyc_inconsistency(
                alert_id, investigation_result, context_result
            )
        elif scenario_code == "SANCTIONS_MATCH":
            return self._adjudicate_sanctions_match(
                alert_id, investigation_result, context_result
            )
        elif scenario_code == "DORMANT_ACCOUNT":
            return self._adjudicate_dormant_account(
                alert_id, investigation_result, context_result
            )
        else:
            self.logger.log_agent_action(
                self.name,
                f"ERROR: Unsupported scenario code: {scenario_code}"
            )
            raise ValueError(f"Unsupported scenario code: {scenario_code}")
    
    def _adjudicate_velocity_spike(self, alert_id, investigation, context):
        """RUL-A001: Velocity Spike Logic"""
        hist_data = investigation["data"]
        kyc_data = context["data"]
        
        # Check conditions
        txn_count = hist_data.get("txn_count_last_48h", 0)
        historical_max = hist_data.get("historical_max_txn_90d", 0)
        prior_spike = hist_data.get("prior_velocity_spike", False)
        declared_income = kyc_data.get("declared_income", 0)
        source_of_funds = kyc_data.get("source_of_funds", "")
        occupation = kyc_data.get("occupation", "").lower()

        # Income Match
        monthly_income = declared_income / 12 if declared_income else 0
        estimated_txn_value = historical_max * txn_count
        income_match = estimated_txn_value <= (monthly_income * 2)

        is_business_cycle = "business" in occupation or "owner" in occupation

        # Decision logic
        if txn_count > 5 and not prior_spike and not income_match:
            return {
                "alert_id": alert_id,
                "recommendation": "ESCALATE_FOR_SAR",
                "rationale": (
                    f"Velocity spike detected: {txn_count} transactions in 48 hours with no prior "
                    f"high-velocity behavior. Estimated transaction volume (${estimated_txn_value:,}) "
                    f"is inconsistent with declared income (${declared_income:,}) and source of funds "
                    f"('{source_of_funds}'), indicating unexplained activity."
                ),
                "confidence": 0.95,
                "applied_rule": "RUL-A001"
            }
        elif txn_count > 5 and is_business_cycle and income_match:
            return {
                "alert_id": alert_id,
                "recommendation": "CLOSE_FALSE_POSITIVE",
                "rationale": (
                    f"Velocity spike observed, but transaction behavior aligns with a known business cycle "
                    f"for occupation '{occupation}' and is supported by declared income."
                ),
                "confidence": 0.75,
                "applied_rule": "RUL-A001"
            }
        else:
            return {
                "alert_id": alert_id,
                "recommendation": "CLOSE_FALSE_POSITIVE",
                "rationale": (
                    "Transaction velocity does not present sufficient deviation from historical "
                    "behavior or declared income to warrant escalation."
                ),
                "confidence": 0.70,
                "applied_rule": "RUL-A001"
            }    
    
    def _adjudicate_structuring(self, alert_id, investigation, context):
        """RUL-A002: Structuring Logic"""
        hist_data = investigation["data"]
        kyc_data = context["data"]
        
        linked_total = hist_data.get("linked_accounts_total", 0)
        deposits = hist_data.get("cash_deposits_7d", [])
        geographically_diverse = hist_data.get("geographically_diverse", False)
        occupation = kyc_data.get("occupation", "").lower()
        source_of_funds = kyc_data.get("source_of_funds", "").lower()
        
        # Check if all deposits are below $10,000 threshold
        below_threshold = all(d < 10000 for d in deposits)
        is_legitimate_business = (
            "business" in occupation or
            "owner" in occupation 
        )

        if geographically_diverse and is_legitimate_business:
            return {
                "alert_id": alert_id,
                "recommendation": "REQUEST_INFORMATION",
                "rationale": (
                    f"Deposits made across geographically diverse branches "
                    f"Customer occupation '{occupation}' "
                    f"and declared source of funds '{source_of_funds}' suggest legitimate "
                    f"business receipts. Request clarification on purpose and source of funds "
                    f"before escalation."
                ),
                "confidence": 0.70,
                "applied_rule": "RUL-A002"
            }
        
        elif linked_total > 28000 and below_threshold:
            return {
                "alert_id": alert_id,
                "recommendation": "ESCALATE_FOR_SAR",
                "rationale": (
                    f"Structuring detected: Total deposits across linked accounts = ${linked_total}, "
                    f"exceeding $28,000 threshold. All individual deposits kept below $10,000 reporting limit. "
                    f"Deposits: {deposits}. This pattern suggests deliberate structuring to avoid CTR filing."
                ),
                "confidence": 0.92,
                "applied_rule": "RUL-A002"
            }
        else:
            return {
                "alert_id": alert_id,
                "recommendation": "CLOSE_FALSE_POSITIVE",
                "rationale": "Deposits appear legitimate based on customer business profile.",
                "confidence": 0.65,
                "applied_rule": "RUL-A002"
            }
    
    def _adjudicate_kyc_inconsistency(self, alert_id, investigation, context):
        """RUL-A003: KYC Inconsistency Logic"""
        hist_data = investigation["data"]
        kyc_data = context["data"]
        
        occupation = kyc_data.get("occupation", "").lower()
        merchant_category = hist_data.get("merchant_category", "")
        wire_amount = hist_data.get("wire_amount", 0)
        
        # Check if occupation matches transaction type
        jewelry_related = "jewel" in occupation or "trader" in occupation
        
        if not jewelry_related and wire_amount >= 20000:
            return {
                "alert_id": alert_id,
                "recommendation": "ESCALATE_FOR_SAR",
                "rationale": (
                    f"KYC inconsistency detected: Customer occupation '{kyc_data.get('occupation')}' "
                    f"does not align with ${wire_amount} transaction to '{merchant_category}'. "
                    f"No logical business connection between profile and transaction behavior."
                ),
                "confidence": 0.90,
                "applied_rule": "RUL-A003"
            }
        else:
            return {
                "alert_id": alert_id,
                "recommendation": "CLOSE_FALSE_POSITIVE",
                "rationale": (
                    f"Customer occupation '{kyc_data.get('occupation')}' is consistent with "
                    f"transaction to '{merchant_category}'. Activity appears legitimate."
                ),
                "confidence": 0.85,
                "applied_rule": "RUL-A003"
            }
    
    def _adjudicate_sanctions_match(self, alert_id, investigation, context):
        """RUL-A004: Sanctions Match Logic"""
        hist_data = investigation["data"]
        
        similarity_score = hist_data.get("similarity_score", 0)
        jurisdiction = hist_data.get("bank_jurisdiction", "")
        counterparty = hist_data.get("counterparty_name", "")
        
        if similarity_score >= 0.80 or jurisdiction == "High Risk":
            return {
                "alert_id": alert_id,
                "recommendation": "ESCALATE_FOR_SAR",
                "rationale": (
                    f"Sanctions screening hit: Counterparty '{counterparty}' has {similarity_score*100:.0f}% "
                    f"similarity to sanctioned entity. Bank jurisdiction: {jurisdiction}. "
                    f"Requires immediate escalation and potential transaction block."
                ),
                "confidence": 0.98,
                "applied_rule": "RUL-A004"
            }
        else:
            return {
                "alert_id": alert_id,
                "recommendation": "CLOSE_FALSE_POSITIVE",
                "rationale": (
                    f"Low similarity score ({similarity_score*100:.0f}%) and safe jurisdiction. "
                    f"Likely a common name false positive."
                ),
                "confidence": 0.80,
                "applied_rule": "RUL-A004"
            }
    
    def _adjudicate_dormant_account(self, alert_id, investigation, context):
        """RUL-A005: Dormant Account Logic"""
        hist_data = investigation["data"]
        kyc_data = context["data"]
        
        months_inactive = hist_data.get("months_inactive", 0)
        risk_rating = kyc_data.get("risk_rating", "LOW")
        international_withdrawal = hist_data.get("international_withdrawal", False)
        
        if risk_rating == "HIGH" and international_withdrawal:
            return {
                "alert_id": alert_id,
                "recommendation": "ESCALATE_FOR_SAR",
                "rationale": (
                    f"High-risk dormant account reactivation: Account inactive for {months_inactive} months. "
                    f"Customer risk rating: {risk_rating}. International ATM withdrawal detected immediately "
                    f"after large inbound transfer. Possible account takeover or money mule activity."
                ),
                "confidence": 0.88,
                "applied_rule": "RUL-A005"
            }
        elif risk_rating == "LOW":
            return {
                "alert_id": alert_id,
                "recommendation": "REQUEST_INFORMATION",
                "rationale": (
                    f"Low-risk customer with dormant account reactivation. Request information "
                    f"about purpose of funds and reason for account inactivity."
                ),
                "confidence": 0.70,
                "applied_rule": "RUL-A005"
            }
        else:
            return {
                "alert_id": alert_id,
                "recommendation": "REQUEST_INFORMATION",
                "rationale": (
                    f"Account inactive for {months_inactive} months. Requires customer clarification "
                    f"before determining next steps."
                ),
                "confidence": 0.65,
                "applied_rule": "RUL-A005"
            }
    