# MCP Learn

A simple example repository demonstrating how to build and interact with an MCP (Model Context Protocol) server and client in Python.

## Overview

This repo contains:
- An MCP server (`server.py`) exposing tools and resources
- Example clients (`client.py`, `llm_client.py`) that connect to the server, list tools/resources, and call tools
- Integration with LLMs (Azure OpenAI) via `llm_client.py`

## Structure

- `server.py`: Defines an MCP server with:
  - A tool: `add(a, b)` to add two numbers
  - A resource: `greeting://{name}` to return a personalized greeting
- `client.py`: Connects to the server via stdio, demonstrates:
  - Reading a resource
  - Listing resources and tools
  - Calling a tool
- `llm_client.py`: Connects to the server and Azure OpenAI, demonstrates:
  - Listing tools and converting them to LLM tool schemas
  - Asking the LLM which tools to call for a prompt
  - Calling suggested tools and printing results

## Usage

### 1. Start the MCP server
```bash
python server.py
```

### 2. Run the example client
```bash
python client.py
```

### 3. Run the LLM client (requires Azure OpenAI credentials)
```bash
export GITHUB_TOKEN=your_azure_api_key
python llm_client.py
```

## Requirements
- Python 3.11+
- MCP Python package
- Azure OpenAI SDK (for `llm_client.py`)

## Customization
- Add more tools/resources in `server.py`
- Update client logic to consume new tools/resources
- Integrate with other LLMs or APIs as needed

## License
MIT
