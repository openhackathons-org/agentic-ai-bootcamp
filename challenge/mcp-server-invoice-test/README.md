# MCP-SERVER-INVOICE-TEST

## Commands

Launch the mcp web server
```bash
cd mcp-servers/invoice
uv run mcp-server-invoice
```

Run the test
```bash
cd mcp-server-invoice-test
uv run main.py --mcp-server-url http://localhost:8000/mcp
```