// Theme toggle, copy buttons and read-along for the narration.
(function () {
  "use strict";
  var root = document.documentElement;

  // Theme: dark by default, remembered per browser when storage is available.
  var themeBtn = document.getElementById("theme");
  function setTheme(t) {
    root.setAttribute("data-theme", t);
    if (themeBtn) themeBtn.textContent = t === "dark" ? "Light theme" : "Dark theme";
    try { localStorage.setItem("theme", t); } catch (e) {}
  }
  try { var saved = localStorage.getItem("theme"); if (saved) setTheme(saved); } catch (e) {}
  if (themeBtn) themeBtn.addEventListener("click", function () {
    setTheme(root.getAttribute("data-theme") === "light" ? "dark" : "light");
  });

  // Copy to clipboard, with a fallback for browsers without the async API.
  var toast = document.getElementById("toast");
  function say(msg) {
    toast.textContent = msg;
    toast.classList.add("show");
    clearTimeout(say.t);
    say.t = setTimeout(function () { toast.classList.remove("show"); }, 1600);
  }
  function copy(text, msg) {
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); say(msg); } catch (e) { say("Copy failed. Select the text instead."); }
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { say(msg); }, fallback);
    } else { fallback(); }
  }
  document.querySelectorAll("[data-copy-post]").forEach(function (b) {
    b.addEventListener("click", function () {
      var n = b.getAttribute("data-copy-post");
      copy(document.getElementById("text-" + n).textContent, "Post " + n + " copied");
    });
  });
  var all = document.getElementById("copy-all");
  if (all) all.addEventListener("click", function () {
    var parts = [];
    document.querySelectorAll(".post-text").forEach(function (p) { parts.push(p.textContent); });
    copy(parts.join("\n\n---\n\n"), "Whole thread copied");
  });

  // Read-along: highlight the post being read and show the current sentence.
  var audio = document.getElementById("narration");
  var data = JSON.parse(document.getElementById("narration-data").textContent);
  var now = document.getElementById("now");
  var current = 0;
  function mark(t) {
    var post = 0, cue = null;
    data.posts.forEach(function (p) { if (t >= p.start - 0.05 && t <= p.end + 0.8) post = p.post; });
    data.cues.forEach(function (c) { if (t >= c.start && t <= c.end + 0.3) cue = c; });
    if (post !== current) {
      document.querySelectorAll(".post.is-reading").forEach(function (el) { el.classList.remove("is-reading"); });
      if (post) document.getElementById("post-" + post).classList.add("is-reading");
      current = post;
    }
    if (cue) {
      now.innerHTML = "";
      var tag = document.createElement("span");
      tag.className = "mono";
      tag.textContent = "Post " + cue.post + " of " + data.posts.length;
      now.appendChild(tag);
      now.appendChild(document.createTextNode(cue.text));
    }
  }
  if (audio) {
    audio.addEventListener("timeupdate", function () { mark(audio.currentTime); });
    audio.addEventListener("ended", function () { mark(-1); });
    // Some servers (python -m http.server, for one) do not support range
    // requests, so the browser cannot seek. Load the file into memory once and
    // seek there instead.
    var seekReady = null;
    function whenSeekable() {
      if (seekReady) return seekReady;
      var ok = audio.seekable.length && audio.seekable.end(0) > 1;
      if (ok || !window.fetch || location.protocol === "file:") { seekReady = Promise.resolve(); return seekReady; }
      seekReady = fetch(audio.currentSrc || audio.querySelector("source").src)
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.blob(); })
        .then(function (blob) {
          return new Promise(function (resolve) {
            audio.addEventListener("loadedmetadata", resolve, { once: true });
            audio.src = URL.createObjectURL(blob);
            audio.load();
          });
        })
        .catch(function () {});
      return seekReady;
    }
    document.querySelectorAll("[data-play]").forEach(function (b) {
      b.addEventListener("click", function () {
        var p = data.posts[Number(b.getAttribute("data-play")) - 1];
        whenSeekable().then(function () {
          audio.currentTime = p.start;
          mark(p.start);
          audio.play();
        });
      });
    });
  }
})();
