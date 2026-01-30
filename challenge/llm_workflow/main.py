from typing import Literal
import json
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import SystemMessage
from langchain_core.messages import convert_to_openai_messages
from langgraph.types import Command, interrupt
from tabulate import tabulate
from typing_extensions import Annotated, TypedDict
from pydantic import BaseModel
from openai import AsyncOpenAI
from qna_agent.main import create_sql_agent
import sqlite3
from pathlib import Path
from .mcp_http_client import MCPHTTPCLIENT

skills_dir = Path(__file__).parent.parent.resolve() / 'qna_agent' / 'skills'
chinook_db_path = Path(__file__).parent.resolve() / "chinook.db"

model_id='nvidia/llama-3.3-nemotron-super-49b-v1'

class State(TypedDict):
    """Agent state."""
    messages: Annotated[list[AnyMessage], add_messages]
    intent: str
    followup: str | None
    invoice_id: int | None
    invoice_line_ids: list[int] | None
    customer_first_name: str | None
    customer_last_name: str | None
    customer_phone: str | None
    track_name: str | None
    album_title: str | None
    artist_name: str | None
    purchase_date_iso_8601: str | None

# Instructions for extracting the user/purchase info from the conversation.
gather_info_instructions = """You are managing an online music store that sells song tracks. \
Customers can buy multiple tracks at a time and these purchases are recorded in a database as \
an Invoice per purchase and an associated set of Invoice Lines for each purchased track.

Your task is to help customers who would like a refund for one or more of the tracks they've \
purchased. In order for you to be able refund them, the customer must specify the Invoice ID \
to get a refund on all the tracks they bought in a single transaction, or one or more Invoice \
Line IDs if they would like refunds on individual tracks.

Often a user will not know the specific Invoice ID(s) or Invoice Line ID(s) for which they \
would like a refund. In this case you can help them look up their invoices by asking them to \
specify:
- Required: Their first name, last name, and phone number.
- Optionally: The track name, artist name, album name, or purchase date.

IMPORTANT: When extracting phone numbers:
- Preserve ALL spaces, dashes, parentheses, and formatting exactly as provided by the user
- Do NOT modify, standardize, or strip any characters from phone numbers
- Example: If user provides '+1 (204) 452-6452', store it exactly as '+1 (204) 452-6452'
- Do not convert formats like '555 123 4567' to '5551234567'

If the customer has not specified the required information (either Invoice/Invoice Line IDs \
or first name, last name, phone) then please ask them to specify it."""

async def qna_agent(state:State,config: RunnableConfig):
    inf_url = config.get("configurable", {}).get("inf_url")
    nvidia_api_key = config.get("configurable", {}).get("nvidia_api_key")
    agent = create_sql_agent(skills_dir,inf_url,nvidia_api_key,debug=True)
    messages = convert_to_openai_messages([*state['messages']])
    result = agent.invoke({'messages':messages})
    try:
        sql_cmd = result['structured_response'].sql
        conn = sqlite3.connect(str(chinook_db_path))
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        results = cursor.fetchall()
        output = {
            "messages": [{"role": "assistant", "content": json.dumps(results)}],
        }
    except:
        output = {
            "messages": [{"role": "assistant", "content": "error executing sql command"}]
        }
    finally:
        conn.close()
    return output

async def refund_agent(state:State,config: RunnableConfig):
    
    mcp_server_url = config.get("configurable", {}).get("mcp_server_url")
    inf_url = config.get("configurable", {}).get("inf_url")
    nvidia_api_key = config.get("configurable", {}).get("nvidia_api_key")
    openAI_client = AsyncOpenAI(
        base_url = inf_url,
        api_key = nvidia_api_key
    )

    system_message = SystemMessage(content=gather_info_instructions)
    messages =  convert_to_openai_messages([system_message,*state['messages']])

    mcp_client = MCPHTTPCLIENT(mcp_server_url)
    await mcp_client.connect()

    ## TODO
    ## list tools, format tools to openai function calling schema, get response from NVIDIA NIM/LLM

    if stop_reason == 'tool_calls':
        for tool_call in response.choices[0].message.tool_calls:
            
            ## TODO
            ## Implement tool calling
            
            if tool_name == 'invoice_refund':
                content = f"You have been refunded a total of: ${result}. Is there anything else I can help with?"
                followup = content
                output = {
                    "messages": [tool_message,{"role": "assistant", "content": content}],
                    "followup": followup,
                }
            elif tool_name == 'invoice_lookup':
                result = json.loads(tool_result.content[0].text)
                if not result:
                    content = "We did not find any purchases associated with the information you've provided. Are you sure you've entered all of your information correctly?"
                    followup = content
                    output = {
                        "messages": [tool_message,{"role": "assistant", "content": content}],
                        "followup": followup,
                    }
                else:
                    content = f"Which of the following purchases would you like to be refunded for?\n\n```json{json.dumps(result, indent=2)}\n```"
                    followup = f"Which of the following purchases would you like to be refunded for?\n\n{tabulate(result, headers='keys')}"
                    output = {
                        "messages": [tool_message,{"role": "assistant", "content": content}],
                        "followup": followup,
                        "invoice_line_ids": [item["invoice_line_id"] for item in result],
                    }
            
    elif stop_reason == 'stop':
        output = {
            "messages": [{"role": "assistant", "content": response.choices[0].message.content}]
        }

    else:
        output = {
            "messages": [{"role": "assistant", "content": f"unknown error with stop reason {stop_reason}"}]
        }
    
    await mcp_client.cleanup()

    return output

class UserIntent(BaseModel):
    """The user's current intent in the conversation"""
    intent: Literal["QNA","REFUND","UNKNOWN"]

router_llm = init_chat_model(model=model_id,model_provider="nvidia",configurable_fields=["base_url","api_key"]).with_structured_output(
    UserIntent, method="json_schema", strict=True
)

intent_classifier_instructions = """You are managing an online music store that sells song tracks. \
You can help customers by answering general questions about tracks sold at your store or help them get a refund on a purhcase they made at your store.

Return 'QNA' if they are asking a general music question or 'REFUND' if they asking for a refund. Return 'UNKNOWN' otherwise. Do NOT return anything else. Do NOT try to respond to the user.
"""

# Node for routing.
async def intent_classifier(state: State,config: RunnableConfig):
    inf_url = config.get("configurable", {}).get("inf_url")
    nvidia_api_key = config.get("configurable", {}).get("nvidia_api_key")
    response = router_llm.with_config({"base_url":inf_url,"api_key":nvidia_api_key}).invoke(
        [{"role": "system", "content": intent_classifier_instructions}, *state["messages"]]
    )

    if response.intent == 'UNKNOWN':
        interrupt("Please ask a relevant question")
    elif response.intent == "QNA":
        return Command(goto="qna_agent")
    elif response.intent == "REFUND":
        return Command(goto="refund_agent")
        

# Node for making sure the 'followup' key is set before our agent run completes.
def compile_followup(state: State) -> dict:
    """Set the followup to be the last message if it hasn't explicitly been set."""
    if not state.get("followup"):
        return {"followup": state["messages"][-1].content}
    return {}

def create_workflow(memory):
    # Agent definition
    workflow = StateGraph(State)
    
    ## TODO
    ## Define nodes and edges for graph

    app = workflow.compile(checkpointer=memory)

    return app

