# Agentic AI NIM Bootcamp

This repo contains the challenge and the tutorial for the bootcamp

## Bootcamp Content

The challenge consists of the following parts.

1. Creating a Question & Answer (Q&A) MCP Server
2. Creating an Invoice MCP Server
3. Modifying the existing LLM workflow to utilise both the Q&A and Invoice MCP Servers

## Tools and Frameworks

The tools and frameworks used in this bootcamp are as follows

1. [NVIDIA NIM](https://docs.nvidia.com/nim/index.html)
2. [Model Context Protocol](https://modelcontextprotocol.io/introduction)
3. [LangGraph](https://langchain-ai.github.io/langgraph/)

## Bootcamp Duration

The duration of the tutorial is 2 hours.  
The duration of the challenge is 4 hours.

## Prerequisites

1. Register for an account and generate API key with [build.nvidia.com](https://build.nvidia.com/)

    **Prepaid cards or numbers marked as spam will not be able to register for an API Key**

2. Setup API key in environment variable

    ### MacOS

    - Open a terminal
    - Edit .zprofile

        `vi ~/.zprofile`

    - insert the following line to end of file

        `export NVIDIA_API_KEY=<your api key>`

    - exit vi editor

        `source ~/.zprofile`

    ### Windows

    - Open CMD terminal

        `setx NVIDIA_API_KEY "<your api key>"`

3. Test your API Key to ensure it has permissions to invoke the cloud endpoints

    ### MacOS

    Replace [YOUR_API_KEY] with your generated API key from 1)
    ```
    curl https://integrate.api.nvidia.com/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer [YOUR_API_KEY]" \
    -d '{
        "model": "nvidia/llama-3.3-nemotron-super-49b-v1",
        "messages": [{"role":"system","content":"detailed thinking on"}],
        "temperature": 0.6,   
        "top_p": 0.95,
        "max_tokens": 4096,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stream": false                
    }'
    ```

    ### Windows

    Replace [YOUR_API_KEY] with your generated API key from 1)
    ```
    curl https://integrate.api.nvidia.com/v1/chat/completions ^
    -H "Content-Type: application/json" ^
    -H "Authorization: Bearer [YOUR_API_KEY]" ^
    -d "{\"model\": \"nvidia/llama-3.3-nemotron-super-49b-v1\", \"messages\": [{\"role\":\"system\",\"content\":\"detailed thinking on\"}], \"temperature\": 0.6, \"top_p\": 0.95, \"max_tokens\": 4096, \"frequency_penalty\": 0, \"presence_penalty\": 0, \"stream\": false}"
    ```

4. Install the following packages

    * [uv package manager](https://docs.astral.sh/uv/getting-started/installation/)
    * [python](https://docs.astral.sh/uv/guides/install-python/)
    * [git version control](https://github.com/git-guides/install-git)
    * [claude desktop](https://claude.ai/download)

5. Deploy NIMs locally (not required if using cloud endpoints)

    Follow the below instructions for the respective NIMs
    [llama-3.3-nemotron-super-49b-v1](https://build.nvidia.com/nvidia/llama-3_3-nemotron-super-49b-v1/deploy?environment=linux.md)
    [mistral-nemo-12b-instruct](https://build.nvidia.com/nv-mistralai/mistral-nemo-12b-instruct/deploy)

## Steps

1. Clone this repository

    ```
    git clone https://github.com/openhackathons-org/bootcamp-challenge-public-nim.git
    ```

2. Learn how to build MCP Clients/Servers for agentic tool calling in the [MCP tutorial](./tutorial/mcp-tutorial.md).

3. Learn how to utilise NVIDIA NIMs and MCP in agentic workflows using the [Agent tutorial](./tutorial/agent-tutorial.md)

4. Attempt the [challenge](./challenge/problem_statement.md) to modify an existing LLM workflow to utilise NVIDIA NIM and MCP.

## Attribution

This material originates from the OpenHackathons Github repository. Check out additional materials [here](https://github.com/openhackathons-org)

Don't forget to check out additional [Open Hackathons Resources](https://www.openhackathons.org/s/technical-resources) and join our [OpenACC and Hackathons Slack Channel](https://www.openacc.org/community#slack) to share your experience and get more help from the community.

## Licensing

Copyright © 2025 OpenACC-Standard.org. This material is released by OpenACC-Standard.org, in collaboration with NVIDIA Corporation, under the Creative Commons Attribution 4.0 International (CC BY 4.0). These materials may include references to hardware and software developed by other entities; all applicable licensing and copyrights apply.