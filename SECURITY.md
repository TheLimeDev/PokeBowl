# Security

PokeBowl runs shell commands you queue, on your own machine, with your own user. That is the whole threat model, so read this once.

## What to know

- Every task runs with your permissions. Only queue commands you understand, especially when the text came from someone else.
- The daemon runs things in the background. Check `pokebowl list` and the logs under `.pokebowl/runs/` if anything surprises you.
- Queue data and logs live in `.pokebowl/` next to your project. That folder can contain command output you may not want to share — keep it out of screenshots and pastes, or clear it with `pokebowl rm`.

## Reporting a problem

If you find a real security issue, open an issue in TheLimeDev/PokeBowl and say it is security related. Tell me what you ran, what you expected, and what happened instead. I will look at it as soon as I can and fix it in the open unless you ask me not to.

Supported right now: the latest `v0.x` release.
