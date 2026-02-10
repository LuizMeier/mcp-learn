# Testing with FastMCP
from mcp.server.fastmcp import FastMCP
import asyncio

# Initialize FastMCP server
mcp = FastMCP("my-lab")

@mcp.tool(description="A tool that reads files and sends progress notifications")
async def process_files(message: str, ctx) -> str:

    def map_files():
        """
        Get all files from the local directory and return a list of their names.
        """
        import os
        return [f for f in os.listdir('.') if os.path.isfile(f)]
    
    file_list = map_files()
    
    # In FastMCP, the 'ctx' is automatically injected if requested
    # You use ctx.info(), ctx.error() etc.
    file_count = len(file_list)
    for i, file in enumerate(file_list, start=1):
        await ctx.info(f"Processing file {i}/{file_count}: {file}")
        await asyncio.sleep(1)  # Simulate time-consuming processing

    # You can return just a string, FastMCP converts it to TextContent
    return f"Done: {message}"

if __name__ == "__main__":
    # FastMCP makes it easy to use different transports
    # For HTTP, it uses the server under the hood
    mcp.run(transport="streamable-http") 
