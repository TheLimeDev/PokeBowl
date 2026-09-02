import os
import signal
import subprocess
import sys
import time

from .runner import run_one
from .store import base_dir, ensure_layout, load_tasks, find_task, now_iso, pick_pending, save_tasks


def pid_path(root):
    return os.path.join(root, "daemon.pid")


def read_pid(root):
    try:
        with open(pid_path(root), encoding="utf-8") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return None


def alive(pid):
    if not pid:
        return False
    try:
        if os.name == "nt":
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"],
                                 capture_output=True, text=True)
            return str(pid) in (out.stdout or "")
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


def start(root):
    ensure_layout(root)
    pid = read_pid(root)
    if alive(pid):
        return pid
    entry = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    flags = 0
    if os.name == "nt":
        flags = getattr(subprocess, "DETACHED_PROCESS", 8) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 512)
    env = dict(os.environ)
    env["PYTHONPATH"] = entry + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.Popen(
        [sys.executable, "-m", "pokebowl", "--dir", root, "_daemon"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=flags,
        close_fds=True,
        cwd=entry,
        env=env,
    )
    with open(pid_path(root), "w", encoding="utf-8") as f:
        f.write(str(proc.pid))
    time.sleep(0.6)
    return proc.pid


def stop(root):
    pid = read_pid(root)
    if alive(pid):
        try:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                               capture_output=True)
            else:
                os.kill(pid, signal.SIGTERM)
        except OSError:
            pass
    try:
        os.remove(pid_path(root))
    except OSError:
        pass


def loop(root):
    ensure_layout(root)
    while True:
        task = pick_pending(load_tasks(root))
        if task is None:
            time.sleep(2)
            continue
        try:
            run_one(root, task)
        except Exception as e:
            tasks = load_tasks(root)
            live = find_task(tasks, task["id"])
            if live is not None:
                live["status"] = "failed"
                live["finished"] = now_iso()
                save_tasks(root, tasks)
            with open(os.path.join(root, "runs", f'{task["id"]}.log'),
                      "a", encoding="utf-8") as log:
                log.write(f"\nerror: {e}\n")
