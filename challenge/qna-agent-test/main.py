import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from qna_agent.main import create_sql_agent
import sqlite3
import json
from rouge import Rouge
import pandas as pd
import asyncio
import argparse

script_base_path = Path(__file__).parent.resolve() 
skills_dir = Path(__file__).parent.parent.resolve() / 'qna_agent' / 'skills'
chinook_db_path = script_base_path / "chinook.db"

async def test_qna_agent(inf_url,nvidia_api_key):
    agent = create_sql_agent(skills_dir,inf_url,nvidia_api_key,debug=True)   
    input = {
        "messages": [{
                "role": "user",
                "content": "Give me all artists with more than 1 album"
        }]
    }     
    result = agent.invoke(input)

    try:
        sql_cmd = result['structured_response'].sql
        conn = sqlite3.connect(str(chinook_db_path))
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        results = cursor.fetchall()
        print(results)
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='qna agent')
    parser.add_argument('--inf-url', 
                       default="https://integrate.api.nvidia.com/v1",
                       help='base url for inference')
    parser.add_argument('--nvidia-api-key', 
                       default="dummy",
                       help='your nvidia api key')
    args = parser.parse_args()
    asyncio.run(test_qna_agent(args.inf_url,args.nvidia_api_key))
