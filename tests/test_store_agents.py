import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pokebowl import agents, store


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, ".pokebowl")

    def test_add_find_next(self):
        tasks = store.load_tasks(self.root)
        self.assertEqual(tasks, [])
        tasks.append({"id": store.next_id(tasks), "title": "a", "status": "pending"})
        tasks.append({"id": store.next_id(tasks), "title": "b", "status": "pending"})
        store.save_tasks(self.root, tasks)
        again = store.load_tasks(self.root)
        self.assertEqual(len(again), 2)
        self.assertEqual(store.find_task(again, "1")["title"], "a")
        self.assertEqual(store.next_id(again), "3")
        self.assertIsNone(store.find_task(again, "9"))

    def test_pick_pending(self):
        tasks = [
            {"id": "1", "status": "done"},
            {"id": "2", "status": "pending"},
        ]
        self.assertEqual(store.pick_pending(tasks)["id"], "2")
        self.assertIsNone(store.pick_pending([{"id": "1", "status": "done"}]))


class AgentsTest(unittest.TestCase):
    def test_resolve_preset(self):
        self.assertEqual(agents.resolve("hi", agent="echo"), 'echo "hi"')
        self.assertIn("claude", agents.resolve("fix it", agent="claude"))

    def test_resolve_extra(self):
        self.assertTrue(agents.resolve("fix it", agent="echo", extra="--loud").endswith("--loud"))

    def test_resolve_raw_command(self):
        self.assertEqual(agents.resolve("t", command="make build"), "make build")

    def test_resolve_openclaw_uses_workdir(self):
        cmd = agents.resolve("fix login", agent="openclaw", workdir="C:\\work\\site")
        self.assertIn("openclaw agent exec", cmd)
        self.assertIn("C:\\work\\site", cmd)

    def test_resolve_pi_print_mode(self):
        self.assertEqual(agents.resolve("audit this", agent="pi"), 'pi -p "audit this"')

    def test_detect_shape(self):
        found = agents.detect()
        self.assertEqual(set(found.keys()), set(agents.names()))
        for info in found.values():
            self.assertIn("installed", info)
            self.assertIn("version", info)
            self.assertIn("hint", info)
        self.assertTrue(found["echo"]["installed"])


if __name__ == "__main__":
    unittest.main()
