async function submitJson() {
  const jsonText = document.getElementById("jsonInput").value;
  const filename = document.getElementById("filename").value || "output.xlsx";
  const errorDiv = document.getElementById("error");
  errorDiv.textContent = "";

  let parsed;
  try {
    parsed = JSON.parse(jsonText);
  } catch (e) {
    errorDiv.textContent = "Invalid JSON format.";
    return;
  }

  try {
    const response = await fetch(
      `/convert?filename=${encodeURIComponent(filename)}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(parsed),
      }
    );

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    errorDiv.textContent = "Error downloading file: " + err.message;
  }
}

window.submitJson = submitJson;
