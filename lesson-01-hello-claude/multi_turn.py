from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# The conversation history - empty at start
conversation = []

# ---------- TURN 1 ----------
conversation.append({
    "role": "user",
    "content": "Hi Claude. Please pick a random number between 1 and 100, and just tell me the number."
})

response_1 = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=conversation
)
claude_reply_1 = response_1.content[0].text
# conversation.append({"role": "assistant", "content": claude_reply_1})

print("=" * 60)
print("TURN 1")
print("=" * 60)
print("USER:", conversation[0]["content"])
print("\nCLAUDE:", claude_reply_1)

# ---------- TURN 2 (testing memory) ----------
conversation.append({
    "role": "user",
    "content": "Quick - was the number you picked odd or even?"
})

response_2 = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=conversation
)
claude_reply_2 = response_2.content[0].text
conversation.append({"role": "assistant", "content": claude_reply_2})

print("\n" + "=" * 60)
print("TURN 2 (testing memory)")
print("=" * 60)
print("USER:", conversation[2]["content"])
print("\nCLAUDE:", claude_reply_2)

# ---------- TURN 3 (building on accumulated context) ----------
conversation.append({
    "role": "user",
    "content": "Suggest one specific AI concept we should master together this month."
})

response_3 = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=conversation
)
claude_reply_3 = response_3.content[0].text
conversation.append({"role": "assistant", "content": claude_reply_3})

print("\n" + "=" * 60)
print("TURN 3 (using accumulated context)")
print("=" * 60)
print("USER:", conversation[4]["content"])
print("\nCLAUDE:", claude_reply_3)

# ---------- THE PROOF: WITHOUT MEMORY ----------
print("\n" + "=" * 60)
print("PROOF: WHAT HAPPENS WITHOUT HISTORY")
print("=" * 60)

# Same question as Turn 2, but only sending THIS message - no history
response_amnesia = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Quick check - who did I say I'm learning with?"}
    ]
)
print("USER (no history sent):", "Quick check - who did I say I'm learning with?")
print("\nCLAUDE:", response_amnesia.content[0].text)

print(f"\n\nFinal conversation history has {len(conversation)} messages.")
