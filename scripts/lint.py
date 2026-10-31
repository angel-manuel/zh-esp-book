#!/usr/bin/env python3
"""Lint src/chapters/*.md against STYLE.md.

Checks: frontmatter title == H1, table column counts, blank lines around tables,
parallel-table headers, pinyin cells (tone marks present, no tone numbers, no CJK,
no ¿¡), hanzi cells (CJK present, no tone-marked latin), ASCII ~, HTML tags,
footnote ids (prefix cNNN-, unique, referenced/defined, placement).
Usage: scripts/lint.py [files...]
"""
import glob, re, sys, unicodedata

files = sys.argv[1:] or sorted(glob.glob("src/chapters/[0-9][0-9][0-9]-*.md"))
errors = 0
all_ids = {}
CJK = re.compile(r"[一-鿿]")
TONED = re.compile(r"[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]", re.I)
# Syllables that legitimately carry no tone mark (neutral tone) when standing alone
NEUTRAL = {"de", "le", "ma", "ne", "ba", "men", "zi", "ge", "a", "ya", "la", "zhe", "guo", "me", "r"}
PAR_HEADERS = {("#", "Pīnyīn", "汉字", "Español"), ("Pīnyīn", "汉字", "Español")}


def err(f, n, msg):
    global errors
    errors += 1
    print(f"{f}:{n}: {msg}")


def check_pinyin(f, n, cell):
    text = re.sub(r"\[\^[^\]]+\]", "", cell)
    text = re.sub(r"^[^:：]{1,20}:\s*", "", text)  # speaker
    if CJK.search(text):
        err(f, n, f"CJK characters in pinyin cell: {cell!r}")
    if re.search(r"[a-zü][1-5]\b", text, re.I):
        err(f, n, f"tone number in pinyin: {cell!r}")
    if "¿" in text or "¡" in text:
        err(f, n, "¿/¡ in pinyin cell (Spanish punctuation only in Spanish column)")
    if re.search(r"\bv\b|[jqxy]ü|lv|nv", text, re.I):
        err(f, n, f"ü spelling problem: {cell!r}")
    for w in re.findall(r"[A-Za-zÀ-ɏ'’ü-]+", text):
        if "___" in w or not re.search(r"[a-zA-Z]", unicodedata.normalize("NFD", w)):
            continue
        if not TONED.search(w) and w.lower().strip("'-") not in NEUTRAL and not w.isupper():
            # whole word without any tone mark: suspicious unless an all-neutral word
            err(f, n, f"word without tone mark: {w!r} (neutral-only words: {sorted(NEUTRAL)[:6]}…)")


for f in files:
    lines = open(f, encoding="utf-8").read().split("\n")
    m = re.search(r"/(\d{3})-", f)
    pre = m.group(1) if m else "???"
    title = None
    refs, defs = set(), set()
    in_table = False
    ncols = header = None
    row_idx = 0
    for i, line in enumerate(lines, 1):
        s = line.rstrip()
        if s.startswith("title:") and title is None:
            title = s.split(":", 1)[1].strip().strip('"')
        if s.startswith("# ") and title is not None and s[2:].strip() != title:
            err(f, i, f"H1 differs from title: {s[2:].strip()!r} vs {title!r}")
        if "~" in s and "~~" not in s:
            err(f, i, "ASCII ~ (use …)")
        if re.search(r"</?[a-zA-Z]+[^>]*>", s):
            err(f, i, "HTML tag")
        is_row = s.startswith("|") and s.endswith("|")
        if is_row:
            cells = [c.strip() for c in s[1:-1].split("|")]
            if not in_table:
                in_table, ncols, header, row_idx = True, len(cells), tuple(cells), 0
                if i > 1 and lines[i - 2].strip() != "":
                    err(f, i, "no blank line before table")
                if "汉字" in cells and header not in PAR_HEADERS:
                    err(f, i, f"parallel-table header must be one of {PAR_HEADERS}")
            else:
                row_idx += 1
                if len(cells) != ncols:
                    err(f, i, f"row has {len(cells)} cells, table has {ncols}")
                elif header in PAR_HEADERS and row_idx >= 2:
                    off = 1 if header[0] == "#" else 0
                    py, hz, es = cells[off], cells[off + 1], cells[off + 2]
                    check_pinyin(f, i, py)
                    if hz and not CJK.search(hz):
                        err(f, i, f"hanzi cell has no characters: {hz!r}")
                    if TONED.search(hz):
                        err(f, i, f"tone-marked latin in hanzi cell: {hz!r}")
                    if not es:
                        err(f, i, "empty Spanish cell")
                    if off and not re.fullmatch(r"\d+", cells[0]):
                        err(f, i, f"dialogue line number missing: {cells[0]!r}")
        elif in_table:
            in_table = False
            if s.strip():
                err(f, i, "no blank line after table")
        for m2 in re.finditer(r"\[\^([^\]]+)\](?!:)", s):
            refs.add(m2.group(1))
        m2 = re.match(r"\[\^([^\]]+)\]:", s)
        if m2:
            fid = m2.group(1)
            defs.add(fid)
            if not fid.startswith(f"c{pre}-"):
                err(f, i, f"footnote id {fid} lacks prefix c{pre}-")
            if fid in all_ids:
                err(f, i, f"duplicate footnote id {fid} (also in {all_ids[fid]})")
            all_ids[fid] = f
            if i > 1 and lines[i - 2].strip():
                err(f, i, f"footnote {fid} not preceded by blank line")
    for r in refs - defs:
        err(f, 0, f"footnote ref [^{r}] has no definition")
    for d in defs - refs:
        err(f, 0, f"footnote [^{d}] never referenced")
    if title is None:
        err(f, 0, "no title in frontmatter")

print(f"{len(files)} files checked, {errors} problem(s)")
sys.exit(1 if errors else 0)
