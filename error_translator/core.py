from .rules import ERROR_RULES, DEFAULT_ERROR
import re

def translate_error(traceback_text: str) -> dict:
    """
    Parses traceback text and returns a human-readable explanation and fix.
    """
    location_match = re.search(r'File "(.*?)", line (\d+), in (.+)', traceback_text)
    file_name = location_match.group(1) if location_match else "unknown file"
    line_number = location_match.group(2) if location_match else "unknown line"
    in_function = location_match.group(3) if location_match else "unknown function"
    # Grab the last non-empty line of the traceback, which usually contains the actual error
    lines = [line.strip() for line in traceback_text.strip().split('\n') if line.strip()]
    if not lines:
        return {"explanation": "No error text provided.", "fix": "Provide a valid Python error."}
    
    actual_error_line = lines[-1]

    for rule in ERROR_RULES:
        match = rule["pattern"].search(actual_error_line)
        if match:
            # Extract the captured regex groups (e.g., the variable name)
            extracted_values = match.groups()
            
            # Format the explanation and fix using the extracted values
            explanation = rule["explanation"].format(*extracted_values)
            fix = rule["fix"].format(*extracted_values)
            
            return {
                "explanation": explanation,
                "fix": fix,
                "matched_error": actual_error_line,
                "file": file_name,
                "line": line_number,
                "function": in_function
            }

    # If no rules match, return the default payload
    return {
        "explanation": DEFAULT_ERROR["explanation"],
        "fix": DEFAULT_ERROR["fix"],
        "matched_error": actual_error_line,
        "file": file_name,
        "line": line_number,
        "function": in_function
    }