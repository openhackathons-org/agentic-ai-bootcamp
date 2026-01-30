# LLM-WORKFLOW-TEST

## Commands

Launch the mcp web server

```bash
cd mcp-servers/invoice
uv run mcp-server-invoice
```

Run the test

```bash
cd llm-workflow-test
uv run main.py --mcp-server-url http://localhost:8000/mcp --inf-url http://localhost:9998/v1 --inf-url-qna-agent http://localhost:9999/v1 --nvidia-api-key dummy 
```