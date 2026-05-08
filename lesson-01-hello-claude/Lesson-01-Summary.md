# Lesson 1: Your First AI Program with Claude

## What We Built

In one session, we went from a blank folder to two working Python scripts that talk to Anthropic's Claude AI over the internet — using a real-world developer workflow (Git branches, pull requests, secure environment variables).

By the end you had:

1. A Python project with an isolated environment
2. A secure way to store your API key (so it never gets pushed to GitHub)
3. **`hello_claude.py`** — sends a question to Claude and prints the answer
4. **`with_system_prompt.py`** — shows how a "system prompt" can completely change Claude's tone and personality
5. Two commits on two feature branches, both merged into `main` via pull request — the same workflow used at every real software company

---

## Section 1: Initial Setup

### 1.1 Python check

```
python3 --version
```

Confirms Python 3 is installed. On Mac, modern versions only ship `python3` (with the 3), not plain `python`. We saw `Python 3.9.6` — perfect.

> ⚠️ **Mac note:** Always use `python3` (with the 3). If you type `python` you'll get "command not found." This is normal — Apple removed the unversioned `python` command years ago.

### 1.2 Anthropic API key

Sign up at **https://console.anthropic.com**, add a small amount of credit (~$5 lasts a long time), and generate an API key — a long string starting with `sk-ant-...`.

> 🔐 **Important:** the API key is shown **only once**. If you lose it, you must delete it and create a new one. Anthropic never displays it again — that's a security feature, not a bug.

The Claude.ai Pro subscription is **separate** from the API account. Pro is for chatting at claude.ai; the Console is for programmatic API access.

### 1.3 Project folder & virtual environment

Inside our existing repo `MY-FIRST-PROJECT`, we created a new folder and set up an isolated Python environment:

```
cd lesson-01-hello-claude
python3 -m venv venv
source venv/bin/activate
```

**What's a virtual environment?** An isolated copy of Python just for this project. When we install libraries, they go into this little bubble instead of polluting the whole computer. Every real Python project uses one.

When activated, your terminal prompt shows `(venv)` at the start — that's how you know you're inside the bubble.

### 1.4 Installing libraries

```
pip install anthropic python-dotenv
```

Two libraries:

- **`anthropic`** — the official Python SDK for talking to Claude
- **`python-dotenv`** — for safely loading the API key from a file

---

## Section 2: Securing the API Key

This is **the single most important habit in AI engineering**: API keys must never end up in your GitHub repo. Bots scrape public GitHub 24/7 looking for leaked keys. We set this up correctly from day one.

### 2.1 The `.env` file

Lives inside `lesson-01-hello-claude/`. A single line:

```
ANTHROPIC_API_KEY=sk-ant-api03-...your-real-key...
```

This file holds the actual key on your machine only.

### 2.2 The `.gitignore` file

Lives at the **repo root** (in `MY-FIRST-PROJECT/`):

```gitignore
# Python virtual environments — can always be recreated, no need to commit
venv/

# Secrets and API keys — NEVER commit these
.env

# Python compiled cache files
__pycache__/
*.pyc
```

Reading the file:

- Lines starting with `#` are comments
- `venv/` — the trailing `/` means "directory named venv" (matches anywhere in the repo)
- `.env` — matches any file called `.env` anywhere in the repo
- `__pycache__/` and `*.pyc` — Python auto-generates these; they're noise

### 2.3 Verification

```
git status
```

`venv/` and `.env` should **NOT** appear in the output. That's how you know git is correctly ignoring them.

---

## Section 3: `hello_claude.py` — Your First AI Call

### Full code

```python
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
```

### Line-by-line explanation

**`from dotenv import load_dotenv`**

*"From the library called `dotenv`, give me the function called `load_dotenv`."* In Python you must *import* tools before using them — like opening a toolbox before grabbing a hammer. We need this function to read our `.env` file.

**`from anthropic import Anthropic`**

Same pattern. From the `anthropic` library, give us the class called `Anthropic` (capital A). This is the main object for talking to Claude. A *class* is like a blueprint; later we'll use it to build an actual usable object.

**`load_dotenv()`**

Calling the function we imported. The parentheses `()` mean "execute now." This looks for a `.env` file in the current folder, reads it, and loads each line as an *environment variable* — meaning the operating system itself now knows `ANTHROPIC_API_KEY=sk-ant-...`.

**`client = Anthropic()`**

Three things happen:

1. `Anthropic()` — builds an instance from the blueprint
2. The Anthropic SDK is clever: it automatically looks for `ANTHROPIC_API_KEY` in environment variables. That's why we never type the key in our code.
3. `client = ...` — stores the instance in a variable named `client`. We'll use `client` to talk to Claude.

This is one of the cleanest patterns in modern AI engineering — **the secret never appears in your code.** Anyone reading your code sees `client = Anthropic()` and learns nothing about your key.

**`response = client.messages.create(...)`**

The actual API call. Reading it:

- `client` — our connection
- `.messages` — the part of the API that handles conversations
- `.create(...)` — make a new message exchange
- `response = ...` — save what comes back

When this runs, your laptop makes an HTTPS request over the internet to Anthropic's servers, Claude generates a reply, the reply travels back, and lands in `response`.

**`model="claude-haiku-4-5-20251001"`**

Which Claude to use. Anthropic offers multiple models with different speed/intelligence/cost trade-offs:

- **Haiku** — fastest, cheapest. We use it for learning (pennies per call).
- **Sonnet** — balanced.
- **Opus** — most intelligent, most expensive.

The `-20251001` suffix is a version date pin, so your code keeps using the same exact model even when newer versions ship.

**`max_tokens=1024`**

Maximum length of Claude's reply, measured in **tokens** (~¾ of a word each). 1024 tokens ≈ 750 words. The API requires this — there's no default.

**`messages=[{"role": "user", "content": "..."}]`**

Where the conversation lives. It's a *list* of message objects, each with:

- `"role"` — `"user"` (you) or `"assistant"` (Claude)
- `"content"` — the actual text

For now, just one message. To give Claude memory of past turns, we'd add more entries to this list.

**`print(response.content[0].text)`**

Unpacking the response. The API doesn't return plain text — it returns a structured object containing the model used, token counts, and the actual reply. The reply lives at `response.content`, which is itself a list (because in advanced cases Claude can return multiple "blocks"). For a simple message, there's one block at index `[0]`. Its `.text` attribute is the actual words. `print(...)` displays them.

### What happens when you run it

`python3 hello_claude.py` triggers this loop:

1. Your laptop packages your question into JSON
2. Sends it over HTTPS to Anthropic's servers
3. Their Haiku model generates an answer
4. Sends it back
5. Your script unpacks it and prints it

That's the entire core of how every AI app works — ChatGPT, Cursor, Perplexity, work AI agents — all built on top of this loop.

---

## Section 4: Git Workflow — Branch, Commit, PR, Merge, Sync

In real-world development, you almost never commit directly to `main`. The principle: `main` is the source of truth — always working, always deployable. In-progress work lives on its own branch, gets reviewed, then merges in.

### 4.1 Create a feature branch

```
git checkout -b feature/lesson-01-hello-claude
```

- `git checkout` — switch branches
- `-b` — but first, *create* a new one
- `feature/...` — naming convention. Common patterns: `feature/...` (new work), `fix/...` (bug fixes), `chore/...` (maintenance). The slash isn't a folder — git just uses it for visual grouping.

### 4.2 Stage files

```
git add ../.gitignore hello_claude.py
```

"These are the files I want to commit." We name files explicitly rather than `git add .` (which adds everything) — for learning, explicit is safer; it forces you to look at what's going in.

### 4.3 Sanity check

```
git status
```

Both files should show under "Changes to be committed" (green). The `.env` should **NOT** appear. Always check before committing — this is the habit that prevents accidentally leaking secrets.

### 4.4 Commit

```
git commit -m "Add lesson 01: hello world API call to Claude"
```

The `-m` flag attaches the *commit message*. Good messages matter — six months from now when you scroll your git history, you should understand each commit from its message alone. Bad: `"changes"`. Good: descriptive.

### 4.5 Push the branch

```
git push -u origin feature/lesson-01-hello-claude
```

The `-u origin <branch-name>` is needed **only the first time** you push a new branch. It links your local branch to the matching branch on GitHub. After that, plain `git push` and `git pull` just work.

### 4.6 Pull Request → review → merge → sync

On GitHub:

- Click "Compare & pull request"
- Write a meaningful title and description
- Self-review the "Files changed" tab
- Merge → optionally delete the remote branch

Then locally:

```
git checkout main
git pull
git branch -d feature/lesson-01-hello-claude
```

Switches you back to main, pulls down the merged code, and deletes the local copy of the now-merged branch. The `-d` (lowercase) is "safe delete" — git refuses if the branch isn't fully merged, which protects you from losing work.

This **branch → commit → push → PR → review → merge → sync → cleanup** loop is the rhythm of every working day in software.

---

## Section 5: System Prompts — Giving Claude a Role

When you chat at claude.ai, Claude has a default personality — helpful, balanced, slightly formal. That personality isn't baked into the model itself; it comes from a *system prompt* that Anthropic writes and prepends to every conversation.

A system prompt is a special instruction that:

- Comes from **you** (the developer), not the user
- Tells Claude its role, tone, constraints, and rules
- Persists for the entire conversation — Claude follows it every turn
- Is invisible to the end user

It's the most powerful lever you have over Claude's behavior. Same model, same question — pirate vs. legal expert vs. code reviewer vs. a beginner-friendly tutor — all controlled by this one parameter.

### `with_system_prompt.py`

```python
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

question = "What is a variable in programming?"

# ---------- Call 1: Default Claude, no system prompt ----------
print("=" * 60)
print("WITHOUT SYSTEM PROMPT (default Claude)")
print("=" * 60)

response_default = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": question}
    ]
)
print(response_default.content[0].text)

# ---------- Call 2: Same question, Claude as a beginner-friendly tutor ----------
print("\n" + "=" * 60)
print("WITH SYSTEM PROMPT (patient tutor for absolute beginners)")
print("=" * 60)

response_tutor = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system="You are a patient, encouraging programming tutor for absolute beginners who have never written code. Use simple everyday analogies. Avoid technical jargon completely. Keep your answer under 4 sentences. End with a tiny, concrete real-world example.",
    messages=[
        {"role": "user", "content": question}
    ]
)
print(response_tutor.content[0].text)
```

### What's new (the rest is the same as `hello_claude.py`)

**`system="..."`** — a top-level parameter to `create(...)`, **not** a message in the messages list. Anthropic designed it this way deliberately so end users can't inject their own system instructions through the message field. This becomes a real security concern in production apps.

The system prompt is plain English. There's no special syntax — just write what you want Claude to be.

### The 4-part system prompt skeleton

Every good system prompt has these four parts:

1. **Role** — who Claude is ("a patient tutor")
2. **Audience** — who Claude is talking to ("absolute beginners")
3. **Style constraints** — how to communicate ("simple analogies, no jargon, under 4 sentences")
4. **Output requirement** — specific shape of the response ("end with a tiny example")

This **role + audience + style + output** pattern is the skeleton of every good system prompt you'll ever write.

**`print("=" * 60)`** — visual separator. `"=" * 60` is Python shorthand for "the `=` character repeated 60 times." Just makes the output easier to read.

---

## Quick Reference / Glossary

| Term | Meaning |
|------|---------|
| **API** | Application Programming Interface. The contract between your code and someone else's service. |
| **API key** | Your password to a paid API like Anthropic's. |
| **Branch** (git) | An independent line of changes; doesn't affect `main` until merged. |
| **Commit** (git) | A saved snapshot of your changes with a message. |
| **Environment variable** | A value the operating system stores, accessible to programs without putting it in their source code. |
| **`.env` file** | A local file that loads values into environment variables when the program starts. |
| **`.gitignore`** | Tells git which files/folders to never track. |
| **HTTPS** | The secure version of HTTP, the protocol for data transfer over the web. |
| **JSON** | JavaScript Object Notation. The standard format for sending structured data over the internet. |
| **`pip`** | Python's package installer. `pip install X` adds library X. |
| **PR (pull request)** | A proposal to merge a branch into another (usually `main`), with a chance for review. |
| **System prompt** | Instructions to Claude about its role, set by the developer, invisible to the user. |
| **Token** | The unit Claude uses to count text length, roughly ¾ of a word. |
| **`venv` (virtual environment)** | An isolated copy of Python for one project, so its libraries don't conflict with other projects. |

---

## What's Next

Future lessons will cover:

- **Multi-turn conversations** — giving Claude memory of previous messages
- **Streaming** — making responses appear word-by-word like at claude.ai
- **Tool use** — giving Claude the ability to call functions (the foundation of agents)
- **Prompt engineering patterns** — chain-of-thought, few-shot examples, structured outputs
- **RAG (Retrieval-Augmented Generation)** — giving Claude access to your own documents

---

## Common Commands Cheat Sheet

```bash
# Activate venv (anytime you open a fresh terminal)
source venv/bin/activate

# Run a Python script
python3 script_name.py

# See what's changed
git status

# Create + switch to a new branch
git checkout -b feature/some-name

# Stage, commit, push (first time)
git add filename
git commit -m "descriptive message"
git push -u origin feature/some-name

# After PR is merged on GitHub
git checkout main
git pull
git branch -d feature/some-name
```
