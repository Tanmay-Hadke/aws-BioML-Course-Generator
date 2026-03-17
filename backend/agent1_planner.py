import json
import os
import urllib.request
import urllib.error

def lambda_handler(event, context):
    print("Incoming State:", event)
    
    api_key = os.environ.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    topic = event.get('course_topic', 'Unknown Topic')
    audience = event.get('target_audience', 'General')
    
    prompt = f"""
    You are an expert Bioinformatics curriculum planner. 
    Create a 3-part syllabus for: {topic} (Target Audience: {audience}).
    
    Respond ONLY with a valid JSON array of three strings representing the sub-topics.
    Example: ["Topic 1", "Topic 2", "Topic 3"]
    """
    
    # 1. We manually build the JSON payload that the Groq SDK used to build for us
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    
    # 2. Package it into a standard HTTP Request
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'))
    req.add_header('Authorization', f'Bearer {api_key}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0') # <-- ADD THIS DISGUISE LINE
    
    try:
        # 3. Send the request and read the response
        response = urllib.request.urlopen(req, timeout=15)
        response_data = json.loads(response.read().decode('utf-8'))
        
        # 4. Extract the message content (Groq uses the exact same JSON structure as OpenAI)
        syllabus_str = response_data['choices'][0]['message']['content'].strip()
        syllabus_list = json.loads(syllabus_str)
        
        # 5. Attach the new data to the state and pass it forward
        event['syllabus'] = syllabus_list
        event['agent1_status'] = "SUCCESS"
        
        return event
        
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        print(f"HTTP Error: {e.code} - {error_msg}")
        raise Exception(f"Agent 1 API Failed: {error_msg}")
    except Exception as e:
        print(f"Agent 1 Error: {e}")
        raise Exception("Agent 1 Failed")