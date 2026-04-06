"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160
And how many of those guests will need vegan meals?
Your input ->  50
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"  # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  500
I need to check one thing with the organiser before I can confirm.
The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline.
Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"  # "confirmed" or "escalated"
CONVERSATION_2_REASON = "insufficient time to process the confirmation before the 5 PM deadline. "  # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
And how many of those guests will need vegan meals?
Your input ->  before I answer that, do you have av equipment available for hire
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
Would you like to resume confirm booking and handle out of scope?
Your input ->  who can I ask about the av equipment
I'm sorry, I'm not trained to help with that.
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
Would you like to resume confirm booking and handle out of scope?
Your input ->  yes
And how many of those guests will need vegan meals?
Your input ->  90
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  I am confirming the booking
Ok, I am updating guest_count, vegan_count to 160, 90 respectively.
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  250
I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 —
insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
It explains that it is unable to help with the out of scope request and ask me to contact event organiser.
This follows the exact response we specified in domain.yml
Then it asks if I want to resume the confirmation
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
In Rasa, it can only state that it is unable to help the user with the request using our
supplied script, and will keep repeating the same script we supplied until the user reverts to one
of the allowed actions. In LangGraph, the agent also told the user that it is unable to
help with the request, however, it is able to suggest alternatives that the user can try themselves
based on the internal knowledge from the llm
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = None  # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = []

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
FILL ME IN
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
FILL ME IN

Think about:
- What does the LLM handle now that Python handled before?
- What does Python STILL handle, and why (hint: business rules)?
- Is there anything you trusted more in the old approach?
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The specifics of Rasa CALM  is that it buys you certainty. The rules you define
must be followed, the fields you want extracted are extracted from
 natural conversation but nothing else,
 and you don't need to worry about random llm choices leading
to potentially expensive errors.

Rasa CALM agent has to follow the rules laid down by the configs yml precisely. For
example, it cannot halluncinate any tools, or to use any default tools the come with
the llm (eg llama3.3 has internal browser tool and wolfram alpha. It cannot enage in
'random conversation' with users -- it's response is very scripted. For this confirmation
use case, it is acceptable -- the business use case is very clear and simple--
it needs to make sure the total number of
people, the number of vegans and the deposit are captured, nothing else. It does not need
to handle open ended requests like e.g. 'find me a pub with scottish vibes and within 10 mins walk
from the train station'

However, I would suggest the current implementation will work better as a 'backend'
in some sort of A2A setup so a human never have to deal with this sort of robotic
responses...

If we look at the 'out of scope' message trace above-- the agent asks 'is there anything
else I can help you with' with it very much can't help with most things, not
even provide info on relevant contact details.
'Would you like to continue with handle out of scope?' which is also very odd phrasing
(almost like some 'backend' logic is leaking out)
If it's for a human user it can get frustrating to use (or rather, why can't I just go
fill a form that takes 10s rather than interact with a bot?)
"""
