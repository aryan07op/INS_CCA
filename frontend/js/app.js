// frontend/js/app.js
document.addEventListener("DOMContentLoaded", () => {
  
  // API Base URL
  const API_URL = "http://127.0.0.1:5000/api";

  // === Step 1: Unsalted Demo ===
  const runStep1Btn = document.getElementById("run_step1");
  const passStep1 = document.getElementById("password_step1");
  const loadingStep1 = document.getElementById("loading_step1");
  const resultStep1 = document.getElementById("result_step1");

  runStep1Btn.addEventListener("click", async () => {
    if (!passStep1.value) {
      alert("Please enter a password for Step 1");
      return;
    }
    
    showLoading(loadingStep1, resultStep1);

    try {
      const response = await fetch(`${API_URL}/step1/unsalted`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: passStep1.value.trim() })
      });
      const data = await response.json();
      
      // Custom formatting for the result
      let output = `--- UNSALTED HASH ---
Password:   "${data.password}"
SHA-256:    ${data.hash}\n
--- RAINBOW TABLE ATTACK ---
Attacking hash: ${data.hash}
...`;
      
      if (data.attack.found) {
        output += `\n<span class="failure">❌ ATTACK SUCCESSFUL!</span>
Password found in table: "${data.attack.password}"
Reason: The hash is always the same for this password.`;
      } else {
        output += `\n<span class="success">✅ ATTACK FAILED.</span>
Reason: Password not in our small demo rainbow table.
(A real attacker's table is billions of entries large!)`;
      }
      
      showResult(loadingStep1, resultStep1, output, true); // true for HTML content

    } catch (err) {
      showError(loadingStep1, resultStep1, err);
    }
  });

  // === Step 2: Salted Comparison Demo ===
  const runStep2Btn = document.getElementById("run_step2");
  const passStep2a = document.getElementById("password_step2a");
  const passStep2b = document.getElementById("password_step2b");
  const reuseSaltCheck = document.getElementById("reuse_salt_step2");
  const loadingStep2 = document.getElementById("loading_step2");
  const resultStep2 = document.getElementById("result_step2");

  runStep2Btn.addEventListener("click", async () => {
    if (!passStep2a.value || !passStep2b.value) {
      alert("Please enter both passwords for Step 2");
      return;
    }

    showLoading(loadingStep2, resultStep2);
    
    try {
      const response = await fetch(`${API_URL}/step2/salted-comparison`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          passwordA: passStep2a.value.trim(),
          passwordB: passStep2b.value.trim(),
          useSameSalt: reuseSaltCheck.checked
        })
      });
      const data = await response.json();
      
      // Custom formatting for the result
      let output = `--- PASSWORD A ---
Pass:  "${data.passwordA.pass}"
Salt:   ${data.passwordA.salt}
Hash:   ${data.passwordA.hash}\n
--- PASSWORD B ---
Pass:  "${data.passwordB.pass}"
Salt:   ${data.passwordB.salt}
Hash:   ${data.passwordB.hash}\n
--- ANALYSIS ---
`;

      const samePass = data.passwordA.pass === data.passwordB.pass;
      const sameHash = data.passwordA.hash === data.passwordB.hash;

      if (data.usingSameSalt) {
        output += `Mode: <span class="highlight">Shared Salt (Bad Practice)</span>
${samePass ? 'Passwords are THE SAME.' : 'Passwords are DIFFERENT.'}
${sameHash ? '<span class="failure">Hashes are THE SAME.</span> This is bad if passwords are the same!' : '<span class="success">Hashes are DIFFERENT.</span>'}`;
      } else {
        output += `Mode: <span class="success">Unique Salt (Good Practice)</span>
${samePass ? 'Passwords are THE SAME.' : 'Passwords are DIFFERENT.'}
${sameHash ? '<span class="failure">Hashes are THE SAME. (This should not happen!)</span>' : '<span class="success">Hashes are DIFFERENT.</span> This is good! Even with the same password.'}`;
      }

      showResult(loadingStep2, resultStep2, output, true); // true for HTML content

    } catch (err) {
      showError(loadingStep2, resultStep2, err);
    }
  });

  // === Step 3: Bcrypt Demo ===
  const runStep3Btn = document.getElementById("run_step3");
  const passStep3 = document.getElementById("password_step3");
  const loadingStep3 = document.getElementById("loading_step3");
  const resultStep3 = document.getElementById("result_step3");

  runStep3Btn.addEventListener("click", async () => {
    if (!passStep3.value) {
      alert("Please enter a password for Step 3");
      return;
    }

    showLoading(loadingStep3, resultStep3);
    
    try {
      const response = await fetch(`${API_URL}/step3/bcrypt`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: passStep3.value.trim() })
      });
      const data = await response.json();
      
      // Custom formatting
      let output = `--- BCRYPT DEMO ---
Password: "${data.password}"\n
Hashing it ONCE:
<span class="highlight">${data.hash1}</span>\n
Hashing it AGAIN (with the *same* password):
<span class="highlight">${data.hash2}</span>\n
--- ANALYSIS ---
The hashes are <span class="success">DIFFERENT!</span>
Bcrypt generates a new random salt *every time* and stores it inside the hash string itself.\n
--- VERIFICATION ---
Verifying "${data.password}" against Hash 1: <span class="success">${data.verification.hash1_valid}</span>
Verifying "${data.password}" against Hash 2: <span class="success">${data.verification.hash2_valid}</span>
`;

      showResult(loadingStep3, resultStep3, output, true); // true for HTML content

    } catch (err) {
      showError(loadingStep3, resultStep3, err);
    }
  });

  // --- Helper Functions ---
  function showLoading(loadingEl, resultEl) {
    loadingEl.style.display = "block";
    resultEl.style.display = "none";
  }

  function showResult(loadingEl, resultEl, content, isHtml = false) {
    loadingEl.style.display = "none";
    resultEl.style.display = "block";
    if (isHtml) {
      resultEl.innerHTML = content;
    } else {
      resultEl.textContent = content;
    }
  }

  function showError(loadingEl, resultEl, err) {
    loadingEl.style.display = "none";
    resultEl.style.display = "block";
    resultEl.innerHTML = `<span class="failure">⚠️ Failed to connect to backend.\nIs the Flask server (app.py) running?</span>\n\n${err}`;
  }
});
