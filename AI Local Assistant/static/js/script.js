// =====================================================
//  Hassan's AI – Frontend logic
//  Handles streaming responses (SSE), UI state, recents
// =====================================================

const $  = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const messagesEl       = $("#messages");
const welcomeEl        = $("#welcome");
const inputEl          = $("#input");
const composer         = $("#composer");
const sendBtn          = $("#sendBtn");
const sidebarEl        = $("#sidebar");
const sidebarBackdrop  = $("#sidebarBackdrop");
const sidebarToggle    = $("#sidebarToggle");
const newChatBtn       = $("#newChatBtn");
const saveBtn          = $("#saveBtn");
const chatListEl       = $("#chatList");
const contentEl        = $(".content");

let isStreaming       = false;
let isNewChat         = true;
let savedChats        = [];   // localStorage list of recent chat titles
let currentAiContent  = "";

// -----------------------------------------------------
// Small helpers
// -----------------------------------------------------
function autoResize() {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 200) + "px";
  sendBtn.disabled = isStreaming || !inputEl.value.trim();
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function renderMarkdown(text) {
  if (!text) return "";
  if (typeof marked === "undefined") return escapeHtml(text);
  const rawHtml = marked.parse(text, {
    breaks: true,
    gfm: true,
    headerIds: false,
    mangle: false,
  });
  return typeof DOMPurify !== "undefined"
    ? DOMPurify.sanitize(rawHtml)
    : rawHtml;
}

function uid() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

function toast(msg) {
  let t = document.querySelector(".toast");
  if (!t) {
    t = document.createElement("div");
    t.className = "toast";
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove("show"), 2200);
}

function scrollToBottom(smooth = true) {
  contentEl.scrollTo({ top: contentEl.scrollHeight, behavior: smooth ? "smooth" : "auto" });
}

function typingDotsHtml() {
  return '<span class="typing"><span></span><span></span><span></span></span>';
}

// -----------------------------------------------------
// Chat rendering
// -----------------------------------------------------
function addMessage({ role, content, streaming = false }) {
  const wrap = document.createElement("div");
  wrap.className = "msg";
  wrap.dataset.role = role;

  const avatar = document.createElement("div");
  avatar.className = `msg-avatar ${role}`;
  avatar.textContent = role === "user" ? "H" : "AI";

  const body = document.createElement("div");
  body.className = "msg-body";

  const roleEl = document.createElement("div");
  roleEl.className = "msg-role";
  roleEl.textContent = role === "user" ? "You" : "Hassan's AI";

  const contentElLocal = document.createElement("div");
  contentElLocal.className = "msg-content";
  if (streaming) {
    contentElLocal.innerHTML = typingDotsHtml();
  } else {
    contentElLocal.innerHTML = renderMarkdown(content);
  }

  body.appendChild(roleEl);
  body.appendChild(contentElLocal);

  if (!streaming && role === "assistant" && content && !content.startsWith("❌")) {
    const actions = buildActions(content);
    body.appendChild(actions);
  }

  wrap.appendChild(avatar);
  wrap.appendChild(body);
  messagesEl.appendChild(wrap);
  return { wrap, body, contentEl: contentElLocal };
}

function buildActions(content) {
  const actions = document.createElement("div");
  actions.className = "msg-actions";

  const copy = document.createElement("button");
  copy.className = "msg-action";
  copy.innerHTML =
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
    '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>' +
    '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg> Copy';
  copy.onclick = () => {
    navigator.clipboard.writeText(content).then(() => toast("Copied!"));
  };
  actions.appendChild(copy);
  return actions;
}

// -----------------------------------------------------
// Streaming chat
// -----------------------------------------------------
async function sendMessage(text) {
  if (isStreaming || !text.trim()) return;

  // hide welcome on first user msg
  if (isNewChat) {
    welcomeEl.hidden = true;
    messagesEl.hidden = false;
    isNewChat = false;
  }

  isStreaming = true;
  sendBtn.disabled = true;
  inputEl.value = "";
  autoResize();

  addMessage({ role: "user", content: text });
  const ai = addMessage({ role: "assistant", content: "", streaming: true });
  currentAiContent = "";
  scrollToBottom();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    if (!response.ok || !response.body) throw new Error("Network error");

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      const events = buffer.split("\n\n");
      buffer = events.pop() || "";

      for (const ev of events) {
        const line = ev.trim();
        if (!line.startsWith("data:")) continue;
        const payload = line.slice(5).trim();
        if (payload === "[DONE]") continue;
        try {
          const { content, error } = JSON.parse(payload);
          if (error) {
            currentAiContent = `❌ ${error}`;
          } else if (content) {
            currentAiContent += content;
          }
          ai.contentEl.innerHTML =
            renderMarkdown(currentAiContent) + typingDotsHtml();
          scrollToBottom(false);
        } catch (_) {
          /* ignore parse errors */
        }
      }
    }

    // finalize: drop typing dots, add copy action
    ai.contentEl.innerHTML = renderMarkdown(currentAiContent);
    if (currentAiContent && !currentAiContent.startsWith("❌")) {
      ai.body.appendChild(buildActions(currentAiContent));
    }

    // record this chat in the sidebar
    addRecentChat(text);
  } catch (err) {
    ai.contentEl.innerHTML =
      `<p>❌ ${escapeHtml(err.message || "Failed to reach the server")}</p>`;
  } finally {
    isStreaming = false;
    sendBtn.disabled = false;
    inputEl.focus();
    autoResize();
  }
}

// -----------------------------------------------------
// Recents (localStorage – just titles for now)
// -----------------------------------------------------
function loadRecents() {
  try {
    savedChats = JSON.parse(localStorage.getItem("hassan_ai_recents") || "[]");
  } catch {
    savedChats = [];
  }
  renderRecents();
}
function saveRecents() {
  localStorage.setItem(
    "hassan_ai_recents",
    JSON.stringify(savedChats.slice(0, 12))
  );
}
function renderRecents() {
  if (!savedChats.length) {
    chatListEl.innerHTML = '<div class="chat-list-empty">No saved chats yet</div>';
    return;
  }
  chatListEl.innerHTML = "";
  savedChats.forEach((c) => {
    const el = document.createElement("div");
    el.className = "chat-item";
    el.dataset.id = c.id;
    el.innerHTML =
      `<span class="chat-item-title">${escapeHtml(c.title)}</span>` +
      `<button class="chat-item-delete" title="Delete" aria-label="Delete">×</button>`;

    el.querySelector(".chat-item-title").onclick = () =>
      toast("Start a New chat to keep going – past chats live on the server.");
    el.querySelector(".chat-item-delete").onclick = (e) => {
      e.stopPropagation();
      savedChats = savedChats.filter((x) => x.id !== c.id);
      saveRecents();
      renderRecents();
    };
    chatListEl.appendChild(el);
  });
}
function addRecentChat(firstUserMsg) {
  const title = firstUserMsg.slice(0, 40) + (firstUserMsg.length > 40 ? "…" : "");
  // Replace any existing entry with the same title
  savedChats = savedChats.filter((c) => c.title !== title);
  savedChats.unshift({ id: uid(), title, ts: Date.now() });
  saveRecents();
  renderRecents();
}

// -----------------------------------------------------
// New chat / save
// -----------------------------------------------------
async function newChat() {
  if (isStreaming) return;
  try {
    await fetch("/api/new_chat", { method: "POST" });
  } catch (_) {}
  messagesEl.innerHTML = "";
  messagesEl.hidden = true;
  welcomeEl.hidden = false;
  isNewChat = true;
  inputEl.focus();
}

async function saveChat() {
  if (isStreaming) return;
  if (isNewChat || !messagesEl.children.length) {
    toast("Nothing to save yet");
    return;
  }
  try {
    const res = await fetch("/api/save", { method: "POST" });
    const data = await res.json();
    if (data.filename) toast(`Saved · ${data.filename}`);
    else toast("Save failed");
  } catch (_) {
    toast("Save failed");
  }
}

// -----------------------------------------------------
// Sidebar toggle (mobile)
// -----------------------------------------------------
function openSidebar() {
  sidebarEl.classList.add("open");
  sidebarBackdrop.classList.add("show");
}
function closeSidebar() {
  sidebarEl.classList.remove("open");
  sidebarBackdrop.classList.remove("show");
}

// -----------------------------------------------------
// Wire everything up
// -----------------------------------------------------
inputEl.addEventListener("input", autoResize);

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    composer.requestSubmit();
  }
});

composer.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = inputEl.value.trim();
  if (text) sendMessage(text);
});

$$(".suggestion").forEach((btn) => {
  btn.addEventListener("click", () => {
    const prompt = btn.dataset.prompt;
    if (prompt) {
      inputEl.value = prompt;
      autoResize();
      inputEl.focus();
    }
  });
});

sidebarToggle.addEventListener("click", () =>
  sidebarEl.classList.contains("open") ? closeSidebar() : openSidebar()
);
sidebarBackdrop.addEventListener("click", closeSidebar);
newChatBtn.addEventListener("click", newChat);
saveBtn.addEventListener("click", saveChat);

// boot
loadRecents();
autoResize();
inputEl.focus();
