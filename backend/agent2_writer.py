import json
import os
import urllib.request
import urllib.error

def lambda_handler(event, context):
    print("Incoming State:", event)
    api_key = os.environ.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    topic = event.get('course_topic', 'Unknown Topic')
    syllabus = event.get('syllabus', [])
    syllabus_text = "\n".join([f"- {item}" for item in syllabus])
    
    prompt = f"""
    You are a Professor of Bioinformatics. Write a highly technical, 2-paragraph lecture summary for the course "{topic}".
    Ensure you specifically cover these syllabus points:
    {syllabus_text}
    """
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'))
    req.add_header('Authorization', f'Bearer {api_key}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0') # The Cloudflare disguise
    
    try:
        response = urllib.request.urlopen(req, timeout=15)
        response_data = json.loads(response.read().decode('utf-8'))
        
        lecture_notes = response_data['choices'][0]['message']['content'].strip()
        
        event['lecture_notes'] = lecture_notes
        event['agent2_status'] = "SUCCESS"
        return event
        
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        print(f"HTTP Error: {e.code} - {error_msg}")
        raise Exception(f"Agent 2 API Failed: {error_msg}")
    except Exception as e:
        print(f"Agent 2 Error: {e}")
        raise Exception("Agent 2 Failed")