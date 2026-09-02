import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pokebowl import daemon, store


class StaleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, ".pokebowl")

    def test_requeue_stale(self):
        tasks = store.load_tasks(self.root)
        tasks.append({"id": "1", "title": "stuck", "cmd": "echo x",
                      "status": "running", "created": store.now_iso(),
                      "started": store.now_iso(), "finished": "", "exit": None})
        tasks.append({"id": "2", "title": "fine", "cmd": "echo y",
                      "status": "done", "created": store.now_iso(),
                      "started": store.now_iso(), "finished": store.now_iso(), "exit": 0})
        store.save_tasks(self.root, tasks)
        self.assertTrue(daemon.requeue_stale(self.root))
        again = store.load_tasks(self.root)
        self.assertEqual(store.find_task(again, "1")["status"], "pending")
        self.assertEqual(store.find_task(again, "2")["status"], "done")

    def test_nothing_stale(self):
        store.load_tasks(self.root)
        store.save_tasks(self.root, [])
        self.assertFalse(daemon.requeue_stale(self.root))


if __name__ == "__main__":
    unittest.main()
