# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona.** Dùng ít 33% và 0,5 phiên/người/tháng, dùng vừa 34% và 2 phiên, dùng nhiều 33% và 3 phiên. P1 ghi nhận 0 tin tháng gần nhất, P2 khoảng 2 và P3 khoảng 3. Các tỷ trọng, tần suất 0,5 và giả định mỗi tin dẫn tới một phiên đều tự ước tính. Một phiên xử lý một SMS. Nguồn tần suất ở `evidence/summary.md`.
- **Quy mô thử nghiệm.** Kịch bản thấp 50 người, cơ sở 100 người, cao 300 người, đều tự ước tính. Kịch bản cơ sở dùng cùng quy mô với `spec.md` §2.
- **Giá.** Dùng giá trả phí giờ cao điểm, token vào tính theo cache miss. Đơn vị USD trên 1 triệu token vào/ra. `deepseek-flash` $0.30/$1.20, `deepseek-v4-pro` $1.32/$3.96. [Bảng giá DeepSeek, xem 28/11/2026](https://api-docs.deepseek.com/quick_start/pricing/)
- **Tỷ lệ đầu vào.** 20/20 (100%) từ `run-2@20261128-001757` của `deepseek-flash`. Đây là kết quả trên bộ thử.
- Token đo bằng `deepseek-flash`. Cột giá Pro là ước tính bằng cách áp giá của Pro lên lượng token đã đo bằng Flash.

## 2. Kết quả mô phỏng

Lượt `simulate-1@20261128-001940` chạy 50 phiên, seed 42, 0 phiên lỗi. Chi tiết trong `cost/simulate-1.csv` và `cost/simulate-1-summary.md`.

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| `deepseek-flash` | $0.00011 | $0.00011 | $0.0105 | $0.0210 | $0.0631 | $0.00021 |
| `deepseek-v4-pro` | $0.00048 | $0.00048 | $0.0449 | $0.0899 | $0.2697 | $0.00090 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- **Impact hiện tại.** Quy mô cơ sở quy đổi khoảng 33,5 phút tự xác minh/người/tháng từ 3.350 phút/100 người/tháng trong `spec.md` §2. Đây là thời gian kiểm tra ước tính trước khi dùng công cụ. Mức tiết kiệm cần đo khi dùng thử.
- **Chi phí cơ sở.** Khoảng $0.00021/người/tháng tiền model với `deepseek-flash`.
- **Kết luận.** Chi phí token thấp ở quy mô thử nghiệm. Thử giới hạn với nhân viên văn phòng để đo thời gian thực tế và mức hữu ích trước khi quyết định mở rộng.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
