import json
import boto3
import uuid

sfn_client = boto3.client('stepfunctions')

# REPLACE THIS WITH YOUR ACTUAL STATE MACHINE ARN
STATE_MACHINE_ARN = "YOUR_STEP_FUNCTION_ARN"

def lambda_handler(event, context):
    try:
        print("Raw incoming event:", event) # Helpful for debugging in CloudWatch
        
        # --- BULLETPROOF DATA EXTRACTION ---
        # Check if API Gateway wrapped the data inside a 'body' property
        if 'body' in event and event['body']:
            if isinstance(event['body'], str):
                parsed_data = json.loads(event['body'])
            else:
                parsed_data = event['body']
        else:
            # If there is no 'body' property, the event ITSELF is the data!
            parsed_data = event
            
        topic = parsed_data.get('course_topic', 'Unknown Topic')
        audience = parsed_data.get('target_audience', 'M.Sc. Students')
        # -----------------------------------
        
        payload = {
            "course_topic": topic,
            "target_audience": audience
        }
        
        execution_name = f"Course-{str(uuid.uuid4())[:8]}"
        
        response = sfn_client.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            name=execution_name,
            input=json.dumps(payload)
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'AI Workflow Successfully Triggered!',
                'course_id': execution_name,
                'received_topic': topic # We return this to the UI to prove it worked
            })
        }
        
    except Exception as e:
        print(f"Trigger Error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }