const $ = (selector) => document.querySelector(selector);
const DEFAULT_API_URL = "https://chat-7bf4.onrender.com";
const elements = {
  form: $("#chatForm"), input: $("#messageInput"), messages: $("#messages"),
  send: $("#sendButton"), prompt: $("#characterPrompt"),
  importance: $("#importance"), importanceValue: $("#importanceValue"),
  memoryList: $("#memoryList"), memoryPanel: $("#memoryPanel"),
  statusDot: $("#statusDot"), connectionText: $("#connectionText"), toast: $("#toast"),
  accessGate: $("#accessGate"), accessToken: $("#accessToken"), unlock: $("#unlockButton"),
  accessError: $("#accessError"), chatControls: $("#chatControls")
};

let conversationId = crypto.randomUUID();
const userIdKey = "luna_user_id_v2";
const userId = localStorage.getItem(userIdKey) || crypto.randomUUID();
localStorage.setItem(userIdKey, userId);

function apiBase() {
  return (localStorage.getItem("luna_api_url") || DEFAULT_API_URL).replace(/\/$/, "");
}
function authHeaders() {
  const token = sessionStorage.getItem("luna_access_token") || "";
  return token ? { Authorization: `Bearer ${token}` } : {};
}
function now() { return new Intl.DateTimeFormat("ko", { hour: "numeric", minute: "2-digit" }).format(new Date()); }
function showToast(text) { elements.toast.textContent = text; elements.toast.classList.add("show"); setTimeout(() => elements.toast.classList.remove("show"), 2200); }

async function responseError(response) {
  const data = await response.json().catch(() => ({}));
  if (typeof data.detail === "string") return data.detail;
  if (data.detail && typeof data.detail.message === "string") return data.detail.message;
  return `요청 실패 (${response.status})`;
}

function setLocked(message = "") {
  sessionStorage.removeItem("luna_access_token");
  elements.chatControls.hidden = true;
  elements.accessGate.hidden = false;
  elements.statusDot.className = "status-dot";
  elements.connectionText.textContent = "테스트 액세스 코드가 필요합니다";
  elements.accessError.textContent = message;
  elements.accessToken.focus();
}

function setUnlocked() {
  elements.accessGate.hidden = true;
  elements.chatControls.hidden = false;
  elements.statusDot.className = "status-dot ok";
  elements.connectionText.textContent = "테스트 사용자 인증됨";
  elements.accessError.textContent = "";
  elements.input.focus();
}

async function verifyAccessCode(code, { quiet = false } = {}) {
  const token = (code || "").trim();
  if (!token) {
    if (!quiet) setLocked("테스트 액세스 코드를 입력해주세요.");
    return false;
  }
  try {
    const response = await fetch(`${apiBase()}/auth/validate`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!response.ok) throw new Error(await responseError(response));
    sessionStorage.setItem("luna_access_token", token);
    setUnlocked();
    if (!quiet) showToast("테스트 액세스 코드가 확인됐습니다");
    return true;
  } catch (error) {
    setLocked(error.message || "유효하지 않은 테스트 액세스 코드예요.");
    return false;
  }
}

elements.unlock.addEventListener("click", () => verifyAccessCode(elements.accessToken.value));
elements.accessToken.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    verifyAccessCode(elements.accessToken.value);
  }
});

const evaluationItems = [["memory_recall","기억을 잘했나"],["natural_use","기억을 자연스럽게 썼나"],["no_false_memory","틀린 기억을 말하지 않았나"],["character_consistency","캐릭터 말투/성격이 유지됐나"],["relationship_continuity","진짜 관계가 이어지는 느낌이 났나"]];
const evaluationDialog = $("#evaluationDialog");
$("#evaluationFields").innerHTML = evaluationItems.map(([key,label]) => `<label>${label}<select name="${key}" required><option value="">점수 선택</option>${[1,2,3,4,5].map(n=>`<option value="${n}">${n}점</option>`).join("")}</select></label>`).join("");
$("#evaluateButton").addEventListener("click", () => evaluationDialog.showModal());
$("#cancelEvaluation").addEventListener("click", () => evaluationDialog.close());
$("#evaluationForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const payload = {conversation_id: conversationId, user_id: userId, note: form.get("note") || $("#evaluationNote").value};
  evaluationItems.forEach(([key]) => payload[key] = Number(form.get(key)));
  try {
    const res = await fetch(`${apiBase()}/evaluations`, {
      method:"POST",
      headers:{"Content-Type":"application/json", ...authHeaders()},
      body:JSON.stringify(payload)
    });
    if(!res.ok) {
      if (res.status === 401) setLocked("액세스 코드가 만료되었거나 유효하지 않습니다.");
      throw new Error(await responseError(res));
    }
    evaluationDialog.close();
    event.currentTarget.reset();
    showToast("세션 평가를 저장했습니다");
  } catch (error) {
    showToast(error.message || "평가 저장에 실패했습니다");
  }
});

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

elements.form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (elements.chatControls.hidden) return;
  const message = elements.input.value.trim();
  if (!message || elements.send.disabled) return;
  if (message.length > 4000) {
    showToast("메시지가 너무 길어요. 4,000자 이하로 줄여주세요.");
    return;
  }

  addMessage("user", message);
  elements.input.value = "";
  elements.input.style.height = "auto";
  elements.send.disabled = true;
  const loading = addLoading();
  const requestId = crypto.randomUUID();

  try {
    const response = await fetch(`${apiBase()}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Request-ID": requestId,
        "Idempotency-Key": requestId,
        ...authHeaders()
      },
      body: JSON.stringify({
        user_id: userId,
        conversation_id: conversationId,
        message,
        character_prompt: elements.prompt.value.trim(),
        importance: Number(elements.importance.value)
      })
    });
    if (!response.ok) {
      if (response.status === 401) setLocked("액세스 코드가 만료되었거나 유효하지 않습니다.");
      throw new Error(await responseError(response));
    }
    const data = await response.json();
    loading.remove();
    addMessage("assistant", data.answer);
    renderMemories(data.recalled_memories || []);
  } catch (error) {
    loading.remove();
    addMessage("assistant", error.message || "답변을 만드는 중 문제가 발생했어. 다시 시도해줘.");
  } finally {
    elements.send.disabled = false;
    if (!elements.chatControls.hidden) elements.input.focus();
  }
});

elements.input.addEventListener("keydown", (event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); elements.form.requestSubmit(); } });
elements.input.addEventListener("input", () => { elements.input.style.height = "auto"; elements.input.style.height = `${elements.input.scrollHeight}px`; });
elements.importance.addEventListener("input", () => elements.importanceValue.textContent = Number(elements.importance.value).toFixed(1));
$("#memoryToggle").addEventListener("click", () => elements.memoryPanel.classList.add("open"));
$("#closeMemory").addEventListener("click", () => elements.memoryPanel.classList.remove("open"));
$("#newChat").addEventListener("click", () => {
  conversationId = crypto.randomUUID();
  document.querySelectorAll(".message").forEach((node) => node.remove());
  addMessage("assistant", "새로운 이야기를 시작해 볼까? 이번에도 잘 기억해 둘게.");
  renderMemories([]);
});

const savedToken = sessionStorage.getItem("luna_access_token");
if (savedToken) {
  elements.accessToken.value = savedToken;
  verifyAccessCode(savedToken, { quiet: true });
} else {
  setLocked();
}
