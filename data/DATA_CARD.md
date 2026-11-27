# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp.

## Dataset 1 · Danh bạ kênh chính thức ngân hàng & ví điện tử (`data/official_channels.json`)

| | |
|---|---|
| Dùng để làm gì | Nguồn căn cứ cho công cụ `lookup_official_channels` khi kiểm tra tin nhắn SMS (đối chiếu `sms_brandnames`, `official_domains` xuất hiện trong nội dung SMS, và cung cấp `official_hotlines` để người dùng tự gọi xác minh) · nguồn `data_that` cho bộ câu thử `eval/benchmark.csv` (6/20 câu dùng tên miền thật trong danh bạ). |
| Từ đâu | Tổng hợp trực tiếp từ trang chủ / mục Liên hệ chính thức của 10 tổ chức tại Việt Nam: Vietcombank (`vietcombank.com.vn`), BIDV (`bidv.com.vn`), VietinBank (`vietinbank.vn`), Techcombank (`techcombank.com`), MB Bank (`mbbank.com.vn`), VPBank (`vpbank.com.vn`), ACB (`acb.com.vn`), Agribank (`agribank.com.vn`), MoMo (`momo.vn`), ZaloPay (`zalopay.vn`). |
| Xử lý những bước gì | Tra cứu tên miền gốc, tên hiển thị SMS Brandname phổ biến, số hotline CSKH 24/7 và email hỗ trợ từ nguồn chính thức → chuẩn hóa sang JSON gồm `aliases`, `sms_brandnames`, `official_domains`, `official_hotlines`, `official_emails`, `verify_guidance`, `source_url`, `verified_date`. Không chứa dữ liệu cá nhân. |
| Số dòng / số đoạn | 10 tổ chức (8 ngân hàng thương mại + 2 ví điện tử). |
| Phiên bản / ngày lấy | `v0.3-cp3-sms` · 27/11/2026 (Trần Việt Thịnh phụ trách rà soát và chốt nguồn CP3). |
| Nhãn | thật (thông tin công khai từ kênh chính thức). |
| Giới hạn | Mới phủ 10 ngân hàng/ví phổ biến nhất, chưa phủ toàn bộ các ngân hàng nhỏ, công ty tài chính hay dịch vụ công; các hotline/tên miền có thể thay đổi theo thời gian. Đặc biệt với kênh SMS, `sms_brandnames` vẫn có thể bị giả mạo qua trạm phát sóng giả (fake BTS), nên không dùng `sms_brandnames` làm bằng chứng duy nhất để kết luận an toàn. Với tổ chức ngoài danh bạ, hệ thống phải báo chưa có dữ liệu để đối chiếu (nguyên tắc G10). |

## Dataset 2 · Bộ quy tắc tên miền giả, người gửi SMS & dấu hiệu rủi ro (`data/domain_rules.json`)

| | |
|---|---|
| Dùng để làm gì | Nguồn quy tắc tất định cho công cụ `check_domain_rules` và `extract_message_signals` chuyên sâu cho tin nhắn SMS (phát hiện link rút gọn, IP trần, HTTP không mã hóa, punycode, đuôi tên miền rủi ro cao, giả mạo thương hiệu trong subdomain/lookalike, tệp `.apk`, đầu số di động cá nhân giả danh ngân hàng, bẫy trạm BTS giả mạo SMS Brandname, và từ khóa đòi OTP/chuyển tiền/đổi điểm thưởng/cập nhật sinh trắc học). |
| Từ đâu | Nhóm tự biên soạn dựa trên khuyến cáo cảnh báo lừa đảo SMS Brandname của các ngân hàng/ví điện tử tại Việt Nam (không thu thập dữ liệu cá nhân). |
| Xử lý những bước gì | Phân tách thành 3 nhóm quy tắc độc lập: `domain_rules` (8 quy tắc URL/tên miền), `sms_sender_rules` (3 quy tắc đặc thù người gửi SMS gồm số di động cá nhân, Brandname biến tấu, và cảnh báo fake BTS), và `content_signal_rules` (4 nhóm tín hiệu nội dung SMS). |
| Số dòng / số đoạn | 8 quy tắc tên miền/URL + 3 quy tắc người gửi SMS + 4 nhóm quy tắc tín hiệu nội dung + 2 ghi chú bảo mật. |
| Phiên bản / ngày lấy | `v0.2-cp2-sms` · 27/11/2026. |
| Nhãn | nhóm tự biên soạn (quy tắc kiểm tra tất định, không phải bằng chứng pain). |
| Giới hạn | Quy tắc từ khóa và danh sách TLD/link rút gọn có thể bỏ sót thủ đoạn biến tấu chữ mới hoặc cảnh báo thận trọng với SMS quảng cáo hợp lệ có dùng link rút gọn. Vì vậy hệ thống luôn nêu rõ từng quy tắc bị kích hoạt và hướng dẫn người dùng tự kiểm tra qua ứng dụng/hotline chính thức, không tự khẳng định 100%. |
