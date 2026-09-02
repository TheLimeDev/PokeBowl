# 🍚 PokeBowl

J'en ai eu marre de surveiller les agents. Je voulais confier une tâche, continuer mon travail et revenir quand c'est fini, avec le journal. Alors j'ai fait PokeBowl.

Il prend les agents que tu utilises déjà — Claude, Codex, Aider, OpenCode, Cursor — et les fait tourner en arrière-plan. Tu files des tâches, un petit démon les traite, chaque exécution finit dans son fichier. Pas de serveurs, pas de comptes, pas de dépendances. Un seul fichier Python, ta machine, c'est tout.

## Comment ça marche

Tu ajoutes une tâche avec la commande à lancer. C'est stocké dans `.pokebowl/` à côté de ton projet. Le démon les prend une par une, les lance, et les marque done ou failed. Tu lis le journal quand tu veux.

```
add  ->  pending  ->  le démon l'exécute  ->  done / failed
```

## L'obtenir

Le plus simple, c'est Homebrew avec mon tap :

```
brew tap TheLimeDev/pokebowl
brew install pokebowl
```

Ou prends `pokebowl.py` et lance-le avec Python 3.9 ou plus récent. Il n'y a rien à installer.

## Démarrage rapide

Mets quelque chose en file :

```
pokebowl add "say hi" "echo hi"
```

Lance-le tout de suite, au premier plan :

```
pokebowl run
pokebowl logs 1
```

Ou laisse le démon s'en charger pendant que tu fais autre chose :

```
pokebowl up
pokebowl add "lint this folder" "python -m py_compile pokebowl.py"
pokebowl status
pokebowl logs 2
pokebowl down
```

## Avec tes agents

Au lieu d'écrire la commande entière, donne le nom de l'agent et PokeBowl complète :

```
pokebowl add "fix the login redirect" --agent claude
pokebowl add "migrate the db utils" --agent codex
pokebowl add "clean up imports" --agent aider
```

Noms acceptés : `echo`, `claude`, `codex`, `aider`, `opencode`, `cursor`. Le programme de l'agent doit être installé sur ta machine — PokeBowl le lance juste pour toi et garde le reçu.

Lister, relancer et supprimer comme d'habitude :

```
pokebowl list
pokebowl retry 3
pokebowl rm 3
pokebowl list --json
```

## Où tout vit

Tout est dans `.pokebowl/` là où tu le lances :

- `tasks.json` — la file
- `runs/<id>.log` — sortie de chaque exécution
- `daemon.pid` — numéro du processus de fond

Ailleurs avec `--dir` :

```
pokebowl --dir C:\work\site add "build" "npm run build"
```

## Pourquoi comme ça

Les grands agents hébergés font tous la même boucle — cloner, tourner sur une VM, ouvrir une PR. Très bien jusqu'à ce qu'on veuille un truc petit, local, à soi. PokeBowl saute la partie cloud. Il fait confiance aux outils déjà installés et leur donne juste une file et une équipe de nuit.

Si ça coince, ouvre une issue dans TheLimeDev/PokeBowl et dis-moi ce que tu as lancé. Je les lis toutes.

MIT — voir LICENSE.
