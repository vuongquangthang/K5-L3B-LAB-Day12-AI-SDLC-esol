# Ma trận truy vết Phase 1

| AC | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-1/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|
| CON-01 | Headless chạy 0 tick và dòng end hợp lệ | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_con_01_ticks_zero_and_end_line`) | Đạt |
| CON-02 | Tính tất định từng byte với cùng seed | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_con_02_deterministic_bytes`) | Đạt |
| CON-03 | Bắt lỗi BadInput trả mã thoát 2 | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_con_03_bad_input_exit_2`) | Đạt |
| GATHER-01 | Bơi, gia tốc ramp, chặn mép d >= 0 và d <= 30 | [test_results.txt](docs/proof/phase-1/test_results.txt) (`Movement.*`) | Đạt |
| GATHER-02 | Tiêu hao oxy dưới nước, hồi oxy mặt nước, sự kiện dive/surface | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_dive_and_surface_events`, `test_oxygen_depletion_and_refill`) | Đạt |
| GATHER-03 | Ngạt (choke) khi oxy = 0, ngất (faint) khi HP = 0 mất sạch giỏ | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_choke_and_faint`) | Đạt |
| GATHER-04 | Hái nút ở mặt nước (interact), hồi sinh nút (regrow), giỏ đầy (hold_full) | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_gather_node_at_surface`, `test_gather_hold_full`) | Đạt |
| GATHER-05 | Bắt cá dưới nước (catch), hồi chiêu bắt cá, loại khỏi hồ | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_catch_fish_underwater`, `test_cannot_catch_at_surface`) | Đạt |
| GATHER-06 | Cập bến bến đò xuất file kho nguyên tử | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_inv_01_gather_writes_inventory_quan_reads_it`), [gather.jsonl](docs/proof/phase-1/gather.jsonl) | Đạt |
| QUAN-01 | Khách đến theo lịch, chọn món, giữ chỗ kho | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_customer_arrives_and_reserves_stock`), [quan.jsonl](docs/proof/phase-1/quan.jsonl) | Đạt |
| QUAN-02 | Phát sự kiện no_dish khi kho không đủ món nào | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_no_dish_when_stock_empty`) | Đạt |
| QUAN-03 | Khách hết kiên nhẫn bỏ về trừ uy tín | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_customer_impatient_and_leaves`) | Đạt |
| QUAN-04 | Nấu bếp, bưng món, phục vụ bàn, thanh toán + tip + uy tín | [test_results.txt](docs/proof/phase-1/test_results.txt) (`test_cook_pick_serve_and_pay`) | Đạt |

## Đánh giá ngắn
- Yêu cầu nào đạt / chưa đạt:
  - Toàn bộ các yêu cầu của Phase 1 (PRD-0) cho cả 2 chế độ `gather` và `quan` đều đã hoàn thành và đạt 100% test (44/44 test cases passed).
  - Đầu ra của headless runner là hoàn toàn tất định và tuân thủ định dạng byte-level.
- Điều cần chỉnh cho phase sau:
  - Chuẩn bị cơ chế cá bơi / đàn cá sinh thêm và các loài thủy sinh phong phú hơn trong Phase 2.
  - Chuẩn bị cơ chế cháy món (`burn_s`) và thêm bàn/bếp cho quán ở các phase tiếp theo.
