console.log("Библиотечная система загружена");
function updateStats() { fetch("/api/health").then(r => r.json()).then(console.log); }