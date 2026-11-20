import pytest
from app.utils.validators import normalize_and_validate_url

def test_rejects_ftp():
    with pytest.raises(ValueError):
        normalize_and_validate_url("ftp://example.com")

def test_rejects_localhost():
    with pytest.raises(ValueError):
        normalize_and_validate_url("http://localhost:8000")

def test_rejects_credentials():
    with pytest.raises(ValueError):
        normalize_and_validate_url("https://user:pass@example.com")
