const $ = (selector) => document.querySelector(selector);
const elements = {
  form: $("#chatForm"), input: $("#messageInput"), messages: $("#messages"),
  send: $("#sendButton"), apiUrl: $("#apiUrl"), prompt: $("#characterPrompt"),
  importance: $("#importance"), importanceValue: $("#importanceValue"),
  memoryList: $("#memoryList"), memoryPanel: $("#memoryPanel"),
  statusDot: $("#statusDot"), connectionText: $("#connectionText"), toast: $("#toast")
};

const storedApiUrl = localStorage.getItem("luna_api_url");
if (storedApiUrl) elements.apiUrl.value = storedApiUrl;
let conversationId = crypto.randomUUID();
const userId = localStorage.getItem("luna_user_id") || crypto.randomUUID();
localStorage.setItem("luna_user_id", userId);

function apiBase() { return elements.apiUrl.value.trim().replace(/\/$/, ""); }
function now() { return new Intl.DateTimeFormat("ko", { hour: "numeric", minute: "2-digit" }).format(new Date()); }
function showToast(text) { elements.toast.textContent = text; elements.toast.classList.add("show"); setTimeout(() => elements.toast.classList.remove("show"), 2200); }

function addMessage(role, text) {
  const article = document.createElement("article");
  article.className = `message ${role}`;
  const avatar = role === "assistant" ? '<div class="mini-avatar">L</div>' : "";
  article.innerHTML = `${avatar}<div class="bubble"><p></p><time>${now()}</time></div>`;
  article.querySelector("p").textContent = text;
  elements.messages.append(article);
  elements.messages.scrollTop = elements.messages.scrollHeight;
  return article;
}

function addLoading() {
  const article = document.createElement("article");
  article.className = "message assistant loading";
  article.innerHTML = '<div class="mini-avatar">L</div><div class="bubble"><i></i><i></i><i></i></div>';
  elements.messages.append(article);
  elements.messages.scrollTop = elements.messages.scrollHeight;
  return article;
}

function renderMemories(memories) {
  if (!memories.length) {
    elements.memoryList.innerHTML = '<div class="empty-memory"><div>✦</div><p>관련된 과거 기억이 없어요</p><span>대화가 쌓이면 루나가 이곳에서 기억을 불러옵니다.</span></div>';
    return;
  }
  elements.memoryList.replaceChildren(...memories.map((memory) => {
    const card = document.createElement("article");
    card.className = "memory-card";
    const percent = Math.round(memory.score * 100);
    card.innerHTML = `<p></p><div class="score-row"><span>종합 점수</span><div class="score-bar"><div class="score-fill" style="width:${Math.min(100, percent)}%"></div></div><strong>${percent}</strong></div><div class="signals"><span>유사도 ${Math.round(memory.similarity * 100)}</span><span>중요도 ${Math.round(memory.importance * 100)}</span><span>최근성 ${Math.round(memory.recency * 100)}</span></div>`;
    card.querySelector("p").textContent = memory.content;
    return card;
  }));
}

async function checkConnection() {
  localStorage.setItem("luna_api_url", apiBase());
  elements.connectionText.textContent = "연결 확인 중…";
  try {
    const response = await fetch(`${apiBase()}/health`);
    if (!response.ok) throw new Error();
    elements.statusDot.className = "status-dot ok";
    elements.connectionText.textContent = "백엔드에 연결됨";
    showToast("API 연결을 확인했습니다");
  } catch {
    elements.statusDot.className = "status-dot bad";
    elements.connectionText.textContent = "백엔드에 연결할 수 없음";
    showToast("API 주소와 CORS 설정을 확인해 주세요");
  }
}

elements.form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = elements.input.value.trim();
  if (!message || elements.send.disabled) return;
  addMessage("user", message);
  elements.input.value = "";
  elements.input.style.height = "auto";
  elements.send.disabled = true;
  const loading = addLoading();
  try {
    const response = await fetch(`${apiBase()}/chat`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, conversation_id: conversationId, message,
        character_prompt: elements.prompt.value.trim(), importance: Number(elements.importance.value) })
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || `요청 실패 (${response.status})`);
    loading.remove();
    addMessage("assistant", data.answer);
    renderMemories(data.recalled_memories || []);
  } catch (error) {
    loading.remove();
    addMessage("assistant", `연결 중 문제가 생겼어. ${error.message}`);
  } finally { elements.send.disabled = false; elements.input.focus(); }
});

elements.input.addEventListener("keydown", (event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); elements.form.requestSubmit(); } });
elements.input.addEventListener("input", () => { elements.input.style.height = "auto"; elements.input.style.height = `${elements.input.scrollHeight}px`; });
elements.importance.addEventListener("input", () => elements.importanceValue.textContent = Number(elements.importance.value).toFixed(1));
$("#saveSettings").addEventListener("click", checkConnection);
$("#memoryToggle").addEventListener("click", () => elements.memoryPanel.classList.add("open"));
$("#closeMemory").addEventListener("click", () => elements.memoryPanel.classList.remove("open"));
$("#newChat").addEventListener("click", () => { conversationId = crypto.randomUUID(); document.querySelectorAll(".message").forEach((node) => node.remove()); addMessage("assistant", "새로운 이야기를 시작해 볼까? 이번에도 잘 기억해 둘게."); renderMemories([]); });

checkConnection();
