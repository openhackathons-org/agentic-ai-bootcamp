
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.resolve()))
import asyncio
import argparse
from langgraph.checkpoint.memory import InMemorySaver
from llm_workflow import create_workflow

async def run(app,config,input):
    await app.ainvoke(input,debug=True,config=config)

async def main(nvidia_api_key,mcp_server_url,inf_url):

    memory = InMemorySaver()
    config = {
        "configurable": {"thread_id": "1"},
        "env":"test",
        "nvidia_api_key": nvidia_api_key,
        "mcp_server_url": mcp_server_url,
        "inf_url": inf_url
    }
    app = create_workflow(memory=memory)

    state = {
        "messages":[
        {
            "role": "user",
            "content":  "my name is Aaron Mitchell and my number is +1 (204) 452-6452. I bought some songs by the artist Led Zeppelin that i'd like refunded",
        }
    ]}
    
    await run(app,config,state)
    snapshot = app.get_state(config)
    print(snapshot.values)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='llm workflow test')
    parser.add_argument('--nvidia-api-key', 
                       default="",
                       help='your nvidia api key')
    parser.add_argument('--mcp-server-url', 
                       default="http://localhost:8000/mcp",
                       help='mcp server url')
    parser.add_argument('--inf-url', 
                       default="https://integrate.api.nvidia.com/v1",
                       help='base url for inference')
    args = parser.parse_args()
    asyncio.run(main(args.nvidia_api_key,args.mcp_server_url,args.inf_url))
   
