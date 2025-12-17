## Screen-Aware AI Assistant

An experimental tool that periodically **captures your screen**, sends the image to an **AI vision model**, and asks it **“What should I do next?”**. You can use it for games (e.g. Roblox) or any on-screen workflow where you want guidance.

This project starts in **advisor mode** (AI only suggests actions). In the future it can be extended to **automation mode** (AI suggestions translated into real mouse/keyboard actions).

---

## Goals

- **Screenshot-based guidance**: Capture the current screen or window and ask an AI what to do next.
- **Game-friendly**: Work well with games like Roblox, but not limited to them.
- **Modular**: Clean separation between:
  - Screenshot capture
  - AI calls
  - Decision logic
  - (Optional) Mouse/keyboard actions
- **Safe by default**: Start as a read-only advisor without automatically controlling your computer.

---

## High-Level Flow

1. Capture a screenshot of the **entire screen** or a **specific window/region**.
2. Send the image plus a **prompt** (e.g. “You are helping me play this game. What should I do next?”) to an **AI vision API**.
3. Receive a **short text suggestion** (or structured JSON) describing the next action.
4. Display the suggestion in the terminal or a small UI.
5. (Future) Optionally convert that suggestion into:
   - Mouse movement/clicks
   - Keyboard presses
   - Higher-level macros
6. Repeat the process on a **timer** (every N seconds) or when **triggered** by a hotkey.

---

## Suggested Tech Stack

You can change this later, but here’s a recommended starting point:

- **Language**: Python
- **Screenshot capture**:
  - `pyautogui` or `mss`
- **Automation (optional)**:
  - `pyautogui` or `pynput` for mouse/keyboard control
- **AI API (vision)**:
  - Any provider that supports **image + text** input (e.g. OpenAI vision models)
- **Config**:
  - `.env` file for API keys and settings

---

## Proposed Project Structure

- `README.md` – You are here.
- `main.py` – Entry point; command-line interface and main loop.
- `screenshot.py` – Functions to capture screen / window regions.
- `ai_client.py` – Code to talk to the AI API (send image + prompt, parse response).
- `actions.py` (later) – Map AI suggestions to concrete mouse/keyboard actions.
- `config.example.env` – Example config for API keys and options.

This structure is just a suggestion; you can simplify or reorganize as needed.

---

## Basic Usage Concept (Future)

Once implemented, you should be able to do something like:

```bash
python main.py --interval 5 --mode advisor
```

Where:

- **`--interval 5`**: Capture and query every 5 seconds.
- **`--mode advisor`**: Only prints AI suggestions; does not control your mouse/keyboard.

Example interaction in the terminal:

```text
[AI] I see a green “Play” button. Click it to start the match.
[AI] Move your character toward the open door on the right.
[AI] Open your inventory and equip the sword in the first slot.
```

---

## Safety & Ethics

- **Game terms of service**:
  - Do **not** use this to violate game rules (e.g. unattended botting or cheating in online games).
- **Privacy**:
  - Screenshots may contain sensitive information (messages, accounts, etc.).
  - Avoid running this over banking apps, emails, or private chats.
- **Control & escape hatches**:
  - Advisor mode is **read-only** (recommended default).
  - If you later add automation, include:
    - A **panic hotkey** to instantly disable all actions.
    - Clear visual indication that automation is active.

---

## Roadmap

Short term:

- **v0.1 – Advisor prototype**
  - Capture one screenshot.
  - Send it to an AI vision API with a prompt.
  - Print “what to do next” in the terminal.

- **v0.2 – Continuous loop**
  - Add interval-based capture (every N seconds).
  - Add basic configuration via CLI flags or `.env`.

Medium term:

- **v0.3 – Structured output**
  - Ask the AI to respond with JSON (e.g. `{ "action": "press_key", "key": "W", "duration_ms": 500 }`).

- **v0.4 – Optional automation**
  - Map structured AI responses to actual mouse/keyboard events.
  - Implement safety mechanisms and “advisor-only” vs “automation” modes.

Long term:

- **Overlays & GUI**
  - On-screen overlay that shows AI suggestions on top of the game/window.

- **Game-specific profiles**
  - Custom prompts and logic for specific games (e.g. Roblox obbies, FPS, etc.).

---

## Getting Started (When You’re Ready to Code)

1. **Pick the language** (this README assumes Python).
2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # on Windows
   ```
3. **Install core dependencies** (for example, once you create `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
4. **Add an AI API key**:
   - Create `.env` from `config.example.env`.
   - Put your API key and desired settings there.
5. **Build the first prototype**:
   - Implement `screenshot.py` with a single function like `capture_screen()`.
   - Implement `ai_client.py` with a `ask_ai(image, prompt)` function.
   - In `main.py`, wire them together to:
     - Capture a screenshot.
     - Call `ask_ai`.
     - Print the suggestion.

Once you’re ready, I can scaffold the initial Python files and a minimal working prototype that sends a screenshot to an AI model and prints back “what to do next”.


