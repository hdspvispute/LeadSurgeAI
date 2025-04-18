# parse_input.py

def parse_input(input_type: str, data: str) -> dict:
    """
    Simulates parsing input from text, email, audio, or video into clean text.
    """
    print(f"[parse_input] Received input_type: {input_type}")
    
    if input_type == "text":
        return {"content": data}
    
    elif input_type == "email":
        return {"content": f"Parsed email: {data}"}
    
    elif input_type == "audio":
        return {"content": f"Transcribed audio: {data}"}
    
    elif input_type == "video":
        return {"content": f"Transcribed video: {data}"}
    
    else:
        raise ValueError("Unsupported input type.")