"""
Workspace 1: Amazon KDP Coloring Book & Print-Ready PDF Studio
=============================================================
Features:
- Trim formats: 8.5x11 (3:4), 8.5x8.5 (1:1), 8x10 (4:5), 6x9 (2:3)
- Modes: Children (bold line art) vs Adult (intricate mandala/zentangle)
- Gemini Gem Master Instruction for character and style consistency
- 5-30 Page Numbered Manifest Generator (KJV Scripture, Palettes, English Prompts)
- ReportLab Print Engine Integration (Margins 0.25"-0.85", swatches, companion pages, bleed protection)
- Batch/Single image generation with Pollinations FLUX / Google Imagen
"""

import os
import json
import streamlit as st
from typing import Dict, Any, List
from PIL import Image
import io

try:
    from core.key_manager import get_key_manager
    from core.pdf_engine import build_kdp_book_pdf
    from core.prompts_bank import (
        build_kdp_gem_master_instruction,
        build_kdp_autopilot_manifest_prompt,
        parse_kdp_autopilot_manifest_json,
        get_model_profile
    )
    from core.drive_sync import save_prompts_file_to_drive, resolve_drive_folder
    from core.project_manager import auto_save_current_project
except (ModuleNotFoundError, ImportError):
    from app.core.key_manager import get_key_manager
    from app.core.pdf_engine import build_kdp_book_pdf
    from app.core.prompts_bank import (
        build_kdp_gem_master_instruction,
        build_kdp_autopilot_manifest_prompt,
        parse_kdp_autopilot_manifest_json,
        get_model_profile
    )
    from app.core.drive_sync import save_prompts_file_to_drive, resolve_drive_folder
    from app.core.project_manager import auto_save_current_project



def render_kdp_coloring_module():
    st.markdown("<div class='path-badge'>🎨 1. Amazon KDP Színező & Nyomdai PDF Összeállító</div>", unsafe_allow_html=True)

    km = get_key_manager()

    tab_autopilot, tab_gem_master, tab_single_prompt = st.tabs([
        "🚀 1. Könyv Vázlat & PDF Összeállító",
        "💎 2. Gemini Gem Mester Utasítás (Stílus & Karakter Állandóság)",
        "✨ 3. Egyedi Színező Prompt Tesztelő (1 Jelenet)"
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1: KÖNYV VÁZLAT & PDF ÖSSZEÁLLÍTÓ
    # ─────────────────────────────────────────────────────────
    with tab_autopilot:
        st.markdown("#### 📖 Teljes KDP Színezőkönyv Generálás & PDF Összefűzés")

        c_meta1, c_meta2 = st.columns(2)
        with c_meta1:
            book_title = st.text_input(
                "Könyv Főcíme (pl. Noah's Ark Adventures):",
                value=st.session_state.get("kdp_book_title", "Noah's Ark Bible Adventures"),
                key="input_kdp_title"
            )
            st.session_state["kdp_book_title"] = book_title

            book_subtitle = st.text_input(
                "Alcím (pl. Inspiring Scripture Coloring Book for Kids):",
                value=st.session_state.get("kdp_book_subtitle", "Inspiring Bible Verse Coloring Book for Children"),
                key="input_kdp_subtitle"
            )
            st.session_state["kdp_book_subtitle"] = book_subtitle

        with c_meta2:
            target_aud = st.selectbox(
                "Célközönség & Stílus Mód:",
                [
                    "👶 Gyermek (Vastag kontúrok, cuki formák, tiszta fehér háttér)",
                    "🧘 Felnőtt (Intrikát mandala, zentangle, részletgazdag vonalrajz)"
                ],
                key="input_kdp_aud"
            )
            is_adult = "Felnőtt" in target_aud
            st.session_state["kdp_style_mode"] = "adult" if is_adult else "child"

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                page_count = st.slider("Színező Oldalak Száma:", min_value=4, max_value=30, value=st.session_state.get("kdp_page_count", 6), step=1)
                st.session_state["kdp_page_count"] = page_count
            with col_p2:
                trim_size = st.selectbox(
                    "KDP Formátum (Trim Size):",
                    ["8.5x11", "8.5x8.5", "8x10", "6x9"],
                    index=0,
                    key="input_kdp_trim"
                )
                st.session_state["kdp_trim_size"] = trim_size

        # ── Nyomdai PDF Beállítások ──
        with st.expander("⚙️ Nyomdai PDF Beállítások (ReportLab Margók & Opciók)", expanded=False):
            c_pdf1, c_pdf2, c_pdf3 = st.columns(3)
            with c_pdf1:
                margin_in = st.slider("Biztonsági Margó (Hüvelyk):", min_value=0.25, max_value=0.85, value=0.50, step=0.05)
                show_frame = st.checkbox("Díszítő keret rajzolása", value=True)
            with c_pdf2:
                show_swatches = st.checkbox("1. Oldali színtesztelő formák", value=True)
                include_companion = st.checkbox("Bal oldali igés kísérő oldalak", value=True)
            with c_pdf3:
                include_bleed = st.checkbox("Filcátütés-gátló üres lapok", value=True)
                show_titles = st.checkbox("Fejléc jelenetcímek és lábléc", value=True)

        if st.button("✨ 1. Lépés: Könyv Vázlat & Promptok Generálása (AI / Offline)", use_container_width=True, type="primary"):
            with st.spinner("AI generálja a sorszámozott KDP könyvvázlatot és KJV igéket..."):
                prompt = build_kdp_autopilot_manifest_prompt(
                    book_title=book_title,
                    target_audience=target_aud,
                    page_count=page_count,
                    niche_context=st.session_state.get("selected_niche", "Christian Faith"),
                    is_adult=is_adult
                )
                ok, response_text = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction="Te egy KDP színezőkönyv tervező mester vagy. Szigorú JSON listát adj vissza.",
                    model_name="groq-llama-3.3-70b"
                )

                scenes = parse_kdp_autopilot_manifest_json(response_text)
                if not scenes:
                    offline_raw = km.generate_offline_content(prompt)
                    scenes = parse_kdp_autopilot_manifest_json(offline_raw)

                if scenes:
                    st.session_state["kdp_scenes_manifest"] = scenes[:page_count]
                    st.session_state["kdp_generated_images"] = {}
                    auto_save_current_project()
                    st.success(f"✅ Sikeresen legenerálva {len(st.session_state['kdp_scenes_manifest'])} jelenet vázlata!")
                    st.rerun()
                else:
                    st.error("Nem sikerült feldolgozni a jelenetek listáját.")

        # ── Jelenetek szerkesztése és képgenerálás ──
        manifest = st.session_state.get("kdp_scenes_manifest", [])
        if manifest:
            st.markdown("---")
            st.markdown(f"##### 📋 Könyv Oldalai ({len(manifest)} színező jelenet)")

            if "kdp_generated_images" not in st.session_state:
                st.session_state["kdp_generated_images"] = {}

            # Tömeges képgenerálás gomb
            c_batch1, c_batch2 = st.columns([1.5, 1.5])
            with c_batch1:
                if st.button("🎨 Összes Kép Generálása Egyszerre (Pollinations FLUX Ingyenes)", use_container_width=True):
                    progress_bar = st.progress(0.0)
                    status_text = st.empty()
                    for idx, scene in enumerate(manifest, start=1):
                        status_text.info(f"Kép {idx}/{len(manifest)} generálása: {scene.get('title', '')}...")
                        v_prompt = scene.get("visual_prompt", "")
                        ratio_str = "1:1" if "8.5x8.5" in trim_size else ("4:5" if "8x10" in trim_size else ("2:3" if "6x9" in trim_size else "3:4"))
                        ok_img, img_bytes_list, _ = km.generate_image_with_fallback(
                            prompt=v_prompt,
                            aspect_ratio=ratio_str,
                            model_name="flux"
                        )
                        if ok_img and img_bytes_list:
                            st.session_state["kdp_generated_images"][idx] = img_bytes_list[0]
                        progress_bar.progress(idx / float(len(manifest)))
                    status_text.success("🎉 Minden kép sikeresen legenerálva!")
                    auto_save_current_project()
                    st.rerun()

            with c_batch2:
                if st.button("💾 Promptok Mentése Drive-ra (.txt)", use_container_width=True):
                    all_prompts = "\n\n".join([f"Page {s.get('page_number', i)}: {s.get('title', '')}\nScripture: {s.get('scripture_reference', '')} - {s.get('scripture_text', '')}\nVisual Prompt:\n{s.get('visual_prompt', '')}" for i, s in enumerate(manifest, start=1)])
                    ok_d, d_path = save_prompts_file_to_drive("kdp", book_title, all_prompts, f"KDP Színező Vázlat: {book_title}")
                    if ok_d:
                        st.success(f"📁 Mentve a Drive-ra: {d_path}")
                    else:
                        st.error(f"Mentési hiba: {d_path}")

            # Jelenetek listája kártyákban
            for s_idx, scene in enumerate(manifest, start=1):
                with st.expander(f"📍 {s_idx}. Oldal: {scene.get('title', f'Scene {s_idx}')} ({scene.get('scripture_reference', 'KJV')})", expanded=(s_idx == 1)):
                    col_s1, col_s2 = st.columns([1.2, 1.0])
                    with col_s1:
                        scene["title"] = st.text_input("Jelenet Címe (Angol):", value=scene.get("title", ""), key=f"title_{s_idx}")
                        scene["scripture_reference"] = st.text_input("Igehely (KJV):", value=scene.get("scripture_reference", ""), key=f"ref_{s_idx}")
                        scene["scripture_text"] = st.text_area("Ige Szövege:", value=scene.get("scripture_text", ""), height=70, key=f"verse_{s_idx}")
                        scene["visual_prompt"] = st.text_area("Képprompt (FLUX / Imagen):", value=scene.get("visual_prompt", ""), height=90, key=f"prompt_{s_idx}")

                        if st.button(f"🎨 Kép Generálása ehhez az oldalhoz (#{s_idx})", key=f"gen_single_{s_idx}", use_container_width=True):
                            with st.spinner(f"Kép generálása a #{s_idx}. oldalhoz..."):
                                ratio_str = "1:1" if "8.5x8.5" in trim_size else ("4:5" if "8x10" in trim_size else "3:4")
                                ok_img, img_list, err = km.generate_image_with_fallback(
                                    prompt=scene["visual_prompt"],
                                    aspect_ratio=ratio_str,
                                    model_name="flux"
                                )
                                if ok_img and img_list:
                                    st.session_state["kdp_generated_images"][s_idx] = img_list[0]
                                    auto_save_current_project()
                                    st.rerun()
                                else:
                                    st.error(f"Képgenerálási hiba: {err}")

                    with col_s2:
                        st.markdown("**Kép Előnézete:**")
                        has_img = s_idx in st.session_state.get("kdp_generated_images", {})
                        if has_img:
                            img_b = st.session_state["kdp_generated_images"][s_idx]
                            st.image(img_b, use_container_width=True)
                            st.download_button(
                                "📥 Kép Letöltése (PNG)",
                                data=img_b,
                                file_name=f"{s_idx:02d}_{scene.get('title', 'scene')[:20]}.png",
                                mime="image/png",
                                key=f"dl_img_{s_idx}",
                                use_container_width=True
                            )
                        else:
                            st.info("Ehhez az oldalhoz még nincs legenerált kép.")

            # ── Nyomdai PDF Összeállítása és Letöltése ──
            st.markdown("---")
            st.markdown("##### 🖨️ Nyomdai KDP PDF Összefűzése")

            if st.button("🚀 Nyomdakész KDP Belső PDF Összeállítása (ReportLab)", use_container_width=True, type="primary"):
                pages_data = []
                for idx, sc in enumerate(manifest, start=1):
                    sc_copy = dict(sc)
                    if idx in st.session_state.get("kdp_generated_images", {}):
                        sc_copy["image_bytes"] = st.session_state["kdp_generated_images"][idx]
                    pages_data.append(sc_copy)

                out_pdf_dir = resolve_drive_folder("kdp_interiors")
                out_pdf_name = f"{book_title.replace(' ', '_')}_{trim_size}_Interior.pdf"
                out_pdf_path = os.path.join(out_pdf_dir, out_pdf_name)

                ok_pdf, pdf_bytes, msg = build_kdp_book_pdf(
                    title=book_title,
                    subtitle=book_subtitle,
                    pages_data=pages_data,
                    output_path=out_pdf_path,
                    trim_size=trim_size,
                    margin_in=margin_in,
                    show_decorative_frame=show_frame,
                    show_image_border=True,
                    show_header_text=show_titles,
                    show_footer_text=show_titles,
                    include_companion_pages=include_companion,
                    include_bleed_protection=include_bleed,
                    include_swatches_tester=show_swatches
                )

                if ok_pdf:
                    st.success(f"🎉 {msg}")
                    st.info(f"📁 Mentve a Drive-ra: {out_pdf_path}")
                    st.download_button(
                        label="📥 Nyomdakész KDP Belső PDF Letöltése",
                        data=pdf_bytes,
                        file_name=out_pdf_name,
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.error(f"Hiba a PDF generálása során: {msg}")

    # ─────────────────────────────────────────────────────────
    # TAB 2: GEMINI GEM MESTER UTASÍTÁS
    # ─────────────────────────────────────────────────────────
    with tab_gem_master:
        st.markdown("#### 💎 Gemini Gem Mester Utasítás (Stílus & Karakter Állandóság)")
        st.caption("Ezt a mester utasítást bemásolhatod a Google Gemini Web / Gem felületére, hogy minden generált kép teljesen egységes karaktereket és stílust kövessen.")

        char_rules = st.text_area(
            "Karakter / Helyszín Állandósági Szabályok:",
            value="Noah: White beard, wearing humble linen tunic, friendly warm grandfatherly expression. Always maintain exact same line weight and face features.",
            height=80
        )

        gem_prompt = build_kdp_gem_master_instruction(
            book_title=book_title,
            is_adult=is_adult,
            character_rules=char_rules
        )

        st.code(gem_prompt, language="markdown")
        st.download_button(
            "💾 Mester Utasítás Letöltése (.txt)",
            data=gem_prompt,
            file_name=f"Gemini_Gem_Master_{book_title.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # ─────────────────────────────────────────────────────────
    # TAB 3: EGYEDI SZÍNEZŐ PROMPT TESZTELŐ
    # ─────────────────────────────────────────────────────────
    with tab_single_prompt:
        st.markdown("#### ✨ Egyedi Színező Prompt Tesztelő (1 Jelenet)")

        c_sin1, c_sin2 = st.columns([1.5, 1.0])
        with c_sin1:
            scene_desc = st.text_area(
                "Jelenet Leírása:",
                value="Jesus calming the storm on the Sea of Galilee with the disciples in the wooden fishing boat with high rolling waves.",
                height=100
            )
            is_single_adult = st.checkbox("Felnőtt mandala stílus", value=False)
            prof = get_model_profile("flux")
            tmpl = prof.get("coloring_adult_template" if is_single_adult else "coloring_child_template", "")
            generated_prompt = tmpl.format(scene=scene_desc)

            st.markdown("**Generált Angol Prompt:**")
            st.code(generated_prompt, language="text")

            if st.button("🚀 Kép Generálása (Pollinations FLUX)", use_container_width=True, type="primary"):
                with st.spinner("Kép generálása folyamatban..."):
                    ok, img_list, err = km.generate_image_with_fallback(
                        prompt=generated_prompt,
                        aspect_ratio="3:4",
                        model_name="flux"
                    )
                    if ok and img_list:
                        st.session_state["single_test_image"] = img_list[0]
                        st.rerun()
                    else:
                        st.error(f"Hiba: {err}")

        with c_sin2:
            st.markdown("**Eredmény Előnézet:**")
            if "single_test_image" in st.session_state:
                st.image(st.session_state["single_test_image"], use_container_width=True)
                st.download_button(
                    "📥 Kép Letöltése",
                    data=st.session_state["single_test_image"],
                    file_name="single_coloring_page.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.info("Kattints a fenti gombra az előnézethez.")
