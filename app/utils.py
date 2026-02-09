import requests

PISTON_API_URL = "https://emkc.org/api/v2/piston/execute"

def execute_code(language, code, input_data=""):
    """
    Executes code using the Piston API.
    
    Args:
        language (str): The programming language (python, c, cpp, java, javascript).
        code (str): The source code to execute.
        input_data (str): Standard input for the program.
        
    Returns:
        dict: A dictionary containing 'output' and 'error'.
    """
    
    # Map our language names to Piston's runtime names
    lang_map = {
        "python": "python",
        "c": "c",
        "cpp": "cpp",
        "java": "java",
        "javascript": "javascript"
    }
    
    runtime = lang_map.get(language)
    if not runtime:
        return {"output": "", "error": f"Unsupported language: {language}"}
        
    payload = {
        "language": runtime,
        "version": "*",
        "files": [
            {
                "content": code
            }
        ],
        "stdin": input_data
    }
    
    try:
        response = requests.post(PISTON_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        # Piston returns 'run' object with 'stdout', 'stderr', 'output', 'code', 'signal'
        run_result = result.get('run', {})
        output = run_result.get('stdout', "")
        error = run_result.get('stderr', "")
        
        # If there's an error from the API itself (like compilation error)
        if run_result.get('code') != 0 and not error:
             error = output # sometimes errors are in stdout depending on the runner
             
        return {"output": output, "error": error}
        
    except requests.exceptions.RequestException as e:
        return {"output": "", "error": f"API Error: {str(e)}"}
