# HANDOFF: Persian (Farsi) translation of Zelda BOTW -> Wii U v1.5.0 EU in Cemu 1.26.2f

Paste/attach this whole file + the zip to the new AI and say: "Continue this project exactly as described; follow the rules below."

## 0. User & communication rules
- User: Persian speaker (Telegram ali123qp, Asia/Tehran). Reply in **Persian**, short, simple, practical. He is not a programmer.
- He DISLIKES repeated tests: verify thoroughly yourself before sending a build; send one zip, not many.
- Whenever he sends screenshots of problems, fix every one of them.
- Credits MUST stay in `README_Credits.txt` and `rules.txt`: original translation by **Majid Hoshyar (مجید هوشیار)**, https://www.radoo.ir/author/majidh1/ (Switch v1.6); Wii U adaptation by **ali123qp**.

## 1. Goal
Port Majid Hoshyar's Persian translation (made for Switch v1.6) to the Wii U version 1.5.0 EU, run in Cemu 1.26.2f with game language EUen (English). Delivered as a Cemu **graphic pack** (folder `Persian_Final`: rules.txt, README_Credits.txt, content/Font, content/Pack, content/System/Resource). **BCML must be OFF** (when ON it merges/breaks the font+text pack and the Persian glyphs vanish). Optional: a BCML-compatible variant (one test zip exists, untested).

Latest build: `out/BOTW_Persian_Final12.zip` (user had not yet reported on it: check the look of «چ» and overflow after wrapping).

## 2. Technical facts
- Wii U files: SARC + Yaz0, **big-endian** MSBT (Switch is little-endian). BFFNT fonts with GX2-swizzled BC4 sheets. RSTB (ResourceSizeTable) entries must be >= real sizes.
- Persian text is stored **pre-shaped** (presentation forms FB50–FEFF). The Wii U engine is LTR only, so every line is stored in **visual (reversed) order**, brackets mirrored. Control tags (0,3) colour and (0,2) size are re-emitted per character. ZWNJ/ZWJ map to a zero-width glyph.
- Direction detection uses `_viol` (join violations) in tools/textfix.py; ties for short names are broken with word-boundary evidence.
- Raw U+0686 «چ» is converted to FB7A (isolated) / FB7B (final) / FB7C (initial) / FB7D (medial) by work/fixche.py. The Switch font's FB7A–D glyphs are WRONG («چشمه» looked like «غشمه»), so forms are synthesized from ج bodies + three drawn dots (tools/che_synth.py, draw_dots in fontbuild).
- Fonts rebuilt: Normal (ratio 39/105), NormalS (30/105), Caption (22/49), Special (71/52). Special was forgotten at first: the golden banner/quest titles were empty.
- Wrapping: `wrap_items` (tools/textfix.py) breaks lines at 1.08 × the English line max width, ONLY for units whose English text contains a newline. Single-line labels are never wrapped (a DLC button once wrapped into 3 lines). Space width is counted.

## 3. Files in the zip
- `tools/` : botw_min.py (SARC/MSBT/yaz0), bffnt.py, swfont.py, fontbuild.py, che_synth.py, textfix.py, shaper/shape.py, rstb.py, apply_edits.py, etc. (`yaz0c` is a compiled C helper; source yaz0c.c)
- `work/pack3.py` : THE current full build (run `python3 -I work/pack3.py` from the project root; then zip `out/R4` → `out/BOTW_Persian_FinalNN.zip`). Loads `work/mw_edited.pkl` (the current edited text for all MSBT files).
- `work/mw_edited.pkl` : current text (already includes quest/NPC/subtitle rewrites AND fixche). **Do NOT re-run fixche on it.** Backups: mw_before_ev/dm/che.pkl.
- `work/fixche.py`, `work/merge_ev.py` (validator `ok()` + `collect()`), `work/chk.py`, `work/val.py`
- `review/BRIEF.md, BRIEF2.md (NPC), BRIEF3.md (subtitles)` : the prompts used for the rewriting sub-agents. `review/validate_edit.py` : validator. `review/dmc_NN.json` inputs (id, fa, en), `dmo_NN.json` outputs.
- `out/BOTW_Persian_Final12.zip` : the latest build.
- NOT included (copyrighted/large, the user has them): the original game files (Wii U Font_EU.sbfarc, Bootup_EUen.pack, ResourceSizeTable) and the Switch Romfs. pack3.py expects them at paths like `/root/.claude/uploads/.../Font_EU.sbfarc`, `r2/BOTW_Persian_FULL/...`, `sw/The Legend Of Zelda Breath Of The Wild/...`: ask the user to supply them and fix the paths at the top of pack3.py.

## 4. Text-rewriting pipeline (for "bookish/robotic" Persian)
`review/*c_NN.json` → sub-agents write `*o_NN.json` using the BRIEF → `validate_edit.py` checks: same ⟦n⟧ markers, same `\n` count, line length ≤ English max + 2, same Latin letters/digits → merge (`work/merge_ev.py` / `apply_edits.apply`) → `fix_yeh` → `fixche` → `pack3.py`. Rejected rewrites keep the old text. Style: natural spoken-ish Persian, meaning of the English preserved, no «گردد/گردید/لذا/هرگاه/همانا/سپاسگزارم»-style stiffness. Never replace «جهت» (means "direction") blindly: only «جهت اطلاع» etc.

## 5. History of bugs (don't repeat)
- Wrong «جهت»→«برای» replacement: reverted, redone with a safe list.
- 1099 NPC rewrites had never been applied: merged later.
- Rumor-book box empty: unbroken paragraphs + space-width bug in wrap_items: fixed.
- Short names displayed reversed: `_viol` tie fixed.
- All text vanished in Final10: BCML was enabled (user turned it off).
- «چ» looked like «غ»: synthesized glyphs. Three dots merged: dots drawn explicitly.
- Unknown: why «محققا» vanished in the "هسته باستانی غول‌پیکر" description (glyphs/data fine; maybe fixed by the new wrap).

## 6. Open items
1. Wait for the user's in-game feedback on Final12 (چ look, overflow).
2. BCML-compatible build is untested.
3. Fix whatever his new screenshots show.

## 7. Install steps to give the user
1. Unzip Final build. 2. Put `Persian_Final` in Cemu's `graphicPacks` folder. 3. Enable it in Cemu → Graphic packs. 4. BCML OFF. 5. Run EU v1.5.0 with English language.

## UPDATE (after Final15)
- Latest build: out/BOTW_Persian_Final15.zip. Subtitles rewritten in plain register (review/BRIEF4.md, d4c/d4o), glossary in work/glossary.py (names unified), segment-order fix in tools/textfix.py (reorder per timing tag (0,4),(1,0),(5,0..2)).
- Glossary decided by user: اوربوسا, داروک, مدوه, ریوال, سیدون, هادسون, هیولای مقدس, پلیدی, هایرول, ایزدبانو هایلیا, لوح شیکا, ظرف قلب, جام استقامت, معبد, گوی روح, بلای گانون, قهرمانان, دینرال/فاروش/نایدرا, سالار گرودو, دروازه‌ی سفر, درخت دکوی بزرگ, کوه مرگ, قهرمان داروک, ترمینال, قابلیت (rune), میزو کیوشیا, «مجسمه ایزدبانو».
- OPEN BUGS from Final13 screenshots: (1) ~430 NPC units are still ARABIC (from the source mod; files Npc_MamonoShop, Npc_Road_044/031/008/045, Npc_UMiiVillage031, Rito_BrosRock, Npc_SmallOasis010/011, Npc_RitoHatago001, TwnObj_Village_Korok_DekuTree_A_01 ...): translate to plain Persian. Detect with chars ة ى أ إ. (2) Speaker name label «درخت بزرگ دکو» must be «درخت دکوی بزرگ». (3) Next big task: rewrite bookish NPC dialogue in plain register, asking the user about ambiguous terms (AskUserQuestion), same pipeline as BRIEF4.
- Open question list from subtitle agents: Rhondson/Bolson names (wedding), Kass poems, "Buh-bye".
- Final17: second consistency pass: لانايرو, تابانتا, كيلتون, موبلين, نايدرا, كلاه رعد, گورو (not چورو), چشمه‌ی حكمت, رابی, هايرولی‌ها. Left as is by user choice: "Mr." (varies by character). Unresolved: Vasaaq (واساش/واساچ).

## UPDATE Final18
Third terminology pass + name decisions: مولدوگا, ريجو, بيدل, واساك. Still open: Arabic NPC units (432), bookish NPC dialogue.

## UPDATE (name change)
Pack renamed: folder `BOTW_Persian`, zip `out/BOTW_Persian.zip` (no build number; version is in rules.txt). Game Over text = «بازی تمام شد». Pack path in Cemu: put `BOTW_Persian` in graphicPacks (delete old `Persian_Final`).

## UPDATE v1.0.0
Versioning is now semantic: zip `BOTW_Persian_v1.0.0.zip`, pack name "Zelda BOTW Persian v1.0.0". Folder stays `BOTW_Persian`. Keep `version = 7` in rules.txt (that is the Cemu rules format, not ours). Bump: patch = small text fixes, minor = new batches (e.g. Arabic NPC translation), major = big changes.
