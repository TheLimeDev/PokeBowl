# Contributing

Nice, you want to poke at PokeBowl. It is a small project on purpose, so the rules are short.

## Setup

You need Python 3.9 or newer and nothing else. No packages to install, the standard library is all there is.

Run the checks like this:

```
python -m unittest
python pokebowl.py add "smoke" "echo ok"
python pokebowl.py run
python pokebowl.py logs 1
```

Clean up after yourself — the commands above create a `.pokebowl/` folder where you run them. Delete it when you are done playing around.

## Style

- Standard library only. If a change needs a new dependency, it probably does not belong here.
- No inline comments. Name things well enough that they read on their own.
- Keep the human tone in docs and readmes. Write like you talk.

## Sending changes

Open an issue or a pull request in TheLimeDev/PokeBowl. Small, working beats big and half-done. Show what you ran and what came out.
