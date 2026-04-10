import json
import os

def load_rules():
    """Loads the error rules from the JSON file."""
    # Find the absolute path to the json file next to this script
    # current_dir = os.path.dirname(data\rules.json)
    current_dir = 'data/'
    json_path = os.path.join(current_dir, 'rules.json')
    
    with open(json_path, 'r') as file:
        return json.load(file)

def translate_error(traceback_text: str) -> dict:
    import re
    import linecache  # <-- NEW: Lazy import the linecache module
    
    data = load_rules()
    rules = data["rules"]
    default_error = data["default"]

    lines = [line.strip() for line in traceback_text.strip().split('\n') if line.strip()]
    if not lines:
        return {"explanation": "No error text provided.", "fix": "Provide a valid Python error."}
    
    actual_error_line = lines[-1]

    location_match = re.search(r'File\s+[\'"]?(.*?)[\'"]?,\s+line\s+(\d+)', traceback_text)
    file_name = location_match.group(1) if location_match else "Unknown File"
    line_number = location_match.group(2) if location_match else "Unknown Line"

    # --- NEW CONTEXT ENGINE LOGIC ---
    code_context = ""
    if file_name != "Unknown File" and line_number != "Unknown Line":
        try:
            # linecache safely fetches the exact line of code as a string
            raw_line = linecache.getline(file_name, int(line_number))
            if raw_line:
                code_context = raw_line.strip() # Remove extra spaces/newlines
        except Exception:
            pass # If the file can't be read for any reason, fail silently
    # --------------------------------

    for rule in rules:
        pattern = re.compile(rule["pattern"])
        match = pattern.search(actual_error_line)
        
        if match:
            extracted_values = match.groups()
            return {
                "explanation": rule["explanation"].format(*extracted_values),
                "fix": rule["fix"].format(*extracted_values),
                "matched_error": actual_error_line,
                "file": file_name,
                "line": line_number,
                "code": code_context 
            }

    return {
        "explanation": default_error["explanation"],
        "fix": default_error["fix"],
        "matched_error": actual_error_line,
        "file": file_name,
        "line": line_number,
        "code": code_context      
    }