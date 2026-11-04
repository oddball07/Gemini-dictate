# Gemini Dictate

Gemini Dictate is a Windows desktop widget for voice dictation. It uses speech recognition on the Gemini website and can paste the recognized text into the application you were using. Optionally, an AI model can clean up a transcript or turn it into a structured prompt.

**Speech recognition uses the Gemini website, not the Gemini API.** API keys are optional and only needed for API-based cleanup and prompt rewriting.

## Requirements

- Windows 10 or 11
- Python 3.9 or later, installed with Tcl/Tk
- Google Chrome, Microsoft Edge, or Brave
- A Google account and internet access
- A microphone

## Install from a Git clone

1. Install Python and a supported browser. During Python setup, enable **Add Python to PATH**.
2. Open PowerShell and clone the stable `main` branch:

   ```powershell
   git clone --branch main --single-branch https://github.com/oddball07/Gemini-dictate.git
   cd Gemini-dictate
   ```

   If you already cloned the repository, switch to `main` and update it:

   ```powershell
   git switch main
   git pull origin main
   ```

3. Create a virtual environment and install the project and its dependencies:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -e .
   ```

   If the `py` command is unavailable, create the environment with:

   ```powershell
   python -m venv .venv
   ```

4. Start the app using **one** of these methods:

   **Run the standalone widget file:**

   ```powershell
   .\.venv\Scripts\pythonw.exe .\gemini_widget.pyw
   ```

   **Run the installed Python package:**

   ```powershell
   .\.venv\Scripts\pythonw.exe -m gemini_dictate
   ```

   Both methods start the widget. Do not start both at the same time. By default, the widget starts hidden in the system tray. Press **Ctrl+Alt+W** or choose **Show widget** from the tray menu to display it.

5. On first launch, sign in to Gemini if prompted and allow microphone access. After sign-in, the dedicated Gemini browser window is normally hidden. Use **Gemini window** in the widget or **Show / hide Gemini window** in the tray menu when you need to bring it back.

## Verify the installation

Run these commands from the project folder:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pip show gemini-dictate
.\.venv\Scripts\python.exe -c "import tkinter, websocket, pystray, PIL, keyboard, pyperclip; from google import genai; import groq; print('All required imports succeeded')"
```

A successful setup should show Python 3.9 or later, report `No broken requirements found.`, display the `gemini-dictate` package information, and print `All required imports succeeded`.

To confirm the app works, start it using one of the commands above. Look for **Ready** in the widget or system tray tooltip. If the app asks you to sign in, sign in to Gemini and try again. You can test dictation in Notepad:

1. Press **Ctrl+Alt+Space**, speak, then press **Ctrl+Alt+Space** again.
2. Confirm the recognized text appears in Notepad. The final text is also copied to the clipboard.
3. Press **Ctrl+Alt+P** to try Prompt mode.

## Use the widget

- **Transcribe:** Click the round microphone button or press **Ctrl+Alt+Space** to start listening. Press it again to stop. By default, the transcript is used as-is. To clean it with AI, enable **Clean the transcript with AI (Transcribe mode)** in **Settings**.
- **Prompt mode:** Choose **Prompt** on the mode switch, or press **Ctrl+Alt+P**. The transcript is rewritten as a prompt by the selected model.
- **Show or hide the widget:** Press **Ctrl+Alt+W** or use the system tray menu.
- **Cancel:** While recording, click **Cancel** to discard the current recording.
- **Convert last to prompt:** Click **Convert last to prompt** to process the last transcript again and copy the result without pasting it.
- **Settings:** Click the gear icon to open the **General**, **Prompts**, and **Activity** tabs. Choose a model, edit or reset prompts, view recent transcripts/results, run diagnostics, or open the error log.
- **Clipboard and paste:** Results are copied to the clipboard and, when possible, pasted into the application that had focus before you used the widget. If automatic pasting is not possible, paste with **Ctrl+V**.
- **System tray:** The tray menu can show or hide the widget, start either mode, show the Gemini browser window, convert the last transcript to a prompt, or quit the app.

## Optional AI provider keys

Gemini website speech recognition does not require an API key. The model menu includes **Gemini website**, which uses the signed-in browser directly. API keys are only needed if you want to use API models for transcript cleanup or prompt rewriting.

| Provider | Environment variable | Optional key file under your user home folder |
| --- | --- | --- |
| Groq | `GROQ_API_KEY` | `.groq_key` |
| Gemini API | `GEMINI_API_KEY` | `.gemini_key` |
| Cerebras | `CEREBRAS_API_KEY` | `.cerebras_key` |
| OpenRouter | `OPENROUTER_API_KEY` | `.openrouter_key` |

Set a key in your Windows user environment variables or save it in the matching file under `%USERPROFILE%`. Environment variables take precedence over key files. For example, to set a Groq key for your Windows user account from PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("GROQ_API_KEY", "your-key", "User")
```

Restart Gemini Dictate after adding or changing a key. In **Settings** (gear icon), choose **Auto** to try available API models with fallbacks, **Gemini website** to use Gemini directly, or **Off** to disable AI processing. Provider API usage may be subject to that provider's limits and terms.

## Start with Windows (optional)

To enable the installed package's startup command, activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then run:

```powershell
dictate-setup startup on
```

To check or disable startup later:

```powershell
dictate-setup startup status
dictate-setup startup off
```

The startup setting is stored for your Windows user account. To leave the virtual environment, run `deactivate`.

## Check which app file is running

The widget looks the same regardless of how it was started. To inspect its process from PowerShell, run:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -in @("pythonw.exe", "python.exe", "pyw.exe", "dictate.exe") } |
  Select-Object ProcessId, Name, ExecutablePath, CommandLine
```

Check the `CommandLine` column:

- A command line containing `gemini_widget.pyw` means the standalone file is running.
- A command line containing `-m gemini_dictate` means the package entry point is running. With the editable install above, that loads the package from `src/gemini_dictate/`, including `app.py`.
- If the process is listed as `dictate.exe`, the installed GUI command was used.

To see where the package is installed from, run:

```powershell
.\.venv\Scripts\python.exe -m pip show gemini-dictate
```

For an editable install from this clone, the package information points back to the project folder. The standalone script and package entry point are separate ways to start the application; do not start both at once.

## How it works

1. The app launches Chrome, Edge, or Brave in app mode at Gemini using a dedicated browser profile and a local Chrome DevTools Protocol connection.
2. When dictation starts, it activates Gemini's microphone control. When you stop, it reads the recognized text from Gemini's prompt editor.
3. Depending on the selected mode and settings, the app uses the transcript as-is, sends it to the selected API model, or uses the Gemini website for prompt processing. Auto mode tries available API models with fallbacks.
4. The result is copied to the clipboard and pasted into the previously focused application when possible.

Gemini requires an active sign-in and working microphone access. If you choose an API model, the transcript is also sent to that provider for processing. Avoid dictating sensitive information unless you are comfortable with the relevant services' data policies.

## Data and privacy

The app stores settings and its dedicated browser profile under your Windows user home folder:

- Gemini browser profile: `%USERPROFILE%\gemini_widget_profile`
- App settings: `%USERPROFILE%\gemini_widget_settings.json`
- Editable prompts: `%USERPROFILE%\gemini_widget_prompts.json`
- Error log: `%USERPROFILE%\gemini_widget_errors.log`
- Optional API key files: `%USERPROFILE%\.groq_key`, `%USERPROFILE%\.gemini_key`, `%USERPROFILE%\.cerebras_key`, and `%USERPROFILE%\.openrouter_key`

Speech is sent to Google's Gemini website for recognition. If you select an API model for cleanup or prompt rewriting, the transcript is also sent to that AI provider. The DevTools connection is intended for local use; do not expose its debugging port to other machines.

## Troubleshooting

- **Python package import error:** Install again using the virtual environment's Python: `.\.venv\Scripts\python.exe -m pip install -e .`.
- **Browser not found:** Install Chrome, Edge, or Brave. If it is installed in a non-standard location, set `BROWSER_PATH` near the top of the Python file you launch.
- **Sign-in or microphone issue:** Use **Gemini window** or the tray menu to show the browser, sign in, and check Gemini's microphone permission. Then retry.
- **Gemini controls not detected:** Use **Diagnose Gemini** in the Settings drawer. A Gemini website update may have changed its interface.
- **AI request fails:** Check the selected model, API key, network connection, and provider limits. Use **Open log** in Settings for error details.
- **Port conflict:** The app uses local port `9223`. If that port is already in use, change `CDP_PORT` near the top of the Python file you launch and restart the app.
