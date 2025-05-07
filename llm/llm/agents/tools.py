from typing import Any, List, Dict
from pydantic import create_model, Field
from langchain.tools import StructuredTool
import json

def _py_type(jtype: str) -> type:
    return {
        "string":  str,
        "integer": int,
        "number":  float,
        "boolean": bool,
        "array":   List[Any],
    }.get(jtype, Any)


def make_structured_tool(mcp_tool, mcp_server):
    """
    Build a LangChain StructuredTool from a Fast-MCP tool.
    """
    # Extract schema from inputSchema
    input_schema = mcp_tool.inputSchema
    props = input_schema.get("properties", {})
    
    fields = {
        name: (_py_type(defn.get("type", "string")), Field(default=defn.get("default", ...), description=defn.get("description", "")))
        for name, defn in props.items()
    }

    ArgsSchema = create_model(f"{mcp_tool.name}Args", **fields)

    async def run(**kwargs):
        try:
            print(f"[DEBUG] 🛠️ Tool '{mcp_tool.name}' input: {kwargs}")
            result = await mcp_server.call_tool(mcp_tool.name, kwargs)
            if result.content:
                content = result.content[0].text
                try:
                    return json.loads(content)
                except Exception:
                    return content
            return ""
        except Exception as e:
            print(f"[ERROR] Tool '{mcp_tool.name}' failed: {str(e)}")
            return f"Error executing tool {mcp_tool.name}: {str(e)}"

    return StructuredTool.from_function(
        name=mcp_tool.name,
        description=mcp_tool.description or f"Tool named {mcp_tool.name}",
        args_schema=ArgsSchema,
        coroutine=run
    )
