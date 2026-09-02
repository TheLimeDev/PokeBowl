# Changelog

## v0.1.1

Small one. The agent presets are real now instead of guesses — OpenClaw runs through its headless `agent exec` with your project as its workspace, Pi runs through print mode, and `pokebowl agents` tells you which ones you actually have installed before you queue anything.

- New presets: openclaw, pi
- New command: `pokebowl agents` shows installed state and versions
- OpenClaw tasks point at your project folder automatically

## v0.1.0

First one that actually works. Queue tasks, run them in the foreground or let the background daemon chew through them, every run keeps its own log.

- `add`, `list`, `run`, `up`, `down`, `status`, `logs`, `retry`, `rm`
- Agent presets: echo, claude, codex, aider, opencode, cursor
- File queue under `.pokebowl/`, one log per run under `.pokebowl/runs/`
- Tests with the standard library: `python -m unittest`
- Readmes in English, Chinese, Japanese, Spanish, German, French
