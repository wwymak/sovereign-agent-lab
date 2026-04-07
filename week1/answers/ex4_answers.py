"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER = (
    "There are currently no Edinburgh venues available that can accommodate 300 guests with"
    " vegan options. Would you like to try adjusting the capacity requirements or "
    "dietary constraints?"
)

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True  # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
The final answer from the model remained unchanged between the 2 scenarios
(both times Haymarket valuts was picked). But how the model arrived at this decision
is different -- in the 2nd scenario when Albanach is unavailable, it's a straighforward
decision as there is only 1 choice. In the first scenario where there are two options, the model
went back and forth in its thinking traces trying to come up with which one is 'better'.
In terms of the files that needs updating -- the mcp_venue_server.py only needs the change to
setting the staus of the Albanach in the VENUE dict to 'full'. However, I needed to fix a
few things in exercise4_mcp_client.py:
- when the mcp wasn't running correctly, the graph got stuck in a loop trying to call the mcp.
I needed to add a maximum number of times the llm can attempt the mcp tool call.
- I needed to update the system prompt to the model to ensure that it doesn't reattempt the
same thing over and over again (if no venue matches then there's no point in retrying)
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 0  # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 0  # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
Both ex2 and ex4 has 0(!) lines of tool code -- in ex2 it's imported from venue_tools and in ex4 it's discovered from
in the mcp. If we consider the 'async def discover_tools(server_script: str)' function, it's ~24 lines
In terms of 'real' tool implementation lines : ~189 in venue_tools.py , ~40 in mcp_venue_server.py.

What the mcp buys you is that the agent can dynamically discover available tools at runtime rather than having them
harcoded. It gives the separation of concerns -- say, the venue info is available through an external api, and is also
available as an mcp from the external source. If you are using mcp server, you as the agent builder does not need
to know the full details of how the api works -- you can let the agent handle the relevant tool calls. The external
provider handles any need changes to the tools if the api or data change.

If you are using the hard coded tools -- every api update you will need to modify your agent code, and you will
also need to write your own tools for every external source of information/functionality your agent needs. Even if
these apis / functionality are all internal to your company, it means if you build more than 1 agent that
uses these tools, they will need to repeat the same tool definition code
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- mcp server with tools
- LLM(s)
- memory
- FILL ME IN
- FILL ME IN
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
I will use the langgraph agent for research and the Rasa CALM agent for the call.
It is not possible to use the Rasa CALM for research -- research is an open ended task
and it is very difficult to anticipate all the possible paths a user might go down.
We can see how when CALM ends up in an 'unanticated' path it keeps repeating the same sentence
until it can go to another defined path, this is likely to frustrate the user and
also doesn't do it's purpose as a research agent. The Langgraph agent, with it's more
modular tools and more flexible llm can help guide the user to a valid choice eg
in ex2 when user wants to find somewhere for 300 people and none of the venus fit the
agent was able to suggest alternatives e.g. 'Calculate costs for combining multiple venues?'

On the other hand, the call needs to be very definitive -- only 3 values must be entered. Probably
to some booking system which we don't want to get wrong values in. If we use the flexible
Langgraph agent we have higher chance that some wrong/halluncinated value will creep in. Also,
since this is a straightforward task, by using CALM we can offload some of the work from the
bigger llm and save some costs.
"""
