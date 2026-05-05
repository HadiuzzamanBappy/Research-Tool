import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from agent.tools import web_search_tool, scrape_website
from agent.prompt import system_instruction

def create_agent():
    # Load .env if present so keys work without shell exports.
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / ".env")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY "
            "in your shell, .env, or .env.local"
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=api_key
    )

    system_message = SystemMessage(content=system_instruction)

    agent = create_react_agent(
        llm,
        tools=[web_search_tool, scrape_website],
        prompt=system_message
    )

    return agent