import ast
import difflib
import os

class ScopedSymbolCollector(ast.NodeVisitor):
    """Walks the AST, respecting lexical scope based on the crash line number."""
    def __init__(self, target_line: int):
        self.target_line = target_line
        self.names = set()        # Variables
        self.attributes = set()   # Object attributes/methods
        self.classes = set()      # Class names
        self.functions = set()    # Function names
        self.imports = set()      # Imported modules or aliases

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.names.add(node.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # The function's name is always added to the enclosing scope
        self.names.add(node.name)
        self.functions.add(node.name)
        
        # SCOPING LOGIC: Only visit the body if the crash happened INSIDE this function
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            if node.lineno <= self.target_line <= node.end_lineno:
                self.generic_visit(node)
        else:
            self.generic_visit(node)

    def visit_ClassDef(self, node):
        # The class name is always added to the enclosing scope
        self.names.add(node.name)
        self.classes.add(node.name)
        
        # SCOPING LOGIC: Only visit the body if the crash happened INSIDE this class
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            if node.lineno <= self.target_line <= node.end_lineno:
                self.generic_visit(node)
        else:
            self.generic_visit(node)

    def visit_Attribute(self, node):
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


def get_ast_suggestions(filepath: str, line_number: str, target_word: str, error_type: str) -> str:
    if not os.path.exists(filepath) or filepath == "Unknown File":
        return None

    try:
        target_line = int(line_number) if line_number.isdigit() else 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        tree = ast.parse(source_code)
        collector = ScopedSymbolCollector(target_line)
        collector.visit(tree)
        
        pool = set()
        if error_type == "NameError":
            pool = collector.names | collector.functions | collector.classes
        elif error_type == "AttributeError":
            pool = collector.attributes | collector.functions 
        elif error_type in ("ImportError", "ModuleNotFoundError"):
            pool = collector.classes | collector.functions | collector.names | collector.imports
        
        matches = difflib.get_close_matches(target_word, pool, n=1, cutoff=0.6)
        
        if matches:
            return matches[0]
        return None
        
    except Exception:
        return None