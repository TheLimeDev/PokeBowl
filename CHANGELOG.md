# Changelog

## v0.1.0

First one that actually works. Queue tasks, run them in the foreground or let the background daemon chew through them, every run keeps its own log.

- `add`, `list`, `run`, `up`, `down`, `status`, `logs`, `retry`, `rm`
- Agent presets: echo, claude, codex, aider, opencode, cursor
- File queue under `.pokebowl/`, one log per run under `.pokebowl/runs/`
- Tests with the standard library: `python -m unittest`
- Readmes in English, Chinese, Japanese, Spanish, German, French
