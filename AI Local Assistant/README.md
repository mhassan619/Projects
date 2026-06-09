# Hassan's AI – Claude-style Web UI

A Flask + HTML/CSS/JS front-end for your CLI `SmartChatbot`.
Same Ollama backend (`llama3.2` by default), now wrapped in a clean
Claude-AI-inspired chat interface with **streaming responses**.

---

## Folder structure

```
chatbot-project/
├── app.py                 # Flask app (routes + SSE streaming)
├── chatbot.py             # SmartChatbot class (refactored for Flask)
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html         # Main page (Claude-like layout)
│
└── static/
    ├── css/
    │   └── style.css      # Responsive theme
    └── js/
        └── script.js      # Streaming client + UI logic
```

---

## Run it

```bash
# 1. Make sure Ollama is running and llama3.2 is pulled
ollama serve
ollama pull llama3.2

# 2. Install Python deps
pip install -r requirements.txt

# 3. Start the web app
python app.py
```

Then open **http://localhost:5000** in your browser.

The CLI mode still works exactly the same:

```bash
python chatbot.py
```

---

## What changed vs. your CLI code

`chatbot.py` keeps your original class 1-to-1 (same `__send`, `__history`,
system prompt, `run()` loop) and just adds a few public methods on top:

| New public method            | Purpose                                |
| ---------------------------- | -------------------------------------- |
| `send(msg)`                  | non-streaming call (alias of `__send`) |
| `stream(msg)`                | **generator** that yields text chunks  |
| `get_history()`              | safe copy of the conversation          |
| `clear_history()`            | reset the conversation                 |
| `model` (property)           | exposes `__model` to templates         |

`save_history()` now also **returns** the filename instead of just
printing, so the Flask app can show a toast: `Saved · chat_20260609_183045.json`.

---

## Features

- ✨ **Streaming** responses (Server-Sent Events) — token-by-token, like Claude
- 📱 **Responsive** — sidebar collapses on mobile, backdrop closes it
- 🎨 **Claude-inspired** colour palette (warm cream + terracotta)
- 🧠 **Markdown rendering** (code blocks, lists, bold/italic, links) via `marked` + `DOMPurify`
- 💬 **Welcome screen** with 4 suggested prompts
- 📋 **Copy** any AI reply with one click
- 💾 **Save chat** to JSON on the server (topbar icon)
- 🆕 **New chat** clears the conversation
- 🕘 **Recents** in the sidebar (titles saved to `localStorage`)
- ⌨️ **Enter** to send, **Shift+Enter** for newline
- 📐 Auto-resizing textarea

---

## API endpoints

| Method | Route          | Body / Returns                                       |
| ------ | -------------- | ---------------------------------------------------- |
| GET    | `/`            | renders `index.html`                                 |
| POST   | `/api/chat`    | `{message: "..."}` → SSE stream of `{content: "..."}` chunks |
| POST   | `/api/new_chat`| clears server-side history                           |
| POST   | `/api/save`    | saves `chat_<timestamp>.json`, returns filename      |
| GET    | `/api/history` | full conversation as JSON                            |

---

## Notes

- `marked` and `DOMPurify` are loaded from a CDN (jsDelivr) — no build step needed.
- For a fully-offline setup, swap the two `<script>` tags in `index.html` for local copies in `static/js/`.
- The global `bot = SmartChatbot()` in `app.py` is fine for a single-user demo. For multi-user, swap it for `flask.session` keys + a `bot` registry.
