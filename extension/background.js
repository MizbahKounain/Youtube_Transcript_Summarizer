// background.js

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.action === "getSummary") {
    const videoUrl = message.videoUrl;
    try {
      const response = await fetch(`http://127.0.0.1:5000/summarize?url=${encodeURIComponent(videoUrl)}`);
      const summaryData = await response.json();

      console.log("Received summary data:", summaryData);  // Debug log

      if (summaryData.error) {
        sendResponse({ summary: `Error: ${summaryData.error}` });
      } else {
        sendResponse({ summary: summaryData.summary || "Summary could not be generated." });
      }
    } catch (error) {
      console.error("Failed to fetch summary:", error);
      sendResponse({ summary: "Error fetching summary from backend." });
    }
  }
  return true;  // Keep the message channel open for async sendResponse
});
