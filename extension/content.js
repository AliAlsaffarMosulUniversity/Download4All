// Floating "Download" button on YouTube video pages -> sends the video to JDM.
(function () {
  const ID = "jdm-yt-button";

  function isVideoPage() {
    return /^\/(watch|shorts\/)/.test(location.pathname);
  }

  function ensureButton() {
    let b = document.getElementById(ID);
    if (!isVideoPage()) { if (b) b.remove(); return; }
    if (b) return;
    b = document.createElement("button");
    b.id = ID;
    b.textContent = "⬇ Download with JDM";
    Object.assign(b.style, {
      position: "fixed", right: "18px", bottom: "18px", zIndex: 2147483647,
      padding: "10px 16px", border: "none", borderRadius: "22px",
      background: "#0e7490", color: "#fff", font: "600 14px system-ui, sans-serif",
      boxShadow: "0 4px 14px rgba(0,0,0,.35)", cursor: "pointer",
    });
    b.addEventListener("click", () => {
      b.textContent = "Sending…";
      chrome.runtime.sendMessage({ type: "jdm-video", url: location.href }, (r) => {
        b.textContent = r && r.ok ? "✓ Sent to JDM" : "✗ Open JDM first";
        setTimeout(() => (b.textContent = "⬇ Download with JDM"), 2500);
      });
    });
    document.body.appendChild(b);
  }

  ensureButton();
  // YouTube is a single-page app: watch for navigation
  document.addEventListener("yt-navigate-finish", ensureButton);
  setInterval(ensureButton, 1500);
})();
