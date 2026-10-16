#!/usr/bin/env python3
"""Claude Code 以外の AI ツール向けに、kiri-verify スキルを ZIP にまとめる。

  python scripts/make-skill-zip.py

plugins/kiri-verify/skills/kiri-verify/ を dist/kiri-verify.zip に固める。
ZIP の中身は kiri-verify/SKILL.md … の形（展開するとフォルダ1つ）。
スキルを直したら、このスクリプトで ZIP を作り直してから commit する。
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "plugins" / "kiri-verify" / "skills" / "kiri-verify"
OUT = ROOT / "dist" / "kiri-verify.zip"


def main():
    OUT.parent.mkdir(exist_ok=True)
    files = sorted(p for p in SKILL.rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            # 区切りは / にする（\ だと Windows 以外で展開できない）
            z.write(p, (Path(SKILL.name) / p.relative_to(SKILL)).as_posix())
    print(f"{OUT.relative_to(ROOT).as_posix()}: {len(files)} files")
    for p in files:
        print("  " + (Path(SKILL.name) / p.relative_to(SKILL)).as_posix())


if __name__ == "__main__":
    main()
