import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from qna_agent.main import create_sql_agent
import asyncio
import argparse

script_base_path = Path(__file__).parent.resolve() 
skills_dir = Path(__file__).parent.parent.resolve() / 'qna_agent' / 'skills'

async def test_qna_agent(model_id,inf_url,nvidia_api_key):
    agent = create_sql_agent(skills_dir,model_id,inf_url,nvidia_api_key,debug=True)   
    input = {
        "messages": [{
                "role": "user",
                "content": "Give me all artists with more than 1 album"
        }]
    }     
    result = agent.invoke(input)
    output = result['messages'][-1].content
    print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='qna agent')
    parser.add_argument('--model-id',
                       default=os.environ.get("MODEL_ID"),
                       help='model ID for the language model')
    parser.add_argument('--inf-url',
                       default=os.environ.get("INF_URL"),
                       help='base url for inference')
    parser.add_argument('--nvidia-api-key', 
                       default="dummy",
                       help='your nvidia api key')
    args = parser.parse_args()
    asyncio.run(test_qna_agent(args.model_id,args.inf_url,args.nvidia_api_key))
