"""
Example MCP client that connects to an MCP server via stdio.
Demonstrates reading a resource, listing resources and tools, and calling a tool.
"""
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="mcp",  # Executable
    args=["run", "server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

async def run():
    """
    Run an MCP client that connects to the server via stdio.
    Demonstrates reading a resource, listing resources and tools, and calling a tool.
    """
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()

            # List available resources
            resources = await session.list_resources()
            print("\nLISTING RESOURCES")
            for resource in resources:
                print("Resource: ", resource)

            # Read a resource
            print("\nREADING RESOURCE")
            contents = await session.read_resource("greeting://User")
            contents = contents.contents
            mime_type = contents[0].mimeType
            if mime_type == "text/plain":
                print("Received text:", contents[0].text)
            elif mime_type == "application/json":
                data = json.loads(contents[0].text)
                print("Received JSON:", data)
            else:
                print(f"Received {mime_type} data:", contents[0].text)

            for content in contents:
                print("Text:", content.text)  # This will print "Hello, Luiz!"
                print("MIME type:", content.mimeType)
                print("URI:", content.uri)
                print("Meta:", content.meta)

            # List available tools
            tools = await session.list_tools()
            print("\nLISTING TOOLS")
            for tool in tools.tools:
                print("Tool: ", tool.name)

            # Call a tool
            print("\nCALL TOOL")
            result = await session.call_tool("add", arguments={"a": 1, "b": 7})
            print(result.content)

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
