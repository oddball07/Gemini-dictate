# Gemini Dictate

Gemini Dictate is a small Windows desktop widget for voice dictation. It uses the microphone and speech recognition on the Gemini website, then puts the resulting text into the app you were using. Optionally, an AI model can clean up the transcript or turn it into a well-structured prompt.

**Speech recognition happens on the Gemini website, not through an AI API.** API keys are only needed for the optional text cleanup and prompt-writing features.

## Requirements

- Windows 10 or 11
- Python 3 with Tcl/Tk included (the standard Python installer for Windows includes it)
- Google Chrome or Microsoft Edge
- A Google account signed in to [Gemini](https://gemini.google.com/)
- Internet access

## Quick setup

1. Install Python 3 for Windows and make sure **Add Python to PATH** is selected. Install Chrome or Edge if needed.
2. Open PowerShell in this project folder and install the Python packages:

   ```powershell
   py -m pip install websocket-client pystray pillow keyboard pyperclip google-genai groq
   ```

3. Start the widget by double-clicking [gemini_widget.pyw](./gemini_widget.pyw), or run:

   ```powershell
   pyw .\gemini_widget.pyw
   ```

4. If the Gemini window appears, sign in to your Google account. The app keeps a separate browser profile for this tool under your user home directory. Once signed in, the Gemini window is normally parked off-screen; use **Show / hide Gemini window** in the tray menu when you need to access it.
5. Allow microphone access if prompted. The widget should show **Ready** when Gemini is available.

The widget can transcribe without any AI API keys. To use AI cleanup or prompt mode, configure at least one provider key as described below.

## Using the widget

- **Transcribe**: click the button or press **Ctrl+Alt+Space** to start listening. Press it again to stop. By default, the transcript is used as-is; enable **Transcribe + AI clean** in the expanded panel to request AI cleanup.
- **Prompt mode**: click the button or press **Ctrl+Alt+P** to dictate a request. When you stop, the transcript is sent to an available AI model and rewritten as a prompt.
- The result is copied to the clipboard and, when possible, pasted into the app that had focus before you used the widget. If pasting is not possible, paste it yourself with **Ctrl+V**.
- The tray icon menu can show or hide the widget, start either mode, show Gemini, or quit the app.
- Expand the widget's **▾** panel to choose a model, edit or reset the prompts, view the last transcript and result, or open the error log.

## Optional AI provider keys

AI text processing supports these providers:

| Provider | Environment variable | Optional key file in your home folder |
| --- | --- | --- |
| Groq | `GROQ_API_KEY` | `.groq_key` |
| Gemini API | `GEMINI_API_KEY` | `.gemini_key` |
| Cerebras | `CEREBRAS_API_KEY` | `.cerebras_key` |
| OpenRouter | `OPENROUTER_API_KEY` | `.openrouter_key` |

Set a key in your Windows user environment variables, or save it in the matching file under `%USERPROFILE%`. Environment variables take precedence over key files. For example, from PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("GROQ_API_KEY", "your-key", "User")
```

Restart Gemini Dictate after adding or changing a key. In the model selector, **Auto** tries available models with fallbacks; you can also select a model or turn AI processing off. Provider API usage may be subject to that provider's limits and terms.

## How it works

1. The app launches Chrome or Edge in app mode at Gemini using a dedicated profile and a local Chrome DevTools Protocol connection. It keeps that browser window hidden when it is not needed.
2. When dictation starts, it activates Gemini's microphone control. On stop, it reads the recognized text from Gemini's prompt editor.
3. Depending on the selected mode and settings, the app either uses the transcript directly or sends it to a configured text-generation provider. In Auto mode, it can fall back to basic local cleanup if no AI model succeeds.
4. The final text is copied to the clipboard and pasted into the previously focused application when possible.

The Gemini website requires an active sign-in and working microphone access. API-generated cleanup and prompts send the transcript to the selected AI provider; avoid dictating sensitive information unless you are comfortable with the relevant services' data policies.

## Packages

The app uses these third-party Python packages:

| Package | Purpose |
| --- | --- |
| `websocket-client` | Communicates with Chrome or Edge through its DevTools Protocol |
| `pystray` | Windows notification-area (system tray) icon and menu |
| `Pillow` (`PIL`) | Creates the tray icon |
| `keyboard` | Global hotkeys and pasting text |
| `pyperclip` | Clipboard access |
| `google-genai` | Gemini API text processing |
| `groq` | Groq API text processing |

Tkinter and the other standard-library modules used by the app come with Python.

## Optional: start with Windows

Run [setup_dictate.bat](./setup_dictate.bat) once to add a `dictate` command and a shortcut to the Windows Startup folder. The batch file also starts the widget immediately. It requires `pythonw.exe` to be on `PATH`. **Review the batch file before running it:** it may rename an existing command found as `dictate` to a `.old` filename, and it changes your user-level Windows command/startup setup. You can instead start [gemini_widget.pyw](./gemini_widget.pyw) manually whenever you need it.

## Troubleshooting

- **Python package import error:** rerun the `py -m pip install ...` command above using the same Python installation that launches the widget.
- **Chrome or Edge not found:** install one of the supported browsers. If it is installed in a non-standard location, set `BROWSER_PATH` near the top of [gemini_widget.pyw](./gemini_widget.pyw) to its executable path.
- **Sign-in or microphone issue:** choose **Show / hide Gemini window** from the tray, sign in, and check the browser's site microphone permission. Then retry.
- **Gemini controls not detected:** use **Diagnose Gemini** in the expanded panel; a Gemini website update may have changed its interface.
- **AI request fails:** verify the provider key, selected model, network connection, and provider limits. Use **Open log** for error details.
- **Port conflict:** if local port `9223` is already in use, change `CDP_PORT` near the top of [gemini_widget.pyw](./gemini_widget.pyw) and restart the app.

Settings, editable prompts, the dedicated browser profile, and the error log are stored under your Windows user home directory. The DevTools connection is intended for local use; do not expose its debugging port to other machines.
