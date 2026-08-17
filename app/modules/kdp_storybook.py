"""
Workspace 2: Amazon KDP Illustrated Storybook Studio
===================================================
Features:
- Complete chapter-based story generation (Hungarian narrative + English color illustration prompts)
- 1:1 native aspect ratio for 8.5x8.5 square books (also supporting other KDP trims)
- Manuscript editor interface with live image preview
- Embedded illustration ReportLab PDF export (Title page, Dedication, Chapter layout)
"""

import os
import json
import streamlit as st
from typing import Dict, Any, List
from PIL import Image
import io

try:
    from core.key_manager import get_key_manager
    from core.pdf_engine import build_illustrated_book_pdf
    from core.prompts_bank import (
        build_illustrated_book_manifest_prompt,
        parse_illustrated_book_manifest_json
    )
    from core.drive_sync import save_prompts_file_to_drive, resolve_drive_folder
    from core.project_manager import auto_save_current_project
except (ModuleNotFoundError, ImportError):
    from app.core.key_manager import get_key_manager
    from app.core.pdf_engine import build_illustrated_book_pdf
    from app.core.prompts_bank import (
        build_illustrated_book_manifest_prompt,
        parse_illustrated_book_manifest_json
    )
    from app.core.drive_sync import save_prompts_file_to_drive, resolve_drive_folder
    from app.core.project_manager import auto_save_current_project



def render_kdp_storybook_module():
    st.markdown("<div class='path-badge'>📖 2. Amazon KDP Illusztrált Mesekönyv Műhely</div>", unsafe_allow_html=True)

    km = get_key_manager()

    c_meta1, c_meta2 = st.columns(2)
    with c_meta1:
        sb_title = st.text_input(
            "Mesekönyv Címe:",
            value=st.session_state.get("sb_title", "Barnabás, a Bátor Bárány"),
            key="input_sb_title"
        )
        st.session_state["sb_title"] = sb_title

        sb_subtitle = st.text_input(
            "Alcím:",
            value=st.session_state.get("sb_subtitle", "Egy tanulságos bibliai mese a hitről és a barátságról"),
            key="input_sb_subtitle"
        )
        st.session_state["sb_subtitle"] = sb_subtitle

        sb_author = st.text_input(
            "Szerző / Illusztrátor Neve:",
            value=st.session_state.get("sb_author", "Keresztény Alkotó"),
            key="input_sb_author"
        )
        st.session_state["sb_author"] = sb_author

    with c_meta2:
        c_ch, c_trim = st.columns(2)
        with c_ch:
            chapter_count = st.slider("Fejezetek / Oldalak Száma:", min_value=4, max_value=16, value=st.session_state.get("sb_chapters_count", 6), step=1)
            st.session_state["sb_chapters_count"] = chapter_count
        with c_trim:
            sb_trim = st.selectbox("Formátum:", ["8.5x8.5 (Négyzet 1:1)", "8.5x11 (Álló 3:4)", "8x10 (4:5)", "6x9 (2:3)"], index=0)
            clean_trim = sb_trim.split()[0]
            st.session_state["sb_trim_size"] = clean_trim

        art_style = st.selectbox(
            "Illusztráció Művészeti Stílusa:",
            [
                "Disney Pixar 3D cuki animációs stílus, meleg fények",
                "Gyengéd akvarell és pasztell ceruzarajz, mesekönyv stílus",
                "Klasszikus vintage aranykönyv illusztráció",
                "Modern letisztult digitális vektorgrafika"
            ]
        )
        st.session_state["sb_art_style"] = art_style

    if st.button("✨ Mesekönyv Kézirat & Illusztrációs Promptok Generálása", use_container_width=True, type="primary"):
        with st.spinner("AI írja a fejezeteket és készíti a 1:1 illusztrációs promptokat..."):
            prompt = build_illustrated_book_manifest_prompt(
                book_title=sb_title,
                chapter_count=chapter_count,
                theme=st.session_state.get("selected_niche", "Biblical faith and love"),
                target_age="Ages 4-8",
                art_style=art_style
            )
            ok, resp_text = km.generate_text_with_fallback(
                prompt=prompt,
                system_instruction="Te egy díjnyertes keresztény gyermekkönyv író és illusztrátor vagy. Szigorú JSON listát adj.",
                model_name="groq-llama-3.3-70b"
            )
            chapters = parse_illustrated_book_manifest_json(resp_text)
            if not chapters:
                offline_raw = km.generate_offline_content(prompt)
                chapters = parse_illustrated_book_manifest_json(offline_raw)

            if chapters:
                st.session_state["sb_chapters_manifest"] = chapters[:chapter_count]
                st.session_state["sb_generated_images"] = {}
                auto_save_current_project()
                st.success(f"✅ Sikeresen elkészült {len(chapters)} fejezet kézirata!")
                st.rerun()
            else:
                st.error("Nem sikerült feldolgozni a mesekönyv fejezeteit.")

    # ── Fejezetek szerkesztése és képgenerálás ──
    chapters_data = st.session_state.get("sb_chapters_manifest", [])
    if chapters_data:
        st.markdown("---")
        st.markdown(f"##### 📖 Mesekönyv Fejezetei ({len(chapters_data)} oldal)")

        if "sb_generated_images" not in st.session_state:
            st.session_state["sb_generated_images"] = {}

        c_sb_b1, c_sb_b2 = st.columns(2)
        with c_sb_b1:
            if st.button("🎨 Összes Színes Illusztráció Generálása (1:1 FLUX)", use_container_width=True):
                p_bar = st.progress(0.0)
                st_msg = st.empty()
                for i, ch in enumerate(chapters_data, start=1):
                    st_msg.info(f"Illusztráció generálása {i}/{len(chapters_data)}...")
                    ok_img, img_list, _ = km.generate_image_with_fallback(
                        prompt=ch.get("illustration_prompt", ""),
                        aspect_ratio="1:1" if "8.5x8.5" in clean_trim else "3:4",
                        model_name="flux"
                    )
                    if ok_img and img_list:
                        st.session_state["sb_generated_images"][i] = img_list[0]
                    p_bar.progress(i / float(len(chapters_data)))
                st_msg.success("🎉 Minden illusztráció elkészült!")
                auto_save_current_project()
                st.rerun()

        with c_sb_b2:
            if st.button("💾 Kézirat Mentése Drive-ra (.txt)", use_container_width=True):
                text_content = f"Cím: {sb_title}\nAlcím: {sb_subtitle}\nSzerző: {sb_author}\n\n"
                for i, ch in enumerate(chapters_data, start=1):
                    text_content += f"=== {ch.get('chapter_title', f'Fejezet {i}')} ===\n{ch.get('story_text', '')}\n\nPrompt:\n{ch.get('illustration_prompt', '')}\n\n"
                ok_d, d_path = save_prompts_file_to_drive("kdp", sb_title, text_content, f"Mesekönyv Kézirat: {sb_title}")
                if ok_d:
                    st.success(f"📁 Kézirat mentve a Drive-ra: {d_path}")
                else:
                    st.error(f"Hiba: {d_path}")

        # Fejezetek kártyái
        for idx, ch in enumerate(chapters_data, start=1):
            with st.expander(f"📖 {idx}. Fejezet: {ch.get('chapter_title', f'Chapter {idx}')}", expanded=(idx == 1)):
                col_c1, col_c2 = st.columns([1.3, 1.0])
                with col_c1:
                    ch["chapter_title"] = st.text_input("Fejezet Címe:", value=ch.get("chapter_title", ""), key=f"sb_ch_title_{idx}")
                    ch["story_text"] = st.text_area("Mese Szövege:", value=ch.get("story_text", ""), height=100, key=f"sb_story_{idx}")
                    ch["illustration_prompt"] = st.text_area("1:1 Illusztrációs Prompt:", value=ch.get("illustration_prompt", ""), height=80, key=f"sb_pr_{idx}")

                    if st.button(f"🎨 Illusztráció Generálása (#{idx})", key=f"sb_gen_{idx}", use_container_width=True):
                        with st.spinner("Színes illusztráció generálása..."):
                            ok_img, img_list, err = km.generate_image_with_fallback(
                                prompt=ch["illustration_prompt"],
                                aspect_ratio="1:1" if "8.5x8.5" in clean_trim else "3:4",
                                model_name="flux"
                            )
                            if ok_img and img_list:
                                st.session_state["sb_generated_images"][idx] = img_list[0]
                                auto_save_current_project()
                                st.rerun()
                            else:
                                st.error(f"Hiba: {err}")

                with col_c2:
                    st.markdown("**Illusztráció Előnézet:**")
                    if idx in st.session_state.get("sb_generated_images", {}):
                        img_b = st.session_state["sb_generated_images"][idx]
                        st.image(img_b, use_container_width=True)
                        st.download_button(
                            "📥 Kép Letöltése (PNG)",
                            data=img_b,
                            file_name=f"Chapter_{idx:02d}.png",
                            mime="image/png",
                            key=f"sb_dl_{idx}",
                            use_container_width=True
                        )
                    else:
                        st.info("Még nincs legenerált illusztráció.")

        # ── Nyomdai PDF Összeállítása ──
        st.markdown("---")
        st.markdown("##### 🖨️ Illusztrált Mesekönyv Nyomdai PDF Export")

        if st.button("🚀 Nyomdakész Mesekönyv PDF Összeállítása", use_container_width=True, type="primary"):
            pages_data = []
            for i, ch in enumerate(chapters_data, start=1):
                ch_copy = dict(ch)
                if i in st.session_state.get("sb_generated_images", {}):
                    ch_copy["image_bytes"] = st.session_state["sb_generated_images"][i]
                pages_data.append(ch_copy)

            out_dir = resolve_drive_folder("kdp_interiors")
            out_filename = f"{sb_title.replace(' ', '_')}_{clean_trim}_Illustrated_Book.pdf"
            out_pdf_path = os.path.join(out_dir, out_filename)

            ok_pdf, pdf_bytes, msg = build_illustrated_book_pdf(
                title=sb_title,
                subtitle=sb_subtitle,
                pages_data=pages_data,
                author=sb_author,
                output_path=out_pdf_path,
                trim_size=clean_trim,
                margin_in=0.5,
                show_decorative_frame=True,
                show_image_border=True,
                show_page_numbers=True,
                show_chapter_header=True
            )

            if ok_pdf:
                st.success(f"🎉 {msg}")
                st.info(f"📁 Mentve a Drive-ra: {out_pdf_path}")
                st.download_button(
                    label="📥 Nyomdakész Mesekönyv PDF Letöltése",
                    data=pdf_bytes,
                    file_name=out_filename,
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.error(f"Hiba a PDF generálásakor: {msg}")
