
# lawconnect-WisconsinCrashs

## Part A: Reliable Workflow Engineering (Core)

**Architecture Overview:**
The core of this platform is designed for robust, reliable, and privacy-conscious crash data ingestion. It features:
- **Requester:** Handles HTTP requests with retry logic, jitter, and proxy rotation to ensure resilient data collection from public systems.
- **Parser:** Uses fuzzy HTML matching and Pydantic validation to normalize and validate incoming data, handling schema drift and data quality issues.
- **Auditor (Exposure Assessment Module):** Scans all ingested data for PII leaks, classifies severity, and outputs standardized evidence to findings.json, including severity and access_state for business/privacy impact analysis.
- **Storage Engine:** Supports both PostgreSQL/JSONB and flat JSON storage, with deduplication via SHA-256 hashing and optional Redis for fast duplicate checks.

## Part B: Multi-City Plugin System (Providers)

**Plugin Design:**
Providers are modular plugins for each city or data source, inheriting from a common BaseProvider interface. Each implements:
- **Authentication:** Handles API keys, tokens, or session cookies as required by the source.
- **Fetch Records:** Retrieves crash data using city-specific endpoints and parameters.
- **Normalization:** Converts raw records to a standard schema for downstream processing.

**Current Providers:**
- MadisonPDProvider (Madison, WI)
- MilwaukeePDProvider (Milwaukee, WI)
- WisDOTPortalProvider (Wisconsin DOT)

## Part C: Storage Strategy

**Data Storage:**
- **PostgreSQL/JSONB:** For scalable, queryable storage of normalized crash records.
- **Flat JSON:** For lightweight, portable evidence and findings output.
- **Deduplication:** SHA-256 hashing and optional Redis cache prevent duplicate record storage.

## Part D: 10 Public Systems List

1. Wisconsin DOT Crash Portal
2. Madison Police Department Open Data
3. Milwaukee Police Department Open Data
4. Illinois State Police Crash Reports
5. Chicago Data Portal (crashes)
6. Indiana BuyCrash Portal
7. Minnesota Crash Records System
8. Iowa DOT Crash Data
9. Michigan Traffic Crash Reporting System
10. Ohio Department of Public Safety Crash Data

---

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the PII audit tool: `python pii_audit_tool.py`
3. Review findings in `findings.json` for evidence output, including severity and access_state fields.

## Architectural Notes

- All providers inherit from a common abstract base for easy extensibility.
- The auditor module ensures privacy compliance by flagging and classifying PII exposure.
- The system is designed for easy addition of new cities or data sources via the plugin pattern.

## Evidence Output Example

See `findings.json` for a standardized output format:

```
{
	"findings": [
		{
			"field_detected": "name",
			"endpoint": "/report/preview",
			"access_state": "pre-authentication",
			"sample_value": "John Doe",
			"severity": "high"
		}
		// ... more findings ...
	]
}
```