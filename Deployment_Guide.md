# Agentic AI Bootcamp

This bootcamp is a hands-on path from inference to production-style agents. You will call **NVIDIA® NIM™** from local endpoints, expose and consume capabilities with the **Model Context Protocol (MCP)** (including a low-level server implementation), and orchestrate reasoning and tool use with **LangGraph**. You will then use **NeMo Agent Toolkit (NAT)** to connect MCP tools to NIM with **YAML** workflow configuration—plus observability and evaluation—before tying the stack together in a final **Challenge**.

### Prerequisites

Participants are expected to have Python programming knowledge, basic prior knowledge of SQL databases and queries, Natural Language Processing knowledge, and NVIDIA NGC and API keys.

Ensure the following tools are installed on your system:
* [UV Package Manager](https://docs.astral.sh/uv/getting-started/installation/)
* [Python](https://docs.astral.sh/uv/guides/install-python/)
* [Git Version Control](https://github.com/git-guides/install-git)
* [Docker](https://docs.docker.com/engine/install/)
* [Jupyer lab](https://jupyter.org/install)

### Labs

#### Clone the git repository

```bash
https://github.com/openhackathons-org/agentic-ai-bootcamp
cd agentic-ai-bootcamp
```

#### Setup environment variables

For a multi-tenant setup, the below ports will need to be dynamically allocated.

```
BOOTCAMP_DIR=$PWD # path to agentic-ai-bootcamp
JUPYTER_PORT=8080 # Port to access jupyer lab
export PHOENIX_PORT=6006 # Port to access phoenix server
export MCP_PORT=8001 # Port to access HTTP based MCP Server
export NIM_PORT=8000 # Port to access NIM server
export INF_URL="http://${HOSTNAME}:${NIM_PORT}/v1" # NIM server URL, use https://integrate.api.nvidia.com/v1 if using cloud endpoints
export MODEL_ID=nvidia/nemotron-3-nano
```

#### Install project dependencies 

```bash
uv sync
```

#### Install OpenCode (Coding harness)

```bash
curl -fsSL https://opencode.ai/install | bash
```

#### Start the labs

```
jupyter lab --ip 0.0.0.0 --port $JUPYTER_PORT --no-browser --ServerApp.token='' --ServerApp.password=''
```

#### Opening the labs

With jupyer lab running, open http://$HOSTNAME:$JUPYTER_PORT. In the workspace, open the tutorial directory and start from start_here.ipynb.

When you are finished with the labs close your shell or pressing Ctrl+D in the terminal. Congratulations, you've successfully built and deployed an Agentic AI Bootcamp!
