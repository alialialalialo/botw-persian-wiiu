Some NPC texts in the Persian translation of Zelda: Breath of the Wild are still written in ARABIC (left over from the source mod). Translate them into natural, plain, everyday Persian (Farsi), like a good game dub.

INPUT: review/ar2_cN.json — list of {id, fa, en, src}. `fa` = current ARABIC text (to be replaced), `en` = official English (use it as the real source of meaning; use the Arabic only as a hint), `src` = file/NPC name. In `fa`, "\n" = fixed manual line breaks and ⟦n⟧ = control markers (colour/pause/page).
If a unit is already Persian (not Arabic), leave it out of the output.

STYLE (decided by the user): plain standard Persian, no literary flourish; NPCs lightly colloquial (می‌خوام / نمی‌تونم / اون / اینجا). Keep each character's personality from the English (cooks, merchants, kids, Gorons say «گورو» sounds: their English "goro" becomes «گورو»). Keep puns/jokes simple; keep Latin names/numbers.

GLOSSARY (mandatory): اوربوسا, داروک, مدوه, ريوال, سيدون, هادسون, هيولای مقدس, پليدی, هايرول, ايزدبانو هايليا, لوح شيكا, ظرف قلب, جام استقامت, معبد (shrine), گوی روح, بلای گانون, قهرمانان, دينرال/فاروش/نايدرا, سالار گرودو, دروازه‌ی سفر, درخت دكوی بزرگ, كوه مرگ, قهرمان داروک, ترمينال, قابليت (rune), ميزو كيوشيا, الدين, يونوبو, تبا, پرنسس زلدا, استاد لينك, روستا (village), بلای بزرگ (Great Calamity), گورون, كوروك, گرودو, ريتو, زورا, هايلی, شيكا, نابوريس, روتا, رودانيا, لاينل, ليزالفوس, سنگ راهنما, قلعه هايرول, شمشير استاد, چشمه. Molduga = مولدوگا, Hylian Shroom etc: translate item names plainly (قارچ هايلی ...). Other unknown names: transliterate simply.

SPELLING: write exactly like the existing Persian text: Arabic-style ك and ي letters (كنم، می‌كنی، يك، اين، ميفا) but the word-final/medial yeh «ی» as U+06CC exactly as existing items write it (copy from the other Persian units, e.g. «می‌كنی»). ZWNJ = U+200C in «می‌روم, كتاب‌ها». Persian punctuation « ، » « ؟ » are fine.

HARD CONSTRAINTS: 1) same number of "\n" and same ⟦n⟧ markers in the same order as `fa` (you may move a marker next to the corresponding words); 2) each line (markers excluded) no longer than the longest line of the ENGLISH `en` text +2 characters (en lines may be broken differently; use its longest line); shorten wording rather than exceed; 3) same numbers/Latin tokens.

OUTPUT: write review/ar2_oN.json = {id(string): new Persian text} for EVERY Arabic item (UTF-8, ensure_ascii false). Then check with: python3 work/ar2_check.py N until "problems 0". If a unit truly cannot fit, shorten the sentence. Reply with counts only (2 lines).
(All paths relative to /tmp/claude-0/-home-claude/e3988272-a021-590f-b21b-178f594b23ac/scratchpad/ .)
