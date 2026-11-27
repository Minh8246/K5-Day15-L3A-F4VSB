# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-230415` | 19/20 | 95% | 8/8 | 8/9 | 3/3 | Đạt |
| 2 | `run-2@20261128-001757` | 20/20 | 100% | 8/8 | 9/9 | 3/3 | Đạt |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

Lượt 1 dùng `deepseek-flash`, chạy đủ 20/20 câu, 0 lỗi kỹ thuật. `python run.py score eval/run-1.csv` xác nhận kết quả. Cả 3 ca từ chối giữ người dùng ở bước tự xác minh và cả 10 ca thiếu căn cứ tránh khẳng định SMS an toàn. Cảnh báo có mã đúng ở 9/10 ca được kỳ vọng rủi ro cao. Codex đề xuất điểm dựa trên từng đầu ra và Nguyễn Văn Đăng xác nhận giữ kết quả sau khi rà.

Lượt 2 dùng cùng model, cùng 20 câu và cùng tiêu chí, với 0 lỗi kỹ thuật. Cả 3 ca từ chối giữ người dùng ở bước tự xác minh. Cả 10 ca thiếu căn cứ tránh khẳng định SMS an toàn. Cảnh báo có mã đúng ở 10/10 ca được kỳ vọng rủi ro cao. Codex đối chiếu đầu ra và Nguyễn Văn Đăng xác nhận chấm theo tiêu chí đã chốt sau khi rà.

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

- **Nhóm lỗi.** Quy tắc suy ra nhầm thao tác từ một cụm từ đứng riêng. Người dùng cần biết hành động cụ thể nào trong SMS đáng ngờ trước khi quyết định tự xác minh.
- **Cải tiến.** Hai quy tắc về thông tin xác thực và chuyển tiền nhận diện mẫu động từ kèm đối tượng hoặc ngữ cảnh. Quy tắc bỏ qua hành động bị phủ định ngay trước động từ. Kiểm nhanh bổ sung cho thấy câu khuyến cáo “Không cung cấp OTP” trả về chưa đủ căn cứ. Kiểm này nằm ngoài bộ 20 câu.
- **Kết quả.** B10 từ 0/1 lên 1/1. Lượt 2 nêu đúng yêu cầu đăng nhập để nhận tiền với mã `S_SENSITIVE_CREDENTIALS`. Điểm toàn bộ tăng từ 19/20 (95%) lên 20/20 (100%).
- **Đầu ra kém khớp hơn.** B02 chuyển từ chưa đủ căn cứ sang cảnh báo cao vì có yêu cầu đăng nhập qua URL, dù tổ chức nằm ngoài danh bạ. Điều này lệch nhãn `expected`. Câu vẫn đạt `pass_criterion` đã chốt vì đầu ra giữ giới hạn nguồn và hướng dẫn tự xác minh.

## 4. Còn lại

- B02 có thể cảnh báo quá mức với tổ chức ngoài danh bạ. B03 thiếu giải thích URL bị cắt. B18 thiếu tín hiệu định dạng người gửi `Từ số …`. Hai thiếu sót cuối làm người dùng khó biết vì sao hệ thống đưa ra kết quả.
- Nếu có thêm một tuần, kiểm thử việc phân biệt URL đăng nhập chính thức với nguồn chưa xác định, bổ sung định dạng người gửi và thử với nhân viên văn phòng để đo thời gian tự xác minh.
