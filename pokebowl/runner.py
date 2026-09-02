import os
import subprocess

from .store import ensure_layout, find_task, load_tasks, now_iso, save_tasks


def run_one(root, task):
    runs = ensure_layout(root)
    log_path = os.path.join(runs, f'{task["id"]}.log')
    task["status"] = "running"
    task["started"] = now_iso()
    persist(root, task)
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f'$ {task["cmd"]}\n')
        log.flush()
        proc = subprocess.Popen(
            task["cmd"],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=os.path.dirname(root),
        )
        out, _ = proc.communicate()
        log.write(out or "")
        log.write(f"\nexit={proc.returncode}\n")
    tasks = load_tasks(root)
    live = find_task(tasks, task["id"])
    if live is not None:
        live["status"] = "done" if proc.returncode == 0 else "failed"
        live["finished"] = now_iso()
        live["exit"] = proc.returncode
        save_tasks(root, tasks)
    return proc.returncode


def persist(root, updated):
    tasks = load_tasks(root)
    for i, t in enumerate(tasks):
        if str(t.get("id")) == str(updated.get("id")):
            tasks[i] = updated
            break
    save_tasks(root, tasks)
