"""
Workspace: NotebookLM RAG Működési Motor & Kutatóközpont
=========================================================
Google NotebookLM Retrieval-Augmented Generation (RAG) integráció az AudHD munkafolyamatba:
1. 100%-ban hallucinációmentes KJV igehely- és jelenetkutatás (Hétfő)
2. 30 napos Áhítatok teológiai gerincének felépítése (Kedd)
3. Versenytárs-értékelések és piaci rések elemzése (Review Mining)
4. Bónusz digitális termék: Audio Devotional / Audio Overview (Gumroad $29 ➔ $39 Upsell)
5. Eszköz-határolási Mátrix (Hol NEM érdemes NotebookLM-et használni?)
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
    st.markdown("<div class='path-badge'>📓 NotebookLM RAG Központ & Hallucinációmentes Kutatóműhely</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid #38bdf8; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <span style='font-size: 2.2rem;'>🧠 ➔ 📓</span>
            <div>
                <strong style='font-size: 1.15rem; color: #38bdf8;'>NotebookLM Mint Szigorú Forrásalapú (RAG) Működési Motor</strong>
                <p style='margin: 4px 0 0 0; color: #cbd5e1; font-size: 0.9rem;'>
                    A hagyományos nagy nyelvi modellek hajlamosak a bibliai igéket pontatlanul idézni vagy felületes teológiai közhelyeket generálni. 
                    A NotebookLM kizárólag a feltöltött forrásokból (KJV Biblia, teológiai jegyzetek, versenytársi értékelések) dolgozik, 
                    így <strong>100%-ban garantálja a tényhűséget és megszünteti a hallucinációt</strong>.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_kjv, tab_matrix, tab_reviews, tab_audio, tab_matrix_guide = st.tabs([
        "📖 1. KJV Igehely & Jelenetkutatás",
        "📑 2. 30 Napos Teológiai Mátrix",
        "⭐ 3. Versenytárs Review Mining",
        "🎙️ 4. Audio Devotional ($29 ➔ $39)",
        "🧭 5. Eszköz-határolási Mátrix"
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1: KJV IGEHELY & JELENETKUTATÁS (HÉTFŐ)
    # ─────────────────────────────────────────────────────────
    with tab_kjv:
        st.markdown("#### 📖 100%-ban Hallucinációmentes Igehely- és Jelenetkutatás")
        st.caption("Használd ezt a munkafolyamatot hétfőnként a színezők, mesekönyvek és faliképek pontos bibliai alapjainak kinyeréséhez.")

        c_k1, c_k2 = st.columns([1.2, 1.0])
        with c_k1:
            testament = st.radio(
                "Bibliai Fókusz:",
                ["Ószövetség (Állatok, nagy csodák, látványos történetek)", "Újszövetség (Jézus példázatai, gyógyítások, apostolok)", "Zsoltárok & Példabeszédek (Megnyugtató, bátorító igék)"],
                index=0,
                key="rag_kjv_testament"
            )
            theme_subject = st.text_input(
                "Téma / Kulcsszavak:",
                value="gyermekek számára könnyen vizualizálható állatok vagy látványos események",
                key="rag_kjv_theme"
            )
            scene_count = st.slider("Kinyerendő Jelenetek Száma:", min_value=10, max_value=50, value=30, step=5, key="rag_kjv_count")

        with c_k2:
            st.markdown("""
            <div class='metric-card'>
                <strong style='color:#38bdf8;'>1. Lépés:</strong> Nyisd meg a <a href='https://notebooklm.google.com' target='_blank' style='color:#38bdf8; text-decoration: underline;'>NotebookLM</a> felületét.<br>
                <strong style='color:#34d399;'>2. Lépés:</strong> Hozz létre egy jegyzetfüzetet és töltsd fel a teljes <strong>KJV Biblia TXT/PDF</strong> állományát.<br>
                <strong style='color:#f59e0b;'>3. Lépés:</strong> Másold be az alábbi operatív promptot, majd a kapott listát illeszd be ide!
            </div>
            """, unsafe_allow_html=True)

        kjv_op_prompt = f"""Gyűjts ki nekem a feltöltött KJV Bibliából {scene_count} olyan {testament.split('(')[0].strip().lower()} jelenetet, amely {theme_subject} tartalmaz. Mindegyikhez add meg a pontos igehelyet (pl. Genesis 6:14-22) és az exakt KJV idézetet szó szerint, valamint egy tömör, 1 mondatos angol vizuális jelenetleírást."""

        st.markdown("##### 📋 Operatív Prompt (NotebookLM-be másolandó):")
        st.code(kjv_op_prompt, language="text")

        st.markdown("---")
        st.markdown("##### 📥 NotebookLM Eredmények Beillesztése & Importálása az Aktív Projektbe")
        pasted_scenes = st.text_area(
            "Illeszd be ide a NotebookLM által kinyert sorszámozott jeleneteket / KJV igéket:",
            height=160,
            placeholder="1. Genesis 6:14 - Noah building the ark with cedar wood...\n2. Genesis 8:11 - The dove returning with an olive leaf in her mouth...",
            key="rag_pasted_scenes"
        )

        if st.button("💾 Jelenetek Mentése & Átadás a KDP Színező / Falikép Modulnak", use_container_width=True, type="primary"):
            if pasted_scenes.strip():
                st.session_state["rag_kjv_scenes_saved"] = pasted_scenes.strip()
                save_prompts_file_to_drive("01_🎨_KDP_COLORING", "notebooklm_kjv_scenes.txt", pasted_scenes.strip())
                st.success("✅ KJV jelenetek sikeresen elmentve és átadva az aktív projekt munkaterületeinek!")
            else:
                st.warning("Kérlek, illeszd be a NotebookLM kimenetet a mentéshez.")

    # ─────────────────────────────────────────────────────────
    # TAB 2: 30 NAPOS TEOLÓGIAI MÁTRIX (KEDD - GUMROAD)
    # ─────────────────────────────────────────────────────────
    with tab_matrix:
        st.markdown("#### 📑 30 Napos Áhítatok Teológiai Gerincének Felépítése (Kedd)")
        st.caption("A repetitív, közhelyes AI-szövegek elkerülése: forrásalapú mátrix generálása NotebookLM-ben, majd kifejtése Gemini Advanced-del.")

        c_m1, c_m2 = st.columns([1.2, 1.0])
        with c_m1:
            dev_subject = st.text_input("Áhítat Címe / Témája:", value="Reménység és Békesség a Nehéz Időkben (Nőknek)", key="rag_dev_sub")
            dev_target = st.text_input("Célcsoport:", value="Keresztény édesanyák és nők, akik lelki megújulásra vágynak", key="rag_dev_aud")
        with c_m2:
            st.markdown("""
            <div class='metric-card'>
                <strong style='color:#a855f7;'>Forrásfájlok:</strong> Tölts fel prédikációvázlatokat, teológiai könyveket vagy megbízható keresztény cikkeket a NotebookLM-be.<br>
                <strong style='color:#34d399;'>Eredmény:</strong> Egy 30 soros, strukturált táblázatos mátrix, ami garantálja a mély teológiai tartalmat.
            </div>
            """, unsafe_allow_html=True)

        matrix_op_prompt = f"""A feltöltött teológiai források és KJV igék alapján hozz létre egy 30 napos tematikus áhítat-mátrixot a(z) '{dev_subject}' témában az alábbi táblázatos szerkezetben:
[Nap száma | Fő KJV igehely és idézet | Központi tanítás/téma | 3 elgondolkodtató önreflektív kérdés].
A stílus legyen meleg, mélyen bátorító, spirituális és mentes minden felszínes klisétől."""

        st.markdown("##### 📋 Operatív Mátrix Prompt (NotebookLM-be másolandó):")
        st.code(matrix_op_prompt, language="text")

        st.markdown("---")
        st.markdown("##### 📥 NotebookLM Mátrix Beillesztése:")
        pasted_matrix = st.text_area(
            "Illeszd be ide a NotebookLM által generált táblázatot / mátrix sorokat:",
            height=150,
            placeholder="[Nap 1 | Philippians 4:6-7 'Be careful for nothing...' | Isten békessége felülmúl minden értelmet | 1. Mi aggaszt ma? 2. Hogyan tudod átadni? 3. Miért lehetsz hálás?]",
            key="rag_pasted_matrix"
        )

        st.markdown("##### 💎 Gemini Advanced Master Prompt (A Mátrix Kifejtéséhez):")
        gemini_dev_master = f"""Szeretnék egy mély, hiteles és lelkileg építő 30 napos keresztény áhítat naplót (devotional) írni '{dev_subject}' címmel {dev_target} számára.
Az alábbiakban megadom a NotebookLM által teológiailag ellenőrzött vázlatot a(z) [NAP SZÁMA, PL.: 1.] naphoz:
[IDE ILLESD BE A FENTI MÁTRIX ADOTT SORÁT]

Kérlek, írd meg a nap teljes tartalmát az alábbi szerkezetben:
1. A megadott KJV bibliai ige és pontos magyar fordítása
2. Egy 200 szavas bátorító, mély magyarázó-elmélkedő szöveg (csendes reflexió)
3. Egy bensőséges, tiszteletteljes napi ima
4. 3 db mély, elgondolkodtató önreflektív kérdés vezetett naplózáshoz

Stílusutasítás: Kerüld a tipikus, mesterkélt AI-fordulatokat és a túl száraz megfogalmazást. Írj meleg, mélyen bátorító, spirituális, tiszteletteljes és emberi tónusban."""

        st.code(gemini_dev_master, language="text")

        if st.button("💾 Mátrix Mentése a Gumroad Áhítat Műhelyhez", use_container_width=True, type="primary"):
            if pasted_matrix.strip():
                st.session_state["rag_devotional_matrix"] = pasted_matrix.strip()
                save_prompts_file_to_drive("05_📖_GUMROAD_PLR", "notebooklm_theological_matrix.txt", pasted_matrix.strip())
                st.success("✅ Teológiai mátrix elmentve a Google Drive 05_📖_GUMROAD_PLR mappába!")

    # ─────────────────────────────────────────────────────────
    # TAB 3: REVIEW MINING & PIACI RÉSEK ELEMZÉSE
    # ─────────────────────────────────────────────────────────
    with tab_reviews:
        st.markdown("#### ⭐ Versenytárs-értékelések és Piaci Rések Elemzése (Review Mining)")
        st.caption("Az Amazon KDP és Etsy top versenytársak 1-3 csillagos értékeléseinek elemzése az AudHD túlterhelődés elkerülésével.")

        c_r1, c_r2 = st.columns([1.2, 1.0])
        with c_r1:
            comp_niche = st.text_input("Versenytárs Termékkategória:", value="Christian Coloring Book for Kids / Toddlers", key="rag_rev_niche")
        with c_r2:
            st.markdown("""
            <div class='metric-card'>
                <strong style='color:#f59e0b;'>Gyors módszer:</strong> Nyiss meg 3-5 top Amazon/Etsy terméket, másolj ki 20-30 db 1-3 csillagos véleményt egy szöveges dokumentumba, és töltsd fel forrásként a NotebookLM-be.
            </div>
            """, unsafe_allow_html=True)

        review_op_prompt = f"""A feltöltött vásárlói vélemények alapján milyen technikai és tartalmi hibákat említenek a leggyakrabban a vevők (pl. vonalvastagság, túl bonyolult részletek, rossz papírméret, filc átvérzése, hiányos igeidézetek), és mi az az 5 konkrét dolog, amivel a mi új '{comp_niche}' termékünk kiemelkedhet és 5 csillagos értékeléseket szerezhet?"""

        st.markdown("##### 📋 Operatív Review Mining Prompt (NotebookLM-be másolandó):")
        st.code(review_op_prompt, language="text")

        st.markdown("---")
        st.markdown("##### 📥 Kinyert Technikai Specifikációk és Termékelőnyök:")
        rev_findings = st.text_area(
            "Illeszd be a NotebookLM által azonosított hibákat és ajánlásokat:",
            height=140,
            placeholder="Gyakori hibák: 1. Átvérzik a filc -> Megoldás: Filcátütés-gátló üres lapok beillesztése\n2. Túl vékony vonalak -> Megoldás: Bold, 4K thick line art\n3. Pontatlan igék -> Megoldás: Szó szerinti KJV idézetek",
            key="rag_rev_findings"
        )
        if st.button("💾 Specifikációk Mentése a Projekt Paramétereihez", use_container_width=True):
            if rev_findings.strip():
                st.session_state["rag_competitor_specs"] = rev_findings.strip()
                st.success("✅ Versenytársi specifikációk mentve!")

    # ─────────────────────────────────────────────────────────
    # TAB 4: AUDIO DEVOTIONAL (GUMROAD $29 ➔ $39 UPSELL)
    # ─────────────────────────────────────────────────────────
    with tab_audio:
        st.markdown("#### 🎙️ Bónusz Digitális Termék: Audio Devotional Companion (Deep Dive Podcast)")
        st.caption("A NotebookLM Audio Overview funkciójával egyetlen kattintással generálható egy 10-15 perces két műsorvezetős angol nyelvű áhítat podcast (MP3), ami $10 tiszta profitnövekedést biztosít termékenként.")

        st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 10px; padding: 14px 18px; margin-bottom: 16px;'>
            <h5 style='color: #10b981; margin: 0 0 6px 0;'>💰 Pénzügyi Hatás & Értéknövelés</h5>
            <p style='margin: 0; color: #e2e8f0; font-size: 0.92rem;'>
                Alap Digitális Áhítat Napló (PDF): <strong>$29</strong><br>
                Prémium Csomag + <strong>Audio Companion (Deep Dive MP3 Podcast)</strong>: <strong>$39</strong><br>
                <span style='color: #34d399; font-weight: bold;'>➔ +$10 (kb. 3 650 HUF) tiszta extra profit vásárlásonként, 0 Ft plusz előállítási költséggel!</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 🛠️ Lépésről-lépésre Megvalósítás (Pénteki rutin):")
        st.markdown("""
        1. **Kézirat feltöltése:** Miután elkészült a 30 napos áhítat szövege (Google Docs / PDF), töltsd fel egy új forrásként a NotebookLM-be.
        2. **Deep Dive generálás:** A jobb oldali **Studio** panelen kattints a **Generate** gombra az *Audio Overview (Deep Dive)* szekcióban.
        3. **Letöltés:** 3-5 perc alatt elkészül a professzionális, rendkívül élethű két műsorvezetős angol nyelvű beszélgetés. Kattints a három pontra és válaszd a **Download Audio (.mp3)** opciót.
        4. **Gumroad csatolás:** Töltsd fel az MP3 fájlt a Gumroad termék oldalán mint *Bonus: Complete Audio Companion (Listen on the go)*.
        """)

        st.markdown("##### 📦 Gumroad Értékhalom (Value Stack) Bónusz Szövegrészlet:")
        audio_copy_snippet = """🎁 EXCLUSIVE BONUS: Complete 15-Minute Audio Devotional Companion (MP3)
- High-quality immersive audio reflection for busy mornings, daily commutes, or evening prayer time.
- Professional deep dive conversation exploring the key theological breakthroughs of the 30-day journey.
- Total Value: $19.00 — Yours FREE with the Premium Devotional Bundle!"""
        st.code(audio_copy_snippet, language="text")

    # ─────────────────────────────────────────────────────────
    # TAB 5: ESZKÖZ-HATÁROLÁSI MÁTRIX
    # ─────────────────────────────────────────────────────────
    with tab_matrix_guide:
        st.markdown("#### 🧭 Eszköz-határolási Mátrix (Hol NEM érdemes NotebookLM-et használni?)")
        st.caption("A technológiai határok pontos ismerete megvédi az AudHD idegrendszert a felesleges próbálkozásoktól és időveszteségtől.")

        table_md = """
| Feladat a Folyamatban | Miért NEM a NotebookLM a megfelelő eszköz? | Helyette Ajánlott Optimális Eszköz |
| :--- | :--- | :--- |
| **Képgenerálás** | A NotebookLM szigorúan szöveg- és hangalapú RAG modell; nem rendelkezik képgenerálási képességekkel. | **Streamlit App + Gemini Nano Banana Pro / FLUX** |
| **Pinterest Leírások Gyártása** | A Pinterest SEO leírásokhoz nincs szükség forrásdokumentumok elemzésére; a gyors chat hatékonyabb. | **Gemini Advanced (Chat felület) / FFC Modul** |
| **PDF Összeállítás és Formázás** | A NotebookLM nem grafikai szerkesztő vagy kiadványszerkesztő szoftver. | **Streamlit ReportLab Engine / Canva Free** |
| **100% Pontos KJV Igehely Kutatás** | A sima LLM hallucinálhat és félreidézhet. | **NotebookLM (Feltöltött KJV Biblia forrással) ✅** |
| **Teológiai 30 Napos Mátrix** | Sima prompttal repetitív és sekélyes lesz a tartalom. | **NotebookLM (Teológiai könyvek forrásként) ✅** |
| **Vásárlói Értékelések Elemzése** | Több száz komment kézi olvasása executive dysfunction-t okoz. | **NotebookLM (Review Mining RAG) ✅** |
| **Audio Devotional Podcast Upsell** | Más eszközökben drága és körülményes a két szereplős podcast. | **NotebookLM Audio Overview (1-Kattintás) ✅** |
"""
        st.markdown(table_md)
