import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
from app import CivicGuideApp

@pytest.fixture(autouse=True)
def clean_session_state():
    """Reset streamlit session state before each test."""
    st.session_state.clear()
    yield

@patch('app.os.environ.get')
@patch('app.st.error')
@patch('app.st.stop')
def test_init_gemini_missing_key(mock_stop, mock_error, mock_get):
    """Test that the app safely stops if no API key is found (Security constraint)."""
    mock_get.return_value = None
    mock_stop.side_effect = SystemExit("st.stop() simulation")
    
    with pytest.raises(SystemExit):
        CivicGuideApp._init_gemini()
        
    mock_error.assert_called_once()
    mock_stop.assert_called_once()

@patch('app.CivicGuideApp._init_gemini')
def test_initialize_chat(mock_init):
    """Test that chat state initializes correctly."""
    mock_init.return_value = MagicMock()
    app = CivicGuideApp()
    assert "messages" in st.session_state
    assert len(st.session_state.messages) == 1
    assert st.session_state.messages[0]["role"] == "assistant"
    assert "Welcome!" in st.session_state.messages[0]["content"]

@patch('app.CivicGuideApp._init_gemini')
def test_input_validation(mock_init):
    """Test input validation blocking empty or malicious prompts."""
    mock_init.return_value = MagicMock()
    app = CivicGuideApp()
    
    # Test empty string (should block)
    assert app._validate_input("") is False
    
    # Test whitespace string (should block)
    assert app._validate_input("   ") is False
    
    # Test valid query (should pass)
    assert app._validate_input("How do I register to vote?") is True
    
    # Test excessively long string (should block to prevent token exhaustion)
    with patch('app.st.warning'):
        assert app._validate_input("A" * 2001) is False
