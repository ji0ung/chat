const $ = (selector) => document.querySelector(selector);
const elements = {
  form: $("#chatForm"), input: $("#messageInput"), messages: $("#messages"),
  send: $("#sendButton"), accessToken: $("#accessToken"), accessGate: $("#accessGate"),
  accessForm: $("#accessForm"), accessError: $("#accessError"), prompt: $("#characterPrompt"),
  importance: $("#importance"), importanceValue: $("#importanceValue"),
  memoryList: $("#memoryList"), memoryPanel: $("#memoryPanel"),
  statusDot: $("#statusDot"), connectionText: $("#connectionText"), toast: $("#toast")
};

const DEFAULT_API_BASE = "https://chat-7bf4.onrender.com";
let accessGranted = false;
elements.accessToken.value = sessionStorage.getItem("luna_access_token") || "";
let conversationId = crypto.randomUUID();
const userIdKey = "luna_user_id_v2";
const userId = localStorage.getItem(userIdKey) || crypto.randomUUID();
localStorage.setItem(userIdKey, userId);

const evaluationItems = [["memory_recall","기억을 잘했나"],["natural_use","기억을 자연스럽게 썼나"],["no_false_memory","틀린 기억을 말하지 않았나"],["character_consistency","캐릭터 말투/성격이 유지됐나"],["relationship_continuity","진짜 관계가 이어지는 느낌이 났나"]];
const evaluationDialog = $("#evaluationDialog");
$("#evaluationFields").innerHTML = evaluationItems.map(([key,label]) => `<label>${label}<select name="${key}" required><option value="">점수 선택</option>${[1,2,3,4,5].map(n=>`<option value="${n}">${n}점</option>`).join("")}</select></label>`).join("");

function apiBase() {
  return (localStorage.getItem("luna_api_url") || DEFAULT_API_BASE).replace(/\/$/, "");
}
function authHeaders() {
  const token = elements.accessToken.value.trim();
  return token ? { "Authorization": `Bearer ${token}` } : {};
}
function now() { return new Intl.DateTimeFormat("ko", { hour: "numeric", minute: "2-digit" }).format(new Date()); }
function showToast(text) { elements.toast.textContent = text; elements.toast.classList.add("show"); setTimeout(() => elements.toast.classList.remove("show"), 2200); }

async function responseError(response) {
  const data = await response.json().catch(() => ({}));
  if (typeof data.detail === "string") return data.detail;
  if (data.detail && typeof data.detail.message === "string") return data.detail.message;
  return `요청 실패 (${response.status})`;
}

function setAccessState(granted, message = "") {
  accessGranted = granted;
  elements.accessGate.classList.toggle("hidden", granted);
  elements.statusDot.className = granted ? "status-dot ok" : "status-dot";
  elements.connectionText.textContent = granted ? "테스트 접근 인증됨" : "액세스 코드가 필요합니다";
  elements.send.disabled = !granted;
  elements.input.disabled = !granted;
  $("#evaluateButton").disabled = !granted;
  $("#newChat").disabled = !granted;
  if (!granted && message) elements.accessError.textContent = message;
}

async function validateAccess() {
  const token = elements.accessToken.value.trim();
  if (!token) {
    setAccessState(false, "액세스 코드를 입력해주세요.");
    return false;
  }
  elements.accessError.textContent = "확인 중…";
  $("#accessButton").disabled = true;
  try {
    const response = await fetch(`${apiBase()}/auth/validate`, { headers: authHeaders() });
    if (!response.ok) throw new Error(await responseError(response));
    sessionStorage.setItem("luna_access_token", token);
    elements.accessError.textContent = "";
    setAccessState(true);
    showToast("테스트 접근이 인증됐습니다");
    elements.input.focus();
    return true;
  } catch (error) {
    sessionStorage.removeItem("luna_access_token");
    setAccessState(false, error.message || "액세스 코드를 확인해주세요.");
    return false;
  } finally {
    $("#accessButton").disabled = false;
  }
}

function requireAccess() {
  if (accessGranted) return true;
  setAccessState(false, "먼저 테스트 액세스 코드를 인증해주세요.");
  elements.accessToken.focus();
  return false;
}

$("#cancelEvaluation").addEventListener("click", () => evaluationDialog.close());
$("#evaluateButton").addEventListener("click", () => { if (requireAccess()) evaluationDialog.showModal(); });
elements.accessForm.addEventListener("submit", async (event) => { event.preventDefault(); await validateAccess(); });

$("#evaluationForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!requireAccess()) return;
  const form = new FormData(event.currentTarget);
  const payload = {conversation_id: conversationId, user_id: userId, note: form.get("note") || $("#evaluationNote").value};
  evaluationItems.forEach(([key]) => payload[key] = Number(form.get(key)));
  try {
    const res = await fetch(`${apiBase()}/evaluations`, {
      method:"POST",
      headers:{"Content-Type":"application/json", ...authHeaders()},
      body:JSON.stringify(payload)
    });
    if(!res.ok) throw new Error(await responseError(res));
    evaluationDialog.close();
    event.currentTarget.reset();
    showToast("세션 평가를 저장했습니다");
  } catch (error) {
    if (error.message.includes("로그인") || error.message.includes("권한")) setAccessState(false, error.message);
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
  if (!requireAccess()) return;
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
    if (!response.ok) throw new Error(await responseError(response));
    const data = await response.json();
    loading.remove();
    addMessage("assistant", data.answer);
    renderMemories(data.recalled_memories || []);
  } catch (error) {
    loading.remove();
    if (error.message.includes("로그인") || error.message.includes("권한")) setAccessState(false, error.message);
    else addMessage("assistant", error.message || "답변을 만드는 중 문제가 발생했어. 다시 시도해줘.");
  } finally {
    elements.send.disabled = !accessGranted;
    if (accessGranted) elements.input.focus();
  }
});

elements.input.addEventListener("keydown", (event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); elements.form.requestSubmit(); } });
elements.input.addEventListener("input", () => { elements.input.style.height = "auto"; elements.input.style.height = `${elements.input.scrollHeight}px`; });
elements.importance.addEventListener("input", () => elements.importanceValue.textContent = Number(elements.importance.value).toFixed(1));
$("#memoryToggle").addEventListener("click", () => { if (requireAccess()) elements.memoryPanel.classList.add("open"); });
$("#closeMemory").addEventListener("click", () => elements.memoryPanel.classList.remove("open"));
$("#newChat").addEventListener("click", () => {
  if (!requireAccess()) return;
  conversationId = crypto.randomUUID();
  document.querySelectorAll(".message").forEach((node) => node.remove());
  addMessage("assistant", "새로운 이야기를 시작해 볼까? 이번에도 잘 기억해 둘게.");
  renderMemories([]);
});

setAccessState(false);
if (elements.accessToken.value.trim()) validateAccess();
