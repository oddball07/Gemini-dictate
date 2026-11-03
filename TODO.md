# To-do

## Done (needs a test on Windows)
- [x] Gemini window hidden (off-screen, no taskbar button), matched by process id
- [x] Hotkeys: Ctrl+Alt+Space (Transcribe), Ctrl+Alt+P (Prompt)
- [x] Result always copied to the clipboard
- [x] "Convert last transcript to a prompt" button
- [x] Fallback ladder: API models -> Gemini website -> offline formatting
- [x] Minimize: start hidden in the tray, hide button, Ctrl+Alt+W show / hide, error notifications while hidden
- [x] pip package (`dictate` command, `dictate-setup` helper) + npm wrapper

## Next
- [ ] Test on Windows: hidden start, Ctrl+Alt+W, tray notifications, website fallback
- [ ] Publish: PyPI (`python -m build`, `twine upload dist/*`), then npm (`npm publish`)
- [ ] Push to GitHub, add LICENSE, tag v1.1.0
- [ ] Test a clean install on a second PC (`pipx install gemini-dictate`)
- [ ] Frontend redesign (ideas in the chat; decide the toolkit first)
