function clearCode() {
  document.getElementById("code").value = "";
  document.getElementById("optimized_code").innerText = "";
  document.getElementById("bugs").innerText = "";
  document.getElementById("performance").innerText = "";
  document.getElementById("security").innerText = "";
  document.getElementById("best_practices").innerText = "";

  document.getElementById("review-panels").classList.add("hidden");
  document.getElementById("optimized-panel").classList.add("hidden");
}

// ✅ File Upload (FIXED)
function loadFile() {
  const input = document.getElementById("fileInput");

  if (!input.files || input.files.length === 0) {
    alert("No file selected!");
    return;
  }

  const file = input.files[0];
  const reader = new FileReader();

  reader.onload = function (e) {
    document.getElementById("code").value = e.target.result;

    // ✅ RESET FILE INPUT (IMPORTANT FIX)
    input.value = "";
  };

  reader.readAsText(file);
}


// ✅ Main AI Processing
async function processCode() {
  const code = document.getElementById("code").value;
  const language = document.getElementById("language").value;
  const mode = document.getElementById("mode").value;

  if (!code.trim()) {
    alert("Please enter or upload code!");
    return;
  }

  // Loading message
  if (mode === "rewrite") {
    document.getElementById("optimized_code").innerText = "⏳ Rewriting code...";
    document.getElementById("optimized-panel").classList.remove("hidden");
    document.getElementById("review-panels").classList.add("hidden");
  } else {
    document.getElementById("review-panels").classList.remove("hidden");
    document.getElementById("optimized-panel").classList.remove("hidden");

    document.getElementById("bugs").innerText = "⏳ Analyzing...";
    document.getElementById("performance").innerText = "⏳ Analyzing...";
    document.getElementById("security").innerText = "⏳ Analyzing...";
    document.getElementById("best_practices").innerText = "⏳ Analyzing...";
    document.getElementById("optimized_code").innerText = "⏳ Generating optimized code...";
  }

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, language, mode })
    });

    const data = await response.json();

    // ✅ REWRITE MODE
    if (mode === "rewrite") {
      document.getElementById("optimized_code").innerText = data.result.REWRITTEN_CODE;
      return;
    }

    // ✅ REVIEW MODE (PANELS)
    const result = data.result;

    document.getElementById("bugs").innerText = result.BUGS || "No issues found.";
    document.getElementById("performance").innerText = result.PERFORMANCE || "No issues found.";
    document.getElementById("security").innerText = result.SECURITY || "No issues found.";
    document.getElementById("best_practices").innerText = result.BEST_PRACTICES || "No issues found.";
    document.getElementById("optimized_code").innerText = result.OPTIMIZED_CODE || "";

  } catch (error) {
    alert("❌ Backend error: " + error);
  }
}
