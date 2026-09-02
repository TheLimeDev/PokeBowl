# 🍚 PokeBowl

Ich hatte keine Lust mehr, Agenten bei der Arbeit zuzusehen. Aufgabe reingeben, etwas anderes machen, später das Protokoll lesen — dafür habe ich PokeBowl gebaut.

Es nimmt die Agenten, die du eh schon benutzt — Claude, Codex, Aider, OpenCode, Cursor — und lässt sie im Hintergrund laufen. Du sammelst Aufgaben, ein kleiner Daemon arbeitet sie ab, jeder Lauf landet in seiner eigenen Datei. Keine Server, keine Konten, keine Abhängigkeiten. Eine Python-Datei, dein Rechner, fertig.

## Wie es läuft

Du legst eine Aufgabe mit dem Befehl an, der laufen soll. Das landet in `.pokebowl/` neben deinem Projekt. Der Daemon nimmt sie der Reihe nach, führt sie aus und markiert done oder failed. Das Protokoll schaust du dir an, wann du willst.

```
add  ->  pending  ->  Daemon führt aus  ->  done / failed
```

## Bekommen

Am einfachsten über Homebrew mit meinem Tap:

```
brew tap TheLimeDev/pokebowl
brew install pokebowl
```

Oder nimm einfach `pokebowl.py` und starte es mit Python 3.9 oder neuer. Es gibt nichts zu installieren.

## Kurzstart

Etwas einreihen:

```
pokebowl add "say hi" "echo hi"
```

Sofort im Vordergrund ausführen:

```
pokebowl run
pokebowl logs 1
```

Oder dem Daemon überlassen, während du etwas anderes machst:

```
pokebowl up
pokebowl add "lint this folder" "python -m py_compile pokebowl.py"
pokebowl status
pokebowl logs 2
pokebowl down
```

## Mit deinen Agenten

Statt den ganzen Befehl zu schreiben, nennst du den Agenten und PokeBowl ergänzt den Rest:

```
pokebowl add "fix the login redirect" --agent claude
pokebowl add "migrate the db utils" --agent codex
pokebowl add "clean up imports" --agent aider
```

Diese Namen gehen: `echo`, `claude`, `codex`, `aider`, `opencode`, `cursor`. Das Agentenprogramm muss bei dir installiert sein — PokeBowl führt es nur für dich aus und hebt den Beleg auf.

Ansehen, nochmal einreihen und löschen wie erwartet:

```
pokebowl list
pokebowl retry 3
pokebowl rm 3
pokebowl list --json
```

## Wo alles liegt

Alles steckt in `.pokebowl/` dort, wo du es startest:

- `tasks.json` — die Warteschlange
- `runs/<id>.log` — Ausgabe jedes Laufs
- `daemon.pid` — Prozessnummer im Hintergrund

Woandershin mit `--dir`:

```
pokebowl --dir C:\work\site add "build" "npm run build"
```

## Warum so

Die großen gehosteten Agenten machen alle dieselbe Schleife — klonen, auf einer VM laufen, PR aufmachen. Gut, bis man etwas Kleines, Lokales, Eigenes will. PokeBowl lässt die Cloud weg. Es vertraut den Werkzeugen, die du schon installiert hast, und gibt ihnen eine Schlange und eine Nachtschicht.

Wenn etwas klemmt, mach ein Issue in TheLimeDev/PokeBowl auf und schreib dazu, was du ausgeführt hast. Ich lese alle.

MIT — siehe LICENSE.
