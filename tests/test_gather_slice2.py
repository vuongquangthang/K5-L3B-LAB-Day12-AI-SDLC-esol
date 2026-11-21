"""Unit test cho GatherSim Lát 2: hái nút, bắt cá, giỏ khoang, hồi chiêu bắt cá, mọc lại."""

import unittest
from chonoi.contract import load_contract
from chonoi.inputs import LiveInputs
from chonoi.runner import Session


class GatherSlice2Test(unittest.TestCase):
    def setUp(self):
        self.tuning = load_contract()["tuning"]

    def test_gather_node_at_surface(self):
        # Node N1 ở [12, 0], player ở [12, 0] (ngoài dock_radius vì dock_pos là [2, 0])
        sess = Session("gather", self.tuning, {"player": {"pos": [12, 0]}}, seed=1)
        inp = LiveInputs()
        inp.set(interact=True)
        events = sess.step(inp.advance())
        g_events = [e for e in events if e["name"] == "gather"]
        self.assertEqual(len(g_events), 1)
        self.assertEqual(g_events[0]["data"]["node_id"], "N1")
        self.assertEqual(g_events[0]["data"]["kind"], "bong_dien_dien")
        self.assertEqual(g_events[0]["data"]["count"], 1)
        self.assertEqual(sess.sim.hold, ["bong_dien_dien"])
        # Node phải chuyển sang regrow
        node_n1 = next(n for n in sess.sim.nodes if n["id"] == "N1")
        self.assertGreater(node_n1["regrow_ticks"], 0)

        # Bấm interact tiếp khi nút chưa mọc -> không hái được thêm
        inp.set(interact=True)
        events2 = sess.step(inp.advance())
        self.assertFalse(any(e["name"] == "gather" for e in events2))

    def test_gather_hold_full(self):
        # Giỏ đầy (12 con ca_loc)
        sess = Session("gather", self.tuning, {
            "player": {"pos": [12, 0]},
            "hold": ["ca_loc"] * 12
        }, seed=1)
        inp = LiveInputs()
        inp.set(interact=True)
        events = sess.step(inp.advance())
        self.assertTrue(any(e["name"] == "hold_full" for e in events))
        self.assertFalse(any(e["name"] == "gather" for e in events))
        self.assertEqual(len(sess.sim.hold), 12)

    def test_catch_fish_underwater(self):
        # Cá F1 ở [15, 5], kind="ca_linh", yield=3
        sess = Session("gather", self.tuning, {"player": {"pos": [15, 5]}}, seed=1)
        inp = LiveInputs()
        inp.set(catch=True)
        events = sess.step(inp.advance())
        caught = [e for e in events if e["name"] == "fish_caught"]
        self.assertEqual(len(caught), 1)
        self.assertEqual(caught[0]["data"]["fish_id"], "F1")
        self.assertEqual(caught[0]["data"]["kind"], "ca_linh")
        self.assertEqual(caught[0]["data"]["count"], 3)
        self.assertEqual(sess.sim.hold, ["ca_linh", "ca_linh", "ca_linh"])
        # Cá F1 đã bị bắt nên không còn trong self.fish
        self.assertFalse(any(f["id"] == "F1" for f in sess.sim.fish))
        # Hồi chiêu catch_cd_ticks được kích hoạt (0.5s * 60 = 30 tick)
        self.assertGreater(sess.sim.catch_cd_ticks, 0)

    def test_cannot_catch_at_surface(self):
        # Ở mặt nước [15, 0], cá ở [15, 1] trong catch_radius nhưng player ở mặt nước
        sess = Session("gather", self.tuning, {
            "player": {"pos": [15, 0]},
            "fish": [{"id": "F99", "kind": "ca_linh", "pos": [15, 1], "heading_deg": 0}]
        }, seed=1)
        inp = LiveInputs()
        inp.set(catch=True)
        events = sess.step(inp.advance())
        self.assertFalse(any(e["name"] == "fish_caught" for e in events))
        self.assertEqual(len(sess.sim.hold), 0)


if __name__ == "__main__":
    unittest.main()
