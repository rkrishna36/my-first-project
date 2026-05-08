from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# Optional: a system prompt to give the chatbot a personality
SYSTEM_PROMPT = "You are a helpful, friendly AI assistant. Keep responses concise unless asked for detail."

# Conversation history - just like Lesson 2, but it'll grow indefinitely
conversation = []

print("=" * 50)
print("Chat with Claude (type 'quit' to exit)")
print("=" * 50)

while True:
    # Get input from the user (the keyboard)
    user_input = input("\nYou: ").strip()

    # Skip if they just hit Enter
    if not user_input:
        continue

    # Exit if they type quit/exit/bye
    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("\nGoodbye!")
        break

    # Add the user's message to the conversation history
    conversation.append({
        "role": "user",
        "content": user_input
    })

    # Send the full conversation to Claude
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversation
    )

    # Get Claude's reply
    claude_reply = response.content[0].text

    # Save Claude's reply to history (so next turn has context)
    conversation.append({
        "role": "assistant",
        "content": claude_reply
    })

    # Display it
    print(f"\nClaude: {claude_reply}")

print(f"\nConversation ended. {len(conversation)} messages exchanged.")
