import json

def lambda_handler(event, context):
    code = event.get('code_snippet', '')
    
    # We remove markdown backticks if the previous agent included them
    clean_code = code.replace("```python", "").replace("```", "").strip()
    
    test_result = "Passed"
    error_message = ""
    
    try:
        # The 'compile' function checks for syntax errors without actually 
        # running heavy logic—perfect for a quick MLOps check.
        compile(clean_code, '<string>', 'exec')
    except Exception as e:
        test_result = "Failed"
        error_message = str(e)
    
    # Return the original data PLUS the test results
    return {
        **event,
        "test_result": test_result,
        "test_debug_info": error_message
    }