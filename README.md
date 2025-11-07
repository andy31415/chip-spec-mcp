# Project info

This is a basic MCP server intended to allow LLMs to access the matter specification
and test plans from a local checkout when performing operations.

To work with gemini cli, this currently uses "tools" rather than resources (that
would require RAGs and it is a different setup).

## Usage

Add in `~/.gemini/settings.json`:

```
"mcpServers": {
  "MatterSpec": {
    "command": "uv",
    "args": [
      "run",
      "/usr/local/google/home/andreilitvin/devel/chip-spec-mcp/server.py"
    ],
    "timeout": 30000,
    "trust": false
  }
}
```

Make sure [uv](https://docs.astral.sh/uv/) is installed.
