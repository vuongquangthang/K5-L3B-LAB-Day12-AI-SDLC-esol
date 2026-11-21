# TEAM

**Tên nhóm:** esol  **Số người:** 1  (khớp `team_size` trong `game.contract.json`)

| Thành viên | GitHub handle | Module chính | Vai quy trình | Người dự phòng cho |
|---|---|---|---|---|
| Vương Quang Thắng | vuongquangthang | sim/gather, sim/quan, client/ui, qa | PO, Integrator, QA lead, Release | Bản thân (làm solo) |

**Vai quy trình:** PO (đầu mối làm rõ yêu cầu, giữ `docs/clarify.md`) · Integrator (giữ `docs/contracts/`, gắn tag) · QA lead · Scrum/Release. Làm 1 mình đảm nhiệm toàn bộ vai trò.

## Thỏa thuận làm việc nhóm (điền trong 15 phút kickoff, ≤ 10 dòng)

- Kênh liên lạc: Làm việc độc lập tại repo cá nhân; ghi chép nhật ký qua `docs/ai-usage-log.md` và `docs/clarify.md`.
- Khi bất đồng về thiết kế: Tự cân nhắc theo Test Contract và PRD-0, ghi rõ lý do vào `docs/clarify.md`.
- Khi vướng mắc kỹ thuật: Debug qua unit test hộp đen và kiểm tra log chi tiết trước khi điều chỉnh sim.
- Giờ standup giữa phase: Tự cập nhật tiến độ vào `docs/standup.md` sau mỗi lát tính năng hoàn thành.
- Cách đọc/kiểm tra code: Tự review diff trước mỗi commit, đảm bảo test xanh 100%.
- Cách làm việc với Git: Commit theo từng lát tính năng nguyên tử (ít nhất 5 commit), gắn tag `phase-1` khi nghiệm thu xong.
