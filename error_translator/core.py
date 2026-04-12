import json
import os
import re
import linecache
from functools import lru_cache
from .ast_handlers import AST_REGISTRY


@lru_cache(maxsize=1)
def load_rules():
    """Load the error rules from disk once and cache them."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "rules.json")

    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def compiled_rules():
    """Compile regex patterns once to avoid repeated work per translation."""
    data = load_rules()
    compiled = []
    for rule in data["rules"]:
        compiled.append((re.compile(rule["pattern"]), rule))
    return compiled


def _extract_location(traceback_text: str) -> tuple[str, str]:
    location_match = re.search(r'File\s+[\'"]?(.*?)[\'"]?,\s+line\s+(\d+)', traceback_text)
    if not location_match:
        return "Unknown File", "Unknown Line"
    return location_match.group(1), location_match.group(2)


def translate_error(traceback_text: str) -> dict:
    data = load_rules()
    rules = compiled_rules()
    default_error = data["default"]

    lines = [line.strip() for line in traceback_text.strip().split("\n") if line.strip()]
    if not lines:
        return {"explanation": "No error text provided.", "fix": "Provide a valid Python error."}

    actual_error_line = lines[-1]

    file_name, line_number = _extract_location(traceback_text)

    code_context = ""
    if file_name != "Unknown File" and line_number != "Unknown Line":
        try:
            raw_line = linecache.getline(file_name, int(line_number))
            if raw_line:
                code_context = raw_line.strip()
        except Exception:
            pass

    for pattern, rule in rules:
        match = pattern.search(actual_error_line)
        if match:
            extracted_values = list(match.groups())
            fix_text = rule["fix"].format(*extracted_values)

            error_type = actual_error_line.split(":")[0].strip()
            handler_function = AST_REGISTRY.get(error_type)
            insight = None
            if handler_function and file_name != "Unknown File":
                insight = handler_function(file_name, extracted_values)
            return {
                "explanation": rule["explanation"].format(*extracted_values),
                "fix": fix_text,
                "ast_insight": insight,
                "matched_error": actual_error_line,
                "file": file_name,
                "line": line_number,
                "code": code_context,
            }

    return {
        "explanation": default_error["explanation"],
        "fix": default_error["fix"],
        "matched_error": actual_error_line,
        "file": file_name,
        "line": line_number,
        "code": code_context,
    }
