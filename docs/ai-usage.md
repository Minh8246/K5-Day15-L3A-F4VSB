# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Codex | Nối DeepSeek, đọc token trực tiếp từ `usage`, chạy thử kết nối và lưu lượt 1. | Đăng phụ trách kiểm lại luồng chạy. | Nguyễn Văn Đăng |
| Prompt / thiết kế lời gọi mô hình | Codex | Soạn prompt trả JSON hai nhãn từ dữ kiện đối chiếu. | Đăng phụ trách rà nhãn và căn cứ đã gửi. | Nguyễn Văn Đăng |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | Antigravity | Hỗ trợ đề xuất 8 câu mở rộng `B13`–`B20` bám sát danh bạ `data/official_channels.json` và quy tắc SMS trong `data/domain_rules.json` (giữ nguyên `B01`–`B12`). | Thịnh kiểm lại nguồn `data_that` / `tu_viet`, kiểm `python run.py check` đạt 0 cảnh báo và giữ đúng tỷ lệ ≥1/3 nguồn thật (8/20). | Trần Việt Thịnh |
| Dữ liệu danh bạ & quy tắc SMS | Antigravity | Hỗ trợ tra cứu tổng hợp 10 ngân hàng/ví phổ biến, cấu trúc JSON (`official_channels.json`, `domain_rules.json`) và soạn `data/DATA_CARD.md`. | Thịnh tự đối chiếu lại tên miền, hotline, email với trang chính thức của từng tổ chức và rà quy tắc SMS. | Trần Việt Thịnh |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | Codex | Đối chiếu đầu ra của hai lượt với tiêu chí từng câu và metric, ghi đề xuất vào CSV. | Đăng rà và xác nhận chấm theo tiêu chí đã chốt. Trần Việt Thịnh đã chấm độc lập 5 đầu ra lượt 2 (`B01`, `B02`, `B07`, `B10`, `B16`), khớp 5/5. | Nguyễn Văn Đăng · Trần Việt Thịnh |
| Cải tiến CP4 | Codex | Sửa mẫu nhận diện yêu cầu xác thực hoặc chuyển tiền, chạy lại cùng bộ và mô phỏng 50 phiên. | Đăng xác nhận kết quả lượt 2. | Đăng và Thịnh phụ trách |
| Slide, văn bản | Codex | Soạn và kiểm tra 8 trang PDF theo bằng chứng, hai lượt đánh giá và mô phỏng có dữ liệu gốc. | Chờ nhóm rà trước khi trình bày. | Quân và Minh phụ trách |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
