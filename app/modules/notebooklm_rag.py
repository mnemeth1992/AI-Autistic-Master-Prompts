"""
Workspace: NotebookLM RAG Működési Motor & Kutatóközpont
=========================================================
Google NotebookLM Retrieval-Augmented Generation (RAG) integráció az AuDHD munkafolyamatba:
1. 100%-ban hallucinációmentes KJV igehely- és jelenetkutatás (Hétfő)
2. 30 napos Áhítatok teológiai gerincének felépítése (Kedd)
3. Versenytárs-értékelések és piaci rések elemzése (Review Mining)
4. Bónusz digitális termék: Audio Devotional / Audio Overview (Gumroad $29 ➔ $39 Upsell)
5. Eszköz-határolási Mátrix (Hol NEM érdemes NotebookLM-et használni?)
100% Kétnyelvű (HU / EN).
"""

import os
import json
import streamlit as st
from typing import Dict, Any, List

try:
    from core.key_manager import get_key_manager
    from core.project_manager import auto_save_current_project
    from core.drive_sync import save_prompts_file_to_drive, resolve_drive_folder
except (ModuleNotFoundError, ImportError):
    from app.core.key_manager import get_key_manager
    from app.core.project_manager import auto_save_current_project
    from app.core.drive_sync import save_prompts_file_to_drive, resolve_drive_folder


def render_notebooklm_rag_module():
    is_hu = st.session_state.get("app_global_lang", "HU") == "HU"

    st.markdown(f"<div class='path-badge'>📓 {'NotebookLM RAG Központ & Hallucinációmentes Kutatóműhely' if is_hu else 'NotebookLM RAG Research & Grounded Mining Hub'}</div>", unsafe_allow_html=True)

    header_text_hu = """A hagyományos nagy nyelvi modellek hajlamosak a bibliai igéket pontatlanul idézni vagy felületes teológiai közhelyeket generálni. A NotebookLM kizárólag a feltöltött forrásokból (KJV Biblia, teológiai jegyzetek, versenytársi értékelések) dolgozik, így <strong>100%-ban garantálja a tényhűséget és megszünteti a hallucinációt</strong>."""
    header_text_en = """Standard LLMs tend to hallucinate scripture verses or generate generic theological text. NotebookLM works strictly on your uploaded sources (KJV Bible, commentaries, reviews), ensuring <strong>100% factual fidelity and zero hallucination</strong>."""

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid #38bdf8; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <span style='font-size: 2.2rem;'>🧠 ➔ 📓</span>
            <div>
                <strong style='font-size: 1.15rem; color: #38bdf8;'>{'NotebookLM Mint Szigorú Forrásalapú (RAG) Működési Motor' if is_hu else 'NotebookLM as Grounded Source-Based (RAG) Engine'}</strong>
                <p style='margin: 4px 0 0 0; color: #cbd5e1; font-size: 0.9rem;'>
                    {header_text_hu if is_hu else header_text_en}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_kjv, tab_matrix, tab_reviews, tab_audio, tab_matrix_guide = st.tabs([
        "📖 1. KJV Igehely & Jelenetkutatás" if is_hu else "📖 1. KJV Scripture & Scene Mining",
        "📑 2. 30 Napos Teológiai Mátrix" if is_hu else "📑 2. 30-Day Theological Matrix",
        "⭐ 3. Versenytárs Review Mining" if is_hu else "⭐ 3. Competitor Review Mining",
        "🎙️ 4. Audio Devotional ($39)" if is_hu else "🎙️ 4. Audio Devotional ($39)",
        "🧭 5. Eszköz-határolási Mátrix" if is_hu else "🧭 5. Tool Boundaries Matrix"
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1: KJV IGEHELY & JELENETKUTATÁS (HÉTFŐ)
    # ─────────────────────────────────────────────────────────
    with tab_kjv:
        st.markdown(f"#### 📖 {'100%-ban Hallucinációmentes Igehely- és Jelenetkutatás' if is_hu else '100% Hallucination-Free Scripture & Scene Mining'}")
        st.caption("Használd ezt a munkafolyamatot hétfőnként a színezők, mesekönyvek és faliképek pontos bibliai alapjainak kinyeréséhez." if is_hu else "Extract accurate biblical scenes and literal verses for coloring books and wall art.")

        c_k1, c_k2 = st.columns([1.2, 1.0])
        with c_k1:
            t_opts = [
                "Ószövetség (Állatok, nagy csodák, látványos történetek)" if is_hu else "Old Testament (Animals, miracles, grand scenes)",
                "Újszövetség (Jézus példázatai, gyógyítások, apostolok)" if is_hu else "New Testament (Parables of Jesus, healings, disciples)",
                "Zsoltárok & Példabeszédek (Megnyugtató, bátorító igék)" if is_hu else "Psalms & Proverbs (Comforting, uplifting scriptures)"
            ]
            testament = st.radio("Bibliai Fókusz:" if is_hu else "Biblical Focus:", t_opts, index=0, key="rag_kjv_testament")
            theme_subject = st.text_input(
                "Téma / Kulcsszavak:" if is_hu else "Theme / Keywords:",
                value="gyermekek számára könnyen vizualizálható állatok vagy látványos események" if is_hu else "children coloring scenes with animals and miracles",
                key="rag_kjv_theme"
            )
            scene_count = st.slider("Kinyerendő Jelenetek Száma:" if is_hu else "Number of Scenes to Extract:", min_value=10, max_value=50, value=30, step=5, key="rag_kjv_count")

        with c_k2:
            step1_lbl = "1. Lépés: Nyisd meg a <a href='https://notebooklm.google.com' target='_blank' style='color:#38bdf8; text-decoration: underline;'>NotebookLM</a> felületét." if is_hu else "Step 1: Open <a href='https://notebooklm.google.com' target='_blank' style='color:#38bdf8; text-decoration: underline;'>NotebookLM</a>."
            step2_lbl = "2. Lépés: Töltsd fel a teljes <strong>KJV Biblia TXT/PDF</strong> állományát." if is_hu else "Step 2: Upload complete <strong>KJV Bible TXT/PDF</strong> as source."
            step3_lbl = "3. Lépés: Másold be az alábbi promptot, majd a kapott listát illeszd be ide!" if is_hu else "Step 3: Run the prompt below and paste the generated list here!"
            st.markdown(f"""
            <div class='metric-card'>
                <strong style='color:#38bdf8;'>{step1_lbl}</strong><br>
                <strong style='color:#34d399;'>{step2_lbl}</strong><br>
                <strong style='color:#f59e0b;'>{step3_lbl}</strong>
            </div>
            """, unsafe_allow_html=True)

        if is_hu:
            kjv_op_prompt = f"""Gyűjts ki nekem a feltöltött KJV Bibliából {scene_count} olyan {testament.split('(')[0].strip().lower()} jelenetet, amely {theme_subject} tartalmaz. Mindegyikhez add meg a pontos igehelyet (pl. Genesis 6:14-22) és az exakt KJV idézetet szó szerint, valamint egy tömör, 1 mondatos angol vizuális jelenetleírást."""
        else:
            kjv_op_prompt = f"""Extract {scene_count} sequential scenes from the uploaded KJV Bible matching: '{theme_subject}'. For each scene, provide: 1. Scripture reference (e.g. Genesis 6:14), 2. Literal KJV quote word-for-word, 3. A concise 1-sentence visual description for 4K image generation."""

        st.markdown(f"##### 📋 {'Operatív Prompt (NotebookLM-be másolandó):' if is_hu else 'Operating Prompt (Copy into NotebookLM):'}")
        st.code(kjv_op_prompt, language="text")

        st.markdown("---")
        st.markdown(f"##### 📥 {'NotebookLM Eredmények Beillesztése & Importálása:' if is_hu else 'Paste & Import NotebookLM Output:'}")
        pasted_scenes = st.text_area(
            "Illeszd be ide a NotebookLM által kinyert sorszámozott jeleneteket:" if is_hu else "Paste generated sequential scenes / scriptures here:",
            height=160,
            placeholder="1. Genesis 6:14 - Noah building the ark with cedar wood...\n2. Genesis 8:11 - The dove returning with an olive leaf in her mouth...",
            key="rag_pasted_scenes"
        )

        if st.button("💾 " + ("Jelenetek Mentése" if is_hu else "Save Scenes to Active Workspace"), use_container_width=True, type="primary"):
            if pasted_scenes.strip():
                st.session_state["rag_kjv_scenes_saved"] = pasted_scenes.strip()
                st.success("✅ " + ("KJV jelenetek sikeresen elmentve!" if is_hu else "Scripture scenes saved successfully!"))
            else:
                st.warning("Kérlek, illeszd be a NotebookLM kimenetet a mentéshez." if is_hu else "Please paste output to save.")

    # ─────────────────────────────────────────────────────────
    # TAB 2: 30 NAPOS TEOLÓGIAI MÁTRIX (GUMROAD)
    # ─────────────────────────────────────────────────────────
    with tab_matrix:
        st.markdown(f"#### 📑 {'30 Napos Áhítatok Teológiai Gerincének Felépítése' if is_hu else 'Building 30-Day Devotional Theological Matrix'}")
        st.caption("A repetitív, közhelyes AI-szövegek elkerülése: forrásalapú mátrix generálása NotebookLM-ben, majd kifejtése Gemini Advanced-del." if is_hu else "Eliminating repetitive AI clichés with source-grounded theological matrix.")

        c_m1, c_m2 = st.columns([1.2, 1.0])
        with c_m1:
            dev_subject = st.text_input("Áhítat Címe / Témája:" if is_hu else "Devotional Title / Theme:", value="Reménység és Békesség a Nehéz Időkben" if is_hu else "Hope and Peace in Difficult Times", key="rag_dev_sub")
            dev_target = st.text_input("Célcsoport:" if is_hu else "Target Audience:", value="Keresztény édesanyák és nők" if is_hu else "Christian mothers and women", key="rag_dev_aud")
        with c_m2:
            st.markdown(f"""
            <div class='metric-card'>
                <strong style='color:#a855f7;'>{'Forrásfájlok' if is_hu else 'Sources'}:</strong> {'Tölts fel prédikációkat, teológiai könyveket a NotebookLM-be.' if is_hu else 'Upload sermons or theological books into NotebookLM.'}<br>
                <strong style='color:#34d399;'>{'Eredmény' if is_hu else 'Output'}:</strong> {'Egy 30 soros, strukturált táblázatos mátrix.' if is_hu else 'A 30-row grounded structured matrix table.'}
            </div>
            """, unsafe_allow_html=True)

        if is_hu:
            matrix_op_prompt = f"""A feltöltött teológiai források és KJV igék alapján hozz létre egy 30 napos tematikus áhítat-mátrixot a(z) '{dev_subject}' témában az alábbi táblázatos szerkezetben:
[Nap száma | Fő KJV igehely és idézet | Központi tanítás/téma | 3 elgondolkodtató önreflektív kérdés].
A stílus legyen meleg, mélyen bátorító, spirituális és mentes minden felszínes klisétől."""
        else:
            matrix_op_prompt = f"""Based on the uploaded theological sources and KJV scriptures, generate a 30-day devotional matrix for '{dev_subject}' in table format:
[Day Number | Core KJV Scripture & Quote | Theological Theme | 3 Reflective Journal Prompts].
Tone: Warm, deeply encouraging, authentic and free from AI clichés."""

        st.markdown(f"##### 📋 {'Operatív Mátrix Prompt (NotebookLM-be másolandó):' if is_hu else 'Operating Matrix Prompt (Copy into NotebookLM):'}")
        st.code(matrix_op_prompt, language="text")

        st.markdown("---")
        st.markdown(f"##### 📥 {'NotebookLM Mátrix Beillesztése:' if is_hu else 'Paste NotebookLM Matrix Output:'}")
        pasted_matrix = st.text_area(
            "Illeszd be ide a NotebookLM által generált táblázatot / mátrix sorokat:" if is_hu else "Paste 30-day matrix rows here:",
            height=150,
            placeholder="[Day 1 | Philippians 4:6-7 | God's peace guards hearts | 1. What worries you today? 2. How do you surrender it? 3. What can you thank God for?]",
            key="rag_pasted_matrix"
        )

        st.markdown(f"##### 💎 {'Gemini Advanced Master Prompt (A Mátrix Kifejtéséhez):' if is_hu else 'Gemini Advanced Master Prompt (To Expand Matrix):'}")
        if is_hu:
            gemini_dev_master = f"""Szeretnék egy mély, hiteles és lelkileg építő 30 napos keresztény áhítat naplót (devotional) írni '{dev_subject}' címmel {dev_target} számára.
Az alábbiakban megadom a NotebookLM által teológiailag ellenőrzött vázlatot a(z) [NAP SZÁMA, PL.: 1.] naphoz:
[IDE ILLESD BE A FENTI MÁTRIX ADOTT SORÁT]

Kérlek, írd meg a nap teljes tartalmát az alábbi szerkezetben:
1. A megadott KJV bibliai ige és pontos fordítása
2. Egy 200 szavas bátorító, mély magyarázó-elmélkedő szöveg (csendes reflexió)
3. Egy bensőséges, tiszteletteljes napi ima
4. 3 db mély, elgondolkodtató önreflektív kérdés vezetett naplózáshoz"""
        else:
            gemini_dev_master = f"""Write a deep, authentic Christian devotional for '{dev_subject}' targeted at {dev_target}.
Here is the source-grounded matrix row for [DAY NUMBER]:
[PASTE MATRIX ROW HERE]

Structure:
1. Scripture quote (KJV)
2. 200-word pastoral reflection
3. Heartfelt daily prayer
4. 3 journal prompts"""

        st.code(gemini_dev_master, language="text")

        if st.button("💾 " + ("Mátrix Mentése" if is_hu else "Save Matrix to Active Project"), use_container_width=True, type="primary"):
            if pasted_matrix.strip():
                st.session_state["rag_devotional_matrix"] = pasted_matrix.strip()
                st.success("✅ " + ("Teológiai mátrix sikeresen elmentve!" if is_hu else "Theological matrix saved successfully!"))

    # ─────────────────────────────────────────────────────────
    # TAB 3: REVIEW MINING & PIACI RÉSEK ELEMZÉSE
    # ─────────────────────────────────────────────────────────
    with tab_reviews:
        st.markdown(f"#### ⭐ {'Versenytárs-értékelések és Piaci Rések Elemzése (Review Mining)' if is_hu else 'Competitor Review Mining & Market Gap Analysis'}")
        st.caption("Az Amazon KDP és Etsy top versenytársak 1-3 csillagos értékeléseinek elemzése." if is_hu else "Analyze 1-3 star competitor reviews on Amazon KDP & Etsy to find product improvements.")

        c_r1, c_r2 = st.columns([1.2, 1.0])
        with c_r1:
            comp_niche = st.text_input("Versenytárs Termékkategória:" if is_hu else "Competitor Category:", value="Christian Coloring Book for Kids / Toddlers", key="rag_rev_niche")
        with c_r2:
            st.markdown(f"""
            <div class='metric-card'>
                <strong style='color:#f59e0b;'>{'Módszer' if is_hu else 'Method'}:</strong> {'Másolj ki 20-30 db 1-3 csillagos véleményt a versenytársaktól, és töltsd fel forrásként a NotebookLM-be.' if is_hu else 'Paste 20-30 competitor 1-3 star reviews into NotebookLM as a source.'}
            </div>
            """, unsafe_allow_html=True)

        if is_hu:
            review_op_prompt = f"""A feltöltött vásárlói vélemények alapján milyen technikai és tartalmi hibákat említenek a leggyakrabban a vevők (pl. vonalvastagság, túl bonyolult részletek, rossz papírméret, filc átvérzése, hiányos igeidézetek), és mi az az 5 konkrét dolog, amivel a mi új '{comp_niche}' termékünk kiemelkedhet és 5 csillagos értékeléseket szerezhet?"""
        else:
            review_op_prompt = f"""Based on the uploaded customer reviews, identify top recurring complaints (bleed-through, thin lines, paper size) and give 5 actionable ways our new '{comp_niche}' product can solve them to earn 5-star ratings."""

        st.markdown(f"##### 📋 {'Operatív Review Mining Prompt:' if is_hu else 'Review Mining Operating Prompt:'}")
        st.code(review_op_prompt, language="text")

        st.markdown("---")
        rev_findings = st.text_area(
            "Illeszd be a NotebookLM által azonosított hibákat és ajánlásokat:" if is_hu else "Paste identified gaps and specs:",
            height=140,
            placeholder="1. Bleed-through -> Add blank back pages\n2. Thin lines -> Use bold 4K line art\n3. Inaccurate verses -> Use literal KJV",
            key="rag_rev_findings"
        )
        if st.button("💾 " + ("Specifikációk Mentése" if is_hu else "Save Specifications"), use_container_width=True):
            if rev_findings.strip():
                st.session_state["rag_competitor_specs"] = rev_findings.strip()
                st.success("✅ " + ("Versenytársi specifikációk mentve!" if is_hu else "Specifications saved!"))

    # ─────────────────────────────────────────────────────────
    # TAB 4: AUDIO DEVOTIONAL (GUMROAD $39 UPSELL)
    # ─────────────────────────────────────────────────────────
    with tab_audio:
        st.markdown(f"#### 🎙️ {'Bónusz Digitális Termék: Audio Devotional Companion (Deep Dive Podcast)' if is_hu else 'Bonus Digital Asset: Audio Devotional Companion ($39 Upsell)'}")
        st.caption("A NotebookLM Audio Overview funkciójával egyetlen kattintással generálható egy 10-15 perces két műsorvezetős áhítat podcast (MP3), ami $10 tiszta profitnövekedést biztosít." if is_hu else "Generate 10-15 min two-host conversational MP3 podcast in NotebookLM for +$10 pure profit bump.")

        st.markdown(f"""
        <div style='background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 10px; padding: 14px 18px; margin-bottom: 16px;'>
            <h5 style='color: #10b981; margin: 0 0 6px 0;'>💰 {'Pénzügyi Hatás & Értéknövelés' if is_hu else 'Financial Impact & Value Stack'}</h5>
            <p style='margin: 0; color: #e2e8f0; font-size: 0.92rem;'>
                {'Alap Digitális Áhítat Napló (PDF):' if is_hu else 'Basic Devotional Journal (PDF):'} <strong>$29</strong><br>
                {'Prémium Csomag +' if is_hu else 'Premium Bundle +'} <strong>Audio Companion (Deep Dive MP3 Podcast)</strong>: <strong>$39</strong><br>
                <span style='color: #34d399; font-weight: bold;'>➔ {'+$10 tiszta extra profit vásárlásonként, 0 Ft plusz előállítási költséggel!' if is_hu else '+$10 pure profit per sale with zero additional cost!'}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        audio_copy_snippet = """🎁 EXCLUSIVE BONUS: Complete 15-Minute Audio Devotional Companion (MP3)
- High-quality immersive audio reflection for busy mornings, daily commutes, or evening prayer time.
- Professional deep dive conversation exploring the key theological breakthroughs of the 30-day journey.
- Total Value: $19.00 — Yours FREE with the Premium Devotional Bundle!"""
        st.code(audio_copy_snippet, language="text")

    # ─────────────────────────────────────────────────────────
    # TAB 5: ESZKÖZ-HATÁROLÁSI MÁTRIX
    # ─────────────────────────────────────────────────────────
    with tab_matrix_guide:
        st.markdown(f"#### 🧭 {'Eszköz-határolási Mátrix (Hol NEM érdemes NotebookLM-et használni?)' if is_hu else 'Tool Boundaries Matrix (When NOT to use NotebookLM)'}")
        
        if is_hu:
            table_md = """
| Feladat a Folyamatban | Miért NEM a NotebookLM a megfelelő eszköz? | Helyette Ajánlott Optimális Eszköz |
| :--- | :--- | :--- |
| **Képgenerálás** | A NotebookLM szigorúan szöveg- és hangalapú RAG modell; nem rendelkezik képgenerálási képességekkel. | **Gemini Web 4K / Custom Gems** |
| **Pinterest Leírások Gyártása** | A Pinterest SEO leírásokhoz nincs szükség forrásdokumentumok elemzésére. | **FFC Marketing Modul** |
| **PDF Összeállítás és Formázás** | A NotebookLM nem grafikai szerkesztő vagy kiadványszerkesztő szoftver. | **Streamlit ReportLab Engine** |
| **100% Pontos KJV Igehely Kutatás** | A sima LLM hallucinálhat és félreidézhet. | **NotebookLM (Feltöltött KJV Biblia forrással) ✅** |
| **Teológiai 30 Napos Mátrix** | Sima prompttal repetitív és sekélyes lesz a tartalom. | **NotebookLM (Teológiai könyvek forrásként) ✅** |
| **Vásárlói Értékelések Elemzése** | Több száz komment kézi olvasása executive dysfunction-t okoz. | **NotebookLM (Review Mining RAG) ✅** |
| **Audio Devotional Podcast Upsell** | Más eszközökben drága és körülményes a két szereplős podcast. | **NotebookLM Audio Overview (1-Kattintás) ✅** |
"""
        else:
            table_md = """
| Task in Pipeline | Why NOT NotebookLM? | Recommended Optimal Tool |
| :--- | :--- | :--- |
| **Image Generation** | NotebookLM is strictly text and audio RAG, cannot create visual graphics. | **Gemini Web 4K / Custom Gems** |
| **Pinterest SEO Pin Copy** | Source documents not needed for short social captions. | **FFC Marketing Module** |
| **Print PDF Compilation** | NotebookLM does not output formatted print PDFs. | **Streamlit ReportLab Engine** |
| **100% Accurate KJV Mining** | Standard LLMs can hallucinate scriptures. | **NotebookLM (Uploaded KJV Source) ✅** |
| **30-Day Theological Matrix** | Generic prompts yield repetitive shallow text. | **NotebookLM (Grounded RAG) ✅** |
| **Competitor Review Mining** | Manual reading triggers cognitive fatigue. | **NotebookLM (Review Mining) ✅** |
| **Audio Devotional Podcast** | Multi-speaker voice synthesis is costly elsewhere. | **NotebookLM Audio Overview (1-Click) ✅** |
"""
        st.markdown(table_md)
