import sys

with open('/Users/harshraj/SELF-ASSESSMENT /index.html', 'r') as f:
    content = f.read()

# Chunk 1
target1 = """const state = DATA.map(() => new Set());
let submitted = false;"""
replacement1 = """const STORAGE_KEY = "proctor_assessment_state_v1";
let state = DATA.map(() => new Set());
let submitted = false;
let timerEndTime = null;

function loadState() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      if (parsed.dataLength === DATA.length && !parsed.submitted) {
        state = parsed.answers.map(arr => new Set(arr));
        if (parsed.endTime) timerEndTime = parsed.endTime;
        return true;
      }
    }
  } catch (e) { console.warn(e); }
  return false;
}

function saveState() {
  if (submitted) {
    localStorage.removeItem(STORAGE_KEY);
    return;
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify({
    dataLength: DATA.length,
    endTime: timerEndTime,
    submitted: submitted,
    answers: state.map(set => Array.from(set))
  }));
}"""
content = content.replace(target1, replacement1)

# Chunk 2
target2 = """// Timer
let timerSeconds = 60 * 60; // 60 minutes
let timerInterval;

function startTimer() {
  const display = document.getElementById("timerDisplay");
  const pill = document.getElementById("timerPill");
  timerInterval = setInterval(() => {
    timerSeconds--;
    if (timerSeconds <= 0) {
      clearInterval(timerInterval);
      timerSeconds = 0;
      submitQuiz();
    }
    const m = Math.floor(timerSeconds / 60);
    const s = timerSeconds % 60;
    display.textContent = `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
    if (timerSeconds <= 300) pill.className = "timer-pill danger";
    else if (timerSeconds <= 600) pill.className = "timer-pill warning";
  }, 1000);
}"""
replacement2 = """// Timer
let timerInterval;

function startTimer() {
  const display = document.getElementById("timerDisplay");
  const pill = document.getElementById("timerPill");
  
  if (!timerEndTime) {
    timerEndTime = Date.now() + (60 * 60 * 1000); // 60 minutes
    saveState();
  }

  function tick() {
    const remainingMs = timerEndTime - Date.now();
    if (remainingMs <= 0) {
      clearInterval(timerInterval);
      display.textContent = "00:00";
      submitQuiz();
      return;
    }
    
    const totalSeconds = Math.floor(remainingMs / 1000);
    const m = Math.floor(totalSeconds / 60);
    const s = totalSeconds % 60;
    display.textContent = `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
    
    if (totalSeconds <= 300) pill.className = "timer-pill danger";
    else if (totalSeconds <= 600) pill.className = "timer-pill warning";
    else pill.className = "timer-pill";
  }
  
  tick();
  timerInterval = setInterval(tick, 1000);
}"""
content = content.replace(target2, replacement2)

# Chunk 3
target3 = """      <div class="options" id="opts-${qi}">
        ${item.opts.map((o, oi) => {
          const letter = LETTERS[oi];
          const inputType = item.type === "msq" ? "checkbox" : "radio";
          return `<label class="opt" data-qi="${qi}" data-letter="${letter}">
            <input type="${inputType}" name="q${qi}" value="${letter}">
            <span class="letter">${letter}.</span>
            <span class="opt-text">${escapeHtml(o)}</span>
          </label>`;
        }).join("")}
      </div>"""
replacement3 = """      <fieldset class="options" id="opts-${qi}" style="border:none; padding:0; margin:0;">
        <legend class="sr-only" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">Options for Q${qi+1}</legend>
        ${item.opts.map((o, oi) => {
          const letter = LETTERS[oi];
          const inputType = item.type === "msq" ? "checkbox" : "radio";
          return `<label class="opt" data-qi="${qi}" data-letter="${letter}">
            <input type="${inputType}" name="q${qi}" value="${letter}" aria-label="Option ${letter}">
            <span class="letter">${letter}.</span>
            <span class="opt-text">${escapeHtml(o)}</span>
          </label>`;
        }).join("")}
      </fieldset>"""
content = content.replace(target3, replacement3)

# Chunk 4
target4 = """      }
      updateOptionVisuals(qi);
      updateProgress();
      // Mark card as answered"""
replacement4 = """      }
      updateOptionVisuals(qi);
      updateProgress();
      saveState();
      // Mark card as answered"""
content = content.replace(target4, replacement4)

# Chunk 5
target5 = """function updateProgress() {
  const answered = state.filter(s => s.size > 0).length;
  document.getElementById("answeredCount").textContent = answered;
  const pct = Math.round((answered / DATA.length) * 100);
  document.getElementById("progressPct").textContent = `${pct}%`;
  document.getElementById("progressFill").style.width = `${pct}%`;
  document.getElementById("statusText").textContent =
    answered === 0 ? "Answer questions to enable submission" :
    answered === DATA.length ? "All questions answered — ready to submit!" :
    `${answered} of ${DATA.length} answered`;
}"""
replacement5 = """function updateProgress() {
  const answered = state.filter(s => s.size > 0).length;
  document.getElementById("answeredCount").textContent = answered;
  const pct = Math.round((answered / DATA.length) * 100);
  document.getElementById("progressPct").textContent = `${pct}%`;
  document.getElementById("progressFill").style.width = `${pct}%`;
  
  const submitBtn = document.getElementById("submitBtn");
  if (answered === 0) {
    document.getElementById("statusText").textContent = "Answer questions to enable submission";
    submitBtn.style.opacity = "0.5";
    submitBtn.style.pointerEvents = "none";
  } else if (answered === DATA.length) {
    document.getElementById("statusText").textContent = "All questions answered — ready to submit!";
    submitBtn.style.opacity = "1";
    submitBtn.style.pointerEvents = "auto";
  } else {
    document.getElementById("statusText").textContent = `${answered} of ${DATA.length} answered`;
    submitBtn.style.opacity = "1";
    submitBtn.style.pointerEvents = "auto";
  }
}"""
content = content.replace(target5, replacement5)

# Chunk 6
target6 = """// Clear
document.getElementById("clearBtn").addEventListener("click", () => {
  if (submitted) return;
  state.forEach(s => s.clear());
  DATA.forEach((_, qi) => {"""
replacement6 = """// Clear
document.getElementById("clearBtn").addEventListener("click", () => {
  if (submitted) return;
  if (!confirm("Are you sure you want to clear all your answers?")) return;
  state.forEach(s => s.clear());
  saveState();
  DATA.forEach((_, qi) => {"""
content = content.replace(target6, replacement6)

# Chunk 7
target7 = """  if (submitted) return;
  submitted = true;
  clearInterval(timerInterval);"""
replacement7 = """  if (submitted) return;
  submitted = true;
  saveState();
  clearInterval(timerInterval);"""
content = content.replace(target7, replacement7)

# Chunk 8
target8 = """// ===========================
// INIT
// ===========================
render();
buildSectionNav();
updateProgress();
startTimer();"""
replacement8 = """// ===========================
// INIT
// ===========================
window.addEventListener("beforeunload", (e) => {
  const answered = state.filter(s => s.size > 0).length;
  if (answered > 0 && !submitted) {
    e.preventDefault();
    e.returnValue = "";
  }
});

loadState();
render();
buildSectionNav();
updateProgress();
startTimer();

// Pre-fill visual states if loaded from storage
DATA.forEach((_, qi) => {
  if (state[qi].size > 0) {
    updateOptionVisuals(qi);
    document.getElementById(`q-${qi}`).classList.add('answered');
  }
});"""
content = content.replace(target8, replacement8)

with open('/Users/harshraj/SELF-ASSESSMENT /index.html', 'w') as f:
    f.write(content)

print("Replacements done.")
