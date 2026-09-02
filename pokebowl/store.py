import datetime
import json
import os
import tempfile

DIRNAME = ".pokebowl"


def base_dir(override=None):
    if override:
        return os.path.abspath(override)
    return os.path.join(os.getcwd(), DIRNAME)


def ensure_layout(root):
    runs = os.path.join(root, "runs")
    os.makedirs(runs, exist_ok=True)
    tasks = os.path.join(root, "tasks.json")
    if not os.path.exists(tasks):
        atomic_write(tasks, "[]")
    return runs


def atomic_write(path, text):
    parent = os.path.dirname(path) or "."
    fd, tmp = tempfile.mkstemp(dir=parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def load_tasks(root):
    ensure_layout(root)
    path = os.path.join(root, "tasks.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = []
    return data if isinstance(data, list) else []


def save_tasks(root, tasks):
    atomic_write(os.path.join(root, "tasks.json"), json.dumps(tasks, indent=2))


def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def next_id(tasks):
    top = 0
    for t in tasks:
        try:
            n = int(str(t.get("id", 0)))
        except ValueError:
            n = 0
        top = n if n > top else top
    return str(top + 1)


def find_task(tasks, tid):
    for t in tasks:
        if str(t.get("id")) == str(tid):
            return t
    return None


def pick_pending(tasks):
    for t in tasks:
        if t.get("status") == "pending":
            return t
    return None
