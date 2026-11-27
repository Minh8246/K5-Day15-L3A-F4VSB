# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp.

## Dataset 1 · Danh bạ kênh chính thức ngân hàng & ví điện tử (`data/official_channels.json`)

| | |
|---|---|
| Dùng để làm gì | Nguồn căn cứ cho công cụ `lookup_official_channels` (đối chiếu tên miền, hotline, email hỗ trợ chính thức và sinh hướng dẫn tự xác minh). |
| Từ đâu | Tổng hợp trực tiếp từ trang chủ / mục Liên hệ chính thức của 10 tổ chức tại Việt Nam: Vietcombank (`vietcombank.com.vn`), BIDV (`bidv.com.vn`), VietinBank (`vietinbank.vn`), Techcombank (`techcombank.com`), MB Bank (`mbbank.com.vn`), VPBank (`vpbank.com.vn`), ACB (`acb.com.vn`), Agribank (`agribank.com.vn`), MoMo (`momo.vn`), ZaloPay (`zalopay.vn`). |
| Xử lý những bước gì | Tra cứu tên miền gốc, số hotline CSKH 24/7 và email hỗ trợ từ nguồn chính thức → chuẩn hóa sang JSON có cấu trúc gồm `aliases`, `official_domains`, `official_hotlines`, `official_emails`, `verify_guidance`, `source_url`, `verified_date`. Không chứa dữ liệu cá nhân. |
| Số dòng / số đoạn | 10 tổ chức (8 ngân hàng thương mại + 2 ví điện tử). |
| Phiên bản / ngày lấy | `v0.1-cp2` · 27/11/2026 (Trần Việt Thịnh phụ trách rà soát nguồn). |
| Nhãn | thật (thông tin công khai từ kênh chính thức). |
| Giới hạn | Mới phủ 10 ngân hàng/ví phổ biến nhất, chưa phủ toàn bộ các ngân hàng nhỏ, công ty tài chính hay dịch vụ công; các hotline/tên miền có thể thay đổi theo thời gian. Với tổ chức ngoài danh bạ, hệ thống phải báo chưa có dữ liệu để đối chiếu (nguyên tắc G10) thay vì tự đoán. |

## Dataset 2 · Bộ quy tắc tên miền giả & dấu hiệu rủi ro (`data/domain_rules.json`)

| | |
|---|---|
| Dùng để làm gì | Nguồn quy tắc tất định cho công cụ `check_domain_rules` và `extract_message_signals` (phát hiện link rút gọn, IP trần, HTTP không mã hóa, punycode, đuôi tên miền rủi ro cao, giả mạo thương hiệu trong subdomain/lookalike, tệp `.apk`, và từ khóa yêu cầu OTP/chuyển tiền/thúc ép khẩn cấp). |
| Từ đâu | Nhóm tự biên soạn dựa trên khuyến cáo an toàn thông tin phổ biến của các ngân hàng/ví điện tử (không thu thập dữ liệu cá nhân). |
| Xử lý những bước gì | Phân tách thành 2 nhóm quy tắc độc lập: `domain_rules` (8 quy tắc URL/tên miền, gán mức `medium`/`high`) và `content_signal_rules` (4 nhóm tín hiệu nội dung). Bổ sung `security_notes` về rủi ro giả mạo SMS Brandname (fake BTS). |
| Số dòng / số đoạn | 8 quy tắc tên miền/URL + 4 nhóm quy tắc tín hiệu nội dung + 2 ghi chú bảo mật. |
| Phiên bản / ngày lấy | `v0.1-cp2` · 27/11/2026. |
| Nhãn | nhóm tự biên soạn (quy tắc kiểm tra tất định, không phải bằng chứng pain). |
| Giới hạn | Quy tắc từ khóa và danh sách TLD/link rút gọn có thể bỏ sót thủ đoạn mới hoặc cảnh báo nhầm (false positive) với một số chiến dịch rút gọn link hợp pháp. Vì vậy hệ thống luôn giải thích lý do cụ thể và hướng dẫn người dùng tự kiểm tra qua kênh chính thức, không tự khẳng định 100%. |
