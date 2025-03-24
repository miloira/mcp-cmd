import asyncio

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.sse import sse_client
from mcp import ClientSession
from langgraph.prebuilt import create_react_agent


def get_role(message):
    if isinstance(message, AIMessage):
        return "AI："
    else:
        return ""


async def run_agent():
    async with sse_client(url="http://127.0.0.1:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print(tools)

            model = ChatOpenAI(
                model="qwen-max-0125",
                api_key="sk-281ea643722a4e1786ffdd270e293f76",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )

            agent = create_react_agent(model, tools)
            messages = []
            while True:
                user_input = input("(USER) ")
                messages.append({
                    "role": "user",
                    "content": user_input + "\n请列出执行步骤，然后调用合适的工具完成任务。与任务无关的内容不要输出，避免不必要的调用工具。"
                })
                role = None

                async for event in agent.astream_events({"messages": messages}):
                    if event["event"] == "on_chat_model_stream":
                        if role is None and event["data"]["chunk"].content:
                            role = get_role(event["data"]["chunk"])
                            print(role, end="", flush=True)

                        print(event["data"]["chunk"].content, end="", flush=True)
                    elif event["event"] == "on_chat_model_end":
                        role = None
                        print()

                    if event["event"] == "on_tool_start":
                        print(f'[TOOLS] {event["data"]["input"]} => {event["name"]}')
                    elif event["event"] == "on_tool_end":
                        print(f'[TOOLS] {event["data"]["output"].content}')

                    await asyncio.sleep(0)

                messages.extend(event["data"]["output"]["messages"])
                print()


# 运行
if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print(result)
