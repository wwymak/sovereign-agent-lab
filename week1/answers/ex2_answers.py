"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

TASK_A_NOTES = (
    "Using Llama 70B for this task DID NOT work, the langgraph lib wasn't able to parse the output format correctly."
    "If we inspect the raw output, the model did attempt tool calls via 'function' fields , but it wasn't in a"
    "format that was parsed correctly by the token factory inference engine "
    "swapping to Qwen32B works and gives correct outputs."
    "It is also interesting to inspect the thinking traces of the model, and how well it automatically uses the "
    "available tools without having to specify this in the prompt."
    "In terms of the flyer generated in task a, with the model specify the prompt:"
    "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-4ce8728b-942d-4e1d-95ca-20cf2b78166a_00001_.webp"
    "it is actually much better than the flyer I tried to generate with the manual prompt below(!)"
)  # optional — anything unexpected

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True  # True or False

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-bbfee49f-514d-4e1b-9430-b2a725ea9250_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = (
    "Professional event flyer for Edinburgh AI Meetup, tech "
    "professionals, modern venue at The Haymarket Vaults, Edinburgh. "
    "160 guests. Warm lighting, Scottish architecture background, "
    "clean modern typography."
)

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
<think>
Okay, so the user wanted to check The Bow Bar for 160 vegan guests. The response from the tool says that The Bow Bar has a capacity of 80, which is less than the required 160. That means it doesn't meet the capacity requirement. The vegan option is available, but since the capacity isn't enough, the overall status is "full" and meets_all_constraints is false.

Now, the user's instruction was to check The Bow Bar first, and if it doesn't work, check any other available venue. So I need to move on to the next venue. The known venues are The Albanach, The Haymarket Vaults, The Guilford Arms, and The Bow Bar. Since The Bow Bar is already checked, the next options are the other three.

I should check each one in order. Let's start with The Albanach. I'll use the same function again with the same parameters: required_capacity 160 and requires_vegan true. If The Albanach meets the requirements, then we're done. If not, proceed to The Haymarket Vaults, then The Guilford Arms.

Wait, the tool response for The Bow Bar mentioned "status": "full". Does that mean it's at capacity but vegan is available? But the capacity is 80, which is less than 160, so even if vegan is available, the capacity isn't met. So the next step is definitely to check another venue.

So the next tool call should be check_pub_availability for The Albanach. Let's see if that works. If not, then The Haymarket Vaults, and so on. The user wants the first available venue that meets both capacity and dietary needs. So I need to iterate through each venue until one returns meets_all_constraints as true.
</think>



  [TOOL]
  {"success": true, "pub_name": "The Albanach", "address": "2 Hunter Square, Edinburgh", "capacity": 180, "vegan": true, "status": "available", "meets_all_constraints": true}
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False  # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
<think>
Okay, let's see. The user is looking for a venue in Edinburgh that can accommodate 300 people with vegan options.
I've checked all four known pubs: The Albanach, The Haymarket Vaults, The Guilford Arms, and The Bow Bar.

The first two, Albanach and Haymarket Vaults, have vegan options but their capacities are 180 and 160 respectively,
 which are below 300. The Guilford Arms has a capacity of 200 but doesn't offer vegan options.
 The Bow Bar has vegan options but only a capacity of 80 and is already full.

None of the venues meet both the capacity and vegan requirements. The user might need to consider alternative solutions
 like booking multiple venues, looking for other pubs outside the known list, or adjusting the event size.
 Since the tools provided don't include a function to search beyond the known venues,
 I should inform the user that the current options don't work and suggest possible next steps.
</think>

None of the known Edinburgh venues can accommodate 300 guests with vegan options.
The closest options have either insufficient capacity or lack vegan provisions. Would you like me to:
1. Suggest alternative venues outside our known list?
2. Calculate costs for combining multiple venues?
3. Adjust the guest count or dietary requirements?
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False  # True or False

SCENARIO_3_RESPONSE = """
I don't have access to real-time train schedules or transportation data.
For the most accurate information about the last train from Edinburgh Waverley to London, I recommend checking:
1. The National Rail website (https://www.nationalrail.co.uk)
2. Train service apps like Citymapper or Trainline
3. The specific train operator's website (e.g., LNER)

Would you like help with anything related to Edinburgh pubs, weather, or event planning instead?
"""

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Yes, this behaviour is acceptable. The agent is working within it's scope -- it only have
tools relevant for event planning (pub availability, weather, flyer generation, calculate costs).
When a user asks for live train times that's out of it's tools functionality, it didn't make stuff up, instead
telling them that it's not possible but that they should look this up.

One point that is potentially concerning is the websites the agent
suggested the user look up for real time information -- these are correct, but it's based
on the agent's internal knowledge, and might get out of date.

For a real assistant I would further work on system propmt/guardrails to prevent even this
(e.g. prefer a response that is along the lines of telling user to look up info on their
favourite travel app)
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	model(model)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> model;
	model -.-> __end__;
	model -.-> tools;
	tools -.-> model;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/rules.yml. Min 30 words.
TASK_D_COMPARISON = """
FILL ME IN
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
Make assumptions about the quiet corner for webniar requirement in task 1. I was expecting the agent to
miss/ignore it due to the limitations of the tools. However, it was acknowledged partway through when looking through
thinking trace (occurs after the price calculation tool use):

Wait, the user also mentioned a quiet corner for a 30-minute webinar. The initial check_pub_availability might not have
considered that. But the function's parameters don't include that, so maybe it's assumed that the pub's availability
includes space for such activities.
Or maybe the user just wants to note that as part of the requirements, but the tool doesn't handle it.
So we can proceed with the given functions.

what is not so ideal is that the agent didn't feed this back to the user -- in a real production scenario the quiet
corner is likely an important constraint
"""
