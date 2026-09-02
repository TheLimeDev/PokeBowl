# 🍚 PokeBowl

我这个人没什么耐心。每次让 AI 写代码，我都不想坐在旁边盯着。所以我做了 PokeBowl：把任务丢进去，该干嘛干嘛，回来直接看结果和日志。

它能把你本来就在用的工具带起来——Claude、Codex、Aider、OpenCode、Cursor都行，放在后台一个一个跑。不用注册账号，不用装服务，就一个 Python 文件。

## 原理

你加一个任务，写清楚要跑哪条命令。任务存在项目旁边的 `.pokebowl/` 里。后台进程按顺序拿起来跑，成功标 done，失败标 failed，输出都留在各自的日志里。

```
add  ->  pending  ->  后台运行  ->  done / failed
```

## 安装

最省事的是用 Homebrew：

```
brew tap TheLimeDev/pokebowl
brew install pokebowl
```

或者直接拿走 `pokebowl.py`，Python 3.9 以上就能跑，什么都不用装。

## 上手

先排一个任务：

```
pokebowl add "say hi" "echo hi"
```

想立刻看效果，前台跑一次：

```
pokebowl run
pokebowl logs 1
```

想挂后台，自己忙别的：

```
pokebowl up
pokebowl add "lint this folder" "python -m py_compile pokebowl.py"
pokebowl status
pokebowl logs 2
pokebowl down
```

## 接你的 agent

不用每次手写完整命令，直接点名就行：

```
pokebowl add "fix the login redirect" --agent claude
pokebowl add "migrate the db utils" --agent codex
pokebowl add "clean up imports" --agent aider
```

支持 `echo`、`claude`、`codex`、`aider`、`opencode`、`cursor`。前提是这些工具你自己已经装好了，PokeBowl 只负责排队、跑、留日志。

常用的查看和整理：

```
pokebowl list
pokebowl retry 3
pokebowl rm 3
pokebowl list --json
```

## 文件都在哪

都在你运行目录下的 `.pokebowl/` 里：

- `tasks.json` —— 任务队列
- `runs/<id>.log` —— 每次运行的输出
- `daemon.pid` —— 后台进程号

想换地方就加 `--dir`：

```
pokebowl --dir C:\work\site add "build" "npm run build"
```

## 为什么做成这样

大厂的后台 agent 流程都差不多：拉代码、上云跑、提 PR。好用，但太重了。我想要个轻的、本地的、完全属于自己的。PokeBowl 不碰云，只管把你装好的工具排好队，让它们替你值夜班。

用着不对劲，就去 TheLimeDev/PokeBowl 提个 issue，把你跑的命令贴上，我每条都会看。

MIT，见 LICENSE。
