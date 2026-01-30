from mcp import ClientSession
from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamablehttp_client
import os

class MCPHTTPCLIENT:
    def __init__(self,url):
        ## TODO
        ## initialize any required class variables
        pass

    async def connect(self):
        ## TODO
        ## connect to mcp server and initialize client session
        pass

    async def cleanup(self):
        ## TODO
        ## clean up resources
        pass