---
noteId: "d682b0a0e58b11f18e48392c27908fcb"
tags: []

---

# vuongquangthang — phản tư cá nhân (≤ 200 từ)

- Tôi đã làm (kèm link commit):
  + Thiết lập thông tin dự án, cấu hình solo dev, hợp đồng tích hợp và kế hoạch Phase 1: commit `1601a06`.
  + Triển khai GatherSim Lát 1 (bơi, oxy, lặn/nổi, ngạt, ngất) và bộ unit test: commit `dcf0d50`.
  + Triển khai GatherSim Lát 2 (hái nút hoa, bắt cá, giỏ khoang LIFO, hồi chiêu) và unit test: commit `92528d5`.
  + Triển khai QuanSim Lát 3 & 4 (vòng đời khách hàng, đặt món, giữ chỗ, nấu bếp, phục vụ, thanh toán, tip & uy tín) và unit test: commit `5cd532f`.
  + Xuất chứng cứ chạy headless, hoàn thiện hồ sơ kiểm chứng, ma trận truy vết và gắn tag `phase-1`.
- Tôi đã review:
  + Tự review toàn bộ diff của các lát tính năng trước khi commit; đối chiếu với Test Contract và dải hợp lệ trong `game.contract.json`.
- AI sai ở đâu và tôi phát hiện thế nào:
  + Khi viết unit test cho `QuanSim`, AI gọi 2 lần `interact=True` liên tiếp mà không nhả phím `interact=False`, khiến `LiveInputs` không nhận diện được cạnh lên ở lần thao tác thứ 2. Tôi đã phát hiện qua failure traceback của test suite và khắc phục ngay lập tức.
- Điều tôi học được:
  + Nắm vững quy trình AI-driven SDLC với Test-First / Spec-First approach: khi có hợp đồng kiểm thử chặt chẽ, việc phát triển các lát tính năng diễn ra cực kỳ nhanh chóng và chính xác.
