"""Tests for NPPES client."""
import pytest
from app.infrastructure.nppes.client import search


@pytest.mark.asyncio
async def test_nppes_search_basic():
    """Test basic NPPES search functionality."""
    # This is an integration test - requires actual API call
    # For unit tests, we'd mock the HTTP client
    results = await search(first_name="JOHN", state="NY", limit=5)
    assert isinstance(results, list)
    # If API returns results, validate structure
    if results:
        result = results[0]
        assert "number" in result or "number" in result.get("basic", {})

