mkdir -p submission/llm-workflow submission/mcp-servers/invoice submission/qna_agent
cp llm_workflow/main.py submission/llm-workflow/main.py
cp llm_workflow/mcp_http_client.py submission/llm-workflow/mcp_http_client.py
cp mcp-servers/invoice/src/mcp_server_invoice/server_http.py submission/mcp-servers/invoice/server_http.py
cp qna_agent/skills/music-store-assistant/SKILL.md submission/qna_agent/SKILL.md
zip -r submission.zip submission