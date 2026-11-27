"""Run the project's SMS workflow for a single web request."""

import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codebase"))

from agent import answer
import tracing


def main():
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    request = json.load(sys.stdin)
    tracing.begin("web")
    try:
        output = answer(request["message"])["output"]
    finally:
        summary, _ = tracing.end()

    label, *details = output.splitlines()
    fields = {}
    for detail in details:
        heading, _, value = detail.partition(": ")
        fields[heading] = value

    organization, _, source = fields.get("Danh bạ đối chiếu", "").partition("; nguồn: ")
    source = source.removesuffix(".")
    parsed_source = urlsplit(source)

    print(json.dumps({
        "risk": "high" if label == "CÓ DẤU HIỆU RỦI RO CAO" else "uncertain",
        "label": label,
        "reason": fields.get("Lý do", ""),
        "organization": organization,
        "source": source if parsed_source.scheme == "https" and parsed_source.hostname else "",
        "guidance": fields.get("Tự xác minh", ""),
        "model": ", ".join(summary["models"]),
        "tokensIn": summary["tokens_in"],
        "tokensOut": summary["tokens_out"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
