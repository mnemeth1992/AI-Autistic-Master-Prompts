"""
Workspace 3: Amazon KDP Cover & Spine Master
============================================
Features:
- Mathematical Spine Thickness & Wrap-Around Dimensions Calculator
- Paper multipliers (White, Cream, Standard Color, Premium Color) & Binding (Paperback, Hardcover)
- 300 DPI Pixel Dimensions & Aspect Ratio Calculation
- Spine text validation (>= 79 pages requirement)
- Wrap-Around Prompt Generator (Right 45% Front, Center Spine, Left 45% Back with Barcode area)
- Cover image generation with Pollinations FLUX / Google Imagen
"""

import os
import streamlit as st
from PIL import Image
import io

try:
    from core.kdp_math import calculate_kdp_cover_dimensions, TRIM_SIZES, PAPER_MULTIPLIERS
    from core.key_manager import get_key_manager
    from core.prompts_bank import build_kdp_dynamic_cover_prompt
    from core.drive_sync import save_prompts_file_to_drive, resolve_drive_folder
    from core.project_manager import auto_save_current_project
except (ModuleNotFoundError, ImportError):
    from app.core.kdp_math import calculate_kdp_cover_dimensions, TRIM_SIZES, PAPER_MULTIPLIERS
    from app.core.key_manager import get_key_manager
    from app.core.prompts_bank import build_kdp_dynamic_cover_prompt
    from app.core.drive_sync import save_prompts_file_to_drive, resolve_drive_folder
    from app.core.project_manager import auto_save_current_project



def render_kdp_cover_module():
    st.markdown("<div class='path-badge'>🎨 3. Amazon KDP Borító, Gerincvastagság-kalkulátor & Wrap-around Prompt</div>", unsafe_allow_html=True)

    km = get_key_manager()

    c_calc1, c_calc2 = st.columns(2)
    with c_calc1:
        st.markdown("##### 📐 Könyv Nyomdai Paraméterei")
        page_count = st.number_input(
            "Könyv Oldalszáma (Belső lapok száma):",
            min_value=4,
            max_value=900,
            value=st.session_state.get("cover_page_count", 80),
            step=2,
            key="input_cover_pages"
        )
        st.session_state["cover_page_count"] = page_count

        trim_size = st.selectbox(
            "Vágási Méret (Trim Size):",
            ["8.5x11", "8.5x8.5", "8x10", "6x9", "5.5x8.5", "7x10", "5x8"],
            index=0,
            key="input_cover_trim"
        )
        st.session_state["cover_trim_size"] = trim_size

        paper_type = st.selectbox(
            "Papírtípus (Amazon KDP Belső):",
            [
                "white (Fekete-fehér szöveg / fehér papír · 0.002252\")",
                "cream (Fekete-fehér szöveg / krém papír · 0.002500\")",
                "standard_color (Standard színes belső · 0.003200\")",
                "premium_color (Prémium színes belső · 0.002252\")"
            ],
            key="input_cover_paper"
        )
        clean_paper = paper_type.split()[0]
        st.session_state["cover_paper_type"] = clean_paper

        binding_type = st.radio(
            "Kötés Típusa:",
            ["Puhatáblás (Paperback)", "Keménytáblás (Hardcover)"],
            horizontal=True,
            key="input_cover_binding"
        )
        clean_binding = "hardcover" if "Kemény" in binding_type else "paperback"
        st.session_state["cover_binding"] = clean_binding

    # ── Matematikai Számítás ──
    metrics = calculate_kdp_cover_dimensions(
        page_count=page_count,
        trim_size=trim_size,
        paper_type=clean_paper,
        binding_type=clean_binding
    )
    st.session_state["cover_calculated_metrics"] = metrics

    with c_calc2:
        st.markdown("##### 📊 Kiszámított Nyomdai Méretek (Amazon KDP)")
        st.markdown(f"""
        <div class='metric-card'>
            <strong style='color:#38bdf8;'>📏 Gerincvastagság (Spine Width):</strong> {metrics['spine_width_inch']}" ({metrics['spine_width_mm']} mm)<br>
            <strong style='color:#34d399;'>🖼️ Teljes Borító (Full Wrap):</strong> {metrics['full_width_inch']}" × {metrics['full_height_inch']}"<br>
            <strong style='color:#f59e0b;'>🎯 300 DPI Pixel Méret:</strong> {metrics['full_width_px_300dpi']} × {metrics['full_height_px_300dpi']} px<br>
            <strong style='color:#a855f7;'>📐 Képarány (Aspect Ratio):</strong> {metrics['aspect_ratio_simplified']} ({metrics['aspect_ratio']})
        </div>
        """, unsafe_allow_html=True)

        if metrics["spine_text_allowed"]:
            st.success(metrics["warning_msg"])
        else:
            st.warning(metrics["warning_msg"])

    # ── Wrap-Around Prompt Generálás ──
    st.markdown("---")
    st.markdown("##### 🎨 Wrap-Around Borító Prompt & Képgenerálás")

    col_w1, col_w2 = st.columns([1.4, 1.0])
    with col_w1:
        c_title = st.text_input("Borító Főcíme:", value=st.session_state.get("kdp_book_title", "Noah's Ark Bible Adventures"), key="input_cov_title")
        c_sub = st.text_input("Alcím:", value=st.session_state.get("kdp_book_subtitle", "Inspiring Scripture Coloring Book for Kids"), key="input_cov_sub")
        c_auth = st.text_input("Szerző Neve:", value=st.session_state.get("sb_author", "Christian Art Studio"), key="input_cov_auth")
        c_desc = st.text_area(
            "Első Borító Jelenet Leírása:",
            value="Noah standing on the wooden ark deck under a magnificent vibrant arching rainbow, with smiling giraffes, lions, and gentle white doves soaring across a golden sunset sky.",
            height=80,
            key="input_cov_desc"
        )

        cover_prompt = build_kdp_dynamic_cover_prompt(
            book_title=c_title,
            subtitle=c_sub,
            author_name=c_auth,
            scene_description=c_desc,
            dimensions_summary=metrics["dimensions_summary"],
            aspect_ratio_str=metrics["aspect_ratio_simplified"]
        )

        st.markdown("**Generált Wrap-Around Prompt (Kimásolható):**")
        st.code(cover_prompt, language="text")

        btn_g1, btn_g2 = st.columns(2)
        with btn_g1:
            if st.button("🚀 Wrap-Around Borító Generálása (FLUX)", use_container_width=True, type="primary"):
                with st.spinner("Panoráma borítókép generálása..."):
                    ok_img, img_list, err = km.generate_image_with_fallback(
                        prompt=cover_prompt,
                        aspect_ratio="16:9",
                        model_name="flux"
                    )
                    if ok_img and img_list:
                        st.session_state["cover_generated_image"] = img_list[0]
                        auto_save_current_project()
                        st.rerun()
                    else:
                        st.error(f"Hiba: {err}")

        with btn_g2:
            if st.button("💾 Borító Prompt Mentése Drive-ra", use_container_width=True):
                meta_info = f"KDP Borító Méretek: {metrics['dimensions_summary']} · Gerinc: {metrics['spine_width_inch']}\""
                ok_d, d_path = save_prompts_file_to_drive("kdp_covers", c_title, cover_prompt, meta_info)
                if ok_d:
                    st.success(f"📁 Mentve a Drive-ra: {d_path}")
                else:
                    st.error(f"Hiba: {d_path}")

    with col_w2:
        st.markdown("**Borítókép Előnézet:**")
        if "cover_generated_image" in st.session_state:
            cov_bytes = st.session_state["cover_generated_image"]
            st.image(cov_bytes, use_container_width=True)
            st.download_button(
                "📥 Wrap-Around Borító Letöltése (PNG)",
                data=cov_bytes,
                file_name=f"{c_title.replace(' ', '_')}_Full_Cover_{metrics['full_width_px_300dpi']}x{metrics['full_height_px_300dpi']}.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            st.info("Kattints a borító generálása gombra a panoráma kép előállításához.")
