import requests
import json

def get_crash_report(report_id, access_token):
    url = f"https://api.lexisnexis.com/aries/v1/in/reports/{report_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def extract_people_block(report_json):
    # Adjust the key path if needed based on actual API response structure
    return report_json.get('People', None)

def main():
    report_id = input("Enter REPORT_ID: ")
    access_token = input("Enter ACCESS_TOKEN: ")
    report_json = get_crash_report(report_id, access_token)
    people_block = extract_people_block(report_json)
    print("\n--- 'People' Data Block ---")
    print(json.dumps(people_block, indent=2))

if __name__ == "__main__":
    main()
