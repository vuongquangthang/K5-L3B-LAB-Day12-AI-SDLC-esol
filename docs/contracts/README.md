# Hợp đồng tích hợp — Quán Ăn Chợ Nổi (Phase 1)

## 1. Schema file kho (`inventory.json`)
File kho trao đổi giữa buổi sáng (`gather`) và buổi tối (`quan`) tuân theo định dạng v1.0 (Contract G):
- Gốc là một JSON object có duy nhất trường `"items"`:
  ```json
  {
    "items": {
      "ca_loc": 1,
      "bong_sung": 2
    }
  }
  ```
- Quy tắc:
  - Chỉ chứa các khóa nguyên liệu hợp lệ trong Phase 1: `ca_loc`, `ca_linh`, `bong_dien_dien`, `bong_sung`.
  - Số lượng là số nguyên dương (`> 0`). Khi ghi file kho, các loại có số lượng 0 bị loại bỏ.
  - Ghi nguyên tử qua file tạm `.inv-*.tmp` cùng thư mục trước khi `os.replace`.

## 2. Giao diện giữa `sim/*` và `client/ui`
- UI chỉ đọc `snapshot()` do sim cung cấp tại mỗi tick hoặc theo chu kỳ.
- UI gửi các lệnh thông qua `InputState`:
  - `move: [x, d]` (trong gather, `d` dương là lặn xuống; trong quan, trục là `[x, z]` với `z` dương là hướng bắc).
  - `interact: bool` (phím E: cập bến, hái bông súng/điên điển, thao tác với bếp/bàn).
  - `catch: bool` (phím Space: dùng trong gather khi lặn dưới nước để bắt cá).

## 3. Danh sách sự kiện (Events Contract)

### Chế độ Lặn & Hái (`gather`):
- `dive`: Người chơi chuyển từ mặt nước (`d <= surface_depth`) xuống dưới nước (`d > surface_depth`). Data: `{"pos": [x, d]}`.
- `surface`: Người chơi ngoi lên mặt nước từ dưới nước. Data: `{"pos": [x, d]}`.
- `oxygen_empty`: Bình oxy tụt về 0 tick khi đang ở dưới nước. Data: `{"pos": [x, d]}`.
- `choke`: Khi oxy = 0 dưới nước đủ `choke_interval_ticks`, bị ngạt và mất 1 Máu. Data: `{"hp": current_hp}`.
- `faint`: Khi Máu tụt về 0, người chơi bị ngất, mất toàn bộ giỏ (kho rỗng). Data: `{}`.
- `gather`: Hái thành công cụm hoa ở mặt nước. Data: `{"node_id": id, "kind": kind, "count": count}`.
- `node_regrown`: Cụm hoa đã hái hết thời gian đếm ngược và mọc lại sẵn sàng. Data: `{"node_id": id}`.
- `fish_caught`: Bắt thành công đàn cá dưới nước. Data: `{"fish_id": id, "kind": kind, "count": count}`.
- `hold_full`: Giỏ khoang đã đầy (`len(hold) >= hold_capacity`), không thể nhặt thêm. Data: `{"kind": kind}`.
- `gather_end`: Kết thúc buổi sáng. Data: `{"reason": reason, "inventory": {"items": items}}`. (reason: `"docked"`, `"time"`, `"fainted"`).

### Chế độ Mở Quán (`quan`):
- `customer_arrived`: Khách mới vào quán, ngồi vào bàn trống và đặt món. Data: `{"customer_id": id, "table_id": id, "dish_id": id}`.
- `no_dish`: Khách đến nhưng kho/nguyên liệu khả dụng không đủ nấu bất kỳ món nào. Data: `{"table_id": id}`.
- `cook_started`: Bắt đầu nấu món tại bếp trống. Data: `{"stove_id": id, "dish_id": id}`.
- `dish_ready`: Bếp nấu xong, món ăn sẵn sàng để bưng. Data: `{"stove_id": id, "dish_id": id}`.
- `dish_picked`: Người chơi bưng món ăn từ bếp trên tay. Data: `{"stove_id": id, "dish_id": id}`.
- `served`: Người chơi phục vụ món ăn đúng yêu cầu cho khách tại bàn. Data: `{"table_id": id, "customer_id": id, "dish_id": id}`.
- `paid`: Khách ăn xong, thanh toán tiền và tiền boa (nếu có). Data: `{"customer_id": id, "table_id": id, "price": int, "tip": int, "total": int, "reputation": float}`.
- `customer_left`: Khách hết kiên nhẫn bỏ về trước khi được phục vụ. Data: `{"customer_id": id, "table_id": id, "reason": "impatient", "reputation": float}`.
- `quan_end`: Ca mở quán kết thúc khi hết giờ. Data: `{"reason": "time", "money": int, "earned": int, "shift_earned": int, "reputation": float}`.
