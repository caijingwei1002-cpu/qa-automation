const state = {
  dashboard: null,
  codex: null,
  session: null,
  eventSource: null,
  eventCursor: 0,
  eventGeneration: 0,
  running: false,
  activeTurnId: null,
  renderedItems: new Map(),
  pendingUserMessage: null,
  files: [],
  currentFile: null,
  savedContent: "",
  dirty: false,
  stage: "preflight",
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
let stageOrder = [];
let stagePrompts = {};

function renderLearningSteps(session) {
  stageOrder = session.workflow.map((step) => step.id);
  stagePrompts = Object.fromEntries(session.workflow.map((step) => [step.id, step.prompt]));
  const rail = $(".learning-path");
  rail.replaceChildren();
  session.workflow.forEach((step, index) => {
    const button = document.createElement("button");
    button.className = "learning-step";
    button.dataset.stage = step.id;
    const number = document.createElement("span"); number.textContent = index + 1;
    const body = document.createElement("div");
    const title = document.createElement("strong"); title.textContent = step.title;
    const detail = document.createElement("small"); detail.textContent = step.deliverable;
    body.append(title, detail);
    button.append(number, body, document.createElement("i"));
    button.addEventListener("click", () => setStage(step.id, true));
    rail.append(button);
  });
  setStage(session.current_stage || stageOrder.at(-1), false);
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  let data;
  try { data = await response.json(); } catch { data = { error: `HTTP ${response.status}` }; }
  if (!response.ok) throw new Error(data.error || `请求失败：${response.status}`);
  return data;
}

function setText(selector, value = "") { $(selector).textContent = value ?? ""; }
function toast(message, error = false) {
  const node = $("#toast");
  node.textContent = message;
  node.className = `toast show${error ? " error" : ""}`;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => { node.className = "toast"; }, 3200);
}
function scrollChat() { requestAnimationFrame(() => { $("#chat-scroll").scrollTop = $("#chat-scroll").scrollHeight; }); }
function normalized(value) { return value.replace(/\r\n/g, "\n").replace(/\r/g, "\n"); }

async function loadDashboard() {
  state.dashboard = await api("/api/dashboard");
  const { progress, plan, active_phase: phase, workspace } = state.dashboard;
  setText("#day-number", progress.current_day);
  setText("#phase-day", `阶段 ${plan.phase_day} / ${plan.phase_total_days}`);
  setText("#plan-title", plan.title || plan.theme);
  setText("#plan-learn", plan.learn);
  setText("#phase-name", phase?.name || "LEARNING SESSION");
  setText("#phase-meta", phase ? `${phase.completed} / ${phase.total} 天` : "");
  $("#phase-progress").style.width = `${phase?.percent || 0}%`;
  setText("#overall-progress-text", progress.scope_label || `${progress.completed} / ${progress.core_days} 天`);
  setText("#deliverable", plan.deliverable || plan.task);
  setText("#done-standard", `完成标准：${plan.done}`);
  const minutes = Object.values(plan.timebox || {}).reduce((sum, value) => sum + Number(value || 0), 0);
  setText("#timebox-badge", `${minutes} min`);
  setText("#change-status", workspace.changes.length ? `${workspace.changes.length} 个当前项目改动` : "尚无当前项目改动");
  setText("#evidence-status", workspace.evidence.length ? `${workspace.evidence.length} 份运行证据` : "今天尚未生成证据");
  setText("#log-status", workspace.log_exists ? workspace.log_path : "今天尚未生成学习日志");
  setText("#target-file-name", (plan.file || "目标文件").split("/").at(-1));
  setText("#run-command-short", plan.run);
  renderRoadmap(state.dashboard.phases);
  renderLearningSteps(state.dashboard.learning_session);
}

function setStage(stage, fillPrompt = false) {
  state.stage = stage;
  $$(".learning-step").forEach((node) => {
    node.classList.toggle("active", node.dataset.stage === stage);
    node.classList.toggle("complete", state.dashboard?.learning_session.stages[node.dataset.stage]?.status === "done");
  });
  if (fillPrompt) {
    $("#message-input").value = stagePrompts[stage];
    resizeComposer();
    updateSendState();
    $("#message-input").focus();
  }
}

function renderRoadmap(phases) {
  const target = $("#roadmap-grid");
  target.replaceChildren();
  phases.forEach((phase, index) => {
    const card = document.createElement("article");
    card.className = `roadmap-phase${phase.active ? " active" : ""}`;
    const num = document.createElement("span"); num.textContent = String(index + 1).padStart(2, "0");
    const title = document.createElement("h3"); title.textContent = phase.name;
    const objective = document.createElement("p"); objective.textContent = phase.objective;
    const meta = document.createElement("small"); meta.textContent = `${phase.completed} / ${phase.total} 天 · ${phase.percent}%`;
    card.append(num, title, objective, meta); target.append(card);
  });
}

function updateConnection(status, label, account = "Codex App Server") {
  const dot = $("#connection-dot");
  dot.className = `connection-dot${status === "online" ? " online" : status === "error" ? " error" : ""}`;
  setText("#connection-label", label);
  setText("#account-label", account);
}

function showSetup(title, message, options = {}) {
  $("#setup-overlay").classList.remove("hidden");
  setText("#setup-title", title); setText("#setup-message", message);
  $("#login-button").classList.toggle("hidden", !options.login);
  $("#setup-retry").classList.toggle("hidden", Boolean(options.hideRetry));
  const detail = $("#setup-detail");
  detail.classList.toggle("hidden", !options.detail); detail.textContent = options.detail || "";
}
function hideSetup() { $("#setup-overlay").classList.add("hidden"); }

async function connectCodex() {
  updateConnection("pending", "正在连接");
  showSetup("正在连接你的 Codex", "工作台正在本机启动 Codex App Server，并读取登录状态。", { hideRetry: true });
  try {
    state.codex = await api("/api/chat/connect", { method: "POST", body: "{}" });
    const account = state.codex.account;
    if (!account && state.codex.requires_openai_auth) {
      updateConnection("error", "需要登录");
      showSetup("连接完成，还需要登录", "使用你的 ChatGPT 账户登录后，学习会话才能开始。", { login: true });
      return;
    }
    const accountLabel = account ? `${account.email || account.type || account.authMode || "ChatGPT"}${account.planType ? ` · ${account.planType}` : ""}` : "Codex 已连接";
    updateConnection("online", "Codex 已连接", accountLabel);
    openEventStream();
    hideSetup();
    $("#start-session-button").disabled = false;
  } catch (error) {
    updateConnection("error", "连接失败");
    showSetup("无法启动 Codex App Server", error.message, { detail: "请确认 Codex CLI 可以在普通 PowerShell 中运行：\n\ncodex app-server --help\n\n如使用自定义位置，请在启动前设置 CODEX_EXE。" });
  }
}

async function loginWithChatGPT() {
  try {
    const result = await api("/api/chat/login", { method: "POST", body: "{}" });
    if (result.authUrl) window.open(result.authUrl, "_blank", "noopener");
    showSetup("请在浏览器中完成登录", "登录成功后，这个页面会自动继续。", { hideRetry: true });
    const started = Date.now();
    const poll = setInterval(async () => {
      try {
        const status = await api("/api/chat/status");
        if (status.account) { clearInterval(poll); state.codex = status; await connectCodex(); }
        else if (Date.now() - started > 120000) { clearInterval(poll); showSetup("登录等待超时", "完成登录后可以点击重试连接。", {}); }
      } catch { /* keep polling during redirect */ }
    }, 1800);
  } catch (error) { toast(error.message, true); }
}

function openEventStream() {
  if (state.eventSource) state.eventSource.close();
  state.eventCursor = Number(state.codex?.event_seq || 0);
  const generation = ++state.eventGeneration;
  pollEventStream(generation);
}

async function pollEventStream(generation) {
  while (generation === state.eventGeneration) {
    try {
      const batch = await api(`/api/chat/events/poll?after=${state.eventCursor}`);
      for (const event of batch.events || []) {
        if (Number(event.seq || 0) <= state.eventCursor) continue;
        state.eventCursor = Number(event.seq);
        handleCodexEvent(event);
      }
      state.eventCursor = Math.max(state.eventCursor, Number(batch.cursor || 0));
    } catch (error) {
      if (generation !== state.eventGeneration) return;
      updateConnection("error", "事件流重连中");
      await new Promise((resolve) => setTimeout(resolve, 900));
    }
  }
}

async function startSession() {
  if (!state.codex?.initialized) { await connectCodex(); if (!state.codex?.initialized) return; }
  $("#start-session-button").disabled = true;
  try {
    const session = await api("/api/chat/session", { method: "POST", body: "{}" });
    state.session = session;
    $("#session-intro").classList.add("hidden");
    renderThreadHistory(session.thread);
    enableComposer(true);
    if (session.active_turn_id) setRunning(true, session.active_turn_id);
    scrollChat();
  } catch (error) {
    $("#start-session-button").disabled = false;
    appendNotice(error.message, true); toast(error.message, true);
  }
}

function renderThreadHistory(thread) {
  if (!thread) return;
  const turns = thread.turns || thread.items || [];
  for (const turn of Array.isArray(turns) ? turns : []) {
    const items = turn.items || (turn.type ? [turn] : []);
    for (const item of items) renderItem(item, true);
  }
}

function textFrom(value) {
  if (typeof value === "string") return value;
  if (Array.isArray(value)) return value.map(textFrom).filter(Boolean).join("\n");
  if (!value || typeof value !== "object") return "";
  if (typeof value.text === "string") return value.text;
  if (typeof value.output_text === "string") return value.output_text;
  return textFrom(value.content || value.message || value.summary || "");
}

function messageNode(role, text, id) {
  const node = document.createElement("article");
  node.className = `message ${role}`; if (id) node.dataset.itemId = id;
  const avatar = document.createElement("span"); avatar.className = "avatar"; avatar.textContent = role === "user" ? "你" : "C";
  const body = document.createElement("div"); body.className = "message-body";
  const meta = document.createElement("div"); meta.className = "message-meta";
  const name = document.createElement("strong"); name.textContent = role === "user" ? "你" : "Codex 教练";
  const time = document.createElement("span"); time.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  const content = document.createElement("div"); content.className = "message-text"; content.textContent = text;
  meta.append(name, time); body.append(meta, content); node.append(avatar, body);
  return node;
}

function upsertMessage(role, text, id) {
  if (!text && !id) return;
  let node = id ? state.renderedItems.get(id) : null;
  if (!node) {
    node = messageNode(role, text, id);
    $("#messages").append(node);
    if (id) state.renderedItems.set(id, node);
  } else {
    node.querySelector(".message-text").textContent = text;
  }
  $("#session-intro").classList.add("hidden"); scrollChat();
}

function reconcilePendingUserMessage(text, serverId) {
  const pending = state.pendingUserMessage;
  if (!pending || normalized(pending.text).trim() !== normalized(text).trim()) return false;
  const node = state.renderedItems.get(pending.id);
  state.renderedItems.delete(pending.id);
  state.pendingUserMessage = null;
  if (!node) return false;
  node.dataset.itemId = serverId;
  node.querySelector(".message-text").textContent = text;
  state.renderedItems.set(serverId, node);
  return true;
}

function discardPendingUserMessage() {
  const pending = state.pendingUserMessage;
  if (!pending) return;
  state.renderedItems.get(pending.id)?.remove();
  state.renderedItems.delete(pending.id);
  state.pendingUserMessage = null;
}

function renderItem(item, fromHistory = false) {
  if (!item || typeof item !== "object") return;
  const id = String(item.id || `item-${Date.now()}-${Math.random()}`);
  const type = item.type || "";
  if (type === "userMessage" || type === "user_message") {
    const text = textFrom(item.content || item);
    if (!reconcilePendingUserMessage(text, id)) upsertMessage("user", text, id);
    return;
  }
  if (type === "agentMessage" || type === "assistantMessage" || type === "assistant_message") { upsertMessage("assistant", textFrom(item.text || item.content || item), id); return; }
  if (type === "commandExecution" || type === "fileChange" || type === "mcpToolCall" || type === "dynamicToolCall" || type === "webSearch") renderTool(item, id, fromHistory);
}

function renderTool(item, id) {
  const existing = state.renderedItems.get(id); if (existing) existing.remove();
  const card = document.createElement("article"); card.className = "tool-card"; card.dataset.itemId = id;
  const head = document.createElement("div"); head.className = "tool-head";
  const icon = document.createElement("span"); icon.textContent = item.type === "fileChange" ? "Δ" : item.type === "commandExecution" ? ">_" : "◇";
  const title = document.createElement("strong"); title.textContent = ({ commandExecution: "执行命令", fileChange: "修改文件", mcpToolCall: "调用工具", dynamicToolCall: "调用工具", webSearch: "网页搜索" })[item.type] || item.type;
  const status = document.createElement("em"); status.textContent = item.status || "进行中"; head.append(icon, title, status); card.append(head);
  const detail = document.createElement("code"); detail.textContent = item.command || item.query || item.tool || textFrom(item.changes) || ""; card.append(detail);
  if (item.aggregatedOutput) { const output = document.createElement("pre"); output.className = "tool-output"; output.textContent = item.aggregatedOutput; card.append(output); }
  $("#messages").append(card); state.renderedItems.set(id, card); scrollChat();
}

function appendNotice(text, error = false) {
  const node = document.createElement("div"); node.className = `notice-card${error ? " error" : ""}`; node.textContent = text;
  $("#messages").append(node); scrollChat(); return node;
}

function renderPlan(plan) {
  const old = $("#messages .plan-card"); if (old) old.remove();
  const card = document.createElement("article"); card.className = "plan-card";
  const title = document.createElement("strong"); title.textContent = "Codex 的行动计划";
  const list = document.createElement("ol");
  for (const entry of plan || []) { const item = document.createElement("li"); item.textContent = `${entry.step}${entry.status ? ` · ${entry.status}` : ""}`; list.append(item); }
  card.append(title, list); $("#messages").append(card); scrollChat();
}

function renderApproval(method, params) {
  const requestId = Number(params.requestId);
  if ($(`[data-approval-id="${requestId}"]`)) return;
  const card = document.createElement("article"); card.className = "approval-card"; card.dataset.approvalId = requestId;
  const title = document.createElement("h4"); title.textContent = method.includes("fileChange") ? "Codex 想修改文件" : "Codex 想执行命令";
  const detail = document.createElement("p"); detail.textContent = params.reason || params.command || params.cwd || "请确认是否允许这次操作。";
  const actions = document.createElement("div"); actions.className = "approval-actions";
  [["accept", "允许一次", true], ["acceptForSession", "本次会话允许", false], ["decline", "拒绝", false]].forEach(([decision, label, primary]) => {
    const button = document.createElement("button"); button.textContent = label; if (primary) button.classList.add("accept");
    button.addEventListener("click", () => resolveApproval(requestId, decision, card)); actions.append(button);
  });
  card.append(title, detail, actions); $("#messages").append(card); scrollChat();
}

async function resolveApproval(requestId, decision, card) {
  card.querySelectorAll("button").forEach((button) => { button.disabled = true; });
  try {
    await api("/api/chat/approval", { method: "POST", body: JSON.stringify({ request_id: requestId, decision }) });
    card.querySelector("p").textContent = decision.startsWith("accept") ? "已允许，Codex 正在继续。" : "已拒绝这次操作。";
    card.querySelector(".approval-actions").remove();
  } catch (error) { toast(error.message, true); card.querySelectorAll("button").forEach((button) => { button.disabled = false; }); }
}

function handleCodexEvent(event) {
  const { method, params = {} } = event;
  if (method === "bridge/status" || method === "bridge/ready") {
    if (params.running || params.initialized) updateConnection("online", "Codex 已连接");
    return;
  }
  if (method === "bridge/disconnected") { updateConnection("error", "连接已断开"); appendNotice(params.error || "Codex 连接已断开", true); return; }
  if (method === "turn/started") { setRunning(true, params.turn?.id); return; }
  if (method === "turn/completed") {
    state.pendingUserMessage = null; setRunning(false); const turn = params.turn || {};
    if (turn.status === "failed") appendNotice(turn.error?.message || "Codex 回合执行失败", true);
    refreshContext().catch(() => {}); return;
  }
  if (method === "item/started" || method === "item/completed") { renderItem(params.item); return; }
  if (method === "item/agentMessage/delta") {
    const id = String(params.itemId || params.id || "streaming-agent");
    const existing = state.renderedItems.get(id); const current = existing?.querySelector(".message-text")?.textContent || "";
    upsertMessage("assistant", current + String(params.delta || params.text || ""), id); return;
  }
  if (method === "item/commandExecution/outputDelta") {
    const id = String(params.itemId || params.id || ""); const card = state.renderedItems.get(id);
    if (card) { let output = card.querySelector(".tool-output"); if (!output) { output = document.createElement("pre"); output.className = "tool-output"; card.append(output); } output.textContent += String(params.delta || ""); }
    return;
  }
  if (method === "turn/plan/updated") { renderPlan(params.plan); return; }
  if (method === "item/commandExecution/requestApproval" || method === "item/fileChange/requestApproval" || method === "item/permissions/requestApproval") { renderApproval(method, params); return; }
  if (method === "warning" || method === "configWarning") appendNotice(params.message || params.summary || "Codex 警告");
  if (method === "error") appendNotice(params.error?.message || "Codex 运行出错", true);
  if (method === "account/updated" && params.authMode) { updateConnection("online", "Codex 已连接", params.planType ? `ChatGPT · ${params.planType}` : params.authMode); hideSetup(); }
}

function setRunning(running, turnId = null) {
  state.running = running; state.activeTurnId = running ? (turnId || state.activeTurnId) : null;
  $("#typing").classList.toggle("hidden", !running); $("#stop-button").classList.toggle("hidden", !running);
  $("#send-button").classList.toggle("hidden", running); updateSendState(); scrollChat();
}
function enableComposer(enabled) { $("#message-input").disabled = !enabled; updateSendState(); }
function updateSendState() { $("#send-button").disabled = !state.session || state.running || !$("#message-input").value.trim(); }
function resizeComposer() { const input = $("#message-input"); input.style.height = "auto"; input.style.height = `${Math.min(120, input.scrollHeight)}px`; }

async function sendMessage() {
  const input = $("#message-input"); const text = input.value.trim();
  if (!text || !state.session || state.running) return;
  const localId = `local-${Date.now()}`;
  state.pendingUserMessage = { id: localId, text };
  upsertMessage("user", text, localId); input.value = ""; resizeComposer(); setRunning(true);
  try {
    const result = await api("/api/chat/message", { method: "POST", body: JSON.stringify({ thread_id: state.session.thread_id, text }) });
    if (result.turn?.id) state.activeTurnId = result.turn.id;
  } catch (error) { discardPendingUserMessage(); setRunning(false); appendNotice(error.message, true); toast(error.message, true); }
}

async function stopTurn() {
  if (!state.session) return;
  try { await api("/api/chat/interrupt", { method: "POST", body: JSON.stringify({ thread_id: state.session.thread_id, turn_id: state.activeTurnId }) }); }
  catch (error) { toast(error.message, true); }
}

async function refreshContext() { await loadDashboard(); }

async function loadFileTree() {
  const result = await api(`/api/tree?project=${encodeURIComponent(state.dashboard.plan.project)}`);
  state.files = result.files; renderFileTree();
}
function renderFileTree() {
  const filter = $("#file-search").value.trim().toLowerCase(); const target = $("#file-tree"); target.replaceChildren(); let folder = "";
  state.files.filter((file) => file.path.toLowerCase().includes(filter)).forEach((file) => {
    const relative = file.path.replace(`${state.dashboard.plan.project}/`, ""); const parts = relative.split("/"); const next = parts.length > 1 ? parts.slice(0, -1).join(" / ") : "项目根目录";
    if (next !== folder) { const group = document.createElement("div"); group.className = "file-group"; group.textContent = next; target.append(group); folder = next; }
    const button = document.createElement("button"); button.className = `file-item${state.currentFile?.path === file.path ? " active" : ""}`; button.textContent = parts.at(-1); button.title = file.path; button.addEventListener("click", () => openFile(file.path)); target.append(button);
  });
}
async function openFile(path) {
  if (state.dirty && state.currentFile?.path !== path && !confirm("当前文件有未保存修改，仍要切换吗？")) return;
  const file = await api(`/api/file?path=${encodeURIComponent(path)}`); state.currentFile = file; $("#editor").value = file.content; state.savedContent = normalized($("#editor").value); state.dirty = false;
  $("#editor").disabled = !file.writable; $("#save-button").disabled = !file.writable; $("#diff-button").disabled = false;
  setText("#current-file", file.path); setText("#file-language", file.language.toUpperCase()); setText("#save-state", file.writable ? "已与磁盘同步" : "只读文件"); renderFileTree();
}
function editorChanged() { state.dirty = Boolean(state.currentFile) && normalized($("#editor").value) !== state.savedContent; setText("#save-state", state.dirty ? "有未保存修改" : "已与磁盘同步"); }
async function saveFile() {
  if (!state.currentFile || !state.dirty) return;
  try { const result = await api("/api/file", { method: "PUT", body: JSON.stringify({ path: state.currentFile.path, content: $("#editor").value, mtime_ns: state.currentFile.mtime_ns }) }); state.currentFile.mtime_ns = result.mtime_ns; state.savedContent = normalized($("#editor").value); editorChanged(); toast("文件已保存"); await refreshContext(); }
  catch (error) { toast(error.message, true); }
}
async function showDiff() {
  if (!state.currentFile) return; const result = await api(`/api/diff?path=${encodeURIComponent(state.currentFile.path)}`); const consoleNode = $("#drawer-console"); consoleNode.textContent = result.diff || "该文件相对 HEAD 没有改动。"; consoleNode.classList.remove("hidden");
}
async function openCodeDrawer() { $("#code-drawer").classList.add("open"); $("#drawer-backdrop").classList.remove("hidden"); await loadFileTree(); if (!state.currentFile && state.dashboard.plan.file) await openFile(state.dashboard.plan.file); }
function closeCodeDrawer() { if (state.dirty && !confirm("文件尚未保存，仍要关闭代码工作区吗？")) return; $("#code-drawer").classList.remove("open"); $("#drawer-backdrop").classList.add("hidden"); }
async function openPycharm() { try { await api("/api/open-pycharm", { method: "POST", body: JSON.stringify(state.currentFile ? { path: state.currentFile.path } : {}) }); toast("已在 PyCharm 中打开"); } catch (error) { toast(error.message, true); } }
async function runTests() {
  openCodeDrawer(); const output = $("#drawer-console"); output.classList.remove("hidden"); output.textContent = `$ ${state.dashboard.plan.run}\n\n正在运行…`;
  try { const result = await api("/api/run-current", { method: "POST", body: "{}" }); output.textContent = `$ ${result.command}\n\n${result.output}\n\n证据：${result.evidence}`; toast(result.passed ? "当天测试通过" : "测试未通过，请查看输出", !result.passed); await refreshContext(); }
  catch (error) { output.textContent = error.message; toast(error.message, true); }
}

$("#start-session-button").addEventListener("click", startSession); $("#setup-retry").addEventListener("click", connectCodex); $("#reconnect-button").addEventListener("click", connectCodex); $("#login-button").addEventListener("click", loginWithChatGPT);
$("#send-button").addEventListener("click", sendMessage); $("#stop-button").addEventListener("click", stopTurn);
$("#message-input").addEventListener("input", () => { resizeComposer(); updateSendState(); });
$("#message-input").addEventListener("keydown", (event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); sendMessage(); } });
$$('.learning-step').forEach((button) => button.addEventListener('click', () => setStage(button.dataset.stage, true)));
$$('[data-prompt]').forEach((button) => button.addEventListener('click', () => { $("#message-input").value = button.dataset.prompt; resizeComposer(); updateSendState(); $("#message-input").focus(); }));
$$('[data-stage-jump]').forEach((button) => button.addEventListener('click', () => setStage(button.dataset.stageJump, true)));
$("#refresh-context").addEventListener("click", () => refreshContext().then(() => toast("学习现场已刷新")).catch((error) => toast(error.message, true)));
$("#open-code-button").addEventListener("click", () => openCodeDrawer().catch((error) => toast(error.message, true))); $("#close-code-button").addEventListener("click", closeCodeDrawer); $("#drawer-backdrop").addEventListener("click", closeCodeDrawer);
$("#file-search").addEventListener("input", renderFileTree); $("#editor").addEventListener("input", editorChanged); $("#save-button").addEventListener("click", saveFile); $("#diff-button").addEventListener("click", () => showDiff().catch((error) => toast(error.message, true)));
$("#editor").addEventListener("keydown", (event) => { if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") { event.preventDefault(); saveFile(); } if (event.key === "Tab") { event.preventDefault(); const start = event.currentTarget.selectionStart; event.currentTarget.setRangeText("    ", start, event.currentTarget.selectionEnd, "end"); editorChanged(); } });
$("#open-pycharm-button").addEventListener("click", openPycharm); $("#run-test-button").addEventListener("click", runTests);
$("#roadmap-button").addEventListener("click", () => $("#roadmap-modal").classList.remove("hidden")); $("#close-roadmap").addEventListener("click", () => $("#roadmap-modal").classList.add("hidden"));
window.addEventListener("beforeunload", (event) => { if (state.dirty) { event.preventDefault(); event.returnValue = ""; } state.eventGeneration += 1; if (state.eventSource) state.eventSource.close(); });

async function init() {
  try { await loadDashboard(); await connectCodex(); }
  catch (error) { toast(error.message, true); showSetup("工作台初始化失败", error.message, {}); }
}
init();
