<?php
// SecurePass - Web Based Password Strength Checker
// The password is evaluated on request and is never written to a file or database.
?><!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0b1020">
  <title>SecurePass | Password Strength Checker</title>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
  <div class="ambient ambient-one"></div><div class="ambient ambient-two"></div>
  <header class="topbar">
    <a class="brand" href="index.php" aria-label="SecurePass home">
      <span class="brand-mark">S</span><span>Secure<span class="brand-accent">Pass</span><small> PASSWORD SECURITY LAB</small></span>
    </a>
    <span class="privacy-pill"><span class="status-dot"></span> Privacy-first analysis</span>
  </header>

  <main class="page-shell">
    <section class="intro">
      <div class="eyebrow"><span class="eyebrow-line"></span> PERSONAL CYBERSECURITY</div>
      <h1>Make your password<br><span>hard to guess.</span></h1>
      <p class="intro-copy">Check password strength instantly. Get clear feedback and practical steps to make it stronger.</p>
      <div class="trust-row">
        <span><span class="mini-check">✓</span> Real-time feedback</span>
        <span><span class="mini-check">✓</span> No password history</span>
        <span><span class="mini-check">✓</span> Free to use</span>
      </div>
    </section>

    <section class="checker-card" aria-labelledby="checker-title">
      <div class="card-heading">
        <div><div class="card-kicker">PASSWORD ANALYZER</div><h2 id="checker-title">Test your password</h2></div>
        <span class="lock-icon" aria-hidden="true">⌑</span>
      </div>
      <label class="field-label" for="password">Enter a password to analyze</label>
      <div class="password-field">
        <input id="password" type="password" autocomplete="new-password" spellcheck="false"
          placeholder="Type a sample password…" aria-describedby="privacy-note">
        <button id="toggle-visibility" class="visibility-btn" type="button" aria-label="Show password">SHOW</button>
      </div>
      <div class="field-meta"><span>Try a sample, not a password you currently use.</span><span id="char-count">0 characters</span></div>

      <div id="empty-state" class="empty-state">
        <div class="empty-symbol">✳</div>
        <strong>Your strength report will appear here</strong>
        <p>Start typing to see your score, strength level and suggestions update live.</p>
      </div>

      <div id="results" class="results hidden" aria-live="polite">
        <div class="score-header">
          <div><div class="muted-label">STRENGTH LEVEL</div><div id="strength-label" class="strength-label">Weak</div></div>
          <div class="score-number"><strong id="score-value">0</strong><span>/100</span></div>
        </div>
        <div class="meter-track" role="progressbar" aria-label="Password strength score" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" id="meter">
          <div id="meter-fill" class="meter-fill"></div>
        </div>
        <div class="meter-scale"><span>WEAK</span><span>MODERATE</span><span>STRONG</span></div>

        <section class="crack-panel" aria-labelledby="crack-title">
          <div class="crack-topline"><div><div class="muted-label">GUESSING-TIME ESTIMATE</div><h3 id="crack-title">How long could it take to crack?</h3></div><span class="crack-icon" aria-hidden="true">◷</span></div>
          <div class="crack-time" id="crack-time" aria-live="polite">Calculating…</div>
          <label class="scenario-label" for="attack-scenario">Assumed attack scenario</label>
          <select id="attack-scenario" class="scenario-select">
            <option value="online">Online attack — 100 guesses/second</option>
            <option value="slow">Offline slow-hash attack — 10,000 guesses/second</option>
            <option value="fast">Offline fast-hash attack — 10 billion guesses/second</option>
          </select>
          <p id="crack-explanation" class="crack-explanation">Estimate assumes a randomly generated password and an average of half the search space.</p>
          <p class="crack-warning">Illustrative estimate only. Real results vary greatly with password predictability, hardware, hash algorithm, rate limits and attacker knowledge. Predictable or reused passwords can be cracked much faster. Do not enter a password you currently use.</p>
        </section>

        <div class="criteria-heading"><h3>Security checklist</h3><span id="criteria-summary">0 of 6 checks</span></div>
        <div class="criteria-grid" id="criteria-list"></div>

        <div class="suggestions-box">
          <div class="suggestion-title"><span class="bulb">✦</span><h3>How to improve</h3></div>
          <ul id="tips-list"></ul>
        </div>
        <div id="result-note" class="result-note"></div>
      </div>
      <p id="privacy-note" class="privacy-note"><span>◈</span> Your password is analyzed for this check only. SecurePass does not save passwords or evaluation history.</p>
    </section>

    <section class="bottom-grid">
      <article class="info-card">
        <div class="info-icon">↗</div><h3>Length matters most</h3>
        <p>Long, unique passphrases are generally harder to guess than short passwords with predictable substitutions.</p>
      </article>
      <article class="info-card">
        <div class="info-icon">⌘</div><h3>Avoid predictable patterns</h3>
        <p>Common words, repeated characters and sequences can make a password easier to guess.</p>
      </article>
      <article class="info-card">
        <div class="info-icon">◉</div><h3>Keep it unique</h3>
        <p>Use a different password for each account. A password manager can help you create and store unique passwords.</p>
      </article>
    </section>

    <section class="method-note">
      <strong>How scoring works</strong>
      <p>SecurePass uses the rule-based scoring described in the project report: length and character types add points; common words, repeated characters and simple sequences reduce points. The score is a learning aid, not a guarantee of security.</p>
    </section>
  </main>

  <footer><span>© SecurePass Mini Project</span><span>Built with HTML · CSS · JavaScript · PHP</span></footer>
  <script src="assets/js/app.js"></script>
</body>
</html>
