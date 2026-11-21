"""Unit test cho GatherSim Lát 1: bơi, lặn, nổi, tiêu hao & hồi oxy, ngạt (choke), ngất (faint)."""

import unittest
from chonoi.contract import load_contract
from chonoi.inputs import LiveInputs
from chonoi.runner import Session


class GatherSlice1Test(unittest.TestCase):
    def setUp(self):
        self.tuning = load_contract()["tuning"]

    def test_dive_and_surface_events(self):
        # Người chơi bắt đầu ở [20, 0] (mặt nước), bơi xuống [0, 1]
        sess = Session("gather", self.tuning, {"player": {"pos": [20, 0]}}, seed=1)
        inp = LiveInputs()
        inp.set(move=[0, 1])
        dive_found = False
        for _ in range(30):
            events = sess.step(inp.advance())
            for ev in events:
                if ev["name"] == "dive":
                    dive_found = True
                    self.assertGreater(ev["data"]["pos"][1], 0.5)
        self.assertTrue(dive_found, "Phải phát sự kiện dive khi bơi xuống vượt surface_depth")

        # Bơi ngược lên mặt nước
        inp.set(move=[0, -1])
        surface_found = False
        for _ in range(60):
            events = sess.step(inp.advance())
            for ev in events:
                if ev["name"] == "surface":
                    surface_found = True
                    self.assertLessEqual(ev["data"]["pos"][1], 0.5)
        self.assertTrue(surface_found, "Phải phát sự kiện surface khi ngoi lên mặt nước")

    def test_oxygen_depletion_and_refill(self):
        # Dưới nước d=10, oxy ban đầu 100 tick
        sess = Session("gather", self.tuning, {"player": {"pos": [20, 10], "oxygen_ticks": 100}}, seed=1)
        inp = LiveInputs()
        sess.step(inp.advance())
        snap = sess.snapshot()
        self.assertEqual(snap["player"]["oxygen_ticks"], 99)

        # Ở mặt nước d=0, oxy ban đầu 50 tick, hồi oxygen_refill_per_tick (6)
        sess2 = Session("gather", self.tuning, {"player": {"pos": [20, 0], "oxygen_ticks": 50}}, seed=1)
        sess2.step(inp.advance())
        snap2 = sess2.snapshot()
        self.assertEqual(snap2["player"]["oxygen_ticks"], 56)

    def test_oxygen_empty_event(self):
        # Oxy còn 1 tick, dưới nước
        sess = Session("gather", self.tuning, {"player": {"pos": [20, 10], "oxygen_ticks": 1}}, seed=1)
        inp = LiveInputs()
        events = sess.step(inp.advance())
        ev_names = [e["name"] for e in events]
        self.assertIn("oxygen_empty", ev_names)

    def test_choke_and_faint(self):
        # Oxy = 0, HP = 1, zero_oxy_ticks = 59
        sess = Session("gather", self.tuning, {
            "player": {"pos": [20, 10], "oxygen_ticks": 0, "hp": 1, "zero_oxy_ticks": 59},
            "hold": ["ca_loc", "bong_sung"]
        }, seed=1)
        inp = LiveInputs()
        events = sess.step(inp.advance())
        ev_names = [e["name"] for e in events]
        self.assertIn("choke", ev_names)
        self.assertIn("faint", ev_names)
        self.assertIn("gather_end", ev_names)
        self.assertTrue(sess.done)
        self.assertEqual(sess.sim.reason, "fainted")
        self.assertEqual(sess.sim.hold, [], "Khi ngất phải mất toàn bộ giỏ")
        self.assertEqual(sess.sim.inventory_items(), {})


if __name__ == "__main__":
    unittest.main()
