# Kế hoạch Phase 1 (Quán Ăn Chợ Nổi)

## Mục tiêu
- Hoàn thiện trọn vẹn 2 chế độ cốt lõi của Phase 1 theo PRD-0 và Test Contract:
  1. Buổi sáng (`gather`): Lặn & Hái (bơi, oxy, ngạt, ngất, hái hoa, bắt cá, cập bến, xuất kho).
  2. Buổi tối (`quan`): Mở Quán (đi lại, khách đến, chọn món, giữ chỗ, nấu bếp, phục vụ bàn, thanh toán/boa, uy tín).
- Đảm bảo tính tất định từng byte qua headless runner với seed cố định.
- Vượt qua 100% test bộ khung starter và bổ sung test phủ kín toàn bộ luật chơi mới.

## Phân chia lát cắt & Tiến độ (Solo Dev)
1. **Lát 0 (Nền tảng & Hợp đồng):**
   - Cập nhật `TEAM.md`, `game.contract.json`, `docs/contracts/README.md`.
   - Làm rõ yêu cầu tại `docs/clarify.md`.
2. **Lát 1 (Gather - Sinh tồn & Di chuyển):**
   - Tính toán oxy khi bơi dưới nước / hồi ở mặt nước.
   - Phát hiện chuyển vùng: `dive` / `surface`.
   - Cơ chế ngạt (`choke`) khi oxy = 0 và ngất (`faint`) khi HP = 0 kèm mất sạch giỏ.
   - Unit test cho Lát 1.
3. **Lát 2 (Gather - Thu hoạch & Cập bến):**
   - Hái hoa ở mặt nước khi bấm `interact` (khoảng cách, ưu tiên id, đếm hồi sinh `regrow_ticks`).
   - Bắt cá dưới nước khi bấm `catch` (hồi chiêu `catch_cd_ticks`, sức chứa giỏ `hold_capacity`).
   - Cập bến bến đò ghi file kho nguyên tử.
   - Unit test cho Lát 2.
4. **Lát 3 & 4 (Quan - Mở Quán & Phục vụ):**
   - Khách đến theo lịch (`first_customer_tick`, `customer_interval_s`).
   - Kiểm tra món nấu được, giữ chỗ nguyên liệu trong kho; `no_dish` nếu không đủ.
   - Đếm lùi thời gian kiên nhẫn; khách bỏ đi (`customer_left`) trừ uy tín nếu trễ.
   - Tương tác bếp: nấu món (`cook_started`, `dish_ready`), bưng món trên tay (`dish_picked`).
   - Tương tác bàn: phục vụ khách (`served`), khách ăn (`eat_ticks_left`), trả tiền + tip (`paid`).
   - Unit test cho Quan.
5. **Nghiệm thu & Đóng gói:**
   - Chạy toàn bộ test suite.
   - Tạo proof output (headless run).
   - Điền báo cáo kiểm chứng `docs/verification/phase-1.md`, nhật ký AI `docs/ai-usage-log.md`, standup, retro và hồ sơ thành viên.
   - Gắn tag git `phase-1`.

## Rủi ro & Giải pháp
- **Rủi ro:** Lệch thứ tự xử lý sự kiện trong vòng tick khiến kết quả không tất định hoặc sai lệch so với test contract.
  - *Giải pháp:* Tuân thủ nghiêm ngặt thứ tự các bước trong hàm `step()` theo PRD: Giảm bộ đếm -> Di chuyển -> Bơi/Oxy -> Tương tác -> Hết giờ.
- **Rủi ro:** Vượt sức chứa giỏ khi bắt bầy cá có số lượng lớn hơn chỗ trống còn lại.
  - *Giải pháp:* Thu hoạch tối đa theo số chỗ trống còn lại và phát sự kiện `hold_full` cảnh báo.
