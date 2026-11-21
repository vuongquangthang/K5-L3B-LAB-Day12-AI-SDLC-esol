# Retro nhóm

## Phase 2 (nhanh)
- Điều tốt:
  - Tách nhỏ bài toán thành 4 lát tính năng rõ ràng (2 lát cho Gather, 2 lát cho Quan), giúp việc triển khai và kiểm thử diễn ra trơn tru.
  - Khung kiến trúc và Test Contract hộp đen rất chặt chẽ, phát hiện ngay lập tức bất kỳ lỗi hồi quy nào.
- Điều tệ:
  - Ban đầu chạy lệnh môi trường Windows cần lưu ý quyền truy cập và chuyển hướng luồng dữ liệu của PowerShell.
- 1 hành động cho Phase 3:
  - Duy trì thói quen viết unit test hộp đen độc lập song song với từng tính năng mới.

## Phase 4 (cuối)
- Rà lại hành động Phase 2: đã làm chưa? vì sao?
  - Đã thực hiện trọn vẹn: Toàn bộ các lát tính năng đều có file unit test riêng biệt (`test_gather_slice1.py`, `test_gather_slice2.py`, `test_quan_sim.py`) chạy song hành cùng bộ smoke test ban đầu.
- Điều tốt / điều tệ:
  - Điều tốt: Tiến độ nhanh gọn, 100% test xanh (44/44 test cases), cam kết tối thiểu 5 commit rõ ràng, tách bạch.
  - Điều tệ: Làm việc solo đòi hỏi phải tự đóng tất cả các vai (PO, Dev, QA, Release) nên cần kỷ luật cao trong việc ghi chép log.
- Số liệu: số commit theo người, cách đọc code của nhau, token theo người:
  - Commit: 5 commit chính thức từ tài khoản `vuongquangthang`.
  - Token tiêu thụ ước tính: ~105k tokens.
- Một lần AI sai và cách nhóm phát hiện:
  - AI viết test tương tác liên tục cho QuanSim nhưng quên nhả phím `interact` giữa 2 hành động liên tiếp, dẫn đến việc `LiveInputs` không kích hoạt cạnh lên ở lần thứ 2. Phát hiện qua việc test runner báo `FAIL` tại bước `served` và đã sửa ngay bằng cách nhả phím trước khi gọi thao tác mới.
- Nếu làm lại, đổi gì:
  - Viết trước các mock helper cho input sequence để test nhanh các kịch bản tương tác phức tạp.
