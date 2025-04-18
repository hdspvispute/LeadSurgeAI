# detect_lead.py

def detect_lead(content: str) -> dict:
    """
    Simulates detecting a lead in freeform text.
    """
    print(f"[detect_lead] Input content: {content}")
    
    # Mock logic — in real case, call OpenAI or run NLP here
    if "interested" in content.lower() or "demo" in content.lower():
        return {
            "is_lead": True,
            "name": "Sarah",
            "company": "XYZ Corp",
            "email": "sarah@xyzcorp.com"
        }
    
    return {"is_lead": True}
