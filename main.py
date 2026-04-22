from pii_audit_tool import CrashPortalAuditor
from faker import Faker
from city_provider import CityProvider

fake = Faker()
fake.add_provider(CityProvider)

if __name__ == "__main__":
    # Example usage for main entry point
    AUDIT_TARGET = "https://prod-exp-wi-license–search-v1.us-e2.cloudhub.io/api/blp/"
    auditor = CrashPortalAuditor(AUDIT_TARGET)

    # MOCK TEST: Use sample data since endpoint is not accessible
    def mock_audit_content(auditor, content, endpoint="/report/preview", access_state="pre-authentication"):
        import re
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
    print(final_report)

    # Write findings to findings.json
    import json
    with open("findings.json", "w") as f:
        json.dump({"findings": auditor.findings}, f, indent=2)

    # Export findings to CSV using pandas
    try:
        import pandas as pd
        data = pd.read_json('findings.json')
        df = pd.DataFrame(data['findings'])
        df.to_csv('findings.csv', index=False)
        print("Exported findings to findings.csv")
    except Exception as e:
        print(f"CSV export failed: {e}")

    # Example usage of CityProvider
    print(fake.city_name())
