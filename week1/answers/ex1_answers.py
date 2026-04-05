"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER = "The Haymarket Vaults"
PART_A_XML_ANSWER = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT = True  # True or False
PART_A_XML_CORRECT = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
In the 'plain' answer, the list of venues are listed before the question. The model only got the requirements of
what it needs to do at the end -- this means it has to look back at it's context window. 'The Haymarket Vaults'
occurs in the list after 'The Albanach', so the model picks this due to recency bias. In addition, the prompt asks
for 'at least 160', and the Haymarket Vaults has capacity of 160, so the model does exact matching on this.

In the XML and sandwich scenarios, the question is at the beginning, with the list of venues enclosed by xml tags.
(the sandwich is the same as xml, just that the question is repeated).The model knows what to look for before it sees
the list of venues. Therefore, it returns the 1st venue that meets the requirements, which is the Albanach. enclosing
in xml tags also ties into the model training of the llm -- since they are trained with a lot of code/ structured
data, by converting the task into this structured form activates the model's "data processing" behaviors
learned during fine-tuning on code and structured data. Instead of the simple exact token match (160 == 160), it
correctly does the math (180 >= 160)

The sandwich setup gives the same result as the xml (same data processing behaviours etc.) The extra reminder
at the end is a general good practice. LLMs tend to put most attention to the end and beginning. By repeating the
question at the bottom, it helps to enforce the requirements of what the model needs to do before it generates
the answer

"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER = "The Haymarket Vaults"
PART_B_XML_ANSWER = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT = True
PART_B_XML_CORRECT = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The 'The Holyrood Arms: capacity=160, vegan=yes, status=full' is most likely to cause a wrong answer, especially in
the plain text prompt setup. The xml and sandwich techniques mean that the model is more likely to pick the Albanach
anyway as it is the first item in the lookup list that matches the requirements and are not near the distractors.

However, in the plain text prompt case, when the model looks back at the list, there are 2 exact keyword matches
'160' and 'vegan=yes', so it might end up picking that and ignore the 'status=full' since the question is
'is available' and the words don't match -- so a model with stronger capabilities will be able to parse the status=full
equate to is_availabe=false, but a much smaller model might not.

In this case, llama 70B is good enough that it is not distracted by the distractors
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True  # True or False

PART_C_PLAIN_ANSWER = "The Haymarket Vaults"
PART_C_XML_ANSWER = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C was meant to show the effects of the distractors, however, the small model is actually capable enough
to handle them. The difference is in the xml and sandwich answers. For the bigger model, it works more like retrieval,
returning the first answer that fits the requirements (the Albanach). For the small model, it wasn't able to switch to
'retrieval mode' in the prompts with xml tags and still works like in the plain case.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the signal-to-noise ratio is low (e.g., long contexts, near-miss distractors)
AND you are using a sufficiently capable model that can use structural cues to trigger logical/reasoning processing.

Counter to intuition, structural cues such as tags are more useful for larger models, which 'shifts' into a more
analytical mode and is more rigorous in the extraction task. Smaller Models needs behavioral (eg chain of thought, very
precise todo list ) and positional formatting (eg putting the question at the end so they don't
forget the constraint.)
"""
