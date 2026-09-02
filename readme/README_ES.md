# 🍚 PokeBowl

Me cansé de mirar cómo trabaja el agente. Quería dejarle una tarea, seguir con lo mío y volver cuando ya estuviera hecha, con su registro. Por eso hice PokeBowl.

Funciona con los agentes que ya usas — Claude, Codex, Aider, OpenCode, Cursor — y los pone en segundo plano. Encolas trabajo, un proceso pequeño lo va sacando, cada ejecución queda en su archivo de registro. Sin servidores, sin cuentas, sin dependencias. Un solo archivo de Python.

## Cómo funciona

Agregas una tarea con el comando que quieres correr. Se guarda en `.pokebowl/` al lado de tu proyecto. El demonio las toma una por una, las corre y las marca done o failed. Revisas el registro cuando quieras.

```
add  ->  pending  ->  el demonio lo corre  ->  done / failed
```

## Conseguirlo

Lo más fácil es Homebrew con mi tap:

```
brew tap TheLimeDev/pokebowl
brew install pokebowl
```

O toma `pokebowl.py` y córrelo con Python 3.9 o más nuevo. No hay nada que instalar.

## Arranque rápido

Encola algo:

```
pokebowl add "say hi" "echo hi"
```

Córrelo al momento, en primer plano:

```
pokebowl run
pokebowl logs 1
```

O déjalo al demonio mientras haces otra cosa:

```
pokebowl up
pokebowl add "lint this folder" "python -m py_compile pokebowl.py"
pokebowl status
pokebowl logs 2
pokebowl down
```

## Con tus agentes

En vez de escribir el comando completo, nombra al agente y PokeBowl lo completa:

```
pokebowl add "fix the login redirect" --agent claude
pokebowl add "migrate the db utils" --agent codex
pokebowl add "clean up imports" --agent aider
```

Nombres soportados: `echo`, `claude`, `codex`, `aider`, `opencode`, `cursor`. El programa del agente tiene que estar instalado en tu máquina — PokeBowl solo lo corre por ti y guarda el comprobante.

Lo de siempre para revisar y ordenar:

```
pokebowl list
pokebowl retry 3
pokebowl rm 3
pokebowl list --json
```

## Dónde queda todo

Todo vive en `.pokebowl/` dentro de la carpeta donde lo corres:

- `tasks.json` — la cola
- `runs/<id>.log` — salida de cada ejecución
- `daemon.pid` — id del proceso de fondo

Apunta a otro lado con `--dir`:

```
pokebowl --dir C:\work\site add "build" "npm run build"
```

## Por qué así

Los agentes grandes hacen todos lo mismo — clonar, correr en una máquina virtual, abrir un PR. Está bien hasta que quieres algo chico, local y tuyo. PokeBowl se salta la nube. Confía en las herramientas que ya instalaste y les da una cola y un turno de noche.

Si algo te falla, abre un issue en TheLimeDev/PokeBowl y cuéntame qué corriste. Los leo todos.

MIT — ver LICENSE.
