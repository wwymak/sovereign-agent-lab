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
TASK_A_OUTDOOR_OK = False

TASK_A_NOTES = (
    "Using Llama 70B for this task DID NOT work, it outputs the tool use as"
    " a 'function' field , whereas eg qwen produces the standard output"
)  # optional — anything unexpected

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True  # True or False

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-30da49ca-6aee-42fe-a017-aa7d06f69c3c_00001_.webp"

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
Okay, let's see. The user wanted to check The Bow Bar for 160 vegan guests. The response from the tool says that The Bow Bar has a capacity of 80, which is less than the required 160. So it doesn't meet the capacity constraint. The vegan option is available, but since the capacity is insufficient, the overall status is "full" and meets_all_constraints is false.

Now, the user's instruction was to check The Bow Bar first, and if it doesn't meet the requirements, check any other available venue. So I need to move on to the next venues. The known venues are The Albanach, The Haymarket Vaults, The Guilford Arms, and The Bow Bar. Since The Bow Bar is already checked, the next ones to check would be the others in the list.

I should start with The Albanach. Let me call the check_pub_availability function again with the same parameters: required_capacity 160 and requires_vegan true. If The Albanach meets the capacity and vegan requirements, then that's the venue. If not, proceed to The Haymarket Vaults, then The Guilford Arms. If none of them meet the requirements, then inform the user that no suitable venue is available.

Wait, but the user said "any other available venue" if The Bow Bar doesn't work. So I need to check each of the other venues one by one. Let's start with The Albanach. If that's not possible, then The Haymarket Vaults, then The Guilford Arms. Each time, using the same function call with the same capacity and vegan requirement.

So the next step is to check The Albanach. Let's make the tool call for that.
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
Okay, let's see. The user is looking for a venue in Edinburgh that can accommodate 300 people with vegan options. They provided a list of four pubs: The Albanach, The Haymarket Vaults, The Guilford Arms, and The Bow Bar. I checked each one using the check_pub_availability function.

First, The Albanach had a capacity of 180 and vegan options, but that's under 300. Then The Haymarket Vaults with 160, also vegan but too small. The Guilford Arms had 200 capacity but no vegan options. Finally, The Bow Bar has 80 capacity and vegan, but it's full. None of them meet both the capacity and vegan requirements. So I need to inform the user that none of the available pubs can handle their request. Maybe suggest looking for larger venues or other options outside the known list.
</think>

None of the known Edinburgh venues can accommodate 300 guests with vegan options. The largest available space (The Guilford Arms) only holds 200 people but lacks vegan options, while venues with vegan options (The Albanach, Haymarket Vaults, Bow Bar) have capacities of 180, 160, and 80 respectively. You'll need to consider alternative venues outside this list or adjust your requirements.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False  # True or False

SCENARIO_3_RESPONSE = """
I don't have access to real-time train schedules or transportation data. For the most accurate information about the last train from Edinburgh Waverley to London, I recommend checking:
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
PASTE MERMAID OUTPUT HERE
"""

# Compare the LangGraph graph to exercise3_rasa/data/rules.yml. Min 30 words.
TASK_D_COMPARISON = """
FILL ME IN
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
FILL ME IN
"""
