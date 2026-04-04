import sys
import argparse

from cv2 import line
from .core import translate_error

# ANSI Color Codes for terminal formatting
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_result(result: dict):
    """Prints the translated error to the terminal with colors."""
    print(f"\n{Colors.RED}{Colors.BOLD}🚨 Error Detected:{Colors.RESET}")
    print(f"{result.get('matched_error', 'N/A')}\n")
    
    # If file and line info is available, print it
    if "file" in result:
        print(f"{Colors.YELLOW}📍 Location: {result['file']} (Line {result['line']}){Colors.RESET}\n")
    else:
        print() # Just a newline

    print(f"{Colors.CYAN}{Colors.BOLD}🧠 Explanation:{Colors.RESET}")
    print(f"{result['explanation']}\n")
    
    print(f"{Colors.GREEN}{Colors.BOLD}🛠️  Suggested Fix:{Colors.RESET}")
    print(f"{result['fix']}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Translate Python error messages into simple English."
    )
    
    parser.add_argument(
        "error_text", 
        nargs="?", 
        help="The error message or traceback string to translate."
    )

    args = parser.parse_args()

    # Read from positional argument OR standard input (piping)
    error_input = args.error_text

    if not error_input and not sys.stdin.isatty():
        # Allows usage like: cat error.log | explain-error
        error_input = sys.stdin.read()

    if not error_input:
        parser.print_help()
        sys.exit(1)

    result = translate_error(error_input)
    print_result(result)

if __name__ == "__main__":
    main()