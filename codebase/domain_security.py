"""So khớp tên miền đồng hình bằng dữ liệu ký tự Unicode."""

import unicodedata
from functools import cache
from pathlib import Path


DOMAIN_DOTS = str.maketrans("\u3002\uff0e\uff61", "...")
CONFUSABLES = Path(__file__).resolve().parents[1] / "data" / "unicode-confusables.txt"


def hostname_labels(hostname: str) -> list[str]:
    return hostname.translate(DOMAIN_DOTS).removesuffix(".").lower().split(".")


def decode_hostname(labels: list[str]) -> str:
    """Đưa nhãn Unicode và Punycode về NFC để đối chiếu tên miền."""
    decoded_labels = []
    for label in labels:
        if not 0 < len(label) <= 63:
            return ""
        if label.startswith("xn--"):
            try:
                decoded = label[4:].encode("ascii").decode("punycode")
                if decoded.isascii():
                    return ""
                if decoded.encode("punycode").decode("ascii") != label[4:]:
                    return ""
            except (UnicodeError, OverflowError):
                return ""
            label = decoded

        # Giữ ranh giới nhãn và từ chối ký tự điều khiển hoặc dấu phân cách.
        if any(
            char != "-" and unicodedata.category(char)[0] not in "LMN"
            for char in label
        ):
            return ""
        decoded_labels.append(unicodedata.normalize("NFC", label))

    return ".".join(decoded_labels)


def belongs_to(hostname: str, domain: str) -> bool:
    return hostname == domain or hostname.endswith("." + domain)


@cache
def _confusable_map() -> dict[int, str]:
    mapping = {}
    with CONFUSABLES.open(encoding="utf-8-sig") as data:
        for line in data:
            fields = line.partition("#")[0].split(";")
            if len(fields) == 3:
                source, target, _ = fields
                mapping[int(source, 16)] = "".join(chr(int(cp, 16)) for cp in target.split())
    return mapping


def _label_skeleton(label: str) -> str:
    decomposed = unicodedata.normalize("NFD", label)
    return unicodedata.normalize("NFD", decomposed.translate(_confusable_map()))


def find_lookalike_domain(hostname: str, references: tuple[str, ...]) -> str:
    """Tìm tên miền tham chiếu có cùng dạng ký tự với hậu tố Unicode."""
    if any(belongs_to(hostname, domain) for domain in references):
        return ""

    labels = tuple(_label_skeleton(label) for label in hostname.split("."))
    for domain in references:
        reference = tuple(_label_skeleton(label) for label in domain.split("."))
        if labels[-len(reference):] == reference:
            return domain
    return ""
