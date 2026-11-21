"""Buổi tối — Mở Quán. KHUNG: đi lại, chặn biên, đồng hồ, kho nạp từ file/scenario.

Luật chơi:
  - Khách đến theo lịch (first_customer_tick, customer_interval_s), chọn món nấu được,
    giữ chỗ nguyên liệu, kiên nhẫn, bỏ đi (customer_left), no_dish.
  - Interact tại bếp/bàn:
    + Bếp: bưng món đã chín (dish_picked), nấu món mới (cook_started, dish_ready).
    + Bàn: phục vụ món đúng yêu cầu (served).
  - Khách ăn xong trả tiền (paid), tính tiền boa (tip) và uy tín (reputation).
  - Hết ca khi hết giờ (quan_end).
"""

import math

from ..ids import sort_by_id
from .ramp import ramp_velocity

TICK = 60.0


class QuanSim:
    mode = "quan"
    phase = "quan"

    def __init__(self, tuning, scenario, streams, ids, inventory=None):
        t = tuning["quan"]
        self.t = t
        self.menu = tuning["menu"]
        self.rng = streams
        self.ids = ids
        p = scenario.get("player", {})
        self.pos = [float(c) for c in p.get("pos", t["start_pos"])]
        self.vel = [float(c) for c in p.get("vel", [0.0, 0.0])]
        self._tgt = None
        self._ramp_left = 0
        # kho: --inventory HOẶC scenario.stock (cả hai -> cli đã báo mã 2)
        self.stock = dict(inventory if inventory is not None else scenario.get("stock", {}))
        self.hand = scenario.get("hand")
        self.time_left_ticks = scenario.get("time_left_ticks", int(round(t["duration_s"] * TICK)))
        self.reputation = float(scenario.get("reputation", t["reputation_initial"]))
        self.stoves = [dict(s, state=s.get("state", "idle"), dish=s.get("dish"),
                            cook_ticks_left=s.get("cook_ticks_left", 0), ready_ticks=s.get("ready_ticks", 0))
                       for s in self._merge(t["stoves"], scenario.get("stoves", []))]
        self.tables = self._merge(t["tables"], scenario.get("tables", []))
        self.random_customers = scenario.get("random_customers", True)
        self.customer_interval_ticks = int(round(t["customer_interval_s"] * TICK))
        self.ticks = 0

        self.customers = []
        for c in scenario.get("customers", []):
            cust = dict(c)
            cust.setdefault("state", "waiting")
            cust.setdefault("patience_ticks_left", int(round(t["patience_s"] * TICK)))
            if "reserved" not in cust and cust.get("dish_id") in self.menu:
                cust["reserved"] = dict(self.menu[cust["dish_id"]]["recipe"])
            else:
                cust.setdefault("reserved", {})
            self.customers.append(cust)

        for e in self.customers:
            ids.reserve(e["id"])
        for s in self.stoves:
            ids.reserve(s["id"])
        for tb in self.tables:
            ids.reserve(tb["id"])

        self.money = 0
        self.earned = 0
        self.shift_earned = 0
        self.done = False
        self.reason = None

    @staticmethod
    def _merge(defaults, updates):
        by_id = {d["id"]: dict(d) for d in defaults}
        for u in updates:
            if u["id"] not in by_id:
                from ..errors import BadInput
                raise BadInput(f"id bếp/bàn không tồn tại: {u['id']}")
            by_id[u["id"]].update(u)
        return sort_by_id(list(by_id.values()))

    def snapshot(self) -> dict:
        occupied = {c["table_id"]: c["id"] for c in self.customers}
        return {
            "player": {"pos": self.pos},
            "stock": {k: self.stock[k] for k in sorted(self.stock) if self.stock[k] > 0},
            "hand": self.hand,
            "stoves": [{k: s.get(k) for k in ("id", "pos", "state", "dish", "cook_ticks_left", "ready_ticks")}
                       for s in self.stoves],
            "tables": [{"id": tb["id"], "pos": tb["pos"], "customer_id": occupied.get(tb["id"])} for tb in self.tables],
            "customers": sort_by_id(self.customers),
        }

    def step(self, inp):
        events = []
        self.time_left_ticks = max(0, self.time_left_ticks - 1)
        self.ticks += 1

        # 1. Bếp nấu
        for st in self.stoves:
            if st["state"] == "cooking":
                st["cook_ticks_left"] -= 1
                if st["cook_ticks_left"] <= 0:
                    st["state"] = "ready"
                    st["cook_ticks_left"] = 0
                    st["ready_ticks"] = 0
                    events.append(("dish_ready", {"stove_id": st["id"], "dish_id": st["dish"]}))
            elif st["state"] == "ready":
                st["ready_ticks"] = st.get("ready_ticks", 0) + 1

        # 2. Khách chờ / ăn
        for c in list(self.customers):
            if c.get("state") == "waiting":
                c["patience_ticks_left"] -= 1
                if c["patience_ticks_left"] <= 0:
                    self.reputation = max(self.t["reputation_min"], self.reputation + self.t["left_reputation_delta"])
                    events.append(("customer_left", {"customer_id": c["id"], "table_id": c["table_id"],
                                                     "reason": "impatient", "reputation": self.reputation}))
                    self.customers.remove(c)
            elif c.get("state") == "eating":
                c["eat_ticks_left"] -= 1
                if c["eat_ticks_left"] <= 0:
                    dish_info = self.menu[c["dish_id"]]
                    price = dish_info["price"]
                    pat_max = int(round(self.t["patience_s"] * TICK))
                    ratio = c.get("patience_ticks_left", 0) / pat_max
                    tip = 0
                    if ratio >= self.t["tip_min_patience_ratio"]:
                        tip = int(price * self.t["tip_rate"])
                        self.reputation = min(self.t["reputation_max"], self.reputation + self.t["tip_reputation"])
                    total = price + tip
                    self.money += total
                    self.earned += total
                    self.shift_earned += total
                    self.customers.remove(c)
                    events.append(("paid", {"customer_id": c["id"], "table_id": c["table_id"],
                                            "price": price, "tip": tip, "total": total, "reputation": self.reputation}))

        # 3. Di chuyển
        self._move(inp)

        # 4. Tương tác (phím interact)
        if inp.pressed("interact"):
            rad = self.t["interact_radius"]
            # Bếp trước, bàn sau; trong cùng nhóm sắp theo (khoảng cách, id)
            near_stoves = [s for s in self.stoves if math.dist(self.pos, s["pos"]) <= rad]
            near_tables = [tb for tb in self.tables if math.dist(self.pos, tb["pos"]) <= rad]

            if near_stoves:
                near_stoves.sort(key=lambda s: (math.dist(self.pos, s["pos"]), s["id"]))
                st = near_stoves[0]
                if st["state"] == "ready" and self.hand is None:
                    dish = st["dish"]
                    self.hand = dish
                    st["state"] = "idle"
                    st["dish"] = None
                    st["cook_ticks_left"] = 0
                    st["ready_ticks"] = 0
                    events.append(("dish_picked", {"stove_id": st["id"], "dish_id": dish}))
                elif st["state"] == "idle":
                    # Tìm khách đang chờ có món nấu được từ kho
                    for c in sort_by_id(self.customers):
                        if c.get("state") == "waiting":
                            dish = c["dish_id"]
                            recipe = self.menu[dish]["recipe"]
                            if all(self.stock.get(k, 0) >= v for k, v in recipe.items()):
                                for k, v in recipe.items():
                                    self.stock[k] -= v
                                c["reserved"] = {}
                                st["state"] = "cooking"
                                st["dish"] = dish
                                st["cook_ticks_left"] = int(round(self.menu[dish]["cook_s"] * TICK))
                                st["ready_ticks"] = 0
                                events.append(("cook_started", {"stove_id": st["id"], "dish_id": dish}))
                                break
            elif near_tables:
                near_tables.sort(key=lambda tb: (math.dist(self.pos, tb["pos"]), tb["id"]))
                tb = near_tables[0]
                c = next((cust for cust in self.customers if cust["table_id"] == tb["id"]), None)
                if c and c.get("state") == "waiting" and self.hand == c["dish_id"]:
                    dish = self.hand
                    self.hand = None
                    c["state"] = "eating"
                    c["eat_ticks_left"] = int(round(self.t["eat_s"] * TICK))
                    events.append(("served", {"table_id": tb["id"], "customer_id": c["id"], "dish_id": dish}))

        # 5. Khách mới theo lịch
        if self.random_customers:
            first_t = self.t["first_customer_tick"]
            if self.ticks >= first_t and (self.ticks == first_t or (self.ticks - first_t) % self.customer_interval_ticks == 0):
                occupied = {c["table_id"] for c in self.customers}
                free_tables = [tb for tb in self.tables if tb["id"] not in occupied]
                if free_tables:
                    free_tables.sort(key=lambda tb: tb["id"])
                    tb = free_tables[0]
                    # Tính kho khả dụng trừ lượng giữ chỗ
                    avail = dict(self.stock)
                    for c in self.customers:
                        for k, v in c.get("reserved", {}).items():
                            avail[k] = avail.get(k, 0) - v
                    eligible = [dish for dish, info in sorted(self.menu.items())
                                if all(avail.get(k, 0) >= v for k, v in info["recipe"].items())]
                    if eligible:
                        chosen_dish = self.rng.get("customer_dish").choice(eligible)
                        recipe = dict(self.menu[chosen_dish]["recipe"])
                        cid = self.ids.new("C")
                        new_cust = {
                            "id": cid,
                            "table_id": tb["id"],
                            "dish_id": chosen_dish,
                            "state": "waiting",
                            "patience_ticks_left": int(round(self.t["patience_s"] * TICK)),
                            "reserved": recipe
                        }
                        self.customers.append(new_cust)
                        events.append(("customer_arrived", {"customer_id": cid, "table_id": tb["id"], "dish_id": chosen_dish}))
                    else:
                        events.append(("no_dish", {"table_id": tb["id"]}))

        # 6. Hết ca
        if self.time_left_ticks <= 0:
            self.done = True
            self.reason = "time"
            events.append(("quan_end", {"reason": "time", "money": self.money, "earned": self.earned,
                                        "shift_earned": self.shift_earned, "reputation": self.reputation}))
        return events

    def _move(self, inp):
        speed = self.t["walk_speed"]
        mx, mz = inp.move
        self.vel = ramp_velocity(self, (mx * speed, mz * speed), int(self.t.get("ramp_max_ticks", 6)))
        b = self.t["bounds"]
        for i, axis in enumerate(("x", "z")):
            self.pos[i] += self.vel[i] / TICK
            lo, hi = b[axis]
            if self.pos[i] <= lo:
                self.pos[i], self.vel[i] = lo, max(0.0, self.vel[i])
            elif self.pos[i] >= hi:
                self.pos[i], self.vel[i] = hi, min(0.0, self.vel[i])
