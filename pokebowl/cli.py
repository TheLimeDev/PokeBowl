import argparse
import json
import sys

from . import VERSION
from .agents import names, resolve
from .daemon import alive, loop, read_pid, start, stop
from .runner import run_one
from .store import base_dir, find_task, load_tasks, next_id, now_iso, pick_pending, save_tasks


def cmd_add(args):
    root = base_dir(args.dir)
    tasks = load_tasks(root)
    title = args.title.strip()
    shell = resolve(title, agent=args.agent, extra=args.extra, command=args.command)
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
    return 0


def cmd_list(args):
    tasks = load_tasks(base_dir(args.dir))
    if args.json:
        print(json.dumps(tasks, indent=2))
        return 0
    if not tasks:
        print("empty")
        return 0
    for t in tasks:
        print(f'{t.get("id")} [{t.get("status")}] {t.get("title")} :: {t.get("cmd")}')
    return 0


def cmd_run(args):
    root = base_dir(args.dir)
    tasks = load_tasks(root)
    if args.id:
        task = find_task(tasks, args.id)
        if task is None:
            print(f"no task {args.id}", file=sys.stderr)
            return 1
        if task.get("status") not in ("pending", "failed"):
            print(f'task {args.id} is {task.get("status")}', file=sys.stderr)
            return 1
    else:
        task = pick_pending(tasks)
        if task is None:
            print("nothing pending")
            return 0
    code = run_one(root, task)
    print("done" if code == 0 else "failed")
    return code


def cmd_up(args):
    root = base_dir(args.dir)
    pid = read_pid(root)
    if alive(pid):
        print(f"already up ({pid})")
        return 0
    print(f"up ({start(root)})")
    return 0


def cmd_down(args):
    stop(base_dir(args.dir))
    print("down")
    return 0


def cmd_status(args):
    root = base_dir(args.dir)
    tasks = load_tasks(root)
    pid = read_pid(root)
    counts = {"pending": 0, "running": 0, "done": 0, "failed": 0}
    for t in tasks:
        s = t.get("status", "pending")
        counts[s] = counts.get(s, 0) + 1
    print(f'daemon: {"up (%s)" % pid if alive(pid) else "down"}')
    print(f'pending={counts.get("pending", 0)} running={counts.get("running", 0)} done={counts.get("done", 0)} failed={counts.get("failed", 0)}')
    return 0


def cmd_logs(args):
    import os
    path = os.path.join(base_dir(args.dir), "runs", f"{args.id}.log")
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


def build_parser():
    p = argparse.ArgumentParser(prog="pokebowl", description="Background runner for coding agents")
    p.add_argument("--dir", default=None, help="queue directory parent (default: cwd)")
    p.add_argument("--version", action="store_true", help="print version")
    sub = p.add_subparsers(dest="cmd")

    a = sub.add_parser("add", help="queue a task")
    a.add_argument("title", help="what to work on")
    a.add_argument("command", nargs="?", default=None, help="shell command to run")
    a.add_argument("--agent", default=None, choices=names(), help="agent preset")
    a.add_argument("--extra", default=None, help="extra args appended to agent preset")
    a.set_defaults(func=cmd_add)

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
    z.set_defaults(func=lambda a: loop(base_dir(a.dir)))

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
