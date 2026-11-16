# HANDOFF: Persian (Farsi) translation of Zelda BOTW -> Wii U v1.5.0 EU in Cemu 1.26.2f

Paste/attach this whole file + the zip to the new AI and say: "Continue this project exactly as described; follow the rules below."

## 0. User & communication rules
- User: Persian speaker (Telegram ali123qp, Asia/Tehran). Reply in **Persian**, short, simple, practical. He is not a programmer.
- He DISLIKES repeated tests: verify thoroughly yourself before sending a build; send one zip, not many.
- Whenever he sends screenshots of problems, fix every one of them.
- Credits: NO separate credits file (user order: delete it, rules.txt is enough). Credit Poormaz (poormaz.com), Majid Hoshyar (radoo.ir/author/majidh1) and ali123qp (Telegram) only in the `rules.txt` description.

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

## UPDATE v1.0.1
Game Over text = «شكست خورديد». Zip: BOTW_Persian_v1.0.1.zip.

## UPDATE v1.0.2
Credits file rewritten (adds Telegram ali123qp, install steps). rules.txt description updated.

## UPDATE v1.1.0
432 Arabic NPC units translated to plain Persian (review/ar_*). Open: bookish NPC dialogue rewrite.

## UPDATE v1.1.1
Found ~590 more Arabic NPC units (merchants, Rito bros, Mamono shop etc.) missed in v1.1.0; translated (review/ar2_*). Removed literal <br>/<color> tags from 30 units (Npc_oasis020). Audit heuristic: Arabic letters/function words without Persian ones.

## UPDATE v1.1.2
Removed literal {variable} (Npc_HighMountain010), unified Molduga variant مولدوراژيك, last Riju/Vasaaq stragglers.

## UPDATE v1.1.3
RSTB fixed: now built from the real v1.5.0 table (uploads 2d737999) changing only Font_EU.bfarc and Msg_EUen entries. Before it came from another version (3,886 entries smaller than v1.5.0, 4 missing). Audited: SARC structure, MSBT labels/unit counts, BFFNT headers/CMAP all OK.

## UPDATE v2.0.0
Text replaced with the Poormaz translation (author gave permission; colloquial, complete). Source: PC installer "Savage Wind" (LE, pre-shaped visual order), extracted statically.
Conversion: work/newtext.py (model E: strip U+2000-200A padding, per-line reverse, re-reverse LTR runs, mirror brackets, rebuild ZWNJ, LE tag params -> ⟦k⟧ markers), work/apply_new.py applies by English unit tags, work/post_new.py normalizes terms (Molduga/Riju/Beedle/Vasaaq etc).
Result: 24,595 units replaced; 2,653 units (tag-type mismatch) + 365 empty + 14 files with unit-count mismatch keep the old Majid-based text (may still be bookish). Backup of old text: work/mw_edited_majid.pkl (not committed, large).
Credits: Poormaz (poormaz.com, t.me/poormaz), Majid Hoshyar, ali123qp. rules.txt name "Zelda BOTW Persian v2.0.0", version = 7 (Cemu format).
NOT tested in game yet. Awaiting screenshots.

## UPDATE v2.0.1
CRASH FIX. v1.1.3 and v2.0.0 crashed Cemu at boot (loading Pack/Bootup_EUen.pack). Cause: v1.1.3 wrongly switched the RSTB base to upload 2d737999 (a different game version: Msg_EUen 6026624, Font 3662176, 58726 entries). The user's real v1.5.0 table is upload 459a7954 (67992 entries; Msg_EUen 6479040 == real decompressed Msg size 6478648; Font 9191776). pack3.py now uses 459a7954 again, Font=newv, Msg=base+0x20000. DO NOT use 2d737999. (v1.1.3 note above is wrong.)

## UPDATE v2.0.2
Removed README_Credits.txt from the pack (user: rules.txt alone is enough; credits are in its description). work/credits.txt deleted. Pack = rules.txt + content/. Same text/RSTB as v2.0.1.

## UPDATE v2.0.3
v2.0.1 booted in Cemu (user screenshot). Bug: letter چ (U+0686) appeared detached/isolated. Cause: Poormaz-based text kept raw U+0686 (+ZWJ), the old pipeline converted it to the font's synthesized forms FB7A-FB7D via work/fixche.py (fix_che). FIX: after apply_new, ALWAYS run fixche.fix_che(mw) on mw_edited before pack3 (script in HANDOFF: python -c using work/fixche). All 9,997 che now FB7A-D; render check OK (tools/render.py). Pipeline order: apply_new -> fix_che -> pack3.

## UPDATE v2.0.4
Self-audit (render + scans). Found 3 untranslated English NPC units (Npc_oasis013 #13/#16 merchant bomb/ice arrows, Npc_Road_009 #21 Lover's Pond): translated to colloquial Persian. Collapsed double spaces in 13 Persian units. StaffRoll English credits intentionally left (original). Remaining known: ~2,653 fallback units keep older text.

## UPDATE v2.1.0
Converted the previously-skipped tag-mismatch units (2,651) with work/convert2.py: lenient tag matching (cosmetic (0,2)/(0,3) tags matched by type, or dropped if counts differ; functional tags must match the English set exactly, else fallback). Now 27,246 of 27,613 units use Poormaz text; only 365 empty units + 14 count-mismatch files keep old text. All 29,730 units verified to have the same functional tags as English. Terms unified in post_new: جانور مقدس -> هیولای مقدس, محفظه‌ی قلب -> ظرف قلب, حلقه‌ی استقامت -> جام استقامت.
Pipeline: apply_new.run(src=mw_edited_majid.pkl, res=newtext_res2.pkl, post=post_new.post) -> fixche.fix_che -> pack3.py.

## UPDATE v2.1.1
Full audit (work/audit_full.py): 1091 msbt, 29,730 units, labels/ATR/sections identical to original, all codes mapped in all 4 fonts, RSTB only Font+Msg changed (Msg 6610112 >= 5.82M actual), no leaks (<br>, ⟦⟧), no untranslated English (except StaffRoll names), the 365 empty units are empty in the English original too. Fixes: Latin ? and , -> ؟ and ، in Persian units; Medoh مدو -> مدوه (user decision). Faron/فارون and Rivan/ریوان are different characters, left alone.
