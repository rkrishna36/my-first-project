# Lessons 2 & 3 Summary: Multi-turn Conversations + Interactive Chatbot

> **Note:** This file covers both lessons because we missed creating one for Lesson 2 at the time. Going forward, each lesson will have its own summary inside its own folder.

## Overview

In Lesson 1 you wrote a single-shot script — ask Claude a question, get a single answer, done. Lessons 2 and 3 transform that into a real conversational experience: Claude appears to *remember* what was said earlier, and you interact in real-time at the keyboard.

What's covered here:
- The "memory" concept (and how it actually works under the hood)
- A subtle quirk in how LLMs handle "randomness"
- What tokens are and why they cost money
- Building an interactive while-loop chatbot
- The full Git workflow for both lessons

---

## Lesson 2: Multi-turn Conversations

### The core concept: Claude is stateless

This is the single most important idea in this lesson:

> **Anthropic's servers do not remember anything between API calls. Each call is a clean slate. The illusion of memory is created entirely by you, the developer, sending the full history every time.**

When you chat at claude.ai, what *feels like* Claude remembering you is actually claude.ai's frontend silently maintaining a conversation list and including it in every backend call. We're now doing manually what they do automatically.

### The mental model

Every API call is like meeting Claude for the very first time. Claude has zero memory of you, this conversation, or anything you've said. To make it *seem* like Claude remembers, you bring a notebook containing everything that's been said so far. Claude reads the entire notebook, says one new thing, and *you* write that new thing into the notebook before the next meeting.

The "memory" effect lives entirely on your side — it lives in the notebook (the `conversation` list). Claude is always meeting you fresh; the notebook is what makes the encounter feel continuous.

### The code that creates "memory"

```python
conversation = []

# Each turn:
conversation.append({"role": "user", "content": user_message})

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=conversation,  # ← send the whole list
)

claude_reply = response.content[0].text

# THE KEY LINE — saves Claude's reply back to history:
conversation.append({"role": "assistant", "content": claude_reply})
```

The single most important line: **`conversation.append({"role": "assistant", "content": claude_reply})`**

Without it, each new turn would only contain *your* messages, never Claude's. Claude wouldn't know what it had previously said, and conversations would break the moment they depended on Claude's prior responses.

### A subtle and important quirk: LLMs are bad at "randomness"

We tested memory by asking Claude to "pick a number between 1 and 100" then asking "what number did you pick?" without saving its reply.

**Surprising result:** Claude picked 42 in turn 1 *and* answered "42" in turn 2 — even though it had no memory of turn 1.

**Why?** LLMs are not actually random. When asked to "pick a random number 1-100," they heavily favor a small set — particularly **42, 37, 73, 17**. The number 42 has an especially strong bias because of *The Hitchhiker's Guide to the Galaxy*.

Both calls reached for the same statistically-loaded "random" answer. The match was coincidence, not memory.

**The lesson:** *Never trust the surface output of an AI system. Reason about what was actually in the messages list, and what Claude could possibly have known.* This is the discipline that separates real AI engineers from people who think their demos work because they happen to.

---

## KTM #1: Tokenization — what Claude actually sees

### What is a token?

A *token* is the unit Claude (and every LLM) actually processes. It's not a word, it's not a character — it's a chunk somewhere in between.

The text "Hi Claude" doesn't reach Claude as the string "Hi Claude." It reaches Claude as something like `[13347, 11220]` — a list of numerical IDs. The tokenizer's job is to convert text into these IDs and back.

### Surprises from the tokenizer explorer

| Text | Tokens | Why |
|---|---|---|
| `"the"` | 1 token | Common word — got its own token slot |
| `"strawberry"` | 3 tokens (`str`, `aw`, `berry`) | Less common; tokenizer chops by *training-data frequency*, not by meaning |
| `"antidisestablishmentarianism"` | 6 tokens | Rare `antidis` prefix gets chopped; common parts like `establish`, `ment`, `ism` survived |
| `"Hello world"` | 2 tokens | Spaces *belong to the next word's token* — the second is `' world'` with a leading space |
| `"Hello, world!"` | 4 tokens | Punctuation creates extra tokens |
| `"こんにちは"` | 1 token | Common Japanese greetings can have their own token |
| Full English sentence | ~9 tokens | Roughly 1 token per word, plus punctuation |

### Why this matters: cost and context

```
After turn 1 (user):       13 tokens
After turn 2 (assistant):  53 tokens
After turn 3 (user):       61 tokens
After turn 4 (assistant): 100 tokens
After turn 5 (user):      110 tokens
After turn 6 (assistant): 152 tokens
```

**Two things to absorb:**

1. **Conversation history grows linearly with turns**, dominantly through Claude's responses (longer than user messages).
2. **Every API call re-sends the entire history.** By turn 6, you're paying to re-send turns 1–5 *every single time.*

This is why **prompt caching** (covered in a future lesson) is one of the highest-leverage cost optimizations in production AI engineering — it lets you cache static parts of conversations server-side instead of re-paying for them.

---

## Lesson 3: Interactive CLI Chatbot

### What changed from Lesson 2

Lesson 2 had three hardcoded turns. Lesson 3 wraps the same memory pattern in a `while` loop with `input()` so you can talk to Claude indefinitely from the keyboard. **The memory pattern is identical** — we just wrapped Python's standard interactive-program tools around it.

### Full code

```python
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

SYSTEM_PROMPT = "You are a helpful, friendly AI assistant. Keep responses concise unless asked for detail."

conversation = []

print("=" * 50)
print("Chat with Claude (type 'quit' to exit)")
print("=" * 50)

while True:
    user_input = input("\nYou: ").strip()

    if not user_input:
        continue

    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("\nGoodbye!")
        break

    conversation.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversation
    )

    claude_reply = response.content[0].text
    conversation.append({"role": "assistant", "content": claude_reply})

    print(f"\nClaude: {claude_reply}")

print(f"\nConversation ended. {len(conversation)} messages exchanged.")
```

### Line-by-line on what's new

**`while True:`**
A loop that runs forever — until something inside says to stop. This is how every interactive program works (chatbots, games, terminals themselves). The way out is `break`.

**`input("\nYou: ")`**
Python's built-in for reading from the keyboard. The program pauses, shows the prompt text, and waits for the user to type and press Enter. Whatever they typed comes back as a string. The `\n` adds a blank line before the prompt for readability.

**`.strip()`**
Removes whitespace from the beginning and end of a string. Cleans up accidental spacebar presses. Tiny detail, big quality-of-life win.

**`if not user_input: continue`**
If the user just hit Enter without typing, skip the rest of this iteration and go back to waiting for input. `continue` means "jump straight to the next loop turn."

**`if user_input.lower() in ['quit', 'exit', 'bye']: break`**
- `.lower()` normalizes case so `"QUIT"` or `"Quit"` both match
- `in [...]` checks list membership
- `break` exits the loop entirely; control jumps past the closing of the `while`

### The rhythm of the loop

Each turn:

1. Wait for keyboard input
2. Skip if empty, exit if it's a quit word
3. Append the user message to history
4. Send the full history to Claude
5. Append Claude's reply to history
6. Print the reply
7. Go back to step 1

Same memory pattern as Lesson 2 — just running indefinitely.

---

## Git Workflow Recap

For each lesson:

```bash
# Start a feature branch off main
git checkout -b feature/lesson-XX-name

# Do the work...

# Commit
git add <files>
git commit -m "Add lesson XX: short description"
git push -u origin feature/lesson-XX-name

# On GitHub: open PR, self-review, merge

# Sync local main and clean up
git checkout main
git pull
git branch -d feature/lesson-XX-name
```

By the end of these two lessons, you've done this twice. It's becoming muscle memory.

---

## Project Structure (current state)

```
MY-FIRST-PROJECT/
├── .gitignore
├── README.md
├── lesson-01-hello-claude/
│   ├── venv/                       ← shared by all lessons (gitignored)
│   ├── .env                        ← API key (gitignored)
│   ├── hello_claude.py             ← Lesson 1
│   ├── with_system_prompt.py       ← Lesson 1
│   ├── multi_turn.py               ← Lesson 2
│   └── tokenizer_explorer.py       ← Lesson 2 (KTM #1)
└── lesson-03-interactive-chatbot/
    ├── .env                        ← copy of the one above
    ├── chatbot.py                  ← Lesson 3
    └── Lessons-02-03-Summary.md    ← this file
```

In a "real" production project, you'd refactor toward **one** `venv/` and **one** `.env` at the repo root, shared across all subfolders. We're being slightly informal for learning velocity. After a few more lessons, we'll do a small structural cleanup as its own exercise — that itself is a real engineering practice.

---

## Quick Reference: New Python Concepts

| Concept | Meaning |
|---|---|
| `[]` (empty list) | A list with nothing in it; ready to grow |
| `.append()` | Add an item to the end of a list |
| `dict` (`{...}`) | Key-value object (like `{"role": "user", "content": "hi"}`) |
| `while True:` | Loop that runs forever until `break` |
| `input("prompt: ")` | Pause and read keyboard input |
| `.strip()` | Remove whitespace from ends of a string |
| `.lower()` | Convert a string to lowercase |
| `in [...]` | Check if something is a member of a list |
| `continue` | Skip rest of this loop iteration; go to next |
| `break` | Exit the loop entirely |
| `f"text {variable}"` | F-string: embed a variable inside a string |

---

## What's Next

**Lesson 4 — Streaming Responses.** Right now your chatbot waits for Claude's full reply, then dumps the whole thing. Streaming makes the words appear one at a time as Claude generates them, like at claude.ai. Small concept, big UX feel — and it teaches you something subtle about how the API actually works.
