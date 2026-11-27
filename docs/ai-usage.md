# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Codex | Nối DeepSeek, đọc token trực tiếp từ `usage`, chạy thử kết nối và lưu lượt 1. | Đăng phụ trách kiểm lại luồng chạy. | Nguyễn Văn Đăng |
| Prompt / thiết kế lời gọi mô hình | Codex | Soạn prompt trả JSON hai nhãn từ dữ kiện đối chiếu. | Đăng phụ trách rà nhãn và căn cứ đã gửi. | Nguyễn Văn Đăng |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | Codex | Đối chiếu 20 đầu ra với tiêu chí từng câu và metric, ghi đề xuất vào `eval/run-1.csv`. | Đăng rà kết quả và xác nhận giữ 19/20. | Nguyễn Văn Đăng |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
