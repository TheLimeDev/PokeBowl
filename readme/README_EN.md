# 🍚 PokeBowl

I got tired of babysitting coding agents. I wanted to throw a task over my shoulder, keep working, and come back to a finished log. So I built PokeBowl.

It takes any coding agent you already use — Claude, Codex, Aider, OpenCode, Cursor — and runs it in the background. You queue work, a small daemon chews through it, every run lands in its own log file. That's the whole idea.

No servers, no accounts, no dependencies. One Python file, your machine, done.

## How it works

You add a task with the shell command you want run. PokeBowl stores it under `.pokebowl/` next to your project. The daemon picks up pending tasks one by one, runs them, and marks them done or failed. You check the log whenever.

```
add  ->  pending  ->  daemon runs it  ->  done / failed
```

## Get it

The easiest way is Homebrew with my tap:

```
brew tap TheLimeDev/pokebowl
brew install pokebowl
```

Or just take `pokebowl.py` and run it with Python 3.9 or newer. There is nothing to install.

## Quick start

Queue something:

```
pokebowl add "say hi" "echo hi"
```

Run it right now in the foreground:

```
pokebowl run
pokebowl logs 1
```

Or let the daemon handle it while you do other stuff:

```
pokebowl up
pokebowl add "lint this folder" "python -m py_compile pokebowl.py"
pokebowl status
pokebowl logs 2
pokebowl down
```

## Using your agents

Instead of writing the full command, name an agent and PokeBowl fills it in:

```
pokebowl add "fix the login redirect" --agent claude
pokebowl add "migrate the db utils" --agent codex
pokebowl add "clean up imports" --agent aider
```

Supported names: `echo`, `claude`, `codex`, `aider`, `opencode`, `cursor`. The agent program itself still needs to be on your machine — PokeBowl just runs it for you in the background and keeps the receipt.

List, retry, and remove work the way you'd expect:

```
pokebowl list
pokebowl retry 3
pokebowl rm 3
pokebowl list --json
```

## Where things live

Everything sits in `.pokebowl/` inside the folder where you run it:

- `tasks.json` — the queue
- `runs/<id>.log` — output of each run
- `daemon.pid` — background process id

Point it somewhere else with `--dir`:

```
pokebowl --dir C:\work\site add "build" "npm run build"
```

## Why I made it this way

The big hosted agents all do the same loop — clone, run on a VM, open a PR. That's great until you want something small, local, and yours. PokeBowl skips the cloud part. It trusts the tools you already installed and just gives them a queue and a night shift.

If it breaks for you, open an issue in TheLimeDev/PokeBowl and tell me what you ran. I read all of them.

More languages live in the `readme/` folder.

MIT — see LICENSE.
