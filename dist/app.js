const $ = (selector) => document.querySelector(selector);
const elements = {
  form: $("#chatForm"), input: $("#messageInput"), messages: $("#messages"),
  send: $("#sendButton"), apiUrl: $("#apiUrl"), prompt: $("#characterPrompt"),
  importance: $("#importance"), importanceValue: $("#importanceValue"),
  memoryList: $("#memoryList"), memoryPanel: $("#memoryPanel"),
  statusDot: $("#statusDot"), connectionText: $("#connectionText"), toast: $("#toast")
};

const storedApiUrl = localStorage.getItem("luna_api_url");
if (storedApiUrl && !storedApiUrl.includes("luna-memory-api.onrender.com")) elements.apiUrl.value = storedApiUrl;
let conversationId = crypto.randomUUID();
const userIdKey = "luna_user_id_v2";
const userId = localStorage.getItem(userIdKey) || crypto.randomUUID();
localStorage.setItem(userIdKey, userId);
const evaluationItems = [["memory_recall","기억을 잘했나"],["natural_use","기억을 자연스럽게 썼나"],["no_false_memory","틀린 기억을 말하지 않았나"],["character_consistency","캐릭터 말투/성격이 유지됐나"],["relationship_continuity","진짜 관계가 이어지는 느낌이 났나"]];
const evaluationDialog = $("#evaluationDialog");
$("#evaluationFields").innerHTML = evaluationItems.map(([key,label]) => `<label>${label}<select name="${key}" required><option value="">점수 선택</option>${[1,2,3,4,5].map(n=>`<option value="${n}">${n}점</option>`).join("")}</select></label>`).join("");
$("#evaluateButton").addEventListener("click", () => evaluationDialog.showModal());
$("#cancelEvaluation").addEventListener("click", () => evaluationDialog.close());
$("#evaluationForm").addEventListener("submit", async (event) => { event.preventDefault(); const form = new FormData(event.currentTarget); const payload = {conversation_id: conversationId, user_id: userId, note: form.get("note") || $("#evaluationNote").value}; evaluationItems.forEach(([key]) => payload[key] = Number(form.get(key))); try { const res = await fetch(`${apiBase()}/evaluations`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)}); if(!res.ok) throw new Error(); evaluationDialog.close(); event.currentTarget.reset(); showToast("세션 평가를 저장했습니다"); } catch { showToast("평가 저장에 실패했습니다"); }});

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
