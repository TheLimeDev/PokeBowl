# 🍚 PokeBowl

AIにコードを書かせるとき、ずっと横で見ているのが嫌で作りました。用事を投げておいて、別のことをして、後でログだけ見ればいい。そういう道具です。

Claude、Codex、Aider、OpenCode、Cursorなど、普段使っているエージェントをそのまま裏で回せます。サーバーもアカウントも不要で、Pythonのファイルがひとつあるだけです。

## 仕組み

やりたいことをコマンド付きで登録すると、プロジェクト横の `.pokebowl/` に保存されます。デーモンが順番に実行して、成功なら done、失敗なら failed、出力はそれぞれのログに残ります。

```
add  ->  pending  ->  バックグラウンドで実行  ->  done / failed
```

## 入手方法

Homebrewが一番手軽です：

```
brew tap TheLimeDev/pokebowl
brew install pokebowl
```

あとは `pokebowl.py` を持っていくだけでも動きます。Python 3.9以降なら何も入れなくて大丈夫です。

## 使い方

まず仕事を積みます：

```
pokebowl add "say hi" "echo hi"
```

すぐ試したいときは手前で実行：

```
pokebowl run
pokebowl logs 1
```

裏に回して自分は別のことをする：

```
pokebowl up
pokebowl add "lint this folder" "python -m py_compile pokebowl.py"
pokebowl status
pokebowl logs 2
pokebowl down
```

## エージェントと使う

長いコマンドを毎回書かなくて大丈夫です。名前で呼べます：

```
pokebowl add "fix the login redirect" --agent claude
pokebowl add "migrate the db utils" --agent codex
pokebowl add "clean up imports" --agent aider
```

使える名前は `echo`、`claude`、`codex`、`aider`、`opencode`、`cursor` です。本体は自分で入れておいてください。PokeBowlは順番に回して、記録を残す役です。

確認や整理はこんな感じ：

```
pokebowl list
pokebowl retry 3
pokebowl rm 3
pokebowl list --json
```

## 置き場所

実行した場所の `.pokebowl/` に全部入ります：

- `tasks.json` —— 仕事の列
- `runs/<id>.log` —— 実行ごとの出力
- `daemon.pid` —— 裏のプロセス番号

場所を変えたいときは `--dir` を付けます：

```
pokebowl --dir C:\work\site add "build" "npm run build"
```

## こう作った理由

大手のバックグラウンド実行はどれも似ています。取ってきて、クラウドで回して、PRを作る。立派だけど重い。手元の道具で、小さく、自分のものとして動くのが欲しかったんです。PokeBowlはクラウドを使いません。入れた道具に順番と夜勤を与えるだけです。

変なところがあったら TheLimeDev/PokeBowl に issue をください。走らせたコマンドを貼ってもらえれば全部読みます。

MIT、LICENSEを見てください。
