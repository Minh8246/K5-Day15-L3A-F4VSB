"""Luồng cố định đánh giá rủi ro của một SMS.

`python run.py`, `python run.py eval` và `python run.py simulate` đều gọi answer(text).

Hợp đồng:
    answer(text: str) -> dict có khoá "output" (str): kết quả đưa cho người dùng.
    Token, tên model, số lần gọi model / công cụ: khung tự đếm qua call_model và @tool — không cần trả.
    Bộ chạy gửi NGUYÊN ô input của câu thử vào text. Dữ liệu nền (bài học, thông báo, lịch…)
    do luồng của nhóm tự đọc qua công cụ trong tools.py.

"""
import json

from ai import HIGH_RISK, MODEL_PROVIDER, call_model
from tools import check_domain_rules, extract_message_signals, lookup_official_channels

SYSTEM = (
    "Phân loại rủi ro của một SMS ngân hàng hoặc ví điện tử bằng các dữ kiện đã kiểm. "
    'Chỉ trả một đối tượng JSON, ví dụ {"label":"CHUA_DU_CAN_CU"}. '
    "Chọn RUI_RO_CAO nếu có tín hiệu high, hoặc nhiều tín hiệu medium "
    "độc lập cùng cho thấy người nhận bị dẫn tới một thao tác không đáng tin. "
    "Chọn CHUA_DU_CAN_CU nếu còn nghi ngờ, chỉ có một tín hiệu medium, hoặc không có tín hiệu. "
    "Tên người gửi và tên miền khớp danh bạ không chứng minh được nguồn gửi."
)


def answer(text: str) -> dict:
    """Phân tích một SMS, chỉ trả cảnh báo và cách người dùng tự xác minh."""
    signals = extract_message_signals(text)
    if not signals["message"]:
        return {"output": "CHƯA ĐỦ CĂN CỨ: Hãy dán nội dung một SMS đã che thông tin cá nhân để kiểm tra."}
    official = lookup_official_channels(signals["organization"])
    checked = check_domain_rules(signals, official)
    context = json.dumps({"organization": official, "findings": checked["findings"],
                          "has_sender": bool(signals["sender"]), "has_url": bool(signals["urls"])},
                         ensure_ascii=False)
    model = call_model(SYSTEM, "Dữ kiện đã kiểm: " + context)
    # Giữ cảnh báo khi quy tắc đã tìm thấy căn cứ mạnh. Model đánh giá những tín hiệu còn lại.
    high = checked["has_high_risk"] or (
        bool(checked["findings"]) and model["text"] == HIGH_RISK
    )
    label = "CÓ DẤU HIỆU RỦI RO CAO" if high else "CHƯA ĐỦ CĂN CỨ ĐỂ KẾT LUẬN AN TOÀN"
    reasons = ["[%s] %s" % (f["id"], f["reason"]) for f in checked["findings"]]
    if len(signals["organizations"]) > 1:
        reasons.append("SMS nhắc nhiều tổ chức; chưa xác định được một nguồn để đối chiếu.")
    elif not official["found"]:
        reasons.append("Chưa xác định được tổ chức trong danh bạ hiện có.")
    if not reasons:
        reasons.append("Chưa thấy tín hiệu đủ mạnh trong dữ liệu hiện có; điều này không chứng minh SMS là thật.")
    result = [label, "Lý do: " + " ".join(reasons[:4])]
    if official["found"]:
        result.append("Danh bạ đối chiếu: %s; nguồn: %s." % (official["name"], official["source_url"]))
    result.append("Tự xác minh: không bấm link hoặc gọi số ghi trong SMS; tự mở ứng dụng ngân hàng/ví hoặc tra kênh liên hệ trên trang chính thức.")
    if MODEL_PROVIDER == "fake":
        result.append("[Bản chạy thử: model giả, chưa phải kết quả đánh giá bằng AI thật.]")
    return {"output": "\n".join(result)}
