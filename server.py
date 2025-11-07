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

import glob
import os


class MatterSpecData:
    def __init__(self, spec_path: str):
        self.spec_path = spec_path
        self.docs = {}

        # figure out all doc names
        for name in glob.glob(os.path.join(spec_path, "src", "**", "*.adoc")):
            self.docs[name[len(spec_path) :].strip("/")] = name

    def get_doc(self, name):
        with open(self.docs[name], "rt", encoding="utf8") as f:
            return f.read()


class MatterTestPlanData:
    def __init__(self, spec_path: str):
        self.spec_path = spec_path
        self.docs = {}

        # figure out all doc names
        for name in glob.glob(os.path.join(spec_path, "src", "**", "*.adoc")):
            self.docs[name[len(spec_path) :].strip("/")] = name

    def get_doc(self, name):
        with open(self.docs[name], "rt", encoding="utf8") as f:
            return f.read()


@click.command()
@click.option(
    "--spec",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Path to the Matter Specification folder.",
    default="~/devel/connectedhomeip-spec",
    show_default=True,
)
@click.option(
    "--test-plans",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Path to the Matter Test plans folder.",
    default="~/devel/chip-test-plans",
    show_default=True,
)
@click.option(
    "--transport",
    type=click.Choice(["stdio", "http"]),
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
def cli(spec, test_plans, transport, host, port: int):
    mcp = FastMCP("Demo")

    print(f"Matter Specification Path: {spec}")
    print(f"Test plan path:            {test_plans}")
    matter_spec = MatterSpecData(spec)
    test_plan_data = MatterTestPlanData(spec)

    @mcp.resource("data://available/spec-docs")
    def get_spec_documents() -> list[str]:
        """
        Get available specification document names.
        """
        return list(matter_spec.docs.keys())

    @mcp.resource("data://available/test-plans")
    def get_test_documents() -> list[str]:
        """
        Get available test plan document names.
        """
        return list(test_plan_data.docs.keys())

    @mcp.resource("spec-doc://{name}")
    def get_spec_data(name: str) -> str:
        """
        Get a specific spec document.
        """
        return matter_spec.get_doc(name)

    @mcp.resource("test-plan://{name}")
    def get_test_plan(name: str) -> str:
        """
        Get a specific test plan document.
        """
        return test_plan_data.get_doc(name)

    if transport == "stdio":
        mcp.run(transport=transport)
    else:
        mcp.run(transport=transport, host=host, port=port)


if __name__ == "__main__":
    cli()
