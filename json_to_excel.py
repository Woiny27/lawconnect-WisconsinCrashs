import json
import pandas as pd

# Read findings.json
with open('findings.json', 'r') as f:
    data = json.load(f)

# Extract name and phone_number sample values
contacts = {}
for item in data.get('findings', []):
    if item['field_detected'] == 'name':
        contacts['Name'] = item['sample_value']
    elif item['field_detected'] == 'phone_number':
        contacts['Phone'] = item['sample_value']

# Save to Excel
if contacts:
    df = pd.DataFrame([contacts])
    df.to_excel('contacts.xlsx', index=False)
    print('Done! Extracted Name and Phone to contacts.xlsx')
else:
    print('No contacts found in findings.json')
