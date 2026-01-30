import uuid
from typing import TypedDict, NotRequired
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware, AgentState
from langchain.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from typing import Callable
from pathlib import Path
from .skills_ref.utils import list_skills
from .skills_ref.parser import read_instruction
from .skills_ref.models import SkillProperties

class SkillsState(AgentState):
    """State for the skills middleware."""

    skills_metadata: NotRequired[list[SkillProperties]]
    """List of loaded skill metadata (name, description, path)."""

# Create skill loading tool
@tool
def load_skill(skills_dir: Path,skill_name: str) -> str:
    """Load the full content of a skill into the agent's context.

    Use this when you need detailed information about how to handle a specific
    type of request. This will provide you with comprehensive instructions,
    policies, and guidelines for the skill area.

    Args:
        skill_name: The name of the skill to load (e.g., "qna agent")
    """
    content = read_instruction(skills_dir / skill_name)
    if content:
        return f"Loaded skill: {skill_name}\n\ncontent"
    else:
        skills = list_skills(skills_dir)
        available = ", ".join(skills.name for s in skills)
        return f"Skill '{skill_name}' not found. Available skills: {available}"

# Create skill middleware
class SkillMiddleware(AgentMiddleware):
    """Middleware that injects skill descriptions into the system prompt."""

    state_schema = SkillsState

    # Register the load_skill tool as a class variable
    tools = [load_skill]

    def __init__(self,skills_dir):
        self.skills_dir = skills_dir
    
    def before_agent(self, state:SkillsState, runtime):
        skills = list_skills(self.skills_dir)
        return SkillsState(skills_metadata=skills)

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Sync: Inject skill descriptions into system prompt."""

        skills = request.state.get("skills_metadata", [])
        skills_list = []
        for skill in skills:
            skills_list.append(
                f"- **{self.skills_dir / skill.name}**: {skill.description}"
            )
        self.skills_prompt = "\n".join(skills_list)

        # Build the skills addendum
        skills_addendum = (
            f"\n\n## Available Skills\n\n{self.skills_prompt}\n\n"
            "Use the load_skill tool when you need detailed information "
            "about handling a specific type of request."
        )

        # Append to system message content blocks
        new_content = list(request.system_message.content_blocks) + [
            {"type": "text", "text": skills_addendum}
        ]
        new_system_message = SystemMessage(content=new_content)
        modified_request = request.override(system_message=new_system_message)
        return handler(modified_request)

from pydantic import BaseModel, Field
class SQLOutput(BaseModel):
    sql: str = Field(description="runnable SQL query")

def create_sql_agent(skills_dir,inf_url,nvidia_api_key,debug=False):
    model_id = "deepseek-ai/deepseek-v3.2"
    nvidia_model = init_chat_model(model=model_id,base_url=inf_url,api_key=nvidia_api_key,model_provider="nvidia")
    # Create the agent with skill support
    agent = create_agent(
        nvidia_model,
        system_prompt=(
            "You are a SQL query assistant that generates runnable SQL query for a music database."
        ),
        middleware=[SkillMiddleware(skills_dir)],
        # checkpointer=InMemorySaver(),
        response_format=SQLOutput,
        debug=debug
    )
    return agent
