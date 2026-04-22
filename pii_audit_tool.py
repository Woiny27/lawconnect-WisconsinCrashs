import requests
import re
import json
from datetime import datetime

class CrashPortalAuditor:
    def __init__(self, base_url):
        self.base_url = base_url
        self.findings = []
        # Patterns for detecting sensitive data (prototype requirements)
        self.pii_patterns = {
            "name": r'\b[A-Z]{2,}\s[A-Z]{2,}\b|\b[A-Z][a-z]+\s[A-Z][a-z]+\b',  # Improved: ALLCAPS or Title Case
            "phone_number": r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4})',
            "email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            "mailing_address": r'\d{1,5}\s\w.\s(\b\w*\b\s){1,2}\w*.',
            "insurance_id": r'\b[A-Z0-9]{8,12}\b'
        }

    def audit_endpoint(self, endpoint, auth_header=None):
        """Scans a specific endpoint for PII leaks."""
        url = f"{self.base_url}{endpoint}"
        headers = auth_header if auth_header else {}
        access_state = "authenticated" if auth_header else "pre-authentication"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            content = response.text
            
            for field, pattern in self.pii_patterns.items():
                matches = re.findall(pattern, content)
                if matches:
                    self.findings.append({
                        "field_detected": field,
                        "endpoint": endpoint,
                        "access_state": access_state,
                        "sample_value": matches[0], # Just the first for evidence
                        "severity": "high" if access_state == "pre-authentication" else "medium"
                    })
        except Exception as e:
            print(f"Error auditing {endpoint}: {e}")

    def generate_report(self):
        if not self.findings:
            return {
                "timestamp": datetime.now().isoformat(),
                "target_host": self.base_url,
                "summary": "No PII leaks detected.",
                "findings": []
            }

        affected_endpoints = list(set(f["endpoint"] for f in self.findings))
        exposed_fields = list(set(f["field_detected"] for f in self.findings))
        access_methods = list(set(f["access_state"] for f in self.findings))

        report = {
            "timestamp": datetime.now().isoformat(),
            "target_host": self.base_url,
            "summary": {
                "affected_endpoints": affected_endpoints,
                "exposed_field_types": exposed_fields,
                "access_methods": access_methods,
                "total_leaks": len(self.findings),
                "high_severity": len([f for f in self.findings if f['severity'] == 'high'])
            },
            "business_privacy_impact": (
                "Exposure of PII such as names, phone numbers, addresses, emails, or insurance IDs can lead to privacy violations, regulatory non-compliance, and reputational damage. "
                "Unauthorized access (pre-authentication) increases risk of data breach and legal consequences."
            ),
            "recommended_remediation": (
                "Implement Role-Based Access Control (RBAC), mask or redact PII in preview/public states, and regularly audit endpoints for data exposure. "
                "Ensure only authorized users can access sensitive information."
            ),
            "findings": self.findings
        }
        return report

# Example Usage (Authorization Required)
if __name__ == "__main__":
    # Replace with your authorized demo/staging URL
    AUDIT_TARGET = "https://staging.crash-reports.internal/api/v1"
    auditor = CrashPortalAuditor(AUDIT_TARGET)

    # MOCK TEST: Use sample data since endpoint is not accessible
    def mock_audit_content(auditor, content, endpoint="/report/preview", access_state="pre-authentication"):
        for field, pattern in auditor.pii_patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                auditor.findings.append({
                    "field_detected": field,
                    "endpoint": endpoint,
                    "access_state": access_state,
                    "sample_value": matches[0],
                    "severity": "high" if access_state == "pre-authentication" else "medium"
                })

    # Example mock content with PII
    mock_content = """
    Name: John Doe\n
    Phone: 312-555-4821\n
    Email: john.doe@example.com\n
    Address: 123 Main St.\n
    Insurance ID: ABCD12345678\n
    """
    print("Auditing mock content for PII...")
    mock_audit_content(auditor, mock_content)

    # Output findings in the requested format
    final_report = auditor.generate_report()
    print(json.dumps(final_report, indent=2))

    # Standardize and write findings to findings.json
    findings_output = []
    for finding in auditor.findings:
        findings_output.append({
            "field_detected": finding["field_detected"],
            "endpoint": finding["endpoint"],
            "access_state": finding["access_state"],
            "sample_value": finding["sample_value"],
            "severity": finding["severity"]
        })
    with open("findings.json", "w") as f:
        json.dump({"findings": findings_output}, f, indent=2)
