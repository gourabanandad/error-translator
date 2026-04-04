import re

# We compile the regex patterns upfront for performance.
ERROR_RULES = [
    {
        "pattern": re.compile(r"NameError: name '(.*)' is not defined"),
        "explanation": "You tried to use a variable or function named '{0}', but Python doesn't recognize it.",
        "fix": "Check if '{0}' is spelled correctly, or ensure you defined/imported it before using it."
    },
    {
        "pattern": re.compile(r"TypeError: can only concatenate str \(not \"(.*)\"\) to str"),
        "explanation": "You are trying to add a string to a {0}, which Python cannot do.",
        "fix": "Convert the {0} to a string first using str() before concatenating."
    },
    {
        "pattern": re.compile(r"TypeError: unsupported operand type\(s\) for \+: '(.*)' and '(.*)'"),
        "explanation": "You are trying to add two incompatible types: a {0} and a {1}.",
        "fix": "Ensure both sides of the '+' are the same type (e.g., both numbers or both strings)."
    },
    {
        "pattern": re.compile(r"IndexError: list index out of range"),
        "explanation": "You are trying to access an item in a list at a position that doesn't exist.",
        "fix": "Check the length of your list using len(). Remember, Python lists start counting at 0!"
    },
    {
        "pattern": re.compile(r"KeyError: '(.*)'"),
        "explanation": "You tried to look up a key named '{0}' in a dictionary, but that key doesn't exist.",
        "fix": "Check for typos in the key name, or use the .get('{0}') method to safely access dictionary values."
    },
    {
        "pattern": re.compile(r"ZeroDivisionError: division by zero"),
        "explanation": "You are trying to divide a number by zero, which is mathematically impossible.",
        "fix": "Add an if-statement before the division to check if the denominator is 0."
    },
    {
        "pattern": re.compile(r"ModuleNotFoundError: No module named '(.*)'"),
        "explanation": "Python is trying to import a package named '{0}', but it isn't installed in your current environment.",
        "fix": "Open your terminal and run: pip install {0}"
    },
    {
        "pattern": re.compile(r"AttributeError: '(.*)' object has no attribute '(.*)'"),
        "explanation": "You are trying to use a method or property named '{1}' on a {0} object, but {0}s don't have that capability.",
        "fix": "Check the spelling of '{1}'. If it's correct, verify that your variable is actually the data type you think it is."
    },
]

DEFAULT_ERROR = {
    "explanation": "This is an unknown error. The tool couldn't find a specific match.",
    "fix": "Try copying the last line of the error into a search engine or StackOverflow."
}