"""Unit test cho QuanSim: vòng đời khách, đặt món, giữ chỗ, nấu bếp, phục vụ, thanh toán, boa & uy tín."""

import unittest
from chonoi.contract import load_contract
from chonoi.inputs import LiveInputs
from chonoi.runner import Session


class QuanSimTest(unittest.TestCase):
    def setUp(self):
        self.tuning = load_contract()["tuning"]

    def test_customer_arrives_and_reserves_stock(self):
        # Kho có đủ cá lóc (1)
        sess = Session("quan", self.tuning, {
            "stock": {"ca_loc": 1},
            "random_customers": True
        }, seed=1)
        inp = LiveInputs()
        # Chạy 120 tick đến first_customer_tick
        arrived = False
        for _ in range(120):
            events = sess.step(inp.advance())
            for ev in events:
                if ev["name"] == "customer_arrived":
                    arrived = True
                    self.assertEqual(ev["data"]["table_id"], "T1")
                    self.assertEqual(ev["data"]["dish_id"], "ca_loc_nuong_trui")
        self.assertTrue(arrived, "Khách phải đến ở tick 120 khi có bàn và nguyên liệu")

    def test_no_dish_when_stock_empty(self):
        # Kho rỗng, khách đến tick 120 nhưng không thể đặt món
        sess = Session("quan", self.tuning, {
            "stock": {},
            "random_customers": True
        }, seed=1)
        inp = LiveInputs()
        no_dish = False
        for _ in range(120):
            events = sess.step(inp.advance())
            for ev in events:
                if ev["name"] == "no_dish":
                    no_dish = True
                    self.assertEqual(ev["data"]["table_id"], "T1")
        self.assertTrue(no_dish, "Phải phát no_dish khi kho không đủ nấu món nào")

    def test_customer_impatient_and_leaves(self):
        # Khách chờ có patience còn 1 tick
        sess = Session("quan", self.tuning, {
            "customers": [{
                "id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui",
                "state": "waiting", "patience_ticks_left": 1
            }],
            "random_customers": False
        }, seed=1)
        inp = LiveInputs()
        events = sess.step(inp.advance())
        left = [e for e in events if e["name"] == "customer_left"]
        self.assertEqual(len(left), 1)
        self.assertEqual(left[0]["data"]["customer_id"], "C1")
        self.assertEqual(left[0]["data"]["reason"], "impatient")
        self.assertAlmostEqual(sess.sim.reputation, 2.5)  # 3.0 - 0.5

    def test_cook_pick_serve_and_pay(self):
        # Bếp B1 ở [2, 8], bàn T1 ở [9, 2]
        # Khách chờ ở T1, món ca_loc_nuong_trui, kho có ca_loc: 1
        sess = Session("quan", self.tuning, {
            "player": {"pos": [2, 8]},
            "stock": {"ca_loc": 1},
            "customers": [{
                "id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui",
                "state": "waiting", "patience_ticks_left": 3600
            }],
            "random_customers": False
        }, seed=1)
        inp = LiveInputs()

        # 1. Bấm interact ở bếp -> bắt đầu nấu
        inp.set(interact=True)
        events = sess.step(inp.advance())
        self.assertTrue(any(e["name"] == "cook_started" for e in events))
        self.assertEqual(sess.sim.stock.get("ca_loc", 0), 0)

        # 2. Đợi nấu xong (6 giây * 60 = 360 tick)
        inp.set(interact=False)
        dish_ready = False
        for _ in range(360):
            events = sess.step(inp.advance())
            if any(e["name"] == "dish_ready" for e in events):
                dish_ready = True
        self.assertTrue(dish_ready, "Bếp phải nấu xong sau cook_s")

        # 3. Bấm interact ở bếp -> bưng món lên tay
        inp.set(interact=True)
        events = sess.step(inp.advance())
        self.assertTrue(any(e["name"] == "dish_picked" for e in events))
        self.assertEqual(sess.sim.hand, "ca_loc_nuong_trui")

        # 4. Nhả phím, di chuyển tới bàn T1 [9, 2] và tương tác phục vụ
        inp.set(interact=False)
        sess.step(inp.advance())
        sess.sim.pos = [9, 2]
        inp.set(interact=True)
        events = sess.step(inp.advance())
        self.assertTrue(any(e["name"] == "served" for e in events))
        self.assertIsNone(sess.sim.hand)

        # 5. Khách ăn xong (eat_s = 10s -> 600 tick) và thanh toán
        inp.set(interact=False)
        paid = False
        for _ in range(600):
            events = sess.step(inp.advance())
            for ev in events:
                if ev["name"] == "paid":
                    paid = True
                    self.assertEqual(ev["data"]["price"], 60)
                    self.assertGreater(ev["data"]["tip"], 0)
        self.assertTrue(paid, "Khách ăn xong phải trả tiền và boa")
        self.assertGreater(sess.sim.money, 60)


if __name__ == "__main__":
    unittest.main()
