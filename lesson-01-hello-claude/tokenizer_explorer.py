# A hands-on look at how text becomes "tokens" - the units LLMs actually see.
# Note: tiktoken is OpenAI's tokenizer. Claude uses a similar but proprietary one.
# Concepts are identical; exact splits can differ slightly.

import tiktoken

# cl100k_base is the encoding used by GPT-4; conceptually similar to Claude's
encoding = tiktoken.get_encoding("cl100k_base")

def explore(text):
    """Show how a piece of text gets broken into tokens."""
    token_ids = encoding.encode(text)
    tokens = [encoding.decode([tid]) for tid in token_ids]
    print(f"\nText:   {repr(text)}")
    print(f"Tokens: {tokens}")
    print(f"Count:  {len(tokens)}")

# ============================================================
# PART 1: What do tokens actually look like?
# ============================================================
print("=" * 70)
print("PART 1: HOW TEXT BECOMES TOKENS")
print("=" * 70)

# Common words = usually 1 token
explore("the")
explore("Hello")
explore("AI")

# Less common or compound words break apart
explore("strawberry")
explore("antidisestablishmentarianism")

# Spaces and punctuation matter
explore("Hello world")
explore("Hello, world!")

# Code looks very different from prose
explore("print('hello')")

# Other languages often use more tokens per word
explore("こんにちは")  # Japanese for "hello"

# Full sentence
explore("I am learning AI engineering with my husband.")

# ============================================================
# PART 2: How conversations grow in tokens
# ============================================================
print("\n" + "=" * 70)
print("PART 2: WHY CONVERSATIONS GROW EXPENSIVE")
print("=" * 70)
print("(This connects to your multi-turn lesson - watch the count grow)\n")

conversation_log = ""
turns = [
    ("user", "Hi Claude, what should I learn first about AI?"),
    ("assistant", "Great question! For someone starting out, I'd suggest learning how to call an LLM API. It's the foundation everything else builds on - chatbots, agents, RAG systems."),
    ("user", "What's an agent specifically?"),
    ("assistant", "An agent is an AI system that can take actions on your behalf - calling tools, looking things up, sending emails. Basically a chatbot that can DO things, not just chat."),
    ("user", "Can you give me a tiny example?"),
    ("assistant", "Sure! Imagine you say 'what's the weather in Phoenix' to an agent. Instead of just guessing, it calls a real weather API, gets actual data, then phrases the answer for you."),
]

for i, (role, content) in enumerate(turns, 1):
    full_msg = f"{role}: {content}"
    conversation_log += full_msg + "\n"
    total_tokens = len(encoding.encode(conversation_log))
    print(f"After turn {i} ({role:9}): {total_tokens:4} tokens in the full history")

print("\nKey insight:")
print("Every API call sends the FULL conversation history.")
print("Turn 6 costs ~6x as many tokens to send as Turn 1.")
print("That's why long conversations get expensive,")
print("and why context windows have limits.")
