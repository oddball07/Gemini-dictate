#!/usr/bin/env node
"use strict";
const { spawn, spawnSync } = require("child_process");

function where(cmd) {
  const r = spawnSync("where", [cmd], { encoding: "utf8" });
  return r.status === 0 ? (r.stdout.split(/\r?\n/).find(Boolean) || "").trim() || null : null;
}

if (process.platform !== "win32") {
  console.error("gemini-dictate only works on Windows.");
  process.exit(1);
}

const args = process.argv.slice(2);

if (args[0] === "--install-python") {
  process.exit(require("../scripts/postinstall.js").installPython() ? 0 : 1);
}

if (args.length) {
  // dictate startup on|off|status   dictate rescue   dictate migrate   dictate --help
  const exe = where("python") ? ["python", []] : where("py") ? ["py", ["-3"]] : null;
  if (!exe) { console.error("Python was not found."); process.exit(1); }
  const sub = args[0] === "--help" || args[0] === "-h" ? ["--help"] : args;
  process.exit(spawnSync(exe[0], [...exe[1], "-m", "gemini_dictate.cli", ...sub], { stdio: "inherit" }).status || 0);
}

const py = where("pythonw") || where("pyw");
if (!py) { console.error("Python was not found. Install Python 3 (tick 'Add to PATH')."); process.exit(1); }
spawn(py, ["-m", "gemini_dictate"], { detached: true, stdio: "ignore", windowsHide: true }).unref();
console.log("Gemini Dictate started (it lives in the tray; Ctrl+Alt+W shows the widget).");
