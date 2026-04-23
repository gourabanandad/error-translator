from .ast_engine import get_ast_suggestions
# --- 1. THE INDIVIDUAL STRATEGIES (PLUGINS) ---

def handle_name_error(file_path: str, line_number: str, extracted_values: list) -> str:
    """Handles NameError: name 'X' is not defined"""
    bad_name = extracted_values[0] if extracted_values else ""

    suggestion = get_ast_suggestions(file_path, line_number, bad_name, "NameError")

    if suggestion:
        return f"Did you mean '{suggestion}'? There appears to be a typo."
    return f"The variable '{bad_name}' was not found in the file's scope. Ensure it is defined before this line."    

def handle_attribute_error(file_path: str, line_number: str, extracted_values: list) -> str:
    """Handles AttributeError: 'X' object has no attribute 'Y'"""
    # Assuming the last extracted value is the missing attribute (e.g., 'apend')
    bad_attr = extracted_values[-1] if extracted_values else ""
    suggestion = get_ast_suggestions(file_path, line_number, bad_attr, "AttributeError")
    if suggestion:
        return f"Did you mean the attribute or method '{suggestion}'?"
    return f"The attribute or method '{bad_attr}' was not found in the file's scope. Ensure it is defined before this line."

def handle_import_error(file_path: str, line_number: str, extracted_values: list) -> str:
   bad_name = extracted_values[0] if extracted_values else ""

   suggestion = get_ast_suggestions(file_path, line_number, bad_name, "ImportError")
   if suggestion:
    return f"Did you mean to import '{suggestion}' instead?"
   return f"Verify that the class/function exists in the target module and is spelled correctly."
    
# --- 2. THE REGISTRY (THE MAGIC ROUTER) ---
# We map the string name of the error to the function that handles it.
AST_REGISTRY = {
    "NameError": handle_name_error,
    "AttributeError": handle_attribute_error,
    "ImportError": handle_import_error,
    # "SyntaxError": handle_syntax_error,
}