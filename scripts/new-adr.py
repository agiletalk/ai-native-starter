#!/usr/bin/env python3
"""새 ADR 초안을 만들고 docs/index.html에 링크를 추가한다.

사용법: scripts/new-adr.py <slug> "<제목>"
예:     scripts/new-adr.py payment-provider "결제사는 토스페이먼츠로 한다"
"""
import datetime
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADR_DIR = ROOT / "docs" / "adr"
INDEX = ROOT / "docs" / "index.html"
MARKER = "<!-- new-adr:"


def main() -> int:
    if len(sys.argv) != 3 or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", sys.argv[1]):
        print(__doc__.strip(), file=sys.stderr)
        print("\nslug는 영문 소문자·숫자·하이픈만 쓴다.", file=sys.stderr)
        return 2
    slug, title = sys.argv[1], html.escape(sys.argv[2].strip())

    numbers = [int(m.group(1)) for p in ADR_DIR.glob("*.html")
               if (m := re.match(r"(\d{4})-", p.name))]
    number = f"{max(numbers, default=0) + 1:04d}"
    target = ADR_DIR / f"{number}-{slug}.html"

    try:
        author = subprocess.run(["git", "config", "user.name"], capture_output=True,
                                text=True, cwd=ROOT).stdout.strip() or "이름"
    except FileNotFoundError:
        author = "이름"

    body = (ADR_DIR / "_template.html").read_text(encoding="utf-8")
    body = (body.replace("NNNN", number)
                .replace("제목", title)
                .replace("YYYY-MM-DD", datetime.date.today().isoformat())
                .replace("작성자 이름", f"작성자 {author}"))
    target.write_text(body, encoding="utf-8")

    index = INDEX.read_text(encoding="utf-8")
    link = f'<li><a href="adr/{target.name}">ADR-{number}: {title}</a></li>'
    lines = index.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if MARKER in line:
            indent = line[: len(line) - len(line.lstrip())]
            lines.insert(i, f"{indent}{link}\n")
            break
    else:
        print(f"경고: {INDEX.name}에서 '{MARKER}' 표시를 못 찾아 링크를 추가하지 않았다.", file=sys.stderr)
    INDEX.write_text("".join(lines), encoding="utf-8")

    print(target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
