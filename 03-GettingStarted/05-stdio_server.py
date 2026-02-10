'''A simple MCP server demonstrating tool and resource definitions.'''
import logging
import requests
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an MCP server
server = FastMCP("Demo")

# Add an addition tool
@server.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@server.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@server.tool()
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers"""
    return a + b

@server.tool()
def calculate_product(a: int, b: int) -> int:
    """Calculate the product of two numbers"""
    return a * b

@server.tool()
def get_server_info() -> dict:
    """Get information about this MCP server"""
    return {
        "server_name": "example-stdio-server",
        "version": "1.0.0",
        "transport": "stdio",
        "capabilities": ["tools"]
    }

@server.tool()
def tell_joke() -> str:
    """Tell a random joke"""
    endpoint = "https://api.chucknorris.io/jokes/random"
    response = requests.get(endpoint, timeout=5).json()
    joke = response["value"]
    return joke

# Main execution block - this is required to run the server
if __name__ == "__main__":
    server.run()
