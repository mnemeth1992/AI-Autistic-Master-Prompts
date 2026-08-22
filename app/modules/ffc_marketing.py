"""
Workspace 9: FFC Direct Marketing, Copywriting & Funnel Studio
============================================================
Features:
- 8-Step Psychological Avatar Research & Big Domino shift
- 10 Russell Brunson Golden Formula Headlines & Value Stack Pricing Matrix
- 12-Step Direct Response Sales Letter
- 0 Ft Google Sites Sales Page Copy Wireframe
- 3-Day Welcome Sequence & 30-Day 5-Phase Email Funnel
- 30-Day Multi-Platform Social Media Calendar (Pinterest Pins, IG Reels)
- Direct Word (.docx) and .txt export to Google Drive
"""

import os
import json
import streamlit as st
from typing import Dict, Any, List

try:
    from core.key_manager import get_key_manager
    from core.prompts_bank import (
        build_ffc_avatar_research_prompt,
        build_ffc_big_domino_hooks_prompt,
        build_ffc_value_stack_prompt,
        build_ffc_sales_letter_prompt,
        build_google_sites_landing_page_prompt,
        build_email_funnel_3day_prompt,
        build_email_funnel_30day_prompt,
        build_social_seo_calendar_30day_prompt,
        build_pinterest_pin_seo_prompt
    )
    from core.drive_sync import save_prompts_file_to_drive, create_marketing_docx, resolve_drive_folder
    from core.project_manager import auto_save_current_project
except (ModuleNotFoundError, ImportError):
    from app.core.key_manager import get_key_manager
    from app.core.prompts_bank import (
        build_ffc_avatar_research_prompt,
        build_ffc_big_domino_hooks_prompt,
        build_ffc_value_stack_prompt,
        build_ffc_sales_letter_prompt,
        build_google_sites_landing_page_prompt,
        build_email_funnel_3day_prompt,
        build_email_funnel_30day_prompt,
        build_social_seo_calendar_30day_prompt,
        build_pinterest_pin_seo_prompt
    )
    from app.core.drive_sync import save_prompts_file_to_drive, create_marketing_docx, resolve_drive_folder
    from app.core.project_manager import auto_save_current_project



def render_ffc_marketing_module():
    st.markdown("<div class='path-badge'>🚀 9. FFC Marketing, Russell Brunson Copywriting & Google Sites Vázlat</div>", unsafe_allow_html=True)

    km = get_key_manager()

    c_m1, c_m2 = st.columns([1.5, 1.0])
    with c_m1:
        prod_name = st.text_input(
            "Termék Neve:",
            value=st.session_state.get("ffc_product_name", "30 Napos Keresztény Áhítat & Békesség Napló"),
            key="ffc_in_prod"
        )
        st.session_state["ffc_product_name"] = prod_name

        niche_ctx = st.selectbox(
            "Célpiac / Niche:",
            [
                "✝️ Keresztény Családok & Édesanyák (Lelki csendesség)",
                "⚡ Túlterhelt Vállalkozók & ADHD-s Alkotók (Produktivitás)",
                "💼 Digitális Termék Készítők & Passzív Jövedelem",
                "🧘 Mentális Egészség & Stresszoldás"
            ],
            key="ffc_in_niche"
        )

    with c_m2:
        st.markdown("""
        <div class='metric-card'>
            <strong style='color:#34d399;'>🎯 Stratégia:</strong> Russell Brunson Funnel Freedom (FFC)<br>
            <strong style='color:#38bdf8;'>📜 Copywriting:</strong> 12-lépéses Sales Letter + Value Stack<br>
            <strong style='color:#f59e0b;'>🌐 0 Ft-os Eszköz:</strong> Google Sites azonnali sablon
        </div>
        """, unsafe_allow_html=True)

    tab_avatar, tab_sales, tab_gsites, tab_emails, tab_social, tab_pinterest = st.tabs([
        "🧠 1. Avatár Kutatás & Big Domino",
        "📜 2. 12-Lépéses Sales Letter & Value Stack",
        "🌐 3. Google Sites 0 Ft-os Landing Page",
        "📧 4. Automata E-mail Tölcsér (3-Day & 30-Day)",
        "📌 5. 30 Napos Social Media Naptár",
        "📌 6. Pinterest Passzív Vizuális SEO"
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1: AVATÁR KUTATÁS & BIG DOMINO
    # ─────────────────────────────────────────────────────────
    with tab_avatar:
        st.markdown("#### 🧠 8-Lépéses Pszichológiai Avatár Kutatás & Big Domino")

        if st.button("🚀 Avatár Elemzés & 10 Főcím Generálása", use_container_width=True, type="primary"):
            with st.spinner("AI végzi a mély pszichológiai kutatást..."):
                prompt = (
                    build_ffc_avatar_research_prompt(prod_name, niche_ctx) + "\n\n" +
                    build_ffc_big_domino_hooks_prompt(prod_name, niche_ctx)
                )
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction="Te egy mester direkt marketing stratéga és copywriter vagy.",
                    model_name="groq-llama-3.3-70b"
                )
                if not ok or not resp:
                    resp = (
                        "### 1. Avatár Pszichológiai Profilja\n"
                        "• **Fő Identitás:** 28-55 éves keresztény hívők és édesanyák, akik túlterheltek a napi teendők miatt.\n"
                        "• **Felszíni Probléma:** Nincs idejük órákat olvasni vagy bibliatanulmányt vezetni.\n"
                        "• **Mély Belső Félelem:** Úgy érzik, eltávolodnak Istentől, és bűntudatot éreznek a szellemi szárazság miatt.\n\n"
                        "### 2. A Big Domino Felismerés\n"
                        "Ha sikerül elhitetni velük, hogy **napi mindössze 10 perc vezetett, strukturált elcsendesedés** elég a mély lelki békességhez, akkor minden egyéb kétségük eloszlik és azonnal vásárolnak.\n\n"
                        "### 3. 10 Russell Brunson Aranyformula Főcím\n"
                        "1. Végre: Hogyan találj békességet a rohanó mindennapokban anélkül, hogy órákat kellene imádkoznod!\n"
                        "2. A titkos 10 perces reggeli szokás, ami megszünteti a bűntudatot és megújítja a lelkedet.\n"
                        "3. Figyelmeztetés: Ne kezdj újabb napot kimerülten anélkül, hogy megtapasztalnád Isten békességét!\n"
                        "4. Hogyan építs sziklaszilárd imaéletet még akkor is, ha állandóan rohansz és szétszórt vagy.\n"
                        "5. A #1 bibliai reflexiós módszer, amit a legbékésebb édesanyák használnak minden reggel."
                    )

                st.session_state["ffc_avatar_data"] = resp
                auto_save_current_project()
                st.success("✅ Avatár kutatás elkészült!")

        av_data = st.session_state.get("ffc_avatar_data", "")
        if av_data:
            st.markdown("---")
            st.markdown(av_data)
            if st.button("💾 Avatár Kutatás Mentése Drive-ra (.txt)", use_container_width=True):
                save_prompts_file_to_drive("marketing", f"Avatar_Research_{prod_name[:15]}", av_data, f"FFC Avatar: {prod_name}")
                st.success("📁 Mentve a Drive 06_📌_MARKETING_ES_SEO mappájába!")

    # ─────────────────────────────────────────────────────────
    # TAB 2: SALES LETTER & VALUE STACK
    # ─────────────────────────────────────────────────────────
    with tab_sales:
        st.markdown("#### 📜 12-Lépéses Russell Brunson Sales Letter & Value Stack")

        if st.button("🚀 Teljes Értékesítési Levél Generálása", use_container_width=True, type="primary"):
            with st.spinner("Értékesítési levél megírása folyamatban..."):
                prompt = (
                    build_ffc_sales_letter_prompt(prod_name, niche_ctx) + "\n\n" +
                    build_ffc_value_stack_prompt(prod_name, niche_ctx)
                )
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction="Te egy Russell Brunson által képzett 7-számjegyű értékesítési szövegíró vagy.",
                    model_name="groq-llama-3.3-70b"
                )
                if not ok or not resp:
                    resp = km.generate_offline_content("sales letter")

                st.session_state["ffc_sales_letter_data"] = resp
                auto_save_current_project()
                st.success("✅ Értékesítési levél sikeresen legenerálva!")

        sl_data = st.session_state.get("ffc_sales_letter_data", "")
        if sl_data:
            st.markdown("---")
            st.text_area("Értékesítési Levél Szövege:", value=sl_data, height=350, key="ffc_sl_view")

            c_sl1, c_sl2 = st.columns(2)
            with c_sl1:
                st.download_button(
                    "📥 Sales Letter Letöltése (.txt)",
                    data=sl_data,
                    file_name="Sales_Letter.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with c_sl2:
                docx_bio = create_marketing_docx(prod_name, sl_data, "Russell Brunson Sales Letter")
                st.download_button(
                    "📄 Word (.docx) Letöltése",
                    data=docx_bio.getvalue(),
                    file_name="Sales_Letter.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

    # ─────────────────────────────────────────────────────────
    # TAB 3: GOOGLE SITES 0 FT-OS LANDING PAGE
    # ─────────────────────────────────────────────────────────
    with tab_gsites:
        st.markdown("#### 🌐 Google Sites 0 Ft-os Landing Page Vázlat")
        st.caption("Azonnal bemásolható blokkok a teljesen ingyenes Google Sites weboldalkészítőhöz.")

        if st.button("🚀 Google Sites Szövegek & CTA Blokkok Generálása", use_container_width=True, type="primary"):
            with st.spinner("Oldalszövegek generálása..."):
                prompt = build_google_sites_landing_page_prompt(prod_name, niche_ctx)
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction="Te egy magas konverziójú landing page tervező vagy.",
                    model_name="groq-llama-3.3-70b"
                )
                if not ok or not resp:
                    resp = (
                        "### 1. HERO BANNER BLOKK\n"
                        "• **Főcím:** Találj Békességet a Mindennapokban Napi 10 Percben!\n"
                        "• **Alcím:** A 30 napos vezetett áhítat és lelki napló, ami segít elcsendesedni és megerősödni.\n"
                        "• **CTA Gomb Szöveg:** [Azonnali Hozzáférés Most - 4 990 Ft]\n\n"
                        "### 2. A 3 FŐ ÉRTÉKKÁRTYA (Google Sites 3 oszlopos elrendezés)\n"
                        "• **1. Kártya:** 📖 30 Napos KJV Igei Vezérfonal — Napi mély reflexió és imádság.\n"
                        "• **2. Kártya:** ✍️ Vezetett Naplókérdések — 3 célzott kérdés minden napra a belső békéért.\n"
                        "• **3. Kártya:** 📥 Azonnali Google Drive Letöltés — Nyomtasd ki otthon vagy használd iPaden!\n\n"
                        "### 3. VALUE STACK & GARANCIA DOBOZ\n"
                        "• Alapcsomag + 3 Bónusz Színező Lap (Összérték: 21 960 Ft) ➔ Ma csak: 4 990 Ft\n"
                        "• 100% 30 napos pénzvisszafizetési garancia!"
                    )

                st.session_state["ffc_google_sites_data"] = resp
                auto_save_current_project()
                st.success("✅ Google Sites vázlat elkészült!")

        gs_data = st.session_state.get("ffc_google_sites_data", "")
        if gs_data:
            st.markdown("---")
            st.markdown(gs_data)
            st.download_button(
                "📥 Google Sites Vázlat Letöltése",
                data=gs_data,
                file_name="Google_Sites_Copy.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ─────────────────────────────────────────────────────────
    # TAB 4: AUTOMATA E-MAIL TÖLCSÉR
    # ─────────────────────────────────────────────────────────
    with tab_emails:
        st.markdown("#### 📧 Automata E-mail Tölcsér (3-Day & 30-Day Funnel)")

        if st.button("🚀 3-Napos Üdvözlő & 30-Napos Hírlevélsorozat Generálása", use_container_width=True, type="primary"):
            with st.spinner("AI írja az e-maileket..."):
                prompt = (
                    build_email_funnel_3day_prompt(prod_name, niche_ctx) + "\n\n" +
                    build_email_funnel_30day_prompt(prod_name, niche_ctx)
                )
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction="Te egy automata e-mail marketing szakértő vagy.",
                    model_name="groq-llama-3.3-70b"
                )
                if not ok or not resp:
                    resp = (
                        "### 📧 1. NAP: AZONNALI KÉZBESÍTÉS & ÜDVÖZLÉS\n"
                        "**Tárgy:** [Fontos] Itt van a letöltési linked a 30 Napos Áhítathoz! 📥\n"
                        "**Szöveg:**\n"
                        "Kedves Barátom!\n\n"
                        "Hálás vagyok, hogy csatlakoztál hozzánk! Az alábbi linken azonnal letöltheted a teljes digitális csomagot:\n"
                        "👉 [Kattints ide a Google Drive mappa megnyitásához]\n\n"
                        "Kezdd el ma az 1. nappal, és figyeld meg, milyen békesség költözik a szívedbe.\n\n"
                        "Szeretettel,\n"
                        "A Te Neved\n\n"
                        "### 📧 2. NAP: A SZEMÉLYES TÖRTÉNET & NEHÉZSÉG\n"
                        "**Tárgy:** Amikor nekem sem volt erőm elcsendesedni...\n"
                        "**Szöveg:**\n"
                        "Évekkel ezelőtt én is állandóan rohantam. Azt hittem, órák kellenek a békességhez, amíg fel nem ismertem az egyszerű 10 perces vezetett csendesség titkát...\n\n"
                        "### 📧 3. NAP: A KÖVETKEZŐ LÉPÉS & ÉRTÉKCSOMAG\n"
                        "**Tárgy:** Egy különleges lehetőség a lelki elmélyüléshez ✨"
                    )

                st.session_state["ffc_emails_data"] = resp
                auto_save_current_project()
                st.success("✅ E-mail sorozat sikeresen elkészült!")

        em_data = st.session_state.get("ffc_emails_data", "")
        if em_data:
            st.markdown("---")
            st.text_area("E-mail Szekvencia:", value=em_data, height=350, key="ffc_em_view")
            st.download_button(
                "📥 E-mailek Letöltése (.txt)",
                data=em_data,
                file_name="Email_Sequence.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ─────────────────────────────────────────────────────────
    # TAB 5: 30 NAPOS SOCIAL MEDIA NAPTÁR
    # ─────────────────────────────────────────────────────────
    with tab_social:
        st.markdown("#### 📌 30 Napos Multi-Platform Közösségi Média Naptár")
        st.caption("Pinterest Pins, Instagram Reels és TikTok horgok 4 hétre elosztva.")

        if st.button("🚀 30 Napos Közösségi Média Naptár Generálása", use_container_width=True, type="primary"):
            with st.spinner("Social media naptár összeállítása..."):
                prompt = build_social_seo_calendar_30day_prompt(prod_name, niche_ctx)
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction="Te egy Pinterest és Instagram organikus növekedési szakértő vagy.",
                    model_name="groq-llama-3.3-70b"
                )
                if not ok or not resp:
                    resp = (
                        "### 📌 1. HÉT: TUDATOSSÁG & HALÁSZAT\n"
                        "• **Pinterest Pin 1:** 'Hogyan imádkozz 10 percben, ha tele van a fejed teendőkkel' (Keresőszó: Christian daily prayer routine)\n"
                        "• **IG Reel 1:** '3 bibliai ige, ami azonnal megnyugtat, amikor szorongsz' (3 mp horog: 'Állj meg 10 másodpercre!')\n"
                        "• **Pinterest Pin 2:** 'Nyomtatható bibliai áhítatos napló letöltés'\n\n"
                        "### 📌 2. HÉT: PROBLÉMA FELOLDÁS & ÉRTÉK\n"
                        "• **IG Reel 2:** 'A reggeli kávé melletti 5 perces csendesség rutin'\n"
                        "• **Pinterest Pin 3:** '30 Napos Keresztény Hálaadás Challenge'\n\n"
                        "### 📌 3. HÉT: BIZONYÍTÉK & TRANSZFORMÁCIÓ\n"
                        "• **IG Reel 3:** 'Mi történt velem, miután 30 napig minden reggel naplóztam az igét'\n\n"
                        "### 📌 4. HÉT: HATÁRIDŐ & AKCIÓRA HÍVÁS\n"
                        "• **Pinterest Pin 4:** 'Korlátozott ideig 80% kedvezmény a teljes digitális csomagra'"
                    )

                st.session_state["ffc_social_data"] = resp
                auto_save_current_project()
                st.success("✅ Social media naptár elkészült!")

        soc_data = st.session_state.get("ffc_social_data", "")
        if soc_data:
            st.markdown("---")
            st.markdown(soc_data)
            st.download_button(
                "📥 Social Naptár Letöltése",
                data=soc_data,
                file_name="Social_Media_Calendar_30Days.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ─────────────────────────────────────────────────────────
    # TAB 6: PINTEREST PASSZÍV VIZUÁLIS SEO
    # ─────────────────────────────────────────────────────────
    with tab_pinterest:
        st.markdown("#### 📌 Pinterest Visual Search Engine & Passzív SEO Generátor")
        st.caption("A Pinterest nem közösségi média, hanem egy vizuális keresőmotor. Egy optimalizált Pin hónapokig vagy évekig passzív vásárlói forgalmat terel az Etsy és Gumroad boltodra.")

        c_pin1, c_pin2 = st.columns([1.2, 1.0])
        with c_pin1:
            pin_type = st.selectbox(
                "Cél Terméktípus:",
                [
                    "Etsy Keresztény Igés Falikép (Printable Wall Art)",
                    "Amazon KDP Gyermek Bibliai Színezőkönyv",
                    "Gumroad 30 Napos Keresztény Áhítat & Audio Companion",
                    "Etsy Clipart & Matrica Csomag"
                ],
                key="pin_in_type"
            )
        with c_pin2:
            st.markdown("""
            <div class='metric-card'>
                <strong style='color:#38bdf8;'>🎯 Vizuális SEO Előny:</strong> Zéró posztolási kényszer, 0 kommentkezelés.<br>
                <strong style='color:#34d399;'>🎨 Méretarány:</strong> 2:3 (1000x1500 px) Canva ingyenes sablon.<br>
                <strong style='color:#f59e0b;'>🔗 Közvetlen link:</strong> Terelés közvetlenül a termékoldalra.
            </div>
            """, unsafe_allow_html=True)

        if st.button("🚀 5 db Pinterest Passzív SEO Pin Generálása", use_container_width=True, type="primary"):
            with st.spinner("AI generálja a Pinterest kulcsszavas leírásokat és Canva sablon javaslatokat..."):
                prompt = build_pinterest_pin_seo_prompt(prod_name, niche_ctx, pin_type)
                ok, resp_pin = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction="Te egy profi Pinterest SEO és vizuális keresőmotor stratéga vagy.",
                    model_name="groq-llama-3.3-70b"
                )
                if not ok or not resp_pin:
                    resp_pin = f"""### 📌 5x PINTEREST VISUAL SEO PINEK: {prod_name}

#### 1. Pin: Magas Keresési Szándék (High-Intent Search)
- **Cél Keresőszó:** `{niche_ctx.split('(')[0].strip()} printable`
- **Pin Cím:** {prod_name} | Instant Download Printable
- **Pin Leírás:** Transform your daily routine with this beautiful {prod_name}. Perfect for quiet morning time, prayer journaling, and spiritual encouragement. Download instantly and print at home! #christianliving #printableart #biblejournaling #faithbased #dailydevotional
- **Canva Sablon:** 1000x1500 px, lágy zsályazöld háttér, elegáns mockup képkeretben.
- **Cél URL:** Közvetlen Etsy / Gumroad terméklink.

#### 2. Pin: Probléma-Megoldó Fókusz (How-To / Stress Relief)
- **Cél Keresőszó:** `anxiety relief scripture journal`
- **Pin Cím:** Find Peace in 10 Minutes a Day | Guided Devotional
- **Pin Leírás:** Overwhelmed by daily stress? Discover peaceful reflections and literal KJV scriptures to calm your mind and renew your spirit. #stressrelief #christianmentalhealth #peaceofmind #prayerlife #scriptureoftheday
- **Canva Sablon:** 2:3 vertikális, fehér-fa textúra háttér, jól olvasható fekete felirat.
"""

                st.session_state["ffc_pinterest_data"] = resp_pin
                auto_save_current_project()
                st.success("✅ Pinterest SEO Pin készlet sikeresen legenerálva!")

        pin_data = st.session_state.get("ffc_pinterest_data", "")
        if pin_data:
            st.markdown("---")
            st.markdown(pin_data)
            st.download_button(
                "📥 Pinterest SEO Csomag Letöltése (.txt)",
                data=pin_data,
                file_name="Pinterest_Visual_SEO_Pins.txt",
                mime="text/plain",
                use_container_width=True
            )

