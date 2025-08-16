# bot.py
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()

def get_response_from_bot(llm_id: str, query: str, allow_search: bool, system_prompt: str, provider: str):
    try:
        TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

        if not TAVILY_API_KEY and allow_search:
            return {"error": "Missing TAVILY_API_KEY for search.", "is_error": True}
        if not TOGETHER_API_KEY and provider.lower() == "together":
            return {"error": "Missing TOGETHER_API_KEY for Together provider.", "is_error": True}

        if provider.lower() == "together":
            llm = ChatOpenAI(
                model=llm_id,
                api_key=TOGETHER_API_KEY,
                base_url="https://api.together.xyz/v1"
            )
        else:
            return {"error": f"Unsupported provider: {provider}. Only 'together' is supported.", "is_error": True}

        # No Tavily search for now, as it's commented out in original
        tools = []
        agent = create_react_agent(model=llm, tools=tools)

        state = {
            "messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=query)
            ]
        }

        response = agent.invoke(state)
        return {"response": response["messages"][-1].content, "is_error": False}
    except Exception as e:
        return {"error": f"Failed to process request: {str(e)}", "is_error": True}

if __name__ == "__main__":
    print("--- Using Together AI ---")
    try:
        together_ai_model = "lgai/exaone-3-5-32b-instruct"
        together_response = get_response_from_bot(
            llm_id=together_ai_model,
            query="What is the capital of France?",
            allow_search=False,
            system_prompt="You are a helpful assistant.",
            provider="together"
        )
        if together_response.get("is_error"):
            print(f"Error: {together_response['error']}")
        else:
            print(f"Together AI Response: {together_response['response']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")