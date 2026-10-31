# zh-esp-book

Assimil-style Mandarin course for Spanish speakers (pinyin first, simplified characters
as a grey second line, Spanish on the right), plus theory and culture chapters.

- Read STYLE.md before writing or editing any chapter; it is the single source of truth.
- CURRICULUM.md fixes the order, file names and scope of every file. Don't renumber.
- After editing chapters run `scripts/lint.py` and `scripts/check-pinyin.sh --tones`.
  SYLLABLE mismatches are errors. TONE mismatches need judgement (neutral tones, 一/不
  sandhi and heteronyms produce false positives) — verify before "fixing".
- Build: `scripts/build.sh pdf <glob>` (falls back to the Docker image with xeCJK).
- Content is in Spanish; Chinese must be natural mainland Mandarin.
