# Canvas — F4VSB · Track E (Tài chính)

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".
> Track F: chép thêm thẻ đề của nhóm (khung trong file track F) xuống dưới bảng này.

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | Track E — đánh giá rủi ro của **một SMS** yêu cầu thao tác tài khoản ngân hàng/ví điện tử hoặc chuyển tiền, do người dùng tự dán vào công cụ. |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") | Nhân viên văn phòng dùng ứng dụng ngân hàng/ví điện tử hằng ngày, vừa nhận một SMS yêu cầu đăng nhập, xác minh tài khoản hoặc chuyển tiền. |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả | Nhân viên văn phòng khi nhận SMS yêu cầu thao tác tài khoản hoặc chuyển tiền mất thời gian tự kiểm tra vì không nhớ kênh liên hệ chính thức, nên có lúc vẫn không chắc nên dừng hay xác minh ở đâu. |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | **Phỏng vấn 3 người** (nhân viên văn phòng dùng app ngân hàng + ví): 2/3 nhận tin yêu cầu thao tác tài khoản/chuyển tiền trong tháng qua; lần gần nhất mất **~10–60 phút** để quyết định; **3/3 không nhớ số tổng đài chính thức**; 1/3 lần đó không kiểm qua kênh chính thức; 0/3 bấm link. Trích: *"Mình thường hỏi người quen trước vì không biết gọi số nào."* — P3. Nguồn: `evidence/summary.md`, `evidence/interviews/P1.md`–`P3.md`. Bằng chứng gồm SMS và Zalo; chưa có số riêng cho SMS. Khảo sát ≥20 người chưa mở. |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | Khi một nhân viên văn phòng dán một SMS yêu cầu thao tác tài khoản hoặc chuyển tiền, AI dựa vào tín hiệu trong tin, danh bạ chính thức và quy tắc tên miền để quyết định **có dấu hiệu rủi ro cao hay chưa đủ căn cứ**, rồi trả lý do cùng kênh chính thức để người dùng tự xác minh. |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | AI chỉ phân tích SMS và gợi ý hướng xác minh; không tự đọc hộp thư, truy cập tài khoản, bấm liên kết hay chuyển tiền. Không có đủ căn cứ thì báo chưa đủ căn cứ, không kết luận tin an toàn; người dùng tự quyết vì đánh giá sai có thể khiến họ mất tiền hoặc lộ thông tin tài khoản. |
| 7 | Phân công có tên | Nguyễn Công Quân — `spec.md` §4, §5, §7, canvas và kiểm CP2; Vũ Quang Minh — giả thuyết, phỏng vấn, tổng hợp bằng chứng; Trần Việt Thịnh — danh bạ kênh chính thức, quy tắc SMS, data card; Nguyễn Văn Đăng — công cụ, luồng chạy thử, bộ câu thử và metric. |
| — | *(CP2)* Đã đổi gì so với CP1 | Thu hẹp từ SMS/Zalo/email sang **SMS do người dùng dán** để khớp dữ liệu và quy tắc của bản chạy thử (`data/DATA_CARD.md`); sửa pain từ nguy cơ bấm link/chuyển tiền sang **mất thời gian và thiếu kênh xác minh**, vì 3 phỏng vấn ghi nhận 10–60 phút, 3/3 không nhớ số tổng đài và 0/3 bấm link (`evidence/summary.md`). |
