# create_salesforce_lead.py

import requests


ACCESS_TOKEN = "00DgK0000025WhS!AQEAQJgB1_MM2Yy5iF8sSDvbsxjNPXLzr.YH2skkp5s9YR16zM3r30b02ddsTzppCYV08Mnye5Fdl2.87uXvBboGTqqyI01S"
INSTANCE_URL = "https://orgfarm-1fb703dbbe-dev-ed.develop.my.salesforce.com"


def create_salesforce_lead(name: str, company: str, email: str) -> str:
    print(f"[create_salesforce_lead] Creating lead: {name}, {company}, {email}")

    url = f"{INSTANCE_URL}/services/data/v63.0/sobjects/lead/"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "LastName": name,
        "Company": company,
        "Email": email,
        "Description": "Test description"
    
    }
    response = requests.post(url, headers=headers, json=data)
     
    
    # In a real app, you'd use requests.post() to Salesforce REST API
    return f"Lead for {name} ({email}) at {company} created in Salesforce. " + response.json()
