import requests
import csv
import json

# --- CONFIGURATION ---
TOKEN = "PASTE_YOUR_OAUTH_TOKEN_HERE"
REPORT_ID = "PASTE_YOUR_REPORT_ID_HERE"
API_URL = f"https://api.lexisnexis.com/aries/v1/in/reports/{REPORT_ID}"

def get_crash_contacts():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }

    print(f"Fetching report {REPORT_ID}...")
    response = requests.get(API_URL, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return

    data = response.json()
    
    # This list will hold our mapped data
    extracted_people = []

    # Mapping logic for Indiana ARIES JSON structure
    # Navigate: Units -> Parties
    units = data.get("units", [])
    for unit in units:
        parties = unit.get("parties", [])
        for person in parties:
            extracted_people.append({
                "Name": person.get("full_name", "N/A"),
                "Phone": person.get("phone_number", "N/A"),
                "Address": person.get("address_line1", "N/A"),
                "City": person.get("city", "N/A"),
                "Zip": person.get("zip_code", "N/A"),
                "Role": person.get("type", "Involved Party"), # Driver, Passenger, etc.
                "Unit_ID": unit.get("unit_number", "N/A")
            })

    # Save to CSV (Excel compatible)
    keys = extracted_people[0].keys() if extracted_people else []
    if not keys:
        print("No people found in this report.")
        return

    with open('findings.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(extracted_people)

    print(f"Done! {len(extracted_people)} people saved to findings.csv")

if __name__ == "__main__":
    get_crash_contacts()
