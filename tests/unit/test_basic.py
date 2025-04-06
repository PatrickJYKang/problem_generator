"""
Basic unit tests to verify that the testing framework works
"""

def test_addition():
    """Test that basic addition works"""
    assert 1 + 1 == 2

def test_string_methods():
    """Test basic string methods"""
    assert "hello".upper() == "HELLO"
    assert "WORLD".lower() == "world"
    assert "hello world".split() == ["hello", "world"]
