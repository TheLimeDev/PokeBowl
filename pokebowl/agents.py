import shutil
import subprocess

SPECS = {
    "echo": {
        "run": 'echo "{task}"',
        "probe": None,
        "hint": "always around, good for trying PokeBowl",
    },
    "claude": {
        "run": 'claude -p "{task}"',
        "probe": ["claude", "--version"],
        "hint": "Claude Code, print mode runs it headless",
    },
    "codex": {
        "run": 'codex exec "{task}"',
        "probe": ["codex", "--version"],
        "hint": "OpenAI Codex CLI, exec runs non-interactive",
    },
    "aider": {
        "run": 'aider --message "{task}" --yes',
        "probe": ["aider", "--version"],
        "hint": "applies the change straight to your files",
    },
    "opencode": {
        "run": 'opencode run "{task}"',
        "probe": ["opencode", "--version"],
        "hint": "run executes one shot and exits",
    },
    "cursor": {
        "run": 'cursor-agent "{task}"',
        "probe": ["cursor-agent", "--version"],
        "hint": "Cursor headless agent",
    },
    "openclaw": {
        "run": 'openclaw agent exec "{task}" --cwd "{dir}"',
        "probe": ["openclaw", "--version"],
        "hint": "headless run, exits 0 on success, 1 on error, 2 on timeout",
    },
    "pi": {
        "run": 'pi -p "{task}"',
        "probe": ["pi", "--version"],
        "hint": "print mode answers once and exits",
    },
}


def names():
    return sorted(SPECS.keys())


def clean_title(title):
    return (title or "").strip().replace('"', "")


def resolve(title, agent=None, extra=None, command=None, workdir=None):
    if command:
        return command
    if agent:
        spec = SPECS.get(agent, SPECS["echo"])
        shell = spec["run"].replace("{task}", clean_title(title))
        shell = shell.replace("{dir}", workdir or ".")
        if extra:
            shell = shell + " " + extra
        return shell
    return "echo " + (title or "").strip()


BINARIES = {
    "echo": "echo",
    "claude": "claude",
    "codex": "codex",
    "aider": "aider",
    "opencode": "opencode",
    "cursor": "cursor-agent",
    "openclaw": "openclaw",
    "pi": "pi",
}


def detect():
    found = {}
    for name in names():
        path = True if name == "echo" else shutil.which(BINARIES[name])
        version = ""
        probe = SPECS[name]["probe"]
        if path and probe:
            try:
                out = subprocess.run(probe, capture_output=True, text=True, timeout=15)
                lines = ((out.stdout or "") + (out.stderr or "")).strip().splitlines()
                version = lines[0][:80] if lines else ""
            except (OSError, subprocess.SubprocessError):
                version = ""
        found[name] = {
            "installed": bool(path),
            "version": version,
            "hint": SPECS[name]["hint"],
        }
    return found
