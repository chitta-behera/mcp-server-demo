# server.py
from mcp.server.fastmcp import FastMCP
# from linkup import LinkupClient

# Create an MCP server
mcp = FastMCP("Demo")
# client = LinkupClient()


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# @mcp.tool()
# def web_search(query: str) -> str:
#     """Search the web for the given query."""
#     search_response = client.search(
#         query=query,
#         depth="standard",  # "standard" or "deep"
#         output_type="sourcedAnswer",  # "searchResults" or "sourcedAnswer" or "structured"
#         structured_output_schema=None,  # must be filled if output_type is "structured"
#     )
#     return search_response

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="stdio")