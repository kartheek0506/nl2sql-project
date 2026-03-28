import os
from dotenv import load_dotenv

from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.google import GeminiLlmService

load_dotenv()


class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(id="default", email="default@example.com", group_memberships=["user"])


def create_agent():
    llm = GeminiLlmService(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.5-flash"
    )

    sql_tool = RunSqlTool(
        sql_runner=SqliteRunner(database_path="clinic.db")
    )

    tools = ToolRegistry()
    tools.register_local_tool(sql_tool, access_groups=["user"])
    tools.register_local_tool(VisualizeDataTool(), access_groups=["user"])
    tools.register_local_tool(SaveQuestionToolArgsTool(), access_groups=["user"])
    tools.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=["user"])

    memory = DemoAgentMemory()

    agent = Agent(
        llm_service=llm,
        tool_registry=tools,
        user_resolver=SimpleUserResolver(),
        agent_memory=memory,
        config=AgentConfig()
    )

    return agent