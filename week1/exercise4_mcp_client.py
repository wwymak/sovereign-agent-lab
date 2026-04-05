"""
Exercise 4 — LangGraph Agent Consuming the MCP Venue Server
=============================================================

WHAT THIS EXERCISE IS ABOUT
-----------------------------
In Exercise 2 the venue tools were hardcoded into research_agent.py.
Here you connect the same agent to the MCP server in
sovereign_agent/tools/mcp_venue_server.py instead.

The agent code barely changes. What changes is where the tools come from.

After this exercise you'll be able to answer:
  - What does MCP actually buy you compared to hardcoded tools?
  - Which file do you change when the venue data changes?
  - Why does it matter that both a LangGraph agent AND a Rasa action
    can connect to the same server?

THE REQUIRED EXPERIMENT
------------------------
You must modify mcp_venue_server.py (change one venue's status),
re-run this file, and report what changed in ex4_answers.py.
This is the most important part of the exercise — it demonstrates
the value of the tool layer in practice, not just in theory.

HOW TO RUN
-----------
    python week1/exercise4_mcp_client.py

The MCP server starts automatically — no separate terminal needed.
Results saved to week1/outputs/ex4_results.json (~30 seconds).
Then fill in week1/answers/ex4_answers.py.
"""

import asyncio
import json
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware.model_call_limit import ModelCallLimitMiddleware
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel, create_model

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

# Path to the shared MCP server in sovereign_agent/
SERVER_SCRIPT = str(
    Path(__file__).parent.parent / "sovereign_agent" / "tools" / "mcp_venue_server.py"
)
OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


# ─── MCP → LangChain bridge ───────────────────────────────────────────────────
#
# _make_mcp_caller returns a sync callable that, when invoked, starts a fresh
# MCP session, calls the tool, and returns the result string.
#
# Why a factory function and not a lambda?
# Each closure must capture its own tool_name. If we used a lambda in a loop,
# every closure would share the last value of tool_name — a classic Python gotcha.


def _make_mcp_caller(tool_name: str, server_script: str) -> Callable[..., str]:
    def call(**kwargs) -> str:
        async def _inner() -> str:
            params = StdioServerParameters(command=sys.executable, args=[server_script])
            async with stdio_client(params) as (r, w):
                async with ClientSession(r, w) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, kwargs)
                    return result.content[0].text if result.content else "{}"

        return asyncio.run(_inner())

    call.__name__ = tool_name
    return call


JSON_TYPE_MAP = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
}


def _schema_to_pydantic(name: str, schema: dict[str, Any]) -> type[BaseModel]:
    """Convert an MCP JSON Schema to a Pydantic model for use as args_schema."""
    fields: dict[str, Any] = {}
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    for field_name, field_info in props.items():
        py_type = JSON_TYPE_MAP.get(field_info.get("type", "string"), str)
        if field_name in required:
            fields[field_name] = (py_type, ...)
        else:
            fields[field_name] = (py_type, None)
    return create_model(name, **fields)


async def discover_tools(server_script: str) -> list:
    """
    Connect once, list all tools, and wrap each as a LangChain StructuredTool.

    Dynamic discovery is the key property: add a new @mcp.tool() to
    mcp_venue_server.py and this function picks it up automatically.
    No changes needed here.
    """
    params = StdioServerParameters(command=sys.executable, args=[server_script])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            raw = await session.list_tools()
            tools = []
            for t in raw.tools:
                args_model = _schema_to_pydantic(f"{t.name}Args", t.inputSchema)
                lc_tool = StructuredTool.from_function(
                    func=_make_mcp_caller(t.name, server_script),
                    name=t.name,
                    description=t.description or f"MCP tool: {t.name}",
                    args_schema=args_model,
                )
                tools.append(lc_tool)
            return tools, [t.name for t in raw.tools]


# ─── Agent queries ────────────────────────────────────────────────────────────


def extract_trace(result: dict) -> list:
    full_trace = []

    for m in result["messages"]:
        role = getattr(m, "type", "unknown")
        content = m.content

        if m.type == "ai":
            for tool_call in m.tool_calls:
                full_trace.append(
                    {
                        "role": "tool_call",
                        "tool": tool_call["name"],
                        "args": tool_call.get("args", {}),
                    }
                )

        if content:
            full_trace.append({"role": role, "content": str(content)})

    return full_trace


def print_trace(trace: list) -> None:
    for entry in trace:
        if entry["role"] == "tool_call":
            args_str = json.dumps(entry.get("args", {}))[:80]
            print(f"  [TOOL_CALL] → {entry['tool']}({args_str})")
        elif entry.get("content"):
            content = entry["content"]
            # if len(content) > 400:
            #     content = content[:400] + "..."
            print(f"  [{entry['role'].upper()}]\n  {content}\n")


async def main() -> None:
    llm = ChatOpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=os.getenv("NEBIUS_KEY"),
        model="Qwen/Qwen3-32B",
        # model="meta-llama/Llama-3.3-70B-Instruct",
        temperature=0,
    )

    print("\nExercise 4 — LangGraph + MCP")
    print("Discovering tools from mcp_venue_server.py...")

    tools, tool_names = await discover_tools(SERVER_SCRIPT)
    print(f"\n  Discovered {len(tools)} tools: {tool_names}")

    agent = create_agent(
        llm,
        tools,
        system_prompt=(
            "You are a venue-finding assistant. Use the provided tools to search for venues. "
            "Do NOT call the same tool with the same arguments more than once. "
            "If no venues match the user's constraints, say so clearly and stop. "
            "Do not keep retrying — report what you found (or didn't find) and finish."
        ),
        middleware=[ModelCallLimitMiddleware(run_limit=8, exit_behavior="end")],
    )
    output = {
        "server_script": SERVER_SCRIPT,
        "tools_discovered": tool_names,
        "queries": {},
    }

    # ── Query 1: search + detail fetch ────────────────────────────────────────
    q1 = "Find Edinburgh venues for 160 guests with vegan options and give me the full address of the best match."
    print(f"\n{'=' * 65}")
    print("  Query 1 — Search + Detail Fetch")
    print(f"{'=' * 65}\n")
    r1 = agent.invoke({"messages": [("user", q1)]})
    trace1 = extract_trace(r1)
    print_trace(trace1)
    output["queries"]["query_1"] = {"query": q1, "trace": trace1}

    # ── Query 2: impossible constraint ────────────────────────────────────────
    q2 = "Find a venue for 300 people with vegan options."
    print(f"\n{'=' * 65}")
    print("  Query 2 — Impossible Constraint")
    print(f"{'=' * 65}\n")
    r2 = agent.invoke({"messages": [("user", q2)]})
    trace2 = extract_trace(r2)
    print_trace(trace2)
    output["queries"]["query_2"] = {"query": q2, "trace": trace2}

    # ── Required experiment reminder ──────────────────────────────────────────
    print("\n" + "─" * 65)
    print("REQUIRED EXPERIMENT (before filling in ex4_answers.py):")
    print()
    print("  1. Open sovereign_agent/tools/mcp_venue_server.py")
    print("  2. Change The Albanach's status from 'available' to 'full'")
    print("  3. Save and run this script again")
    print("  4. Compare the output to what you just saw")
    print("  5. Revert the change")
    print()
    print(
        "  Record what changed (and what didn't) in ex4_answers.py → EX4_EXPERIMENT_RESULT"
    )

    out_path = OUTPUTS_DIR / "ex4_results.json"
    out_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\n✅  Results saved to {out_path}")
    print(
        "    Complete the experiment above, then fill in week1/answers/ex4_answers.py"
    )


if __name__ == "__main__":
    asyncio.run(main())
