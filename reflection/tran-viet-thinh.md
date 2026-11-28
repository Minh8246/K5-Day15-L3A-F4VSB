# Reflection — Trần Việt Thịnh

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Mình phụ trách kiểm nguồn chính thức, biên soạn quy tắc nhận diện tên miền/người gửi SMS và mở rộng bộ dữ liệu mẫu (`data/official_channels.json`, `data/domain_rules.json`, `data/DATA_CARD.md` qua PR #2, commit `d7183b5`), sau đó mở rộng `eval/benchmark.csv` từ 12 lên 20 câu cho CP3 (nhánh `feat/benchmark_20`, giữ nguyên `B01`–`B12` và bổ sung `B13`–`B20` gồm 4 câu `data_that` và 4 câu `tu_viet`, đạt 8/20 câu từ người dùng/data thật). Ở CP4, mình phối hợp với Đăng và Minh rà kết quả lượt 2, mô phỏng chi phí 50 phiên và phụ trách trình bày Trang 5–6 (Đánh giá & Chi phí) trong buổi demo.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   Mình dùng Antigravity để hỗ trợ tra cứu danh bạ kênh chính thức của 10 ngân hàng/ví điện tử, cấu trúc hai tệp JSON quy tắc và soạn bản nháp 8 câu thử mở rộng `B13`–`B20`. Điểm phải tự kiểm và sửa lại là rà trực tiếp từng tên miền, hotline chính thức, đồng thời khi nhóm thu hẹp phạm vi từ SMS/Zalo/email xuống chuyên sâu **SMS**, mình đã yêu cầu bổ sung riêng nhóm `sms_sender_rules` (đầu số cá nhân, Brandname biến tấu và cảnh báo trạm BTS giả) và sửa lại định dạng câu `B18` từ xuống dòng `\n` sang một dòng CSV để công cụ đọc khớp đúng tổ chức MB Bank.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   Ở lượt đánh giá 1 (`run-1@20261127-230415`), câu `B10` (tin SMS thật do P3 cung cấp, dụ bấm link và đăng nhập tài khoản để nhận hoàn tiền 500.000đ) bị trượt vì hệ thống cảnh báo đúng mức rủi ro cao nhưng lại gán nhầm mã `S_TRANSFER_REQUEST` (yêu cầu chuyển tiền) chỉ vì thấy từ khóa *"hoàn tiền"*. Từ lỗi này mình học được rằng bắt từ khóa đơn lẻ trong `domain_rules.json` rất dễ giải thích sai bản chất hành vi; phải kết hợp mẫu động từ kèm ngữ cảnh và phân biệt rõ *"đăng nhập để nhận tiền"* với *"chuyển tiền"* thì người dùng mới tin vào lý do cảnh báo.
