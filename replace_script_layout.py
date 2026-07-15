import sys

with open('/Users/harshraj/SELF-ASSESSMENT /index.html', 'r') as f:
    content = f.read()

# 1. Update app-shell max-width
target_appshell = """  .app-shell {
    position: relative;
    z-index: 1;
    max-width: 860px;
    margin: 0 auto;
    padding: 24px 16px 100px;
  }"""
replacement_appshell = """  .app-shell {
    position: relative;
    z-index: 1;
    max-width: 1140px;
    margin: 0 auto;
    padding: 24px 16px 100px;
  }"""
content = content.replace(target_appshell, replacement_appshell)

# 2. Replace .controls-row CSS with .layout-columns and sidebar
target_css = """  /* ===== Controls Row ===== */
  .controls-row {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 28px;
    align-items: center;
  }

  /* ===== Section Nav Pills ===== */
  .section-nav {
    display: flex;
    gap: 6px;
    padding: 6px;
    border-radius: 14px;
    background: var(--ink-card);
    border: 1px solid var(--border);
    margin-bottom: 0;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    flex: 1;
    min-width: 320px;
  }
  .section-nav::-webkit-scrollbar { display: none; }
  .nav-pill {
    flex: 0 0 auto;
    min-width: 0;
    padding: 10px 14px;
    border-radius: 10px;
    border: none;
    background: transparent;
    color: var(--text-dim);
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
    text-align: center;
    position: relative;
  }"""

replacement_css = """  /* ===== Layout Columns ===== */
  .layout-columns {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    align-items: flex-start;
  }
  .sidebar {
    width: 260px;
    flex-shrink: 0;
    position: sticky;
    top: 24px;
  }
  .main-column {
    flex: 1;
    min-width: 0;
  }

  @media (max-width: 900px) {
    .sidebar { width: 100%; position: static; }
    .layout-columns { gap: 16px; }
  }

  /* ===== Section Nav Pills ===== */
  .section-nav {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 8px;
    border-radius: 14px;
    background: var(--ink-card);
    border: 1px solid var(--border);
    margin-bottom: 0;
  }
  .nav-pill {
    width: 100%;
    padding: 12px 14px;
    border-radius: 10px;
    border: none;
    background: transparent;
    color: var(--text-dim);
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }"""
content = content.replace(target_css, replacement_css)

# 3. Restore .progress-wrap margin
target_progress = """  /* ===== Progress ===== */
  .progress-wrap {
    padding: 16px 20px;
    border-radius: var(--radius);
    background: var(--ink-card);
    border: 1px solid var(--border);
    margin-bottom: 0;
    flex-basis: 260px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }"""
replacement_progress = """  /* ===== Progress ===== */
  .progress-wrap {
    padding: 16px 20px;
    border-radius: var(--radius);
    background: var(--ink-card);
    border: 1px solid var(--border);
    margin-bottom: 28px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }"""
content = content.replace(target_progress, replacement_progress)

# 4. Update the HTML structure
target_html = """  <div class="controls-row">
    <nav class="section-nav" id="sectionNav"></nav>

    <div class="progress-wrap">
      <div class="progress-top">
        <span class="progress-label"><strong id="answeredCount">0</strong> of 50 answered</span>
        <span class="progress-label" id="progressPct">0%</span>
      </div>
      <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
    </div>
  </div>

  <main id="quizMain"></main>

  <!-- RESULTS -->
  <section id="resultsPanel">
    <div class="results-hero">
      <div class="score-ring-wrap">
        <svg class="score-ring-svg" viewBox="0 0 140 140">
          <defs>
            <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:var(--accent-1)"/>
              <stop offset="100%" style="stop-color:var(--accent-2)"/>
            </linearGradient>
          </defs>
          <circle class="ring-bg" />
          <circle class="ring-fill" id="ringFill" />
        </svg>
        <div class="score-value">
          <div class="score-pct" id="scorePct">0%</div>
          <div class="score-pct-label">Score</div>
        </div>
      </div>
      <h2 id="scoreHeadline">Calculating…</h2>
      <p class="results-sub" id="scoreSub">0 of 50 correct</p>
    </div>
    <div class="section-scores-grid" id="sectionScores"></div>
    <div class="omr-section">
      <p class="omr-title">Answer Sheet — tap any bubble to jump</p>
      <div class="omr-grid" id="omrGrid"></div>
      <div class="omr-legend">
        <span><div class="legend-dot green"></div> Correct</span>
        <span><div class="legend-dot red"></div> Incorrect</span>
        <span><div class="legend-dot gray"></div> Unanswered</span>
      </div>
    </div>
    <div class="results-actions">
      <button class="ghost" id="retakeBtn" type="button">↻ Retake Assessment</button>
    </div>
  </section>

</div>"""

replacement_html = """  <div class="layout-columns">
    <aside class="sidebar">
      <nav class="section-nav" id="sectionNav"></nav>
    </aside>

    <div class="main-column">
      <div class="progress-wrap">
        <div class="progress-top">
          <span class="progress-label"><strong id="answeredCount">0</strong> of 50 answered</span>
          <span class="progress-label" id="progressPct">0%</span>
        </div>
        <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
      </div>

      <main id="quizMain"></main>

      <!-- RESULTS -->
      <section id="resultsPanel">
        <div class="results-hero">
          <div class="score-ring-wrap">
            <svg class="score-ring-svg" viewBox="0 0 140 140">
              <defs>
                <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:var(--accent-1)"/>
                  <stop offset="100%" style="stop-color:var(--accent-2)"/>
                </linearGradient>
              </defs>
              <circle class="ring-bg" />
              <circle class="ring-fill" id="ringFill" />
            </svg>
            <div class="score-value">
              <div class="score-pct" id="scorePct">0%</div>
              <div class="score-pct-label">Score</div>
            </div>
          </div>
          <h2 id="scoreHeadline">Calculating…</h2>
          <p class="results-sub" id="scoreSub">0 of 50 correct</p>
        </div>
        <div class="section-scores-grid" id="sectionScores"></div>
        <div class="omr-section">
          <p class="omr-title">Answer Sheet — tap any bubble to jump</p>
          <div class="omr-grid" id="omrGrid"></div>
          <div class="omr-legend">
            <span><div class="legend-dot green"></div> Correct</span>
            <span><div class="legend-dot red"></div> Incorrect</span>
            <span><div class="legend-dot gray"></div> Unanswered</span>
          </div>
        </div>
        <div class="results-actions">
          <button class="ghost" id="retakeBtn" type="button">↻ Retake Assessment</button>
        </div>
      </section>
    </div>
  </div>

</div>"""
content = content.replace(target_html, replacement_html)

with open('/Users/harshraj/SELF-ASSESSMENT /index.html', 'w') as f:
    f.write(content)

print("Replacements done.")
