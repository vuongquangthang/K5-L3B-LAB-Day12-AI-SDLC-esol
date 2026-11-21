# Nhật ký dùng AI (theo phase và theo người)

| Phase | Người | Công cụ / model | Việc | Token / chi phí ước tính | Ghi chú (AI sai ở đâu?) |
|---|---|---|---|---|---|
| Phase 1 | Vương Quang Thắng | Antigravity (Gemini 3.8 Flash High) | Thiết lập dự án solo, thỏa thuận nhóm, cập nhật hợp đồng tích hợp và kế hoạch Phase 1 | ~15k tokens | Ban đầu chưa chú ý việc check_team có ràng buộc 4-6 người trong mock test. Đã phát hiện ra test_template_is_rejected yêu cầu validate trả về lỗi nên 1 người vẫn thỏa mãn bài test. |
| Phase 1 | Vương Quang Thắng | Antigravity (Gemini 3.8 Flash High) | Viết luật Gather Lát 1 (oxy, bơi, lặn/nổi, ngạt, ngất) & unit test | ~20k tokens | Không có lỗi logic, tuân thủ đúng thứ tự vòng tick. |
| Phase 1 | Vương Quang Thắng | Antigravity (Gemini 3.8 Flash High) | Viết luật Gather Lát 2 (hái hoa, bắt cá, giỏ đầy, hồi chiêu) & unit test | ~20k tokens | Cần chú ý kẹp chặt số lượng hái/bắt vào không gian còn trống của giỏ khoang. |
| Phase 1 | Vương Quang Thắng | Antigravity (Gemini 3.8 Flash High) | Viết luật Quan Lát 3 & 4 (khách đến, giữ chỗ, nấu bếp, phục vụ, thanh toán, tip) & unit test | ~35k tokens | Trong unit test tương tác liên tiếp, `LiveInputs` cần được nhả (release `interact=False`) trước khi bấm lại để bộ phát hiện cạnh lên (edge detector) hoạt động đúng. |
| Phase 1 | Vương Quang Thắng | Antigravity (Gemini 3.8 Flash High) | Chạy headless, sinh bằng chứng proof, tài liệu nghiệm thu và đóng gói | ~15k tokens | Lệnh chuyển hướng PowerShell cần dùng đúng để bắt cả luồng stderr của unittest. |
