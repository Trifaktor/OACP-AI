"""
Simple wrapper around duckduckgo-search to perform web searches.

This helper uses the DDGS context manager to issue a text search and
returns a list of result dicts. In production you may wish to swap
this out for a dedicated search API with higher quotas or reliability.
"""

from duckduckgo_search import DDGS
from typing import List, Dict


def web_search(query: str, max_results: int = 8) -> List[Dict[str, str]]:
    """Perform a web search and return up to `max_results` results.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.

    Returns:
        A list of dictionaries containing titles and other metadata.
    """
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))