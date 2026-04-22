import re

class ExposureAssessmentModule:
    def __init__(self):
        # Specific patterns for the requested fields
        self.pii_signatures = {
            "name": r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', # Simple Full Name detection
            "phone_number": r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4})',
            "mailing_address": r'\d{1,5}\s\w.\s(\b\w*\b\s){1,2}\w*\.',
            "email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            "insurance_identifiers": [r'policy[-_]no', r'ins[-_]id', r'\b[A-Z0-9]{8,12}\b']
        }

    def evaluate_exposure(self, response_data, endpoint_context):
        """
        Evaluates a response body for specific PII exposure.
        """
        detected_fields = []
        content_str = str(response_data)

        for field, patterns in self.pii_signatures.items():
            # Handle list of patterns for insurance identifiers
            current_patterns = patterns if isinstance(patterns, list) else [patterns]
            
            for pattern in current_patterns:
                if re.search(pattern, content_str, re.IGNORECASE):
                    detected_fields.append({
                        "field": field,
                        "evidence": "Pattern Match Found",
                        "risk_level": "High" if "public" in endpoint_context else "Medium"
                    })
                    break # Move to next field once one pattern hits

        return detected_fields
