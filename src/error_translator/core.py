"""
Core translation engine for the Error Translator CLI.

This module is responsible for:
1. Loading and compiling regex-based error translation rules.
2. Parsing Python traceback messages.
3. Matching errors against rules to provide human-readable explanations.
4. Using a fast C extension for matching if available, with a Python fallback.
5. Delegating to AST handlers for deep, code-specific insights.
"""
import json
import os
import re
import linecache
from functools import lru_cache
from .ast.ast_handlers import AST_REGISTRY

# Attempt to load the ultra-fast C extension for matching rules,
# and fallback to the Python implementation if it's unavailable.
try:
    from .fast_matcher import match_loop
    C_EXTENSION_AVAILABLE = True
except ImportError:
    C_EXTENSION_AVAILABLE = False


@lru_cache(maxsize=1)
def load_rules():
    """
    Load the error translation rules from the 'rules.json' file.
    The rules dictate how Python tracebacks map to human-readable explanations.
    This function is cached so we only read the file once per runtime.
    
    Returns:
        dict: Parsed JSON data containing "rules" and "default".
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "rules.json")

    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def compiled_rules():
    """
    Pre-compile the regular expressions for each rule defined in 'rules.json'.
    Compiling regex patterns once avoids redundant compilation during every
    error translation request, significantly speeding up the matching process.
    
    Returns:
        list of tuples: Each tuple is (compiled_regex, rule_dict).
    """
    data = load_rules()
    compiled = []
    for rule in data["rules"]:
        compiled.append((re.compile(rule["pattern"]), rule))
    return compiled


def _extract_location(traceback_text: str) -> tuple[str, str]:
    """
    Extract the file name and line number where the error occurred
    by parsing the standard Python traceback format.
    
    Args:
    Extract the file path and line number from the traceback text.
    Looks for the standard Python format: File "...", line X
    """
    # Regex to capture "File <path>, line <number>"
    location_match = re.search(r'File\s+[\'"]?(.*?)[\'"]?,\s+line\s+(\d+)', traceback_text)
    if not location_match:
        return "Unknown File", "Unknown Line"
    return location_match.group(1), location_match.group(2)


def translate_error(traceback_text: str) -> dict:
    """
        dict: A dictionary containing the explanation, suggested fix,
              AST-based insight (if any), file, line number, code context, 
              and the matched error line.
    """
    # Load configuration rules and pre-compiled regex patterns
    data = load_rules()
    rules = compiled_rules()
    default_error = data["default"]

    # Extract non-empty lines from the traceback
    lines = [line.strip() for line in traceback_text.strip().split("\n") if line.strip()]
    if not lines:
        return {"explanation": "No error text provided.", "fix": "Provide a valid Python error."}

    # The actual error message is typically the last line in a traceback
    actual_error_line = lines[-1]

    # Extract the origin of the error (file name and line number)
    file_name, line_number = _extract_location(traceback_text)

    # Attempt to read the exact line of code that caused the error
    code_context = ""
    if file_name != "Unknown File" and line_number != "Unknown Line":
        try:
            raw_line = linecache.getline(file_name, int(line_number))
            if raw_line:
                code_context = raw_line.strip()
        except Exception:
            pass

    # ==========================================
    # FAST MATCHING ENGINE (C Extension + Python Fallback)
    # ==========================================
    match = None
    rule = None

    if C_EXTENSION_AVAILABLE:
        # Execute the C extension for maximum performance
        result = match_loop(actual_error_line, rules)
        if result:
            match, rule = result
    else:
        # Fallback to standard Python regex loop
        for pattern, r in rules:
            m = pattern.search(actual_error_line)
            if m:
                match, rule = m, r
                break

    # If we found a matching rule, format the explanation and fix
    if match and rule:
        # Extract variables from the regex groups (e.g., variable names, functions)
        extracted_values = list(match.groups())
        
        # Inject the extracted values into the template fix string
        fix_text = rule["fix"].format(*extracted_values)

        # Parse the error type (e.g., "NameError", "TypeError") to dispatch AST insights
        error_type = actual_error_line.split(":")[0].strip()
        
        # Check if there's a specialized AST handler for this specific error type
        handler_function = AST_REGISTRY.get(error_type)
        insight = None
        
        # If an AST handler exists and the file is accessible, run deep code analysis
        if handler_function and file_name != "Unknown File":
            insight = handler_function(file_name, line_number, extracted_values)
        
        return {
            "explanation": rule["explanation"].format(*extracted_values),
            "fix": fix_text,
            "ast_insight": insight,
            "matched_error": actual_error_line,
            "file": file_name,
            "line": line_number,
            "code": code_context,
        }

    # Fallback when the error doesn't match any known rules
    return {
        "explanation": default_error["explanation"],
        "fix": default_error["fix"],
        "matched_error": actual_error_line,
        "file": file_name,
        "line": line_number,
        "code": code_context,
    }