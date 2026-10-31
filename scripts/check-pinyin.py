#!/usr/bin/env python3
"""Cross-check the Pīnyīn column against the 汉字 column with pypinyin.

Reports, per table row:
  SYLLABLE  the syllables differ (wrong word, missing word, typo)  -> almost always a real error
  TONE      same syllables, different tones                         -> check: may be a real error,
            a neutral tone, or a heteronym pypinyin got wrong (verify with Pleco/a dictionary)
Run via scripts/check-pinyin.sh (installs pypinyin on the fly with uv).
Usage: check-pinyin.py [--tones] [files...]   (tone mismatches are only shown with --tones)
"""
import glob, re, sys, unicodedata
from pypinyin import pinyin, Style

args = [a for a in sys.argv[1:] if not a.startswith("--")]
show_tones = "--tones" in sys.argv
files = args or sorted(glob.glob("src/chapters/[0-9][0-9][0-9]-*.md"))
HEADERS = {("#", "Pīnyīn", "汉字", "Español"), ("Pīnyīn", "汉字", "Español")}
CJK = re.compile(r"[一-鿿]")
# Readings the book prefers over pypinyin defaults (standard colloquial mainland forms)
PREFERRED = {("谁", "shuí"): "shéi"}


def strip_tones(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn" or c == "̈")
    return unicodedata.normalize("NFC", s)


def norm(s):
    s = s.lower().replace("ü", "v").replace("ü", "v")
    return re.sub(r"[^a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜv]", "", s)


n_syl = n_tone = 0
for f in files:
    lines = open(f, encoding="utf-8").read().split("\n")
    header = None
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            header = None
            continue
        cells = [c.strip() for c in s[1:-1].split("|")]
        if header is None:
            header = tuple(cells)
            continue
        if header not in HEADERS or set(s) <= set("|:- "):
            continue
        off = 1 if header[0] == "#" else 0
        py, hz = cells[off], cells[off + 1]
        py = re.sub(r"\[\^[^\]]+\]", "", py)
        py = re.sub(r"^[^:]{1,25}:\s*", "", py) if re.match(r"^[^:]{1,25}:", py) else py
        hz = re.sub(r"^[^：]{1,12}：", "", hz)
        py = re.sub(r"^\d+\.\s*", "", py)
        hz = re.sub(r"^\d+\.\s*", "", hz)
        if re.search(r"\d|___|…|\.\.\.", hz + py) or not CJK.search(hz):
            continue
        chars = "".join(CJK.findall(hz))
        ref = [p[0] for p in pinyin(chars, style=Style.TONE, neutral_tone_with_five=False)]
        ref = [PREFERRED.get((h, r), r) for h, r in zip(chars, ref)]
        mine = norm(py)
        # Candidate reference spellings: plain, and with erhua 儿 written as -r.
        # Each is a list of (normalized char, source hanzi) so tone diffs can be traced.
        cands = []
        for erhua in (False, True):
            seq = []
            for k, (h, r) in enumerate(zip(chars, ref)):
                syl = "r" if (erhua and h == "儿" and k) else r
                seq += [(c, h) for c in norm(syl)]
            cands.append(seq)
        if any(mine == "".join(c for c, _ in seq) for seq in cands):
            continue
        same_letters = [seq for seq in cands
                        if len(seq) == len(mine) and norm(strip_tones(mine)) == norm(strip_tones("".join(c for c, _ in seq)))]
        if same_letters:
            seq = same_letters[-1]
            # forgive: unmarked syllable in the book (neutral tone) and 一/不 sandhi
            real = [(a, b, h) for a, (b, h) in zip(mine, seq)
                    if a != b and not (strip_tones(b) == a) and h not in "一不"]
            if not real:
                continue
            n_tone += 1
            if show_tones:
                print(f"{f}:{i}: TONE      {py!r}\n{'':>{len(f)+len(str(i))+3}}pypinyin: {' '.join(ref)}")
        else:
            n_syl += 1
            print(f"{f}:{i}: SYLLABLE  {py!r}\n{'':>{len(f)+len(str(i))+3}}pypinyin: {' '.join(ref)}  ({hz})")
print(f"{len(files)} files: {n_syl} syllable mismatch(es), {n_tone} tone mismatch(es)"
      + ("" if show_tones else " — run with --tones to list tone mismatches"))
sys.exit(1 if n_syl else 0)
