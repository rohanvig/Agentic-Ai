from duckduckgo_search import DDGS
from agents import function_tool

@function_tool
def duckduckgo_search(query: str) -> str:
    """Perform a web search using DuckDuckGo and return the results as a string."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
        if not results:
            return "No results found."
        
        formatted_results = []
        for r in results:
            formatted_results.append(f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n")
        
        return "\n---\n".join(formatted_results)
