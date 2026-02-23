async function generate() {
  const charsetEl = document.getElementById("charset");
  const lengthEl = document.getElementById("length");
  const listEl = document.getElementById("list");
  const errorEl = document.getElementById("error");

  errorEl.textContent = "";
  listEl.innerHTML = "";

  const payload = {
    charset: charsetEl.value,
    length: parseInt(lengthEl.value, 10),
  };

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      errorEl.textContent = data.error || "Ошибка генерации.";
      return;
    }

    const passwords = data.passwords || [];
    for (const pw of passwords) {
      const row = document.createElement("div");
      row.className = "item";

      const code = document.createElement("code");
      code.className = "pw";
      code.textContent = pw;

      const btn = document.createElement("button");
      btn.className = "btn small";
      btn.textContent = "Copy";
      btn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(pw);
          btn.textContent = "Copied";
          setTimeout(() => (btn.textContent = "Copy"), 900);
        } catch {
          btn.textContent = "Failed";
          setTimeout(() => (btn.textContent = "Copy"), 900);
        }
      });

      row.appendChild(code);
      row.appendChild(btn);
      listEl.appendChild(row);
    }
  } catch (e) {
    errorEl.textContent = "Сетевая ошибка. Проверь, что сервер запущен.";
  }
}

document.getElementById("generateBtn").addEventListener("click", generate);

// Генерируем сразу при открытии
generate();