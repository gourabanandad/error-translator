import error_translator.auto

def test_name_error_translation_double_quotes():
    """Test standard traceback with double quotes around the filename."""
    mock_traceback = """Traceback (most recent call last):
  File "script.py", line 2, in <module>
    print(my_variable)
NameError: name 'my_variable' is not defined"""

    result = error_translator(mock_traceback)
    
    assert "my_variable" in result["explanation"]
    assert result["file"] == "script.py"
    assert result["line"] == "2"

def test_name_error_translation_single_quotes():
    """Test PowerShell-style traceback with single quotes."""
    mock_traceback = """Traceback (most recent call last):
  File 'script.py', line 2, in <module>
    print(my_variable)
NameError: name 'my_variable' is not defined"""

    result = error_translator(mock_traceback)
    
    assert result["file"] == "script.py"
    assert result["line"] == "2"

def test_unknown_error_fallback():
    """Test that garbage input returns the default safe message."""
    mock_traceback = "Something completely random went wrong here."
    
    result = error_translator(mock_traceback)
    
    assert "unknown error" in result["explanation"]
    assert result["matched_error"] == "Something completely random went wrong here."