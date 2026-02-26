"""
Example MCP client that connects to an MCP server via http.
Demonstrates reading a resource, listing resources and tools, and calling a tool.

It will also read context messages (notifications) from the server.
"""
import json
import asyncio
import httpx

# HTTP transport helper (not stdio)
from mcp.client.streamable_http import streamable_http_client
from mcp.client.session import ClientSession
# parameter class lives in the session_group module
from mcp.client.session_group import StreamableHttpParameters
import mcp.types as types

async def message_handler(msg):
    """"
    Handle incoming messages from the server, including notifications.
    """
    if isinstance(msg, types.ServerNotification):
        print("NOTIFICATION:", msg)
    else:
        print("SERVER MESSAGE:", msg)



# Create server parameters with http transport
# NOTE: the installed MCP library uses the streamable_http transport helper
server_params = StreamableHttpParameters(
    url="http://localhost:8000/mcp",  # MCP server endpoint
    headers={"Authorization": "Bearer my-secret-token"},  # Optional headers for authentication
    # you can also adjust timeouts or termination behavior here
)

async def run():
    """
    Run an MCP client that connects to the server via http.
    Demonstrates reading a resource, listing resources and tools, and calling a tool.
    """
    # streamable_http_client expects a URL (and optional httpx client).
    # we'll build a simple httpx client to include the headers from our
    # parameters object.  for a real application you might call
    # ``create_mcp_http_client`` from ``mcp.shared._httpx_utils`` instead.
    async with streamable_http_client(
        server_params.url,
        http_client=httpx.AsyncClient(headers=server_params.headers),
        terminate_on_close=server_params.terminate_on_close,
    ) as (read, write, get_session_id):
        async with ClientSession(
            read,
            write,
            message_handler=message_handler,   # receive notifications
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

            # Call all tools
            for tool in tools.tools:
                print(f"\nCALLING TOOL: {tool.name}")
                result = await session.call_tool(
                    tool.name,
                    arguments={"message": "Hello from the client!", "ctx": None})
                print("Tool result:", result.content)

if __name__ == "__main__":
    asyncio.run(run())
