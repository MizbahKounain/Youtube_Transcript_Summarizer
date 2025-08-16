// popup.js

document.getElementById("summarize-button").addEventListener("click", function () {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const url = tabs[0].url;  // Get the URL of the active YouTube tab
    const summaryDiv = document.getElementById("summary");

    // Show loading message
    summaryDiv.innerHTML = "<em>Generating summary, please wait...</em>";

    fetch(`http://127.0.0.1:5000/summarize?url=${encodeURIComponent(url)}`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          summaryDiv.innerHTML = `<span style="color: red; font-weight: bold;">Error:</span> ${data.error}`;
        } else if (data.summary) {
          summaryDiv.innerHTML = data.summary;
        } else {
          summaryDiv.innerHTML = `<span style="color: red;">Unexpected response from server.</span>`;
        }
      })
      .catch(error => {
        summaryDiv.innerHTML = `<span style="color: red;">Error fetching summary: ${error}</span>`;
      });
  });
});
