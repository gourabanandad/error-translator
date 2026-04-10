import sys
import argparse
from .core import translate_error

# ANSI Color Codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

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

def main():
    parser = argparse.ArgumentParser(
        description="Translate Python error messages into simple English."
    )
    
    # Allow multiple arguments so we can accept "run script.py" or a long error string
    parser.add_argument(
        "args", 
        nargs="*", 
        help="Use 'run <script.py>' to execute a file, or pass an error string."
    )

    parsed_args = parser.parse_args()

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

    # 3. Check if the user used the "run" command
    if parsed_args.args[0] == "run" and len(parsed_args.args) > 1:
        script_name = parsed_args.args[1]
        run_script(script_name)
    
    # 4. Fallback: Treat the input as a raw error string
    else:
        error_input = " ".join(parsed_args.args)
        print_result(translate_error(error_input))

if __name__ == "__main__":
    main()