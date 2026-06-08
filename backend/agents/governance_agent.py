"""
Data Governance Agent - Enforces schema rules, privacy, and compliance
"""
import json
from datetime import datetime
from typing import Dict, List
from anthropic import Anthropic

class GovernanceAgent:
    def __init__(self, api_key):
        self.client = Anthropic()
        self.role = "Data Governance Agent"
        self.conversation_history = []
        self.governance_rules = {
            "data_classification": {
                "PII": ["customer_id", "email", "phone", "address"],
                "SENSITIVE": ["password", "credit_card", "ssn"],
                "PUBLIC": ["product_name", "category", "price"]
            },
            "compliance": ["GDPR", "CCPA", "SOC2"],
            "retention_days": 365
        }
        
    def validate_schema(self, data_schema: Dict, expected_schema: Dict) -> dict:
        """Validate data schema against governance rules"""
        violations = []
        
        # Check required fields
        for field, expected_type in expected_schema.items():
            if field not in data_schema:
                violations.append(f"Missing required field: {field}")
            elif data_schema[field] != expected_type:
                violations.append(f"Type mismatch for {field}: expected {expected_type}, got {data_schema[field]}")
        
        # Check for sensitive data handling
        pii_fields = self.governance_rules["data_classification"]["PII"]
        for field in data_schema:
            if field in pii_fields:
                violations.append(f"PII field detected: {field} - encryption required")
        
        compliance_report = self._generate_compliance_report(violations, data_schema)
        
        return {
            "status": "valid" if not violations else "invalid",
            "agent": self.role,
            "violations": violations,
            "compliance_report": compliance_report,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def apply_privacy_rules(self, data: Dict, sensitive_fields: List[str]) -> dict:
        """Apply privacy rules to sensitive fields"""
        masked_data = data.copy()
        masked_fields = []
        
        for field in sensitive_fields:
            if field in masked_data:
                if isinstance(masked_data[field], str):
                    # Mask the field
                    masked_data[field] = f"***MASKED***"
                    masked_fields.append(field)
        
        report = self._generate_privacy_report(masked_fields, sensitive_fields)
        
        return {
            "status": "success",
            "agent": self.role,
            "masked_data": masked_data,
            "masked_fields": masked_fields,
            "privacy_report": report,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def enforce_retention_policy(self, data_age_days: int) -> dict:
        """Enforce data retention policies"""
        retention_days = self.governance_rules["retention_days"]
        should_archive = data_age_days > retention_days
        
        action = "ARCHIVE" if should_archive else "KEEP"
        
        prompt = f"""
        As a Data Governance Agent, assess this data retention decision:
        
        Data Age: {data_age_days} days
        Retention Policy: {retention_days} days
        Recommended Action: {action}
        
        Provide a compliance assessment including:
        1. Retention policy compliance
        2. Archive recommendations
        3. Long-term data strategy
        """
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=400,
            messages=self.conversation_history
        )
        
        report = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": report
        })
        
        return {
            "status": "success",
            "agent": self.role,
            "data_age_days": data_age_days,
            "action": action,
            "governance_report": report,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_compliance_report(self, violations: List[str], schema: Dict) -> str:
        """Generate AI-powered compliance report"""
        violations_text = "\n".join(violations) if violations else "No violations detected"
        
        prompt = f"""
        As a Data Governance Agent, review these schema compliance findings:
        
        Schema: {json.dumps(schema, indent=2)}
        Violations: {violations_text}
        Compliance Standards: {', '.join(self.governance_rules['compliance'])}
        
        Provide a compliance summary with:
        1. Risk assessment
        2. Recommended remediation
        3. Compliance status
        """
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=400,
            messages=self.conversation_history
        )
        
        report = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": report
        })
        
        return report
    
    def _generate_privacy_report(self, masked_fields: List[str], sensitive_fields: List[str]) -> str:
        """Generate privacy protection report"""
        prompt = f"""
        As a Data Governance Agent, summarize privacy protections:
        
        Sensitive Fields Identified: {len(sensitive_fields)}
        Fields Masked: {masked_fields}
        Masking Strategy: Encryption and anonymization
        
        Provide a privacy protection summary.
        """
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=self.conversation_history
        )
        
        report = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": report
        })
        
        return report
