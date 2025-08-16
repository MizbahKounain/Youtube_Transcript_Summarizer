// content.js

const videoUrl = window.location.href;  // Get the current YouTube video URL

chrome.runtime.sendMessage({ action: "getSummary", videoUrl: videoUrl }, (response) => {
  if (response.summary) {
    alert("Summary:\n\n" + response.summary);
  } else {
    alert("Error: Unable to generate summary.");
  }
});
