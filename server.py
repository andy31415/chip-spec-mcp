#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "fastmcp",
#     "click",
# ]
# ///
import click
from fastmcp import FastMCP

@click.command()
@click.option(
    "--matter-spec-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Path to the Matter Specification folder.",
    default=".",
    show_default=True,
)
@click.option(
    "--transport",
    type=click.Choice(['stdio', 'http']),
    default="stdio",
    help="Transport protocol for the MCP server (e.g., http, websockets).",
    show_default=True,
)
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Host address for the MCP server.",
    show_default=True,
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Port for the MCP server.",
    show_default=True,
)
def cli(matter_spec_path, transport, host, port):
    mcp = FastMCP("Demo")

    # Add an addition tool
    @mcp.tool()
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    # Add a dynamic greeting resource
    @mcp.resource("greeting://{name}")
    def get_greeting(name: str) -> str:
        """Get a personalized greeting"""
        return f"Hello, {name}!"

    print(f"Running for Matter Specification Path: {matter_spec_path}")
    if transport == 'stdio':
        mcp.run(transport=transport)
    else:
        mcp.run(transport=transport, host=host, port=port)

if __name__ == "__main__":
    cli()
