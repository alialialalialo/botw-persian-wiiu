You are editing a Persian (Farsi) game translation of The Legend of Zelda: Breath of the Wild (NPC and character dialogue). Your job is a careful, MINIMAL editorial pass.

INPUT: review/evc_NN.json — a JSON list of {id, fa, en}. `fa` is the current Persian text, `en` the official English text for the same string (use it to check meaning). In `fa`, "\n" are hard line breaks (fixed manual wraps for a small text box) and ⟦n⟧ are control-tag markers (colour spans etc.).

TASK: For each item decide whether the Persian is (a) clearly wrong vs the English (mistranslation, wrong meaning, missing/extra info), (b) ungrammatical or garbled, or (c) stilted, over-literary, "bookish" or machine-translated-sounding where a native speaker would phrase it more naturally (needless flourishes like «با شایستگی و لیاقت», «بزرگ بزرگوار ما», overly formal verb forms, word-for-word English structure). Fix ONLY those. If acceptable, DO NOT touch it — most items stay unchanged. Do not rewrite for taste.

STYLE: natural modern standard Persian, readable, not stiff. This is spoken dialogue: use natural spoken Persian (محاوره‌ای ملایم, e.g. «می‌خوام/اون/رو» only if the item already leans that way; otherwise plain neutral standard). Fix stiff, literary, word-for-word English structure and archaic words (اكنون، نيز، زيرا، بدين، ستودنی, etc.) especially when a casual NPC speaks. Keep dignified register for gods, sages, Zelda, the Great Deku Tree etc. Leave literal «<br>» text as it is (handled separately). Keep existing game terminology (e.g. «زیارتگاه» shrine, «شمشیر استادی» Master Sword, «آزمون» trial, place/character names) exactly as the existing text spells them — consistency beats your preference. Use ZWNJ (U+200C) in «می‌شود», «کتاب‌ها» etc. Write Arabic-style ك and ي letters EXACTLY as the existing text does (e.g. كنم، می‌كنی، يك، اين) — match the existing item spelling; ZWNJ stays U+200C. Do NOT add content not in the English; do not remove information.

HARD CONSTRAINTS (validator checks them):
1. Same number of "\n" and the same ⟦n⟧ markers in the same order (you may move a marker to wrap the corresponding words in your new wording).
2. No edited line longer (characters, markers excluded) than the longest line of the original item (+2 tolerance). The box is fixed — shorten rather than lengthen.
3. Keep digits and Latin words/tokens exactly as they are.

OUTPUT: JSON object id(string) -> full new `fa`, ONLY changed items, to review/evo_NN.json (UTF-8, ensure_ascii false). Run: python3 review/validate_edit.py review/evc_NN.json review/evo_NN.json and fix until "problems 0". Also write review/evn_NN.txt (5-10 lines: count changed, main problem kinds, terminology inconsistencies noticed but not changed). Final reply: counts + notes path, short.
(All paths are relative to /tmp/claude-0/-home-claude/e3988272-a021-590f-b21b-178f594b23ac/scratchpad/ .)
