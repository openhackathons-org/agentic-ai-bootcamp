# NeMo Agent Toolkit Challenge

Complete `workflow.yaml` to configure a NeMo Agent Toolkit workflow that connects to the invoice MCP server and answers queries about invoices in the Chinook database.

## Testing your solution

First start the invoice MCP server:

```bash
cd ../mcp-servers/invoice && uv run mcp-server-invoice &
```

Then test your workflow with a question, for example:

```bash
nat run --config_file workflow.yaml --input "How many Led Zeppelin tracks did Aaron Mitchell (Number +1 (204) 452-6452) purchase?"
```
