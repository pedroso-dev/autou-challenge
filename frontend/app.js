document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.getElementById("submit-btn");
  const emailContentTextarea = document.getElementById("email-content");
  const loadingDiv = document.getElementById("loading");
  const resultsDiv = document.getElementById("results");
  const categoryResult = document.getElementById("category-result");
  const responseResult = document.getElementById("response-result");
  const errorMessageDiv = document.getElementById("error-message");

  resultsDiv.classList.add("hidden");
  loadingDiv.classList.add("hidden");
  errorMessageDiv.classList.add("hidden");

  submitBtn.addEventListener("click", async () => {
    const emailContent = emailContentTextarea.value.trim();

    if (!emailContent) {
      alert("Por favor, insira o conteúdo do e-mail.");
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Analisando...";

    resultsDiv.classList.add("hidden");
    errorMessageDiv.classList.add("hidden");
    loadingDiv.classList.remove("hidden");

    try {
      const backendUrl = "http://127.0.0.1:5000/classify_email";

      const response = await fetch(backendUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email_content: emailContent }),
      });

      const data = await response.json().catch(() => ({}));

      if (response.ok && data) {
        categoryResult.textContent = data.category ?? "-";
        responseResult.textContent = data.suggested_response ?? "-";
        resultsDiv.classList.remove("hidden");
      } else {
        errorMessageDiv.classList.remove("hidden");
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
      errorMessageDiv.classList.remove("hidden");
    } finally {
      loadingDiv.classList.add("hidden");
      submitBtn.disabled = false;
      submitBtn.textContent = "Classificar e sugerir resposta";
    }
  });
});
