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
- 100% Bilingual (HU / EN).
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
    is_hu = st.session_state.get("app_global_lang", "HU") == "HU"

    st.markdown(f"<div class='path-badge'>🚀 {'3. FFC Marketing, Russell Brunson Copywriting & Google Sites Vázlat' if is_hu else '3. FFC Marketing, Russell Brunson Copywriting & Funnels'}</div>", unsafe_allow_html=True)

    km = get_key_manager()

    c_m1, c_m2 = st.columns([1.5, 1.0])
    with c_m1:
        prod_name = st.text_input(
            "Termék Neve:" if is_hu else "Product Name:",
            value=st.session_state.get("ffc_product_name", "30 Napos Keresztény Áhítat & Békesség Napló" if is_hu else "30-Day Christian Devotional & Prayer Journal"),
            key="ffc_in_prod"
        )
        st.session_state["ffc_product_name"] = prod_name

        niche_opts = [
            "✝️ Keresztény Családok & Édesanyák (Lelki csendesség)" if is_hu else "✝️ Christian Families & Mothers (Spiritual quietness)",
            "⚡ Túlterhelt Vállalkozók & ADHD-s Alkotók (Produktivitás)" if is_hu else "⚡ Busy Entrepreneurs & AuDHD Creators (Productivity)",
            "💼 Digitális Termék Készítők & Passzív Jövedelem" if is_hu else "💼 Digital Product Creators (Passive income)",
            "🧘 Mentális Egészség & Stresszoldás" if is_hu else "🧘 Mental Health & Stress Relief"
        ]
        niche_ctx = st.selectbox("Célpiac / Niche:" if is_hu else "Target Niche / Audience:", niche_opts, key="ffc_in_niche")

    with c_m2:
        st.markdown(f"""
        <div class='metric-card'>
            <strong style='color:#34d399;'>🎯 {'Stratégia' if is_hu else 'Strategy'}:</strong> Russell Brunson Funnel Freedom (FFC)<br>
            <strong style='color:#38bdf8;'>📜 Copywriting:</strong> {'12-lépéses Sales Letter + Value Stack' if is_hu else '12-Step Sales Letter + Value Stack'}<br>
            <strong style='color:#f59e0b;'>🌐 {'Ingyenes Oldal' if is_hu else 'Landing Page'}:</strong> Google Sites
        </div>
        """, unsafe_allow_html=True)

    tab_avatar, tab_sales, tab_gsites, tab_emails, tab_social, tab_pinterest = st.tabs([
        "🧠 1. Avatár Kutatás & Big Domino" if is_hu else "🧠 1. Avatar & Big Domino",
        "📜 2. Sales Letter & Value Stack" if is_hu else "📜 2. Sales Letter & Value Stack",
        "🌐 3. Google Sites Landing Page" if is_hu else "🌐 3. Google Sites Landing Page",
        "📧 4. E-mail Tölcsér" if is_hu else "📧 4. Automated Email Funnel",
        "📌 5. Social Media Naptár" if is_hu else "📌 5. 30-Day Social Calendar",
        "📌 6. Pinterest Vizuális SEO" if is_hu else "📌 6. Pinterest Passive SEO"
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1: AVATÁR KUTATÁS & BIG DOMINO
    # ─────────────────────────────────────────────────────────
    with tab_avatar:
        st.markdown(f"#### 🧠 {'8-Lépéses Pszichológiai Avatár Kutatás & Big Domino' if is_hu else '8-Step Psychological Avatar Research & Big Domino Hook'}")

        btn_av_lbl = "🚀 Avatár Elemzés & 10 Főcím Generálása" if is_hu else "🚀 Generate Avatar Research & 10 Golden Headlines"
        if st.button(btn_av_lbl, use_container_width=True, type="primary"):
            with st.spinner("AI végzi a mély pszichológiai kutatást..." if is_hu else "AI conducting psychographic analysis..."):
                prompt = (
                    build_ffc_avatar_research_prompt(prod_name, niche_ctx) + "\n\n" +
                    build_ffc_big_domino_hooks_prompt(prod_name, niche_ctx)
                )
                lang_sys = "Kizárólag magyar nyelven válaszolj." if is_hu else "Respond strictly in English."
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction=f"Te egy mester direkt marketing stratéga és copywriter vagy. {lang_sys}",
                    model_name="groq-llama-3.3-70b"
                )
                if not ok or not resp:
                    if is_hu:
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
                    else:
                        resp = (
                            "### 1. Customer Avatar Psychographic Profile\n"
                            "• **Core Identity:** Busy Christian mothers and creators seeking daily peace.\n"
                            "• **Surface Pain:** No time for multi-hour Bible studies.\n"
                            "• **Deep Root Fear:** Feeling spiritually depleted and guilty about inconsistency.\n\n"
                            "### 2. The Big Domino Shift\n"
                            "If they believe that **just 10 minutes of structured daily guided reflection** is enough to feel God's peace, they will buy instantly.\n\n"
                            "### 3. 10 Russell Brunson Golden Headlines\n"
                            "1. At Last: How to Find Daily Biblical Peace in Just 10 Minutes a Day!\n"
                            "2. The Simple Morning Routine That Eliminates Spiritual Guilt and Restores Peace.\n"
                            "3. Warning: Don't Start Another Stressful Morning Without This 10-Minute Sanctuary."
                        )

                st.session_state["ffc_avatar_data"] = resp
                st.success("✅ " + ("Avatár kutatás elkészült!" if is_hu else "Avatar research completed!"))

        av_data = st.session_state.get("ffc_avatar_data", "")
        if av_data:
            st.markdown("---")
            st.markdown(av_data)

    # ─────────────────────────────────────────────────────────
    # TAB 2: SALES LETTER & VALUE STACK
    # ─────────────────────────────────────────────────────────
    with tab_sales:
        st.markdown(f"#### 📜 {'12-Lépéses Russell Brunson Sales Letter & Value Stack' if is_hu else '12-Step Direct Response Sales Letter & Value Stack'}")

        btn_sl_lbl = "🚀 Teljes Értékesítési Levél Generálása" if is_hu else "🚀 Generate 12-Step Sales Letter"
        if st.button(btn_sl_lbl, use_container_width=True, type="primary"):
            with st.spinner("Értékesítési levél megírása folyamatban..." if is_hu else "Writing direct response sales letter..."):
                prompt = (
                    build_ffc_sales_letter_prompt(prod_name, niche_ctx) + "\n\n" +
                    build_ffc_value_stack_prompt(prod_name, niche_ctx)
                )
                lang_sys = "Kizárólag magyar nyelven válaszolj." if is_hu else "Respond strictly in English."
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction=f"Te egy Russell Brunson által képzett értékesítési szövegíró vagy. {lang_sys}",
                    model_name="groq-llama-3.3-70b"
                )
                st.session_state["ffc_sales_letter_data"] = resp
                st.success("✅ " + ("Értékesítési levél sikeresen legenerálva!" if is_hu else "Sales letter generated successfully!"))

        sl_data = st.session_state.get("ffc_sales_letter_data", "")
        if sl_data:
            st.markdown("---")
            st.text_area("Értékesítési Levél Szövege:" if is_hu else "Sales Letter Copy:", value=sl_data, height=350, key="ffc_sl_view")
            st.download_button(
                "📥 " + ("Sales Letter Letöltése (.txt)" if is_hu else "Download Sales Letter (.txt)"),
                data=sl_data,
                file_name="Sales_Letter.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ─────────────────────────────────────────────────────────
    # TAB 3: GOOGLE SITES 0 FT-OS LANDING PAGE
    # ─────────────────────────────────────────────────────────
    with tab_gsites:
        st.markdown(f"#### 🌐 {'Google Sites 0 Ft-os Landing Page Vázlat' if is_hu else 'Google Sites 0 HUF Landing Page Wireframe'}")
        st.caption("Azonnal bemásolható blokkok a teljesen ingyenes Google Sites weboldalkészítőhöz." if is_hu else "Ready-to-paste sections for free Google Sites.")

        btn_gs_lbl = "🚀 Google Sites Szövegek & CTA Blokkok Generálása" if is_hu else "🚀 Generate Landing Page Sections & CTAs"
        if st.button(btn_gs_lbl, use_container_width=True, type="primary"):
            with st.spinner("Oldalszövegek generálása..." if is_hu else "Generating landing page copy..."):
                prompt = build_google_sites_landing_page_prompt(prod_name, niche_ctx)
                lang_sys = "Kizárólag magyar nyelven válaszolj." if is_hu else "Respond strictly in English."
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction=f"Te egy magas konverziójú landing page tervező vagy. {lang_sys}",
                    model_name="groq-llama-3.3-70b"
                )
                st.session_state["ffc_google_sites_data"] = resp
                st.success("✅ " + ("Google Sites vázlat elkészült!" if is_hu else "Landing page copy ready!"))

        gs_data = st.session_state.get("ffc_google_sites_data", "")
        if gs_data:
            st.markdown("---")
            st.markdown(gs_data)
            st.download_button(
                "📥 " + ("Google Sites Vázlat Letöltése" if is_hu else "Download Wireframe (.txt)"),
                data=gs_data,
                file_name="Google_Sites_Copy.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ─────────────────────────────────────────────────────────
    # TAB 4: AUTOMATA E-MAIL TÖLCSÉR
    # ─────────────────────────────────────────────────────────
    with tab_emails:
        st.markdown(f"#### 📧 {'Automata E-mail Tölcsér (3-Day & 30-Day Funnel)' if is_hu else 'Automated Email Funnel (3-Day Welcome & 30-Day Broadcasts)'}")

        btn_em_lbl = "🚀 E-mail Sorozat Generálása" if is_hu else "🚀 Generate Automated Email Sequence"
        if st.button(btn_em_lbl, use_container_width=True, type="primary"):
            with st.spinner("AI írja az e-maileket..." if is_hu else "AI generating email sequence..."):
                prompt = (
                    build_email_funnel_3day_prompt(prod_name, niche_ctx) + "\n\n" +
                    build_email_funnel_30day_prompt(prod_name, niche_ctx)
                )
                lang_sys = "Kizárólag magyar nyelven válaszolj." if is_hu else "Respond strictly in English."
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction=f"Te egy automata e-mail marketing szakértő vagy. {lang_sys}",
                    model_name="groq-llama-3.3-70b"
                )
                st.session_state["ffc_emails_data"] = resp
                st.success("✅ " + ("E-mail sorozat sikeresen elkészült!" if is_hu else "Email sequence generated successfully!"))

        em_data = st.session_state.get("ffc_emails_data", "")
        if em_data:
            st.markdown("---")
            st.text_area("E-mail Szekvencia:" if is_hu else "Email Sequence:", value=em_data, height=350, key="ffc_em_view")
            st.download_button(
                "📥 " + ("E-mailek Letöltése (.txt)" if is_hu else "Download Emails (.txt)"),
                data=em_data,
                file_name="Email_Sequence.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ─────────────────────────────────────────────────────────
    # TAB 5: 30 NAPOS SOCIAL MEDIA NAPTÁR
    # ─────────────────────────────────────────────────────────
    with tab_social:
        st.markdown(f"#### 📌 {'30 Napos Multi-Platform Közösségi Média Naptár' if is_hu else '30-Day Multi-Platform Social Media Calendar'}")
        st.caption("Pinterest Pins, Instagram Reels és TikTok horgok 4 hétre elosztva." if is_hu else "Pinterest Pins, IG Reels and TikTok hooks.")

        btn_soc_lbl = "🚀 30 Napos Közösségi Média Naptár Generálása" if is_hu else "🚀 Generate 30-Day Social Calendar"
        if st.button(btn_soc_lbl, use_container_width=True, type="primary"):
            with st.spinner("Social media naptár összeállítása..." if is_hu else "Generating social calendar..."):
                prompt = build_social_seo_calendar_30day_prompt(prod_name, niche_ctx)
                lang_sys = "Kizárólag magyar nyelven válaszolj." if is_hu else "Respond strictly in English."
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction=f"Te egy organikus növekedési szakértő vagy. {lang_sys}",
                    model_name="groq-llama-3.3-70b"
                )
                st.session_state["ffc_social_data"] = resp
                st.success("✅ " + ("Social media naptár elkészült!" if is_hu else "Social calendar ready!"))

        soc_data = st.session_state.get("ffc_social_data", "")
        if soc_data:
            st.markdown("---")
            st.markdown(soc_data)
            st.download_button(
                "📥 " + ("Social Naptár Letöltése" if is_hu else "Download Calendar (.txt)"),
                data=soc_data,
                file_name="Social_Media_Calendar_30Days.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ─────────────────────────────────────────────────────────
    # TAB 6: PINTEREST PASSZÍV VIZUÁLIS SEO
    # ─────────────────────────────────────────────────────────
    with tab_pinterest:
        st.markdown(f"#### 📌 {'Pinterest Visual Search Engine & Passzív SEO Generátor' if is_hu else 'Pinterest Visual Search Engine & Passive SEO'}")
        st.caption("A Pinterest egy vizuális keresőmotor. Egy optimalizált Pin hónapokig vagy évekig passzív vásárlói forgalmat terel." if is_hu else "Pins drive long-tail organic visual search traffic for months and years.")

        c_pin1, c_pin2 = st.columns([1.2, 1.0])
        with c_pin1:
            pin_opts = [
                "Etsy Keresztény Igés Falikép (Printable Wall Art)" if is_hu else "Etsy Scripture Wall Art Printable",
                "Amazon KDP Gyermek Bibliai Színezőkönyv" if is_hu else "Amazon KDP Children Bible Coloring Book",
                "Gumroad 30 Napos Keresztény Áhítat & Audio Companion" if is_hu else "Gumroad 30-Day Devotional & Audio Podcast",
                "Etsy Clipart & Matrica Csomag" if is_hu else "Etsy Clipart & Sticker Bundle"
            ]
            pin_type = st.selectbox("Cél Terméktípus:" if is_hu else "Target Product Type:", pin_opts, key="pin_in_type")
        with c_pin2:
            st.markdown(f"""
            <div class='metric-card'>
                <strong style='color:#38bdf8;'>🎯 {'Vizuális SEO Előny' if is_hu else 'Visual SEO Advantage'}:</strong> {'Zéró posztolási kényszer, 0 kommentkezelés.' if is_hu else 'Zero DM management, passive visual search.'}<br>
                <strong style='color:#34d399;'>🎨 {'Méretarány' if is_hu else 'Ratio'}:</strong> 2:3 (1000x1500 px) Canva.<br>
                <strong style='color:#f59e0b;'>🔗 {'Közvetlen Link' if is_hu else 'Direct Link'}:</strong> {'Terelés közvetlenül a termékoldalra.' if is_hu else 'Direct traffic to product page.'}
            </div>
            """, unsafe_allow_html=True)

        btn_pin_lbl = "🚀 5 db Pinterest Passzív SEO Pin Generálása" if is_hu else "🚀 Generate 5 Passive Pinterest SEO Pins"
        if st.button(btn_pin_lbl, use_container_width=True, type="primary"):
            with st.spinner("AI generálja a Pinterest kulcsszavas leírásokat..." if is_hu else "Generating SEO Pins..."):
                prompt = build_pinterest_pin_seo_prompt(prod_name, niche_ctx, pin_type)
                lang_sys = "Kizárólag magyar nyelven válaszolj." if is_hu else "Respond strictly in English."
                ok, resp_pin = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction=f"Te egy profi Pinterest SEO stratéga vagy. {lang_sys}",
                    model_name="groq-llama-3.3-70b"
                )
                st.session_state["ffc_pinterest_data"] = resp_pin
                st.success("✅ " + ("Pinterest SEO Pin készlet sikeresen legenerálva!" if is_hu else "Pinterest SEO Pins generated!"))

        pin_data = st.session_state.get("ffc_pinterest_data", "")
        if pin_data:
            st.markdown("---")
            st.markdown(pin_data)
            st.download_button(
                "📥 " + ("Pinterest SEO Csomag Letöltése (.txt)" if is_hu else "Download Pinterest Pins (.txt)"),
                data=pin_data,
                file_name="Pinterest_Visual_SEO_Pins.txt",
                mime="text/plain",
                use_container_width=True
            )
