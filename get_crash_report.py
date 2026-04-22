import requests

def get_crash_report(report_id, access_token):
    url = f"https://trust.dot.state.wi.us/pars/api/v1/reports/{report_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except Exception:
        return response.text

if __name__ == "__main__":
    report_id = "YOUR_REPORT_ID"  # Replace with your report ID
    access_token = "YOUR_ACCESS_TOKEN"  # Replace with your access token
    result = get_crash_report(report_id, access_token)
    print(result)
