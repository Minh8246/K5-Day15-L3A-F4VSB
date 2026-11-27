"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Model thật: DeepSeek Chat Completions. Cách cấu hình ở docs/connect-model.md.
"""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
DEEPSEEK_CHAT_URL = "https://api.deepseek.com/chat/completions"
HIGH_RISK = "RUI_RO_CAO"
INSUFFICIENT_EVIDENCE = "CHUA_DU_CAN_CU"


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if MODEL_PROVIDER != "deepseek":
        raise NotImplementedError("MODEL_PROVIDER phải là fake hoặc deepseek. Xem docs/connect-model.md.")
    if not MODEL_NAME or not API_KEY:
        raise NotImplementedError("Hãy điền MODEL_NAME và API_KEY của DeepSeek trong .env.")

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0,
        "max_tokens": 64,
        "thinking": {"type": "disabled"},
        "response_format": {"type": "json_object"},
    }
    request = Request(DEEPSEEK_CHAT_URL, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                      headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as error:
        hints = {401: "Xác minh API key.", 402: "Kiểm tra số dư API.", 429: "Giảm tốc độ gọi bằng --wait."}
        hint = hints.get(error.code, "Kiểm tra MODEL_NAME và trạng thái API.")
        raise RuntimeError(f"DeepSeek trả HTTP {error.code}. {hint}") from error
    except (URLError, TimeoutError) as error:
        raise RuntimeError("Không nhận được phản hồi từ API DeepSeek.") from error
    except ValueError as error:
        raise RuntimeError("API DeepSeek trả phản hồi không đọc được dưới dạng JSON.") from error

    try:
        label = json.loads(result["choices"][0]["message"]["content"])["label"]
        model = result["model"]
        tokens_in = result["usage"]["prompt_tokens"]
        tokens_out = result["usage"]["completion_tokens"]
    except (IndexError, KeyError, TypeError, ValueError) as error:
        raise RuntimeError("Phản hồi DeepSeek thiếu nhãn, tên model hoặc usage.") from error
    if label not in (HIGH_RISK, INSUFFICIENT_EVIDENCE):
        raise RuntimeError("DeepSeek trả nhãn ngoài hai giá trị cho phép.")
    if not isinstance(model, str) or not model.strip() or type(tokens_in) is not int or type(tokens_out) is not int or min(tokens_in, tokens_out) <= 0:
        raise RuntimeError("DeepSeek không trả tên model hoặc số token hợp lệ.")
    return {"text": label, "model": model, "tokens_in": tokens_in, "tokens_out": tokens_out}
