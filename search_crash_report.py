import requests

def search_crash_report(document_number):
    url = "https://crashreports.wi.gov/Search/Result"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "SearchCriteria": "DocumentNumber",
        "DocumentNumber": document_number
    }
    response = requests.post(url, headers=headers, data=data)
    return response.text

if __name__ == "__main__":
    test_id = "123456"  # Replace with your test document number
    result = search_crash_report(test_id)
    print(result)
