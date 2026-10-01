#!/usr/bin/env python3
from hashlib import sha256
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
NAME = "china-travel-decision"
CANONICAL = (ROOT / "skills" / NAME / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
VERSION_MATCH = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', CANONICAL, re.M)
AUTHOR_MATCH = re.search(r'^  author: "([^"\n]+)"$', CANONICAL, re.M)
if VERSION_MATCH is None or AUTHOR_MATCH is None:
    raise ValueError("Canonical metadata must contain a quoted version and author")
VERSION = VERSION_MATCH.group(1)
AUTHOR = AUTHOR_MATCH.group(1)
FILES = ("SKILL.md", "references/research-and-review.md", "references/offline-itinerary-html.md")


def build(platform: str, source: Path, destination: Path) -> Path:
    payloads = {relative: (source / relative).read_bytes() for relative in FILES}
    for relative, payload in payloads.items():
        if not payload.strip():
            raise ValueError(f"Empty source: {source / relative}")
    skill = payloads["SKILL.md"].decode("utf-8")
    header = skill.split("---", 2)[1]
    if f"name: {NAME}" not in header:
        raise ValueError(f"Unexpected skill name: {source}")
    if platform == "codex":
        required = ('metadata:', f'  version: "{VERSION}"', f'  author: "{AUTHOR}"')
        if set(re.findall(r"^([a-z_]+):", header, re.M)) != {"name", "description", "metadata"}:
            raise ValueError("Codex frontmatter must have name, description and metadata")
        for relative in FILES[1:]:
            if f"]({relative})" not in skill:
                raise ValueError(f"Missing Codex reference link: {relative}")
    else:
        required = (f"version: {VERSION}", f'author: "{AUTHOR}"', 'display_name: 中国旅行决策助手')
    if not all(value in header for value in required):
        raise ValueError(f"Unexpected {platform} frontmatter")

    archive = destination / f"{platform}-{NAME}-v{VERSION}.zip"
    temporary = archive.with_suffix(".zip.tmp")
    try:
        with ZipFile(temporary, "w", compression=ZIP_DEFLATED) as package:
            for relative, payload in payloads.items():
                entry = ZipInfo(f"{NAME}/{relative}", date_time=(2026, 1, 1, 0, 0, 0))
                entry.compress_type = ZIP_DEFLATED
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                package.writestr(entry, payload)
        with ZipFile(temporary) as package:
            expected = {f"{NAME}/{relative}" for relative in FILES}
            if set(package.namelist()) != expected or package.testzip() is not None:
                raise ValueError(f"Archive validation failed: {archive.name}")
            for relative, payload in payloads.items():
                if package.read(f"{NAME}/{relative}") != payload:
                    raise ValueError(f"Archive content differs: {relative}")
        temporary.replace(archive)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"PASS {archive.relative_to(ROOT)}: 3 files, CRC and byte comparison verified")
    return archive


def main() -> None:
    destination = ROOT / "dist"
    destination.mkdir(exist_ok=True)
    archives = [
        build("codex", ROOT / "skills" / NAME, destination),
        build("workbuddy", ROOT / "targets" / "workbuddy" / NAME, destination),
    ]
    checksums = "".join(f"{sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in archives)
    (destination / "SHA256SUMS.txt").write_text(checksums, encoding="utf-8")
    print(checksums, end="")


if __name__ == "__main__":
    main()
