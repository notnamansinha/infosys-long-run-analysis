from pathlib import Path
import csv
import re


ROOT = Path(__file__).resolve().parent
BLOCKED_TERMS = ("bloom" + "berg",)
BLOCKED_SUFFIXES = (".eml", ".xls", ".xlsx", ".pdf", ".docx")
IGNORED_DIRS = {".git", "__pycache__", ".venv", "venv"}
LOCAL_ONLY_PATHS = {
    ("private-archive",),
    ("data", "raw"),
    ("data", "derived"),
    ("output",),
}
TEXT_SUFFIXES = {".md", ".py", ".txt", ".cff", ".csv", ".json", ".yaml", ".yml"}
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+\d{1,3}[\s.-]?)?(?:\d[\s().-]?){10,14}(?!\d)")
SECRET_PATTERN = re.compile(
    r"\b(?:ghp_|github_pat_)[A-Za-z0-9]{20,}\b|\bsk-[A-Za-z0-9_-]{20,}\b|\bAKIA[0-9A-Z]{16}\b|\bxox[baprs]-[A-Za-z0-9-]{20,}\b"
)
DIRECT_IDENTIFIER_HEADERS = {
    "name", "full_name", "first_name", "last_name", "email", "email_address",
    "phone", "phone_number", "mobile", "address", "street_address", "account_id",
    "user_id", "customer_id", "client_id", "ssn", "tax_id", "passport",
    "national_id", "ip_address",
}


def files_in_public_tree():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(ROOT).parts
        if any(part in IGNORED_DIRS for part in relative_parts):
            continue
        if any(relative_parts[:len(prefix)] == prefix for prefix in LOCAL_ONLY_PATHS):
            continue
        yield path


def main():
    failures = []
    for path in files_in_public_tree():
        rel = path.relative_to(ROOT).as_posix()
        lower_rel = rel.lower()
        if any(term in lower_rel for term in BLOCKED_TERMS):
            failures.append(f"blocked name: {rel}")
        if path.suffix.lower() in BLOCKED_SUFFIXES:
            failures.append(f"restricted suffix: {rel}")
        if path.suffix.lower() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for term in BLOCKED_TERMS:
                if term in text:
                    failures.append(f"blocked text: {rel}")
                    break
            if EMAIL_PATTERN.search(text):
                failures.append(f"possible email address: {rel}")
            if SECRET_PATTERN.search(text):
                failures.append(f"possible credential: {rel}")
            if path.suffix.lower() == ".csv":
                with path.open(newline="", encoding="utf-8", errors="ignore") as handle:
                    headers = next(csv.reader(handle), [])
                normalized = {re.sub(r"[\s-]+", "_", header.strip().lower()) for header in headers}
                for header in sorted(normalized & DIRECT_IDENTIFIER_HEADERS):
                    failures.append(f"possible direct identifier column '{header}': {rel}")
                if PHONE_PATTERN.search(text):
                    failures.append(f"possible phone number: {rel}")
    if failures:
        print("PUBLIC RELEASE CHECK FAILED")
        print("\n".join(sorted(set(failures))))
        return 1
    print("PUBLIC RELEASE CHECK PASSED")
    print(f"Scanned {sum(1 for _ in files_in_public_tree())} public files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
