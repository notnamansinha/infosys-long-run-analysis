"""Create a small, allow-listed CSV from an already-authorized input.

This is a privacy and minimization aid, not a licence checker or legal opinion.
The output should remain local until the release checklist is complete.
"""

from __future__ import annotations

import argparse
import csv
import re
import tempfile
from pathlib import Path


DIRECT_IDENTIFIER_HEADERS = {
    "name", "full_name", "first_name", "last_name", "email", "email_address",
    "phone", "phone_number", "mobile", "address", "street_address", "account_id",
    "user_id", "customer_id", "client_id", "ssn", "tax_id", "passport",
    "national_id", "ip_address",
}
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+\d{1,3}[\s.-]?)?(?:\d[\s().-]?){10,14}(?!\d)")


def normalized_header(value: str) -> str:
    return re.sub(r"[\s-]+", "_", value.strip().lower())


def normalize_category(value: str) -> str:
    """Canonicalize harmless formatting differences without inventing labels."""

    return re.sub(r"[\s_/-]+", " ", value.strip().casefold())


def parse_columns(value: str) -> list[str]:
    columns = [item.strip() for item in value.split(",") if item.strip()]
    if not columns:
        raise argparse.ArgumentTypeError("provide at least one column")
    if len(set(columns)) != len(columns):
        raise argparse.ArgumentTypeError("duplicate column in --keep")
    return columns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write an allow-listed, minimally transformed CSV for a rights-cleared release."
    )
    parser.add_argument("input", type=Path, help="authorized local CSV input")
    parser.add_argument(
        "--keep",
        required=True,
        type=parse_columns,
        help="comma-separated columns to retain; every other column is dropped",
    )
    parser.add_argument(
        "--category-columns",
        type=parse_columns,
        default=[],
        help="comma-separated retained columns to normalize for whitespace, case, and separators",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/public_subset.csv"),
        help="local output path (defaults to ignored data/derived/)",
    )
    parser.add_argument(
        "--rights-confirmed",
        action="store_true",
        help="confirm that the permission expressly covers public redistribution of this result",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.rights_confirmed:
        raise SystemExit(
            "Refusing to write: pass --rights-confirmed only after reviewing the release checklist."
        )
    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}")

    keep_headers = args.keep
    keep_normalized = {normalized_header(header) for header in keep_headers}
    forbidden = sorted(keep_normalized & DIRECT_IDENTIFIER_HEADERS)
    if forbidden:
        raise SystemExit(f"Refusing direct-identifier columns: {', '.join(forbidden)}")

    category_headers = set(args.category_columns)
    unknown_categories = sorted(category_headers - set(keep_headers))
    if unknown_categories:
        raise SystemExit(
            "Category columns must also appear in --keep: " + ", ".join(unknown_categories)
        )

    with args.input.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        headers = reader.fieldnames or []
        missing = [header for header in keep_headers if header not in headers]
        if missing:
            raise SystemExit(f"Missing input columns: {', '.join(missing)}")

        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                "w",
                newline="",
                encoding="utf-8",
                delete=False,
                dir=args.output.parent,
                prefix=f".{args.output.name}.",
                suffix=".tmp",
            ) as destination:
                temporary_path = Path(destination.name)
                writer = csv.DictWriter(destination, fieldnames=keep_headers, extrasaction="ignore")
                writer.writeheader()
                rows = 0
                for row in reader:
                    selected = {header: row.get(header, "") for header in keep_headers}
                    if any(
                        EMAIL_PATTERN.search(value) or PHONE_PATTERN.search(value)
                        for value in selected.values()
                    ):
                        raise SystemExit(
                            f"Refusing possible direct identifier in input row {rows + 2}; no output was published."
                        )
                    for header in category_headers:
                        selected[header] = normalize_category(selected[header])
                    writer.writerow(selected)
                    rows += 1
            temporary_path.replace(args.output)
        except BaseException:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise

    print(f"Wrote {rows} rows and {len(keep_headers)} columns to {args.output}")
    print("Keep the output local until rights, privacy, and provenance reviews are complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
