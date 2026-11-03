"""Brings back Chromium-style windows (VS Code, Brave, Chrome, Edge...) that an OLD version of the widget wrongly
pushed off-screen. Minimized windows and the widget's own hidden Gemini window are left alone."""
import ctypes
import subprocess

CDP_PORT = 9223


def _gemini_pid():
    try:
        out = subprocess.run(["netstat", "-ano", "-p", "TCP"], capture_output=True, text=True,
                             creationflags=0x08000000).stdout
        for line in out.splitlines():
            p = line.split()
            if len(p) >= 5 and p[1].endswith(":" + str(CDP_PORT)) and p[2].endswith(":0"):
                return int(p[-1])
    except Exception:
        pass
    return None


def main():
    from ctypes import wintypes
    u32 = ctypes.windll.user32
    skip_pid = _gemini_pid()
    rescued = []
    Enum = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def cb(h, _):
        if h is None:
            return True
        hw = ctypes.c_void_p(h)
        if not u32.IsWindowVisible(hw) or u32.IsIconic(hw):
            return True
        cls = ctypes.create_unicode_buffer(64)
        u32.GetClassNameW(hw, cls, 64)
        if cls.value != "Chrome_WidgetWin_1":
            return True
        pid = ctypes.c_ulong(0)
        u32.GetWindowThreadProcessId(hw, ctypes.byref(pid))
        if skip_pid and pid.value == skip_pid:
            return True
        r = wintypes.RECT()
        u32.GetWindowRect(hw, ctypes.byref(r))
        if r.left > -20000 or r.top > -20000:
            return True
        title = ctypes.create_unicode_buffer(256)
        u32.GetWindowTextW(hw, title, 256)
        zoomed = bool(u32.IsZoomed(hw))
        if zoomed:
            u32.ShowWindow(hw, 9)                                   # SW_RESTORE
        ex = u32.GetWindowLongW(hw, -20)
        u32.SetWindowLongW(hw, -20, (ex & ~0x80) | 0x40000)          # normal window, taskbar button back
        u32.SetWindowPos(hw, None, 80 + 30 * len(rescued), 80 + 30 * len(rescued), 0, 0, 0x1 | 0x4 | 0x20)
        if zoomed:
            u32.ShowWindow(hw, 3)                                   # SW_MAXIMIZE
        rescued.append(title.value or "(no title)")
        return True

    u32.EnumWindows(Enum(cb), 0)
    if rescued:
        print("Brought back %d window(s):" % len(rescued))
        for t in rescued:
            print("  -", t)
    else:
        print("No off-screen windows found. If a window is really gone, check Task Manager; VS Code restores it")
        print("when you reopen it, and Brave can reopen it with Ctrl+Shift+T.")
    return len(rescued)
