# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-230415` | 19/20 | 95% | 8/8 | 8/9 | 3/3 | Đạt |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

Lượt 1 dùng `deepseek-flash`, chạy đủ 20/20 câu, 0 lỗi kỹ thuật. `python run.py score eval/run-1.csv` xác nhận kết quả. Cả 3 ca từ chối giữ người dùng ở bước tự xác minh và cả 10 ca thiếu căn cứ tránh khẳng định SMS an toàn. Cảnh báo có mã đúng ở 9/10 ca được kỳ vọng rủi ro cao. Codex đề xuất điểm dựa trên từng đầu ra và Nguyễn Văn Đăng xác nhận giữ kết quả sau khi rà.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Giải thích sai thao tác trong SMS | 1 câu trượt | B10 |
| Giải thích thiếu một tín hiệu đã thấy trong đầu vào | 2 câu vẫn đạt tiêu chí | B03, B18 |

**Ba điểm quan sát ở lượt 1**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B10 | SMS yêu cầu mở đường dẫn và đăng nhập để nhận hoàn tiền. | Cảnh báo cao bằng mã `S_TRANSFER_REQUEST`. | Mã quy kết SMS yêu cầu chuyển tiền. Thao tác thực tế là đăng nhập. |
| B03 | SMS có đường dẫn dừng ở `https://`. | Chưa đủ căn cứ vì chưa xác định được tổ chức. | Lý do chưa chỉ ra đường dẫn bị cắt. Hướng dẫn xác minh vẫn đạt. |
| B18 | SMS có số di động ở dạng `Từ số …` và đòi OTP qua URL lạ. | Cảnh báo cao với mã tên miền và mã yêu cầu thông tin nhạy cảm. | Công cụ chưa trích được người gửi ở dạng này. Căn cứ URL và OTP vẫn đạt tiêu chí. |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
