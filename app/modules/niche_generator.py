"""
Workspace 4: 30 Niche Idea Workshop & Bulk Etsy CSV Exporter
===========================================================
Features:
- 30 marketable niche idea generator across 22 high-demand categories (7 supergroups)
- Bulk prompt package exporter (.txt to Drive / local download)
- Strict Etsy CSV Exporter with FFC description, 13 tags, and instant download instructions
"""

import os
import streamlit as st
from typing import Dict, Any, List

try:
    from core.key_manager import get_key_manager
    from core.prompts_bank import NICHE_CATEGORIES, get_niche_prompt_context
    from core.drive_sync import save_prompts_file_to_drive, generate_etsy_csv, resolve_drive_folder
    from core.project_manager import auto_save_current_project
except (ModuleNotFoundError, ImportError):
    from app.core.key_manager import get_key_manager
    from app.core.prompts_bank import NICHE_CATEGORIES, get_niche_prompt_context
    from app.core.drive_sync import save_prompts_file_to_drive, generate_etsy_csv, resolve_drive_folder
    from app.core.project_manager import auto_save_current_project



def render_niche_generator_module():
    st.markdown("<div class='path-badge'>💡 4. 30 Niche Ötletműhely & Etsy CSV Exportőr</div>", unsafe_allow_html=True)

    km = get_key_manager()

    col_n1, col_n2 = st.columns([1.5, 1.0])
    with col_n1:
        niche_list = list(NICHE_CATEGORIES.keys())
        selected_niche = st.selectbox(
            "Válassz Piaci Kategóriát (22 Piac / 5 Szupercsoport):",
            options=niche_list,
            index=0,
            key="niche_gen_select"
        )
        st.session_state["selected_niche"] = selected_niche
        niche_info = get_niche_prompt_context(selected_niche)

        custom_angle = st.text_input(
            "Egyedi Fókusz / Téma szűkítés (opcionális):",
            value=st.session_state.get("custom_topic_prompt", ""),
            placeholder="pl. Kezdő édesanyák csendessége / Zsoltárok békessége",
            key="input_custom_angle"
        )
        st.session_state["custom_topic_prompt"] = custom_angle

    with col_n2:
        st.markdown(f"""
        <div class='metric-card'>
            <strong style='color:#34d399;'>📂 Szupercsoport:</strong> {niche_info.get('group', 'General')}<br>
            <strong style='color:#38bdf8;'>🎯 Célközönség:</strong> {niche_info.get('default_audience', '')[:65]}...<br>
            <strong style='color:#f59e0b;'>🏷️ Kulcsszavak:</strong> {', '.join(niche_info.get('keywords', [])[:4])}
        </div>
        """, unsafe_allow_html=True)

    if st.button("🚀 30 Piacképes Téma & Termékötlet Generálása", use_container_width=True, type="primary"):
        with st.spinner("AI kutatja a 30 legkeresettebb réspiaci témát és kulcsszót..."):
            prompt = (
                f"Generate exactly 30 profitable digital product ideas and themes for the niche: '{selected_niche}' "
                f"({niche_info.get('name_en', '')}). Angle: {custom_angle or 'Evergreen high-demand'}. "
                f"Include Title in English and Hungarian, Scripture reference / core theme, and a 1-sentence image concept for each item. "
                f"Number them clearly from 1 to 30."
            )
            ok, resp_text = km.generate_text_with_fallback(
                prompt=prompt,
                system_instruction="Te egy elit Etsy és KDP piaci kutató vagy. Részletes, számozott 30-as listát adj.",
                model_name="groq-llama-3.3-70b"
            )
            if not ok or not resp_text:
                resp_text = km.generate_offline_content("30 topic ideas")

            st.session_state["niche_ideas_list"] = resp_text
            auto_save_current_project()
            st.success("✅ 30 témaötlet sikeresen elkészült!")

    # ── Eredmények és Export ──
    ideas_text = st.session_state.get("niche_ideas_list", "")
    if ideas_text:
        st.markdown("---")
        st.markdown("##### 📋 Generált 30 Piaci Téma")
        st.text_area("Ötletek listája:", value=ideas_text, height=350, key="ideas_display_area")

        c_exp1, c_exp2 = st.columns(2)
        with c_exp1:
            st.download_button(
                "📥 30 Téma Letöltése (.txt)",
                data=ideas_text,
                file_name=f"30_Themes_{selected_niche[:15]}.txt",
                mime="text/plain",
                use_container_width=True
            )

        with c_exp2:
            if st.button("💾 Mentés Google Drive-ra", use_container_width=True):
                ok_d, d_path = save_prompts_file_to_drive(
                    "kdp",
                    f"30_Themes_{selected_niche[:15]}",
                    ideas_text,
                    f"30 Niche Ötlet: {selected_niche}"
                )
                if ok_d:
                    st.success(f"📁 Mentve: {d_path}")
                else:
                    st.error(f"Hiba: {d_path}")

        # ── Gyors Etsy CSV Konvertáló ──
        st.markdown("---")
        st.markdown("##### 🛍️ Gyors Etsy CSV Exportőr (30 Tétel alapján)")
        st.caption("A fenti 30 témából automatikusan létrehoz egy hivatalos Etsy Listing CSV fájlt.")

        c_csv1, c_csv2 = st.columns(2)
        with c_csv1:
            csv_price = st.text_input("Alapértelmezett Ár ($):", value="6.99", key="csv_def_price")
        with c_csv2:
            csv_sku_prefix = st.text_input("SKU Előtag:", value="CHRISTIAN-ART", key="csv_sku_pre")

        if st.button("📊 Etsy CSV Generálása és Letöltése", use_container_width=True):
            listings = []
            lines = [l.strip() for l in ideas_text.split("\n") if l.strip() and (l[0].isdigit() or l.startswith("-"))]
            for idx, line in enumerate(lines[:30], start=1):
                clean_title = line.lstrip("0123456789.-• ").split("|")[0].strip()
                listings.append({
                    "title": f"Christian Wall Art Printable {clean_title} Scripture Decor",
                    "tags": ["christian wall art", "bible verse print", "scripture poster", "faith gift", "printable art", "digital download"],
                    "description": f"Beautiful printable scripture artwork: {clean_title}. High resolution 300 DPI files included.",
                    "price": csv_price,
                    "sku": f"{csv_sku_prefix}-{idx:02d}",
                    "drive_url": "Google Drive Instant Download Link"
                })

            ok_c, msg_c, csv_bytes = generate_etsy_csv(listings)
            if ok_c:
                st.success(f"✅ {len(listings)} termék sikeresen összefűzve Etsy CSV formátumba!")
                st.download_button(
                    "📥 Hivatalos Etsy CSV Letöltése",
                    data=csv_bytes,
                    file_name="Etsy_Listings_30_Batch.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.error(f"Hiba: {msg_c}")
