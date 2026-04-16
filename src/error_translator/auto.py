import sys
import traceback
from .core import translate_error
from .cli import print_result

def magic_hook(exc_type, exc_value, tb):
    """
    This function intercepts a Python crash right before it prints 
    to the terminal, formats the error, and translates it.
    """
    # 1. Convert the raw crash data into a standard traceback string
    tb_lines = traceback.format_exception(exc_type, exc_value, tb)
    tb_string = "".join(tb_lines)
    
    # 2. Pass it through our translation engine
    result = translate_error(tb_string)
    
    # 3. Print our beautiful colorized output instead of the ugly default
    print_result(result)

# The Magic Trick: Replace Python's default crash handler with ours
sys.excepthook = magic_hook