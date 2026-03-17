import json
import os
import urllib.request
import urllib.error

def lambda_handler(event, context):
    print("Incoming State:", event)
    api_key = os.environ.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    lecture_notes = event.get('lecture_notes', '')
    
    prompt = f"""
    You are a Senior Python Engineer in Bioinformatics. 
    Read these lecture notes: {lecture_notes[:1000]}
    
    Generate a short, executable Python code snippet (using pandas or sklearn) that demonstrates the core concept. 
    Provide ONLY the python code inside ```python ``` tags.
    """
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'))
    req.add_header('Authorization', f'Bearer {api_key}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0') 
    
    try:
        response = urllib.request.urlopen(req, timeout=15)
        response_data = json.loads(response.read().decode('utf-8'))
        
        code_snippet = response_data['choices'][0]['message']['content'].strip()
        
        event['code_snippet'] = code_snippet
        event['workflow_status'] = "READY_FOR_DYNAMODB"
        return event
        
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        print(f"HTTP Error: {e.code} - {error_msg}")
        raise Exception(f"Agent 3 API Failed: {error_msg}")
    except Exception as e:
        print(f"Agent 3 Error: {e}")
        raise Exception("Agent 3 Failed")