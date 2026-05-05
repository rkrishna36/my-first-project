from dotenv import load_dotenv
from anthropic import Anthropic

# Step 1: Load the API key from the .env file
load_dotenv()

# Step 2: Create a Claude client
client = Anthropic()

# Step 3: Send a message and get a response
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello Claude! In one sentence, what's the difference between AI and machine learning?"}
    ]
)

# Step 4: Print Claude's response
print(response.content[0].text)
