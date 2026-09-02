import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pokebowl import runner, store


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, ".pokebowl")

    def queue(self, title, cmd):
        tasks = store.load_tasks(self.root)
        tid = store.next_id(tasks)
        task = {
            "id": tid,
            "title": title,
            "cmd": cmd,
            "status": "pending",
            "created": store.now_iso(),
            "started": "",
            "finished": "",
            "exit": None,
        }
        tasks.append(task)
        store.save_tasks(self.root, tasks)
        return tid

    def test_run_marks_done(self):
        tid = self.queue("hi", "echo hello-tests")
        code = runner.run_one(self.root, store.find_task(store.load_tasks(self.root), tid))
        self.assertEqual(code, 0)
        live = store.find_task(store.load_tasks(self.root), tid)
        self.assertEqual(live["status"], "done")
        with open(os.path.join(self.root, "runs", f"{tid}.log"), encoding="utf-8") as f:
            self.assertIn("hello-tests", f.read())

    def test_run_marks_failed(self):
        tid = self.queue("bad", "exit 3")
        code = runner.run_one(self.root, store.find_task(store.load_tasks(self.root), tid))
        self.assertNotEqual(code, 0)
        live = store.find_task(store.load_tasks(self.root), tid)
        self.assertEqual(live["status"], "failed")


if __name__ == "__main__":
    unittest.main()
