import ast
import difflib
import os

class ComprehensiveSymbolCollector(ast.NodeVisitor):
    """Walks the Abstract Syntax Tree to collect all defined symbols in a file."""
    def __init__(self):
        self.names = set()        # Variables
        self.attributes = set()   # Object attributes/methods
        self.classes = set()      # Class names
        self.functions = set()    # Function names
        self.imports = set()      # Imported modules or aliases

    def visit_Name(self, node):
        # Only collect names that are being assigned/stored (defining a variable)
        if isinstance(node.ctx, ast.Store):
            self.names.add(node.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.names.add(node.name)
        self.functions.add(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.names.add(node.name)
        self.classes.add(node.name)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Collects any '.attribute' used in the file
        self.attributes.add(node.attr)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports.add(name)
            self.names.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports.add(name)
            self.names.add(name)
        self.generic_visit(node)


def get_ast_suggestions(filepath: str, target_word: str, error_type: str) -> str:
    """
    Parses the file, builds a pool of valid symbols based on the error type,
    and returns the closest match using Levenshtein distance.
    """
    if not os.path.exists(filepath) or filepath == "Unknown File":
        return None

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        tree = ast.parse(source_code)
        collector = ComprehensiveSymbolCollector()
        collector.visit(tree)
        
        # Determine which pool of words to check against based on the error
        pool = set()
        if error_type == "NameError":
            pool = collector.names | collector.functions | collector.classes
        elif error_type == "AttributeError":
            pool = collector.attributes | collector.functions 
        elif error_type in ("ImportError", "ModuleNotFoundError"):
            pool = collector.classes | collector.functions | collector.names | collector.imports
        
        # Find the closest match (cutoff=0.6 means it must be at least 60% similar)
        matches = difflib.get_close_matches(target_word, pool, n=1, cutoff=0.6)
        
        if matches:
            return matches[0]
        return None
        
    except Exception:
        # Failsafe: if the file has a SyntaxError and cannot be parsed, degrade gracefully
        return None