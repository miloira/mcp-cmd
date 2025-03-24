from mcp.server.fastmcp import FastMCP

from tools.utils import load_tools
from tools import filesystem_

mcp = FastMCP("mcp-cmd", host="127.0.0.1", port=8000, log_level="DEBUG")

load_tools(
    tools=[
        filesystem_
    ],
    mcp=mcp
)

if __name__ == "__main__":
    mcp.run("sse")
