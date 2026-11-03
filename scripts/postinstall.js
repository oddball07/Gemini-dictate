"use strict";
// The npm package is a thin wrapper: it installs the bundled Python package (and its dependencies) with pip.
const { spawnSync } = require("child_process");
const path = require("path");

const ROOT = path.join(__dirname, "..");

function installPython() {
  const attempts = [["python", ["-m", "pip"]], ["py", ["-3", "-m", "pip"]]];
  for (const [cmd, args] of attempts) {
    const r = spawnSync(cmd, [...args, "install", "--upgrade", ROOT], { stdio: "inherit" });
    if (r.status === 0) return true;
  }
  return false;
}

module.exports = { installPython };

if (require.main === module) {
  if (process.platform !== "win32") {
    console.warn("gemini-dictate only works on Windows.");
    process.exit(0);
  }
  if (installPython()) {
    console.log("\n[gemini-dictate] Installed. Type:  dictate");
    console.log("Start with Windows:  dictate startup on\n");
  } else {
    console.warn("\n[gemini-dictate] Could not install the Python part automatically.");
    console.warn("Install Python 3 (tick 'Add to PATH') and run:  dictate --install-python\n");
  }
}
