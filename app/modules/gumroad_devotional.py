"""
Workspace 6: 30-Day Christian Devotional & Gumroad Sales Copy Studio
===================================================================
Features:
- 30-Day Devotional Generator (KJV Scripture + Hungarian Verse, 200-word deep reflection, Daily Prayer, 3 Journaling Questions)
- High-Conversion Gumroad Sales Letter & Value Stack Copywriter
- 1-Click Gumroad API v2 Direct Publishing Integration
- Direct export to Google Drive (.docx Word & .txt format)
"""

import os
import json
import streamlit as st
from typing import Dict, Any, List

try:
    from core.key_manager import get_key_manager
    from core.drive_sync import (
        save_prompts_file_to_drive,
        create_marketing_docx,
        publish_to_gumroad,
        resolve_drive_folder
    )
    from core.project_manager import auto_save_current_project
except (ModuleNotFoundError, ImportError):
    from app.core.key_manager import get_key_manager
    from app.core.drive_sync import (
        save_prompts_file_to_drive,
        create_marketing_docx,
        publish_to_gumroad,
        resolve_drive_folder
    )
    from app.core.project_manager import auto_save_current_project



def render_gumroad_devotional_module():
    st.markdown("<div class='path-badge'>✍️ 6. 30 Napos Keresztény Áhítat & Gumroad Értékesítési Szövegíró</div>", unsafe_allow_html=True)

    km = get_key_manager()

    tab_devotional, tab_gumroad_copy, tab_publish = st.tabs([
        "🕊️ 1. Napi Áhítat & Vezetett Napló Író",
        "📜 2. Gumroad Értékesítési Szöveg (Sales Letter)",
        "🚀 3. Gumroad API v2 1-Kattintásos Publikálás"
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1: NAPI ÁHÍTAT & NAPLÓ
    # ─────────────────────────────────────────────────────────
    with tab_devotional:
        st.markdown("#### 🕊️ 30 Napos Keresztény Áhítat & Vezetett Lelki Napló")

        c_d1, c_d2 = st.columns([1.2, 1.0])
        with c_d1:
            dev_title = st.text_input(
                "Áhítatos Kötet Címe:",
                value=st.session_state.get("gumroad_product_name", "30 Napos Békesség a Viharban Áhítat"),
                key="dev_in_title"
            )
            st.session_state["gumroad_product_name"] = dev_title

            day_number = st.slider("Nap Száma:", min_value=1, max_value=30, value=st.session_state.get("gumroad_devotional_day", 1), key="dev_in_day")
            st.session_state["gumroad_devotional_day"] = day_number

            dev_theme = st.text_input("Napi Fókusz / Téma:", value="Isten Békessége a Szorongás Helyett (Filippi 4:6-7)", key="dev_in_theme")

            # NotebookLM Matrix Row Input (Optional RAG Enhancement)
            saved_matrix = st.session_state.get("rag_devotional_matrix", "")
            matrix_row_input = st.text_area(
                "📓 NotebookLM Teológiai Mátrix Sor (opcionális RAG forrás):",
                value=st.session_state.get("dev_matrix_row", f"[Nap {day_number} | Philippians 4:6-7 | Isten békessége a szorongás helyett | 1. Mi aggaszt? 2. Hogyan adod át? 3. Miért vagy hálás?]") if not saved_matrix else saved_matrix.split("\n")[0],
                height=70,
                key="dev_in_matrix_row"
            )

        with c_d2:
            st.markdown("""
            <div class='metric-card'>
                <strong style='color:#34d399;'>📖 KJV + Magyar Ige:</strong> Pontos bibliai alap<br>
                <strong style='color:#38bdf8;'>🕊️ 200 Szavas Reflexió:</strong> Mesterséges kliséktől mentes, meleg lelkigondozói hangvétel<br>
                <strong style='color:#f59e0b;'>✍️ 3 Naplókérdés:</strong> Mély önreflexió és csendesség<br>
                <strong style='color:#a855f7;'>🎙️ Audio Companion:</strong> $29 ➔ $39 upsell MP3 podcast bónusz
            </div>
            """, unsafe_allow_html=True)

        if st.button(f"✨ {day_number}. Napi Áhítat Generálása (Gemini Advanced Master Prompt / AI)", use_container_width=True, type="primary"):
            with st.spinner(f"AI írja a(z) {day_number}. napi áhítatot a Master Prompt alapján..."):
                prompt = f"""Szeretnék egy mély, hiteles és lelkileg építő 30 napos keresztény áhítat naplót (devotional) írni nőknek '{dev_title}' címmel.
Az alábbiakban megadom a NotebookLM által teológiailag ellenőrzött vázlatot a(z) {day_number}. naphoz:
{matrix_row_input or dev_theme}

Kérlek, írd meg a nap teljes tartalmát. Tartalmazzon:
1. 📖 A megadott KJV bibliai ige szó szerint és pontos magyar fordítása
2. 🕊️ Egy 200 szavas bátorító magyarázó-elmélkedő szöveg (csendes reflexió)
3. 🙏 Egy bensőséges, tiszteletteljes napi ima
4. ✍️ 3 db mély, elgondolkodtató önreflektív kérdés vezetett naplózáshoz

Stílusutasítás: Kerüld a tipikus, mesterkélt AI-fordulatokat és a túl száraz megfogalmazást. Írj meleg, mélyen bátorító, spirituális, tiszteletteljes és emberi tónusban."""

                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction="Te egy melegszívű, tapasztalt lelkipásztor és lelkigondozó író vagy. Kerüld az elcsépelt kliséket.",
                    model_name="groq-llama-3.3-70b"
                )
                if not ok or not resp:
                    resp = (
                        f"### {day_number}. Nap: {dev_theme}\n\n"
                        "**📖 Napi Ige:**\n"
                        "*'Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto God.' - Philippians 4:6*\n"
                        "*(Semmi felől ne aggódjatok, hanem imádságotokban és könyörgéstekben minden alkalommal hálaadással tárjátok fel kívánságaitokat az Úr előtt.)*\n\n"
                        "**🕊️ Csendes Reflexió:**\n"
                        "A modern világban a szorongás és a túlterheltség szinte észrevétlenül válik mindennapi társunkká. Pál apostol azonban börtönből írva emlékeztet minket: a békesség nem a körülményeink hiátusából, hanem Isten jelenlétéből fakad. Amikor a gondjainkat nem magunkban forgatjuk, hanem hálaadással letesszük az Úr elé, a Krisztus békessége őrzi meg szívünket és gondolatainkat.\n\n"
                        "**🙏 Napi Imádság:**\n"
                        "Uram, köszönöm, hogy Te nagyobb vagy minden félelmemnél és aggodalmamban is velem vagy. Segíts ma letenni eléd a nehézségeket, és elfogadni a Te megnyugtató békességedet. Ámen.\n\n"
                        "**✍️ Vezetett Naplókérdések:**\n"
                        "1. Mi az a konkrét aggodalom, amit ma teljes szívvel át kell adnom Istennek?\n"
                        "2. Milyen 3 dologért lehetek ma őszintén hálás a nehézségek ellenére is?\n"
                        "3. Hogyan tudom ma emlékeztetni magam Isten hűségére a rohanó pillanatokban?"
                    )

                st.session_state["gumroad_devotional_text"] = resp
                auto_save_current_project()
                st.success("✅ Napi áhítat sikeresen elkészült!")

        dev_text = st.session_state.get("gumroad_devotional_text", "")
        if dev_text:
            st.markdown("---")
            st.markdown(f"##### 📄 {day_number}. Nap Kézirata")
            st.markdown(dev_text)

            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                st.download_button(
                    "📥 Áhítat Letöltése (.txt)",
                    data=dev_text,
                    file_name=f"Devotional_Day_{day_number:02d}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with c_btn2:
                docx_bio = create_marketing_docx(f"{dev_title} - Day {day_number}", dev_text, "Napi Áhítat & Napló")
                st.download_button(
                    "📄 Word (.docx) Letöltése",
                    data=docx_bio.getvalue(),
                    file_name=f"Devotional_Day_{day_number:02d}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

    # ─────────────────────────────────────────────────────────
    # TAB 2: GUMROAD SALES LETTER & VALUE STACK
    # ─────────────────────────────────────────────────────────
    with tab_gumroad_copy:
        st.markdown("#### 📜 Magas Konverziójú Gumroad Értékesítési Szöveg & Audio Upsell ($39)")

        include_audio_upsell = st.checkbox("🎙️ NotebookLM Audio Companion Podcast bónusz beépítése (Áremelés: $29 ➔ $39)", value=True)

        if st.button("🚀 Gumroad Értékesítési Szöveg & Value Stack Generálása", use_container_width=True, type="primary"):
            with st.spinner("AI írja az ellenállhatatlan Russell Brunson stílusú értékesítési szöveget..."):
                audio_extra = "Tartalmazza az exkluzív NotebookLM Deep Dive Audio Companion (15 perces MP3 podcast) bónuszt, ami indokolja a $39 prémium árat." if include_audio_upsell else "Alap digitális PDF árazás: $29."
                prompt = f"""Írj egy magas konverziójú Gumroad termékleírást és értékesítési szöveget ehhez a termékhez:
Termék: "{dev_title}"
Téma: Keresztény áhítatos napló és digitális PDF + MP3 csomag
{audio_extra}

Tartalmazza:
- Erős figyelemfelkeltő főcím
- A lelki szomjúság, szorongás és túlterheltség megértő feltárása
- Mit tartalmaz a digitális csomag (Bullet pontok)
- Russell Brunson Value Stack (Főkönyv $47 értékben + Bónusz Audio Companion $19 értékben + Imakártyák $15 értékben)
- Teljes csomag ára: $39 (Több mint 65% kedvezmény a $81-os összértékből)
- Google Drive azonnali hozzáférési útmutató
- Kockázatmentes 30 napos garancia
"""
                ok, resp_copy = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction="Te egy elit közvetlen válaszmarketing szövegíró vagy.",
                    model_name="groq-llama-3.3-70b"
                )
                if not ok or not resp_copy:
                    resp_copy = km.generate_offline_content("sales letter")

                st.session_state["gumroad_sales_letter"] = resp_copy
                auto_save_current_project()
                st.success("✅ Gumroad értékesítési levél elkészült!")

        sales_copy = st.session_state.get("gumroad_sales_letter", "")
        if sales_copy:
            st.markdown("---")
            st.text_area("Értékesítési Szöveg (HTML / Markdown kompatibilis):", value=sales_copy, height=350, key="gumroad_sales_view")

            if st.button("💾 Mentés Google Drive-ra (.docx és .txt)", use_container_width=True):
                save_prompts_file_to_drive("gumroad", dev_title, sales_copy, f"Gumroad Copy: {dev_title}")
                st.success("📁 Mentve a Google Drive 05_📖_GUMROAD_PLR mappájába!")

    # ─────────────────────────────────────────────────────────
    # TAB 3: GUMROAD API V2 PUBLISHING
    # ─────────────────────────────────────────────────────────
    with tab_publish:
        st.markdown("#### 🚀 1-Kattintásos Termékpublikálás Gumroadra (API v2)")
        st.caption("A termék azonnal megjelenik a Gumroad fiókodban a beállított árral és leírással.")

        c_pub1, c_pub2 = st.columns(2)
        with c_pub1:
            p_name = st.text_input("Termék Neve a Gumroadon:", value=dev_title, key="gum_pub_name")
            p_price = st.number_input("Ár USD-ben ($):", min_value=0.0, max_value=999.0, value=9.99, step=1.0, key="gum_pub_price")
        with c_pub2:
            p_drive_link = st.text_input("Google Drive Kézbesítési Link (Vásárlói nyugtához):", placeholder="https://drive.google.com/drive/folders/...", key="gum_pub_drive")
            p_token = st.text_input("Gumroad Access Token (ha nincs mentve a beállításokban):", type="password", key="gum_pub_tok")

        if st.button("🚀 Termék Publikálása Gumroadra Most", use_container_width=True, type="primary"):
            with st.spinner("Kapcsolódás a Gumroad API v2 szerverhez..."):
                desc_to_use = st.session_state.get("gumroad_sales_letter", f"Digital Christian Devotional Pack: {dev_title}")
                ok_pub, pub_url, raw_res = publish_to_gumroad(
                    product_name=p_name,
                    price_usd=p_price,
                    description=desc_to_use,
                    drive_delivery_url=p_drive_link,
                    access_token=p_token or None
                )
                if ok_pub:
                    st.success(f"🎉 Termék sikeresen publikálva! Élő link: {pub_url}")
                    st.markdown(f"👉 **[Kattints ide a Gumroad termék megnyitásához]({pub_url})**")
                else:
                    st.error(pub_url)
