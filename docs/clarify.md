# Clarify — câu hỏi và câu trả lời (Phase 1)

| # | Ngày giờ | Câu hỏi | Trả lời / giả định | Ai quyết |
|---|---|---|---|---|
| 1 | 2026-11-21 16:05 | Hình thức làm bài: 1 người (solo) có được chấp nhận trong quy trình không? | Được chấp nhận theo chỉ đạo của người dùng; 1 người kiêm nhiệm tất cả các vai trò quy trình (PO, Integrator, QA, Release) và cập nhật đầy đủ tài liệu. | PO (Vương Quang Thắng) |
| 2 | 2026-11-21 16:06 | Khi người chơi ngất (`faint`), kho đồ xử lý thế nào? | Khi HP về 0, toàn bộ đồ trong giỏ `self.hold` bị xóa rỗng (`[]`), phát sự kiện `faint` và kết thúc với lý do `fainted`. File kho xuất ra rỗng (`{"items": {}}`). | PO / Test Contract |
| 3 | 2026-11-21 16:07 | Sự kiện `dive` và `surface` được kích hoạt khi nào? | So sánh trạng thái `at_surface` trước và sau khi di chuyển (`_move`): từ mặt nước xuống dưới nước -> `dive`; từ dưới nước lên mặt nước -> `surface`. | PO / Contract |
| 4 | 2026-11-21 16:08 | Khi bắt cá mà giỏ chỉ còn trống ít hơn sản lượng của đàn cá? | Nhặt số lượng vừa đủ sức chứa tối đa (`hold_capacity`), phần dư không nhặt và phát thêm sự kiện `hold_full`. | PO / PRD-0 |
| 5 | 2026-11-21 16:09 | Thứ tự tương tác phím E trong quán ăn (`quan`)? | Ưu tiên Bếp (`stoves`) trước Bàn (`tables`). Nếu có nhiều đối tượng cùng loại trong tầm, ưu tiên đối tượng gần hơn, hòa thì chọn theo thứ tự ID nhỏ hơn. | PO / PRD-0 |
