# LLM-WORKFLOW-TEST

## Commands

Launch the mcp web server

```bash
cd mcp-servers/invoice
uv run mcp-server-invoice
```

Run the test

```
cd llm-workflow-test
uv run main.py --mcp-server-url http://localhost:$MCP_PORT/mcp --inf-url $INF_URL --inf-url-qna-agent $INF_URL --nvidia-api-key dummy 
```