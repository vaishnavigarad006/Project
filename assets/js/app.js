(() => {
  'use strict';
  const input = document.getElementById('password');
  const toggle = document.getElementById('toggle-visibility');
  const count = document.getElementById('char-count');
  const emptyState = document.getElementById('empty-state');
  const results = document.getElementById('results');
  const label = document.getElementById('strength-label');
  const scoreValue = document.getElementById('score-value');
  const meter = document.getElementById('meter');
  const meterFill = document.getElementById('meter-fill');
  const criteriaList = document.getElementById('criteria-list');
  const criteriaSummary = document.getElementById('criteria-summary');
  const tipsList = document.getElementById('tips-list');
  const resultNote = document.getElementById('result-note');
  const crackTime = document.getElementById('crack-time');
  const attackScenario = document.getElementById('attack-scenario');
  const crackExplanation = document.getElementById('crack-explanation');
  let requestId = 0;

  attackScenario.addEventListener('change', () => {
    if (input.value) updateCrackEstimate(input.value);
  });

  toggle.addEventListener('click', () => {
    const showing = input.type === 'text';
    input.type = showing ? 'password' : 'text';
    toggle.textContent = showing ? 'SHOW' : 'HIDE';
    toggle.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
    input.focus();
  });

  input.addEventListener('input', () => {
    const password = input.value;
    count.textContent = `${password.length} ${password.length === 1 ? 'character' : 'characters'}`;
    if (!password) {
      emptyState.classList.remove('hidden');
      results.classList.add('hidden');
      resultNote.textContent = '';
      crackTime.textContent = 'Enter a password to estimate';
      crackExplanation.textContent = 'The estimate updates locally as you type.';
      return;
    }
    // Real-time local fallback keeps the interface responsive even if PHP is not running.
    render(evaluateLocally(password));
    updateCrackEstimate(password);
    evaluateOnServer(password);
  });

  async function evaluateOnServer(password) {
    const current = ++requestId;
    try {
      const response = await fetch('api/evaluate.php', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        cache: 'no-store',
        body: JSON.stringify({password})
      });
      if (!response.ok) throw new Error('PHP endpoint unavailable');
      const payload = await response.json();
      if (current !== requestId || input.value !== password || !payload.success || !payload.result) return;
      render(payload.result);
      resultNote.textContent = 'Server-side PHP validation complete. Password was not saved.';
    } catch (_) {
      if (current === requestId) resultNote.textContent = 'Showing browser-side analysis. Start PHP server to enable server-side validation.';
    }
  }


  // Illustrative rates, not guarantees. Actual rates vary by hardware and hash algorithm.
  function updateCrackEstimate(pw) {
    const rates = {
      online: { guessesPerSecond: 100, label: 'online attack' },
      slow: { guessesPerSecond: 10000, label: 'offline slow-hash attack' },
      fast: { guessesPerSecond: 1e10, label: 'offline fast-hash attack' }
    };
    const scenario = rates[attackScenario.value] || rates.online;
    let pool = 0;
    if (/[a-z]/.test(pw)) pool += 26;
    if (/[A-Z]/.test(pw)) pool += 26;
    if (/\d/.test(pw)) pool += 10;
    if (/[^A-Za-z0-9]/.test(pw)) pool += 33;
    if (!pool) pool = 1;

    // Use logarithms so very large search spaces do not overflow JavaScript numbers.
    const log10ExpectedGuesses = Math.max(0, pw.length * Math.log10(pool) - Math.log10(2));
    const log10Seconds = log10ExpectedGuesses - Math.log10(scenario.guessesPerSecond);
    crackTime.textContent = formatDurationFromLog10Seconds(log10Seconds);
    crackExplanation.textContent = `Assumption: about ${scenario.guessesPerSecond.toLocaleString('en-US')} guesses per second for an estimated ${scenario.label}. This is a simplified brute-force model for a randomly generated password.`;
  }

  function formatDurationFromLog10Seconds(logSeconds) {
    if (!Number.isFinite(logSeconds)) return 'Not enough information';
    if (logSeconds < Math.log10(1)) return 'Less than a second';
    const units = [
      { name: 'second', seconds: 1 },
      { name: 'minute', seconds: 60 },
      { name: 'hour', seconds: 3600 },
      { name: 'day', seconds: 86400 },
      { name: 'year', seconds: 31557600 }
    ];
    const logYears = logSeconds - Math.log10(31557600);
    if (logYears >= 12) return `About 10^${Math.min(300, Math.floor(logYears))} years`;
    if (logYears >= 0) {
      const years = Math.pow(10, logYears);
      return `About ${formatMagnitude(years)} ${years < 2 ? 'year' : 'years'}`;
    }
    for (let i = units.length - 2; i >= 0; i--) {
      if (logSeconds >= Math.log10(units[i].seconds)) {
        const amount = Math.pow(10, logSeconds) / units[i].seconds;
        return `About ${formatMagnitude(amount)} ${units[i].name}${amount >= 2 ? 's' : ''}`;
      }
    }
    return 'Less than a second';
  }

  function formatMagnitude(value) {
    if (value >= 1000) return value.toLocaleString('en-US', {maximumFractionDigits: 1});
    if (value >= 10) return Math.round(value).toLocaleString('en-US');
    if (value >= 1) return value.toLocaleString('en-US', {maximumFractionDigits: 1});
    return value.toLocaleString('en-US', {maximumSignificantDigits: 2});
  }

  function evaluateLocally(pw) {
    let score = 0;
    const n = pw.length;
    score += n >= 16 ? 40 : n >= 12 ? 30 : n >= 8 ? 20 : 0;
    const upper = /[A-Z]/.test(pw), lower = /[a-z]/.test(pw), digit = /[0-9]/.test(pw), special = /[^A-Za-z0-9]/.test(pw);
    if (upper) score += 15;
    if (lower) score += 15;
    if (digit) score += 15;
    if (special) score += 15;
    const low = pw.toLowerCase();
    const common = ['password','123456','123456789','qwerty','admin','welcome','letmein','iloveyou','monkey','dragon','sunshine','abc123','passw0rd'];
    const commonFound = common.some(w => low.includes(w));
    const repeated = /(.)\1\1/s.test(pw);
    const sequence = hasSequence(low);
    if (commonFound) score -= 30;
    if (repeated) score -= 10;
    if (sequence) score -= 10;
    score = Math.max(0, Math.min(100, score));
    const tips = [];
    if (n < 12) tips.push('Use at least 12 characters; a longer passphrase is even better.');
    if (!upper) tips.push('Add an uppercase letter (A–Z), if it fits your passphrase.');
    if (!lower) tips.push('Add a lowercase letter (a–z).');
    if (!digit) tips.push('Consider including a number (0–9).');
    if (!special) tips.push('Consider including a symbol such as !, @, # or $.');
    if (commonFound) tips.push('Avoid common passwords and predictable words such as “password” or “welcome”.');
    if (repeated) tips.push('Avoid three or more identical characters in a row.');
    if (sequence) tips.push('Avoid simple keyboard or character sequences such as abc or 123.');
    if (!tips.length) tips.push('Good job. Keep it unique to one account and store it in a reputable password manager.');
    return {
      score, label: score < 40 ? 'Weak' : score < 70 ? 'Moderate' : 'Strong', tips,
      checks: {
        length: {ok:n >= 12,title:'12+ characters'}, uppercase:{ok:upper,title:'Uppercase letter'},
        lowercase:{ok:lower,title:'Lowercase letter'}, number:{ok:digit,title:'Number'},
        special:{ok:special,title:'Special character'}, patterns:{ok:!commonFound&&!repeated&&!sequence,title:'No obvious patterns'}
      }
    };
  }

  function hasSequence(value) {
    const sequences = ['abcdefghijklmnopqrstuvwxyz','0123456789','qwertyuiop','asdfghjkl','zxcvbnm'];
    return sequences.some(seq => {
      for (let i = 0; i <= seq.length - 3; i++) {
        const part = seq.slice(i, i + 3);
        if (value.includes(part) || value.includes([...part].reverse().join(''))) return true;
      }
      return false;
    });
  }

  function render(result) {
    emptyState.classList.add('hidden');
    results.classList.remove('hidden');
    label.textContent = result.label;
    label.className = `strength-label ${result.label.toLowerCase()}`;
    scoreValue.textContent = result.score;
    meterFill.style.width = `${result.score}%`;
    meterFill.className = `meter-fill ${result.label.toLowerCase()}`;
    meter.setAttribute('aria-valuenow', result.score);
    meter.setAttribute('aria-valuetext', `${result.label}, ${result.score} out of 100`);
    const checks = Object.values(result.checks || {});
    const passed = checks.filter(c => c.ok).length;
    criteriaSummary.textContent = `${passed} of ${checks.length} checks`;
    criteriaList.replaceChildren();
    checks.forEach(c => {
      const item = document.createElement('div');
      item.className = `criterion ${c.ok ? 'passed' : 'failed'}`;
      const icon = document.createElement('span');
      icon.className = 'criterion-icon';
      icon.textContent = c.ok ? '✓' : '–';
      const text = document.createElement('span');
      text.textContent = c.title;
      item.append(icon, text);
      criteriaList.append(item);
    });
    tipsList.replaceChildren();
    result.tips.forEach(tip => {
      const li = document.createElement('li');
      li.textContent = tip;
      tipsList.append(li);
    });
  }
})();
