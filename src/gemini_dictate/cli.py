"""dictate-setup: small helper commands (kept light, so they start instantly and never open the widget).

  dictate-setup startup on|off|status   start Gemini Dictate when Windows starts
  dictate-setup rescue                  bring back windows an old version pushed off-screen
  dictate-setup migrate                 remove leftovers of the old gemini_widget.pyw / setup_dictate.bat install
"""
import argparse
import os
import sys

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
RUN_NAME = "GeminiDictate"


def _pythonw():
    exe = sys.executable
    w = os.path.join(os.path.dirname(exe), "pythonw.exe")
    return w if os.path.exists(w) else exe


def startup(action):
    import winreg
    if action == "on":
        cmd = f'"{_pythonw()}" -m gemini_dictate'
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as k:
            winreg.SetValueEx(k, RUN_NAME, 0, winreg.REG_SZ, cmd)
        print("Gemini Dictate will now start with Windows (hidden in the tray).")
    elif action == "off":
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as k:
                winreg.DeleteValue(k, RUN_NAME)
            print("Removed from Windows startup.")
        except FileNotFoundError:
            print("It was not set to start with Windows.")
    else:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as k:
                print("Starts with Windows:", winreg.QueryValueEx(k, RUN_NAME)[0])
        except FileNotFoundError:
            print("Does not start with Windows. Turn it on with:  dictate-setup startup on")


def migrate():
    done = []
    launcher = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WindowsApps", "dictate.cmd")
    if os.path.exists(launcher):
        try:
            text = open(launcher, encoding="utf-8", errors="ignore").read().lower()
        except OSError:
            text = ""
        if "gemini_widget.pyw" in text:               # only our own old launcher, never someone else's file
            os.replace(launcher, launcher + ".old")
            done.append("renamed the old launcher to " + launcher + ".old")
    lnk = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs",
                       "Startup", "Gemini Dictate.lnk")
    if os.path.exists(lnk):
        os.remove(lnk)
        done.append("removed the old startup shortcut")
    print("\n".join(done) if done else "Nothing to clean up.")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="dictate-setup", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    st = sub.add_parser("startup", help="start with Windows")
    st.add_argument("action", nargs="?", choices=["on", "off", "status"], default="status")
    sub.add_parser("rescue", help="bring back off-screen windows")
    sub.add_parser("migrate", help="clean up the old script-based install")
    args = ap.parse_args(argv)
    if args.cmd is None:
        ap.print_help()
        return 0
    if sys.platform != "win32":
        print("Gemini Dictate only works on Windows.")
        return 1
    if args.cmd == "startup":
        startup(args.action)
    elif args.cmd == "rescue":
        from .rescue import main as rescue_main
        rescue_main()
    elif args.cmd == "migrate":
        migrate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
