# Tóm tắt mô phỏng simulate-1@20261128-001940

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 19 | 1 | 318 | 11 | 1.0 | 3.0 |
| dung_vua | 12 | 1 | 363 | 11 | 1.0 | 3.0 |
| dung_nhieu | 19 | 1 | 325 | 11 | 1.0 | 3.0 |

Tỉ lệ đạt dùng để tính: 20/20 (100%) — lượt run-2@20261128-001757

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (50 người) | Chi phí / tháng — cơ sở (100 người) | Chi phí / tháng — cao (300 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-flash (vào 0.3 · ra 1.2 $/1M) | $0.00011 | $0.00011 | $0.00011 | $0.0105 | $0.0210 | $0.0631 | $0.00021 |
| deepseek-v4-pro (vào 1.32 · ra 3.96 $/1M) | $0.00048 | $0.00048 | $0.00048 | $0.0449 | $0.0899 | $0.2697 | $0.00090 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: deepseek-flash. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
