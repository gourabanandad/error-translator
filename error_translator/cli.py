import sys
import argparse
from .core import translate_error
from importlib.metadata import version, PackageNotFoundError

try:
    VERSION = version("error-translator-cli-v2")
except PackageNotFoundError:
    VERSION = "unknown (not installed via pip)"  # Fallback version if package metadata is not found

# ANSI Color Codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    MAGENTA = '\033[95m'


def print_about():
    """Prints the about message for the tool."""
    about_text = f"""
ERROR TRANSLATOR CLI
=====================
A lightning-fast, offline tool that translates raw Python tracebacks 
into human-readable explanations with actionable fixes.

Authors: Gourabananda Datta
Repository: https://github.com/gourabanandad/error-translator-cli-v2
Usage:
  1. Run a script and translate its errors:
        explain-error run your_script.py
    2. Translate an error message directly:
        explain-error "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    3. Pipe an error log:
        cat error.log | explain-error
    4. Get help:
        explain-error --help
    5. About:
        explain-error --about
"""
    print(f"\033[96m{about_text}\033[0m")


def print_result(result: dict):
    """Prints the translated error to the terminal with colors."""
    print(f"\n{Colors.RED}{Colors.BOLD} Error Detected:{Colors.RESET}")
    print(f"{result.get('matched_error', 'N/A')}")
    
    if "file" in result:
        print(f"{Colors.YELLOW} Location: {result['file']} (Line {result['line']}){Colors.RESET}\n")
        if result.get("code"):
            print(f"{Colors.RESET}   |")
            print(f"{Colors.RESET}   |  {Colors.RED}{result['code']}{Colors.RESET}")
            print(f"{Colors.RESET}   |\n")
        else:
            print("\n")

    else:
        print()
    
    print(f"{Colors.CYAN}{Colors.BOLD} Explanation:{Colors.RESET}")
    print(f"{result['explanation']}\n")
    
    print(f"{Colors.GREEN}{Colors.BOLD} Suggested Fix:{Colors.RESET}")
    print(f"{result['fix']}\n")

    if result.get("ast_insight"):
        print(f"{Colors.MAGENTA}{Colors.BOLD} AST Insight:{Colors.RESET}")
        print(f"{result['ast_insight']}\n")

def run_script(script_name: str):
    """Runs a python script in the background and catches its errors."""
    import subprocess
    try:
        # Run the script using the current Python environment
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True
        )
        
        # If the script ran perfectly (Return Code 0), print standard output
        if result.returncode == 0:
            print(result.stdout, end="")
        
        # If the script crashed, print whatever succeeded, THEN translate the error
        else:
            if result.stdout:
                print(result.stdout, end="")
            
            translation = translate_error(result.stderr)
            print_result(translation)
            
    except FileNotFoundError:
        print(f"{Colors.RED}Error: Could not find script '{script_name}'{Colors.RESET}")

# Entry point of the program
def main():
    parser = argparse.ArgumentParser(
        prog="explain-error",
        description="Translate Python error messages into simple English.",
        epilog="Examples:\n  explain-error run script.py\n  explain-error \"NameError: name 'x' is not defined\"\n  cat error.log | explain-error",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-a",
        "--about",
        action="store_true",
        help="Display information about the tool."
    )
    
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Show the current version of the tool."
    )
    # Allow multiple arguments so we can accept "run script.py" or a long error string
    parser.add_argument(
        "args", 
        nargs="*", 
        help="Use 'run <script.py>' to execute a file, or pass an error string."
    )

    parsed_args = parser.parse_args()

    if parsed_args.about:
        print_about()
        sys.exit(0)
    
    if parsed_args.version:
        print(f"Error Translator CLI Version: {Colors.GREEN}{VERSION}{Colors.RESET}")
        sys.exit(0)
    
    # 1. Handle Piped Input (e.g., cat error.log | explain-error)
    if not sys.stdin.isatty():
        error_input = sys.stdin.read()
        if error_input.strip():
            print_result(translate_error(error_input))
            return

    # 2. Print help if no arguments
    if not parsed_args.args:
        parser.print_help()
        sys.exit(1)

    if parsed_args.args:
        # 3. Check if the user used the "run" command
        if parsed_args.args[0] == "run" and len(parsed_args.args) > 1:
            script_name = parsed_args.args[1]
            run_script(script_name)
        
        # 4. Fallback: Treat the input as a raw error string
        else:
            error_input = " ".join(parsed_args.args)
            print_result(translate_error(error_input))
    else:
        parser.print_help()
        sys.exit(1)
if __name__ == "__main__":
    main()