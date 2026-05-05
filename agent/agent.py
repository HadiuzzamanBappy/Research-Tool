import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from agent.tools import web_search_tool, scrape_website
from agent.prompt import build_prompt


def create_agent(user_input: str, profile: str = "auto"):
    # Load .env if present so keys work without shell exports.
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / ".env")

    api_key = os.getenv("ZAI_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing Z.ai API key. Set ZAI_API_KEY "
            "in your shell, .env, or environment variable"
        )

    # Set the environment variable so ChatOpenAI picks it up automatically
    os.environ["OPENAI_API_KEY"] = api_key

    llm = ChatOpenAI(
        model="glm-4.6",
        temperature=0,
        base_url="https://api.z.ai/api/coding/paas/v4",
        streaming=True,
    )

    system_message = SystemMessage(content=build_prompt(user_input, profile))

    agent = create_react_agent(
        llm,
        tools=[web_search_tool, scrape_website],
        prompt=system_message,
    )

    return agent
