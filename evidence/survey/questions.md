# Khảo sát — tin nhắn yêu cầu thao tác tài khoản / chuyển tiền

> Nguồn để kiểm lại giả thuyết ở `evidence/hypothesis.md`. Ngưỡng: **≥20 người ngoài nhóm, đúng người dùng** (có dùng app ngân hàng hoặc ví điện tử trên điện thoại).
> Hỏi **hành vi đã xảy ra**, không hỏi "có thích không". Không thu tên, SĐT, email, số tài khoản.

- Kênh gửi: __ (vd nhóm lớp, nhóm Zalo gia đình / công ty — ghi rõ kênh nào)
- Giờ mở form: __ · giờ chốt: __
- Link form: __

## Câu hỏi

| # | Câu hỏi | Kiểu trả lời |
|---|---|---|
| 1 | Bạn đang dùng những dịch vụ nào trên điện thoại? | Chọn nhiều: app ngân hàng · ví điện tử (MoMo, ZaloPay…) · không dùng cái nào *(chọn "không dùng" → kết thúc form)* |
| 2 | Lần gần nhất bạn nhận tin nhắn (SMS / Zalo / email) yêu cầu đăng nhập, xác minh tài khoản, cung cấp mã hoặc chuyển tiền là khi nào? | Hôm nay · tuần này · trong tháng này · lâu hơn 1 tháng · chưa bao giờ *(chưa bao giờ → nhảy câu 8)* |
| 3 | Trong 1 tháng qua, bạn nhận tin kiểu này khoảng mấy lần? | Số |
| 4 | Lần gần nhất đó, lúc đầu bạn có chắc tin đó thật hay giả không? | Chắc là thật · chắc là giả · không chắc |
| 5 | Lần đó bạn đã làm gì? | Chọn nhiều: xoá / bỏ qua · xem tên người gửi · xem đường link · bấm thử link · mở app ngân hàng / ví để kiểm · gọi tổng đài chính thức · gọi số trong tin · hỏi người quen · tra Google · khác |
| 6 | Lần đó bạn mất khoảng bao lâu để quyết định? | Dưới 1' · 1–5' · 5–15' · trên 15' |
| 7 | Sau cùng bạn có chắc mình xử lý đúng không? | Chắc · không chắc lắm · đến giờ vẫn không biết |
| 8 | Bạn có nhớ số tổng đài hoặc trang web chính thức của ngân hàng / ví bạn dùng nhiều nhất không? | Nhớ · biết chỗ tra · không biết |
| 9 | Bạn hoặc người quen đã từng bấm link / đưa OTP / chuyển tiền theo một tin như vậy chưa? | Bản thân đã từng · người quen đã từng · chưa · không muốn trả lời |
| 10 | (tuỳ chọn) Điều gì khiến bạn khó quyết định nhất ở lần đó? | Đoạn văn |

## Lưu kết quả

- `results.csv` — bản xuất **đã xoá** mọi cột nhận ra người trả lời. Bản gốc còn thông tin cá nhân thì **không** commit.
- Số chính + ≥3 câu trả lời nguyên văn (câu 10) → chép vào `evidence/summary.md`. Dưới khoảng 10 người thì chỉ ghi x/n, không ghi %.
