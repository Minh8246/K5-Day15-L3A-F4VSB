"""Công cụ đọc dữ liệu công khai và phân tích một SMS do người dùng tự dán."""
import ipaddress
import json
import os
import re
from urllib.parse import urlsplit

from tracing import tool

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
NEGATED_REQUEST = re.compile(r"\b(?:đừng|chớ|không(?:\s+(?:được|nên|cần|bao giờ|yêu cầu))*)\s+$")


def _data(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as handle:
        return json.load(handle)


@tool
def extract_message_signals(message: str) -> dict:
    """Tách tín hiệu SMS. Input: văn bản SMS. Output: người gửi, tổ chức, URL. Tác động ra ngoài: không."""
    content = (message or "").strip()
    match = re.search(r"(?im)^\s*(?:người gửi|sender)\s*:\s*(.+)$", content)
    sender = match.group(1).strip() if match else ""
    urls = re.findall(r"(?:https?://|www\.)[^\s<>\"']+", content, flags=re.I)
    urls = [url.rstrip(".,;!?)") for url in urls]
    mentioned = []
    for item in _data("official_channels.json")["organizations"]:
        names = [item["name"]] + item.get("aliases", []) + item.get("sms_brandnames", [])
        if any(re.search(r"(?<!\w)" + re.escape(name.casefold()) + r"(?!\w)", content.casefold()) for name in names if len(name) >= 3):
            mentioned.append(item["id"])
    mentioned = list(dict.fromkeys(mentioned))
    return {"sender": sender, "organizations": mentioned,
            "organization": mentioned[0] if len(mentioned) == 1 else "",
            "urls": urls, "message": content}


@tool
def lookup_official_channels(organization: str) -> dict:
    """Tra kênh chính thức. Input: mã tổ chức. Output: tên miền và nguồn hoặc chưa có dữ liệu. Tác động ra ngoài: không."""
    for item in _data("official_channels.json")["organizations"]:
        if organization and organization.casefold() in (item["id"].casefold(), item["name"].casefold()):
            return {"found": True, "id": item["id"], "name": item["name"],
                    "official_domains": item.get("official_domains", []),
                    "source_url": item.get("source_url", "")}
    return {"found": False, "reason": "Không xác định được tổ chức trong danh bạ."}


@tool
def check_domain_rules(signals: dict, official: dict) -> dict:
    """Kiểm quy tắc SMS. Input: tín hiệu và danh bạ. Output: mã quy tắc, lý do, mức độ. Tác động ra ngoài: không."""
    rules = _data("domain_rules.json")
    findings = []

    def add(code, severity, reason):
        if code not in {entry["id"] for entry in findings}:
            findings.append({"id": code, "severity": severity, "reason": reason})

    domains = [d.casefold() for d in official.get("official_domains", [])]
    shorteners = next(r["shortener_domains"] for r in rules["domain_rules"] if r["id"] == "R_SHORTENER")
    suspect_tlds = next(r["suspicious_tlds"] for r in rules["domain_rules"] if r["id"] == "R_SUSPICIOUS_TLD")
    for url in signals.get("urls", []):
        try:
            parsed = urlsplit(url if "://" in url else "https://" + url)
            host = (parsed.hostname or "").rstrip(".").casefold()
        except ValueError:
            continue
        official_host = any(host == d or host.endswith("." + d) for d in domains)
        if host in shorteners:
            add("R_SHORTENER", "high", "URL rút gọn che tên miền đích.")
        try:
            ipaddress.ip_address(host)
            add("R_RAW_IP", "high", "URL trỏ trực tiếp tới địa chỉ IP.")
        except ValueError:
            pass
        if parsed.scheme == "http":
            add("R_NO_HTTPS", "medium", "URL dùng http thay vì https.")
        if "xn--" in host:
            add("R_PUNYCODE", "high", "Tên miền có mã punycode cần xác minh.")
        if not official_host and any(host.endswith(tld) for tld in suspect_tlds):
            add("R_SUSPICIOUS_TLD", "medium", "Đuôi tên miền cần kiểm tra thêm.")
        if domains and not official_host:
            add("R_DOMAIN_MISMATCH", "high", "Tên miền không thuộc danh bạ chính thức của tổ chức.")
        if re.search(r"\.(?:apk|exe|msi|zip|rar)$", parsed.path, re.I):
            add("R_APK_OR_EXECUTABLE", "high", "URL dẫn tới tệp cài đặt hoặc tệp nén.")

    sender = signals.get("sender", "")
    if official.get("found") and re.fullmatch(r"(?:\+?84|0)[35789]\d{8}", sender):
        add("R_SMS_PERSONAL_SENDER", "high", "Số cá nhân tự xưng là tổ chức tài chính.")
    text = signals.get("message", "").casefold()
    for rule in rules["content_signal_rules"]:
        requests = rule.get("requests")
        if requests:
            for request in requests:
                matches = re.finditer(request["pattern"], text)
                if any(not NEGATED_REQUEST.search(text, 0, match.start()) for match in matches):
                    add(rule["id"], rule["severity"], request.get("reason", rule["description"]))
                    break
        elif any(word.casefold() in text for word in rule.get("keywords", [])):
            add(rule["id"], rule["severity"], rule["description"])
    return {"findings": findings,
            "has_high_risk": any(f["severity"] == "high" for f in findings)}
