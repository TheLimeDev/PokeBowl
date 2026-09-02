import argparse
import datetime
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time

VERSION = "0.1.0"
DIRNAME = ".pokebowl"

AGENTS = {
    "echo": 'echo "{task}"',
    "claude": 'claude -p "{task}"',
    "codex": 'codex exec "{task}"',
    "aider": 'aider --message "{task}" --yes',
    "opencode": 'opencode run "{task}"',
    "cursor": 'cursor-agent "{task}"',
}


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
    tmp_fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(path) or ".")
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
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
    if not isinstance(data, list):
        data = []
    return data


def save_tasks(root, tasks):
    path = os.path.join(root, "tasks.json")
    atomic_write(path, json.dumps(tasks, indent=2))


def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def next_id(tasks):
    top = 0
    for t in tasks:
        try:
            n = int(str(t.get("id", 0)))
        except ValueError:
            n = 0
        if n > top:
            top = n
    return str(top + 1)


def find_task(tasks, tid):
    for t in tasks:
        if str(t.get("id")) == str(tid):
            return t
    return None


def cmd_add(args):
    root = base_dir(args.dir)
    ensure_layout(root)
    tasks = load_tasks(root)
    title = args.title.strip()
    if args.agent:
        template = AGENTS.get(args.agent, AGENTS["echo"])
        shell = template.replace("{task}", title.replace('"', ""))
        if args.extra:
            shell = shell + " " + args.extra
    else:
        shell = args.command or args.extra or ("echo " + title)
    tid = next_id(tasks)
    tasks.append({
        "id": tid,
        "title": title,
        "cmd": shell,
        "status": "pending",
        "created": now_iso(),
        "started": "",
        "finished": "",
        "exit": None,
    })
    save_tasks(root, tasks)
    print(tid)


def cmd_list(args):
    root = base_dir(args.dir)
    tasks = load_tasks(root)
    if args.json:
        print(json.dumps(tasks, indent=2))
        return
    if not tasks:
        print("empty")
        return
    for t in tasks:
        print(f'{t.get("id")} [{t.get("status")}] {t.get("title")} :: {t.get("cmd")}')


def run_one(root, task):
    runs = ensure_layout(root)
    log_path = os.path.join(runs, f'{task["id"]}.log')
    task["status"] = "running"
    task["started"] = now_iso()
    save_tasks(root, load_tasks(root) and merge_status(root, task))
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"$ {task['cmd']}\n")
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


def merge_status(root, updated):
    tasks = load_tasks(root)
    for i, t in enumerate(tasks):
        if str(t.get("id")) == str(updated.get("id")):
            tasks[i] = updated
            break
    return tasks


def pick_pending(tasks):
    for t in tasks:
        if t.get("status") == "pending":
            return t
    return None


def cmd_run(args):
    root = base_dir(args.dir)
    tasks = load_tasks(root)
    if args.id:
        task = find_task(tasks, args.id)
        if task is None:
            print(f"no task {args.id}", file=sys.stderr)
            return 1
        if task.get("status") not in ("pending", "failed"):
            print(f"task {args.id} is {task.get('status')}", file=sys.stderr)
            return 1
    else:
        task = pick_pending(tasks)
        if task is None:
            print("nothing pending")
            return 0
    code = run_one(root, task)
    print("done" if code == 0 else "failed")
    return code


def pid_path(root):
    return os.path.join(root, "daemon.pid")


def is_running(pid):
    if not pid:
        return False
    try:
        if os.name == "nt":
            out = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True, text=True,
            )
            return str(pid) in (out.stdout or "")
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


def read_pid(root):
    try:
        with open(pid_path(root), encoding="utf-8") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return None


def cmd_up(args):
    root = base_dir(args.dir)
    ensure_layout(root)
    pid = read_pid(root)
    if is_running(pid):
        print(f"already up ({pid})")
        return 0
    script = os.path.abspath(sys.argv[0])
    creation = 0
    if os.name == "nt":
        creation = getattr(subprocess, "DETACHED_PROCESS", 8) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 512)
    proc = subprocess.Popen(
        [sys.executable, script, "--dir", root, "_daemon"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=creation,
        close_fds=True,
    )
    atomic_write(pid_path(root), str(proc.pid))
    time.sleep(0.6)
    print(f"up ({proc.pid})")
    return 0


def cmd_down(args):
    root = base_dir(args.dir)
    pid = read_pid(root)
    if not is_running(pid):
        try:
            os.remove(pid_path(root))
        except OSError:
            pass
        print("down")
        return 0
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
    print("down")
    return 0


def cmd_status(args):
    root = base_dir(args.dir)
    tasks = load_tasks(root)
    pid = read_pid(root)
    alive = is_running(pid)
    counts = {"pending": 0, "running": 0, "done": 0, "failed": 0}
    for t in tasks:
        s = t.get("status", "pending")
        counts[s] = counts.get(s, 0) + 1
    print(f'daemon: {"up (%s)" % pid if alive else "down"}')
    print(f'pending={counts.get("pending", 0)} running={counts.get("running", 0)} done={counts.get("done", 0)} failed={counts.get("failed", 0)}')
    return 0


def cmd_logs(args):
    root = base_dir(args.dir)
    path = os.path.join(root, "runs", f"{args.id}.log")
    if not os.path.exists(path):
        print(f"no logs for {args.id}", file=sys.stderr)
        return 1
    with open(path, encoding="utf-8", errors="replace") as f:
        sys.stdout.write(f.read())
    return 0


def cmd_retry(args):
    root = base_dir(args.dir)
    tasks = load_tasks(root)
    task = find_task(tasks, args.id)
    if task is None:
        print(f"no task {args.id}", file=sys.stderr)
        return 1
    task["status"] = "pending"
    task["exit"] = None
    save_tasks(root, tasks)
    print(f"queued {args.id}")
    return 0


def cmd_rm(args):
    root = base_dir(args.dir)
    tasks = load_tasks(root)
    kept = [t for t in tasks if str(t.get("id")) != str(args.id)]
    if len(kept) == len(tasks):
        print(f"no task {args.id}", file=sys.stderr)
        return 1
    save_tasks(root, kept)
    print(f"removed {args.id}")
    return 0


def daemon_loop(root):
    ensure_layout(root)
    while True:
        tasks = load_tasks(root)
        task = pick_pending(tasks)
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
            log_path = os.path.join(root, "runs", f'{task["id"]}.log')
            with open(log_path, "a", encoding="utf-8") as log:
                log.write(f"\nerror: {e}\n")


def build_parser():
    p = argparse.ArgumentParser(prog="pokebowl", description="Background runner for coding agents")
    p.add_argument("--dir", default=None, help="queue directory parent (default: cwd)")
    p.add_argument("--version", action="store_true", help="print version")
    sub = p.add_subparsers(dest="cmd")

    a = sub.add_parser("add", help="queue a task")
    a.add_argument("title", help="what to work on")
    a.add_argument("command", nargs="?", default=None, help="shell command to run")
    a.add_argument("--agent", default=None, choices=sorted(AGENTS.keys()), help="agent preset")
    a.add_argument("--extra", default=None, help="extra args appended to agent preset")
    a.set_defaults(func=lambda a: (cmd_add(a), 0)[1])

    l = sub.add_parser("list", help="show tasks")
    l.add_argument("--json", action="store_true")
    l.set_defaults(func=cmd_list)

    r = sub.add_parser("run", help="run one task in foreground")
    r.add_argument("id", nargs="?", default=None)
    r.set_defaults(func=cmd_run)

    u = sub.add_parser("up", help="start background daemon")
    u.set_defaults(func=cmd_up)

    d = sub.add_parser("down", help="stop background daemon")
    d.set_defaults(func=cmd_down)

    s = sub.add_parser("status", help="daemon and queue status")
    s.set_defaults(func=cmd_status)

    g = sub.add_parser("logs", help="show task log")
    g.add_argument("id")
    g.set_defaults(func=cmd_logs)

    y = sub.add_parser("retry", help="requeue a task")
    y.add_argument("id")
    y.set_defaults(func=cmd_retry)

    m = sub.add_parser("rm", help="remove a task")
    m.add_argument("id")
    m.set_defaults(func=cmd_rm)

    z = sub.add_parser("_daemon", help=argparse.SUPPRESS)
    z.set_defaults(func=lambda a: daemon_loop(base_dir(a.dir)))

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print(VERSION)
        return 0
    if not getattr(args, "cmd", None):
        parser.print_help()
        return 0
    result = args.func(args)
    return result if isinstance(result, int) else 0


if __name__ == "__main__":
    raise SystemExit(main())
