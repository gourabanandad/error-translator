from error_translator.core import translate_error

def test_name_error_translation():
    mock_traceback = """Traceback (most recent call last):
  File "main.py", line 3, in <module>
    print(x)
NameError: name 'x' is not defined"""

    result = translate_error(mock_traceback)
    
    assert "x" in result["explanation"]
    assert result["file"] == "main.py"
    assert result["line"] == "3"