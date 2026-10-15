#!/usr/bin/env python3
"""桐の一括処理／イベント処理テキスト（Shift-JIS）を走査して、検証の下調べをする。

  python kiri_scan.py <file> [<file> ...]        # 集計と機械チェック
  python kiri_scan.py --dump <file>              # 行番号付きで UTF-8 表示

ファイルは読むだけで、書き換えない。
出力の「候補」は機械的な判定なので、最終判断はヘルプと本文で行うこと。
"""
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

HELP_CMD = "https://www.kthree.co.jp/kihelp/cmd/stx/{}.html"
TABLE_MD = Path(__file__).resolve().parent.parent / "references" / "command-pages.md"
SPACES = " \t　"

# 終了状態= を付けないと、失敗時に一括処理が止まるコマンド
NEEDS_STATUS = {"表", "結合", "行訂正", "行追加", "行挿入", "行削除", "置換",
                "ファイル削除", "ファイル複写", "ファイル移動", "ファイル名変更",
                "印字開始", "書き出し", "読み込み", "併合"}
VARIANTS = {"メソッド呼出し": "メソッド呼び出し", "メソッド呼出": "メソッド呼び出し"}
COMPARE_OPS = ("<>", "<=", ">=", "=", "<", ">", "≠", "≦", "≧", "＝", "＜", "＞")


def load_table():
    """command-pages.md の表から {キー: (正式名, [page…])} を作る。"""
    table = {}
    for line in TABLE_MD.read_text(encoding="utf-8").splitlines():
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) != 4 or cols[2] == "page" or not cols[0] or set(cols[0]) <= set("-"):
            continue
        name, aliases, pages, _ = cols
        entry = (name, pages.split())
        table[name] = entry
        if aliases != "-":
            for a in aliases.split():
                table.setdefault(a.lower(), entry)
    return table


def decode(raw, path):
    note = None
    try:
        raw.decode("utf-8")
        if any(b >= 0x80 for b in raw):
            note = "UTF-8 として読める（Shift-JIS でない可能性。桐が読めなくなっていないか確認）"
    except UnicodeDecodeError:
        pass
    return raw.decode("cp932", errors="replace"), note


def strip_comments(text):
    """/* */ を除く（文字列の中は残す）。"""
    out, i, inq = [], 0, False
    while i < len(text):
        c = text[i]
        if c == '"':
            inq = not inq
        if not inq and text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = len(text) if j < 0 else j + 2
            out.append(" ")
            continue
        out.append(c)
        i += 1
    return "".join(out)


def logical_lines(text):
    """継続行（行末の \\）をつなぎ、(開始行番号, 文) を返す。注釈行は除く。"""
    buf, start = [], None
    for no, line in enumerate(text.splitlines(), 1):
        body = line.rstrip(SPACES)
        if not buf:
            s = body.lstrip(SPACES)
            if not s or s[0] in "*＊":
                continue
            start = no
        if body.endswith("\\") and not body.endswith("\\\\"):
            buf.append(body[:-1])
            continue
        buf.append(body)
        stmt = strip_comments(" ".join(buf)).strip(SPACES)
        buf = []
        if stmt:
            yield start, stmt


def skip_paren(s):
    """s は '(' か '（' で始まる。対応する閉じ括弧の次の位置を返す。"""
    depth, inq = 0, False
    for i, c in enumerate(s):
        if c == '"':
            inq = not inq
        elif not inq and c in "(（":
            depth += 1
        elif not inq and c in ")）":
            depth -= 1
            if depth == 0:
                return i + 1
    return len(s)


def split_command(s, table):
    """文をコマンド名と残りに分ける。返り値は (キー, 表記, 残り)。"""
    s = s.lstrip(SPACES)
    if s[0] in "&＆":
        return "代入", "代入", s
    m = re.match(r"^([^\s　(（\"&@＠\[:：]+)[:：](?![:：])(.*)$", s)
    if m:
        return "名札：", m.group(1), m.group(2)
    m = re.match(r"[^\s　(（,，]+", s)
    tok = m.group(0) if m else s
    rest = s[len(tok):]
    nxt = re.match(r"[\s　]+([^\s　(（,，]+)", rest)
    if nxt and f"{tok} {nxt.group(1)}" in table:
        return f"{tok} {nxt.group(1)}", tok, rest[nxt.end():]
    key = VARIANTS.get(tok, tok)
    if key.lower() in table:
        key = key.lower()
    return key, tok, rest


class FileScan:
    def __init__(self, path, table):
        self.path = Path(path)
        self.table = table
        self.is_event = "_kex" in self.path.stem.lower() or self.path.suffix.lower() == ".kex"
        self.used = OrderedDict()          # 正式名 -> [行…]
        self.unknown = defaultdict(list)
        self.findings = []                 # (行, 分類, 内容)
        self.defined, self.calls, self.libraries = set(), [], []
        self.proc = None
        self.stack = []

    def flag(self, no, kind, msg):
        self.findings.append((no, kind, msg))

    def run(self):
        raw = self.path.read_bytes()
        text, note = decode(raw, self.path)
        if note:
            self.flag(0, "文字コード", note)
        for no, stmt in logical_lines(text):
            self.statement(no, stmt)
        if self.stack:
            self.flag(0, "ブロック", f"ファイル末尾で閉じていないブロック: {', '.join(k for k, _ in self.stack)}")
        return self

    # --- 1文の処理 -------------------------------------------------------
    def statement(self, no, stmt):
        key, written, rest = split_command(stmt, self.table)
        if key == "名札：":
            self.record(no, "名札：", None)
            if rest.strip(SPACES):
                self.statement(no, rest)
            return
        if key == "代入":
            self.record(no, "代入", self.table.get("代入"))
            return
        entry = self.table.get(key)
        if entry is None:
            self.unknown[written].append(no)
        else:
            self.record(no, entry[0], entry)
        name = entry[0] if entry else key
        self.check(no, name, written, rest.strip(SPACES), stmt)

        # 条件 ( ) <コマンド> / else if は中のコマンドも見る
        r = rest.lstrip(SPACES)
        if name == "条件" and r[:1] in "(（":
            inner = r[skip_paren(r):].strip(SPACES)
            if inner:
                self.statement(no, inner)

    def record(self, no, name, entry):
        self.used.setdefault(name, [entry[1] if entry else [], []])[1].append(no)

    # --- 機械チェック ------------------------------------------------------
    def check(self, no, name, written, rest, stmt):
        low = written.lower()

        if written in VARIANTS:
            self.flag(no, "表記", f"「{written}」はヘルプにない表記（ヘルプは「{VARIANTS[written]}」）")

        if name in ("手続き実行", "分岐") and rest[:1] in "(（":
            after = rest[skip_paren(rest):].lstrip(SPACES)
            if after[:1] not in (",", "，"):
                self.flag(no, "書式", f"条件付き{name}で、( 条件式 ) の後にカンマがない（ヘルプ: {name} ( 条件式 )，…）")

        if name in ("検索", "絞り込み"):
            m = re.search(r"\[[^\]]*\]", rest)
            if m:
                after = rest[m.end():].lstrip(SPACES)
                if after[:1] not in ("{", "｛", "_", "＿") and after.startswith(COMPARE_OPS):
                    self.flag(no, "記載外", f"{name}の [項目]{after[:2].strip()}値 形式はヘルプに記載なし（[項目]{{ 比較式 }} か [項目]_&変数）")

        if name == "メッセージボックス" and re.search(r"ｱｲｺﾝ|ﾎﾞﾀﾝ", rest):
            self.flag(no, "記載外", "msgbox の ｱｲｺﾝ= / ﾎﾞﾀﾝ= はヘルプに記載なし（正式名: アイコン= / ボタン指定=）")

        if name == "終了 表" and "#" in rest:
            self.flag(no, "記載外", "終了 表 に関数で表番号を渡している（ヘルプ: 表番号の定数・変数 か 編集対象表）")

        if name == "表" and "変数使用" in rest:
            self.flag(no, "書式", "表コマンドに 変数使用= はない（結合コマンドのパラメータ）")

        if name == "変数宣言":
            no_str = re.sub(r'"[^"]*"', "", rest)
            names = re.findall(r"[&＆]([^\s　,，{}=＝\[\]()\"]+)", no_str)
            dups = sorted({n for n in names if names.count(n) > 1})
            if dups:
                self.flag(no, "書式", f"同じ変数宣言の中で重複: {', '.join('&' + d for d in dups)}")

        if name in NEEDS_STATUS and rest and "終了状態" not in rest:
            self.flag(no, "終了状態", f"{name} に 終了状態= がない（失敗時に止まる）")

        if name == "エラー処理" and self.proc and rest and not rest.startswith("手続き名"):
            self.flag(no, "書式", "手続き内で エラー処理 <名札> は使えない（手続き名= を使う）")

        if self.is_event:
            if name == "ライブラリ" and self.proc:
                self.flag(no, "イベント", "ライブラリ はイベントのメイン処理でのみ使える")
            if name == "終了":
                self.flag(no, "イベント", "終了（一括処理の終了）はイベントでは使えない")
            if name == "ウィンドウリスト取得" and self.proc and re.search(r"::(ﾌｫｰﾑ|フォーム)開始", self.proc):
                self.flag(no, "イベント", "[フォーム開始] ハンドラ内の ウィンドウリスト取得 は結果が不定")

        if name == "ライブラリ":
            m = re.search(r'"([^"]+)"', rest)
            if m:
                self.libraries.append((no, m.group(1)))

        # 手続きの定義・呼び出し
        if name == "手続き定義開始":
            self.proc = re.split(r"[(（]", rest, 1)[0].strip(SPACES)
            self.defined.add(self.proc)
            self.stack = []
        elif name == "手続き定義終了":
            if self.stack:
                self.flag(no, "ブロック", f"手続き {self.proc} の終わりで閉じていないブロック: {', '.join(k for k, _ in self.stack)}")
            self.proc, self.stack = None, []
        elif name == "手続き実行":
            r = rest
            if r[:1] in "(（":
                r = r[skip_paren(r):].lstrip(SPACES + ",，")
            callee = re.split(r"[(（\s　]", r, 1)[0]
            if callee:
                self.calls.append((no, callee))
        elif name == "エラー処理":
            m = re.match(r"手続き名\s*[=＝]\s*([^\s　,，]+)", rest)
            if m:
                self.calls.append((no, m.group(1)))

        self.blocks(no, name, low)

    def blocks(self, no, name, low):
        """if / 繰り返し / for / ケース開始 の開閉の対応を緩くたどる。"""
        if low == "if":
            self.stack.append(("if", no))
        elif name == "繰り返し":
            self.stack.append(("繰り返し", no))
        elif name == "for":
            self.stack.append(("for", no))
        elif name == "ケース開始":
            self.stack.append(("ケース開始", no))
        elif name == "繰り返し終了":
            self.pop(no, ("繰り返し", "for"), "繰り返し終了")
        elif name == "ケース終了":
            self.pop(no, ("ケース開始",), "ケース終了")
        elif low == "end":
            self.pop(no, ("if", "for", "繰り返し", "ケース開始"), "end")

    def pop(self, no, accept, closer):
        if not self.stack:
            self.flag(no, "ブロック", f"{closer} に対応する開始がない")
        elif self.stack[-1][0] not in accept:
            k, at = self.stack.pop()
            self.flag(no, "ブロック", f"{closer} が {at}行目の {k} を閉じている（対応の食い違い）")
        else:
            self.stack.pop()


def dump(path):
    text, note = decode(Path(path).read_bytes(), path)
    if note:
        print(f"# 注意: {note}")
    for no, line in enumerate(text.splitlines(), 1):
        print(f"{no:5d}\t{line}")


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    if len(argv) >= 2 and argv[0] == "--dump":
        for p in argv[1:]:
            print(f"=== {p}")
            dump(p)
        return 0
    if not argv:
        print(__doc__)
        return 1

    table = load_table()
    scans = [FileScan(p, table).run() for p in argv]
    all_defined = set().union(*(s.defined for s in scans))
    all_pages = OrderedDict()

    for s in scans:
        kind = "イベント処理（kex）" if s.is_event else "一括処理（cmx 等）"
        print(f"\n## {s.path.name}  — {kind}\n")
        print("### 使用コマンド\n")
        print("| コマンド | 回数 | 行 | ヘルプ |\n|---|---|---|---|")
        for name, (pages, lines) in s.used.items():
            shown = ", ".join(map(str, lines[:8])) + (" …" if len(lines) > 8 else "")
            print(f"| {name} | {len(lines)} | {shown} | {' '.join(pages) or '-'} |")
            for p in pages:
                all_pages.setdefault(p, set()).add(name)
        if s.unknown:
            print("\n### 対応表にないコマンド（綴り違い・未知のコマンドの可能性）\n")
            for w, lines in s.unknown.items():
                print(f"- `{w}` 行 {', '.join(map(str, lines))}")

        print("\n### 機械チェックの候補（ヘルプと本文で確認すること）\n")
        if s.findings:
            for no, kind_, msg in sorted(s.findings):
                where = f"{no}行" if no else "全体"
                print(f"- {where} [{kind_}] {msg}")
        else:
            print("- なし")

        undefined = [(no, c) for no, c in s.calls if c not in all_defined]
        print("\n### 手続き\n")
        print(f"- 定義: {len(s.defined)} 件")
        if s.libraries:
            scanned = {x.path.resolve() for x in scans}
            for no, lib in s.libraries:
                stem = Path(lib.replace("\\", "/")).stem
                hits = sorted(s.path.parent.glob(f"{stem}_*.txt"))
                if not hits:
                    print(f"- {no}行 ライブラリ {lib} → 同じフォルダに {stem}_*.txt が見つからない（未定義判定は不完全）")
                    continue
                names = ", ".join(h.name for h in hits)
                missing = [h for h in hits if h.resolve() not in scanned]
                print(f"- {no}行 ライブラリ {lib} → {names}"
                      + ("（未走査。一緒に渡すと未定義判定が正確になる）" if missing else "（走査済み）"))
        if undefined:
            print("- 走査したファイル群に定義が見つからない呼び出し: "
                  + ", ".join(f"{c}（{no}行）" for no, c in undefined))

    print("\n## 照合するヘルプページ\n")
    for p, names in all_pages.items():
        print(f"- {HELP_CMD.format(p)}  （{'、'.join(sorted(names))}）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
