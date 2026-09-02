AGENTS = {
    "echo": 'echo "{task}"',
    "claude": 'claude -p "{task}"',
    "codex": 'codex exec "{task}"',
    "aider": 'aider --message "{task}" --yes',
    "opencode": 'opencode run "{task}"',
    "cursor": 'cursor-agent "{task}"',
}


def names():
    return sorted(AGENTS.keys())


def resolve(title, agent=None, extra=None, command=None):
    clean = (title or "").strip().replace('"', "")
    if agent:
        template = AGENTS.get(agent, AGENTS["echo"])
        shell = template.replace("{task}", clean)
        if extra:
            shell = shell + " " + extra
        return shell
    if command:
        return command
    return "echo " + (title or "").strip()
