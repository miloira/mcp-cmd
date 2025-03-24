import functools
import sys


def load_tools(tools, mcp):
    for module in tools:
        module.attach_to_mcp(mcp)


def register_mcp_tools(fs, tool_group_name=""):
    def _register_tool(fs, mcp):
        if tool_group_name:
            tool_name_prefix = tool_group_name + "-"
        else:
            tool_name_prefix = tool_group_name

        for f in fs:
            if f.__doc__ is not None:
                mcp.add_tool(f, name=f"{tool_name_prefix}{f.__doc__}")
            else:
                mcp.add_tool(f, name=f"{tool_name_prefix}{f.__name__}")

    caller_frame = sys._getframe(1)
    caller_module = caller_frame.f_globals
    caller_module["attach_to_mcp"] = functools.partial(_register_tool, fs)
