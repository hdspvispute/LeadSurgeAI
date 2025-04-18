# create_salesforce_lead.py

def create_salesforce_lead(name: str, company: str, email: str) -> str:
    """
    Simulates creating a lead in Salesforce.
    """
    print(f"[create_salesforce_lead] Creating lead: {name}, {company}, {email}")
    
    # In a real app, you'd use requests.post() to Salesforce REST API
    return f"Lead for {name} ({email}) at {company} created in Salesforce."
