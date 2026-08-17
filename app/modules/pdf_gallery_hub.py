"""
Workspace 8: Image Harvester, Flipbook Reader & Standalone PDF Hub
================================================================
Features:
- Folder scanning (auto-detects 01.png, 02.png, scene_01.png) or file uploader
- Grid gallery preview with reordering support
- Interactive Virtual Flipbook / Book Page Flipper Preview
- Standalone PDF compiler into 8.5x11, 8.5x8.5, 8x10, 6x9 with custom margins
"""

import os
import io
import streamlit as st
from PIL import Image
from typing import List, Dict, Any

try:
    from core.pdf_engine import build_kdp_book_pdf
    from core.drive_sync import get_drive_root, resolve_drive_folder
except (ModuleNotFoundError, ImportError):
    from app.core.pdf_engine import build_kdp_book_pdf
    from app.core.drive_sync import get_drive_root, resolve_drive_folder



def render_pdf_gallery_hub_module():
    st.markdown("<div class='path-badge'>🖼️ 8. Képbegyűjtő, Flipbook Könyvlapozó & PDF Fűző</div>", unsafe_allow_html=True)

    tab_scan, tab_flipbook, tab_compiler = st.tabs([
        "📁 1. Mappa Szkennelés & Képgaléria",
        "📖 2. Virtuális Flipbook Könyvlapozó",
        "🖨️ 3. Önálló PDF Összefűző"
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1: MAPPA SZKENNELÉS & GALÉRIA
    # ─────────────────────────────────────────────────────────
    with tab_scan:
        st.markdown("#### 📁 Mappa Szkennelés & Képbegyűjtés")
        
        default_scan_dir = resolve_drive_folder("kdp")
        scan_path = st.text_input("Keresési Mappa Útvonala:", value=default_scan_dir, key="gallery_scan_path")

        c_sc1, c_sc2 = st.columns([1.5, 1.0])
        with c_sc1:
            uploaded_batch = st.file_uploader(
                "VAGY Tölts fel több képet egyszerre (PNG, JPG):",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                key="gallery_uploader"
            )

        images_found = []
        if os.path.exists(scan_path):
            valid_exts = (".png", ".jpg", ".jpeg", ".webp")
            for f in sorted(os.listdir(scan_path)):
                if f.lower().endswith(valid_exts):
                    images_found.append((f, os.path.join(scan_path, f)))

        if uploaded_batch:
            st.session_state["gallery_uploaded_images"] = [
                (uf.name, uf.read()) for uf in uploaded_batch
            ]

        # Display images
        all_imgs = []
        if "gallery_uploaded_images" in st.session_state and st.session_state["gallery_uploaded_images"]:
            all_imgs = st.session_state["gallery_uploaded_images"]
            st.success(f"✅ {len(all_imgs)} feltöltött kép betöltve a galériába!")
        elif images_found:
            all_imgs = [(name, path) for name, path in images_found]
            st.info(f"📂 {len(all_imgs)} kép található a mappában: `{scan_path}`")

        if all_imgs:
            st.markdown("---")
            st.markdown("##### 🖼️ Begyűjtött Képek Rácsa")
            cols_per_row = 4
            for i in range(0, len(all_imgs), cols_per_row):
                row_cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i + j
                    if idx < len(all_imgs):
                        name, data = all_imgs[idx]
                        with row_cols[j]:
                            if isinstance(data, (bytes, bytearray)):
                                st.image(data, caption=f"#{idx+1} {name[:18]}", use_container_width=True)
                            elif isinstance(data, str) and os.path.exists(data):
                                st.image(data, caption=f"#{idx+1} {name[:18]}", use_container_width=True)
        else:
            st.warning("Még nincsenek betöltött képek. Adj meg egy érvényes mappa útvonalat vagy tölts fel képeket.")

    # ─────────────────────────────────────────────────────────
    # TAB 2: VIRTUÁLIS FLIPBOOK
    # ─────────────────────────────────────────────────────────
    with tab_flipbook:
        st.markdown("#### 📖 Virtuális Flipbook Könyvlapozó")
        st.caption("Lapozz végig a kész könyv oldalain úgy, ahogy a vásárló látni fogja a nyomtatásban.")

        if all_imgs:
            if "flipbook_idx" not in st.session_state:
                st.session_state["flipbook_idx"] = 0

            cur_idx = st.session_state["flipbook_idx"]
            total_pages = len(all_imgs)

            c_nav1, c_nav2, c_nav3 = st.columns([1, 2, 1])
            with c_nav1:
                if st.button("◀️ Előző Oldal", use_container_width=True):
                    if cur_idx > 0:
                        st.session_state["flipbook_idx"] -= 1
                        st.rerun()
            with c_nav2:
                st.markdown(f"<div style='text-align:center; font-weight:bold; font-size:1.1rem; padding:6px;'>📖 {cur_idx + 1} / {total_pages}. Oldal</div>", unsafe_allow_html=True)
            with c_nav3:
                if st.button("Következő Oldal ▶️", use_container_width=True):
                    if cur_idx < total_pages - 1:
                        st.session_state["flipbook_idx"] += 1
                        st.rerun()

            # Show active page in reader frame
            name_cur, data_cur = all_imgs[cur_idx]
            st.image(data_cur, caption=f"Oldal #{cur_idx + 1}: {name_cur}", use_container_width=True)
        else:
            st.info("A Flipbook megjelenítéséhez előbb tölts be képeket az 1. fülön.")

    # ─────────────────────────────────────────────────────────
    # TAB 3: ÖNÁLLÓ PDF ÖSSZEFŰZŐ
    # ─────────────────────────────────────────────────────────
    with tab_compiler:
        st.markdown("#### 🖨️ Önálló PDF Összefűző & Nyomdai Konvertáló")

        c_p1, c_p2 = st.columns(2)
        with c_p1:
            pdf_title = st.text_input("Könyv Címe a PDF-ben:", value="Christian Coloring Book Collection", key="pdf_comp_title")
            pdf_trim = st.selectbox("Méret:", ["8.5x11", "8.5x8.5", "8x10", "6x9"], key="pdf_comp_trim")
            pdf_margin = st.slider("Margó (Hüvelyk):", 0.25, 0.85, 0.5, step=0.05, key="pdf_comp_margin")

        with c_p2:
            opt_frame = st.checkbox("Díszkeret a képek körül", value=True, key="comp_opt_frame")
            opt_swatches = st.checkbox("1. Oldali színtesztelő", value=True, key="comp_opt_swatches")
            opt_bleed = st.checkbox("Üres filcátütés-gátló lapok beszúrása", value=True, key="comp_opt_bleed")

        if st.button("🚀 Teljes PDF Generálása a Betöltött Képekből", use_container_width=True, type="primary"):
            if not all_imgs:
                st.error("Nincsenek képek a PDF generáláshoz! Kérlek tölts be képeket az 1. fülön.")
            else:
                pages_data = []
                for idx, (name, data) in enumerate(all_imgs, start=1):
                    pages_data.append({
                        "title": f"Scene {idx} - {name.split('.')[0]}",
                        "scripture_reference": f"Page {idx}",
                        "scripture_text": "",
                        "image_bytes": data if isinstance(data, (bytes, bytearray)) else None,
                        "filepath": data if isinstance(data, str) else None
                    })

                out_pdf_path = os.path.join(resolve_drive_folder("kdp_interiors"), f"{pdf_title.replace(' ', '_')}_{pdf_trim}.pdf")

                ok_pdf, pdf_bytes, msg = build_kdp_book_pdf(
                    title=pdf_title,
                    subtitle="Digital Collection",
                    pages_data=pages_data,
                    output_path=out_pdf_path,
                    trim_size=pdf_trim,
                    margin_in=pdf_margin,
                    show_decorative_frame=opt_frame,
                    include_companion_pages=False,
                    include_bleed_protection=opt_bleed,
                    include_swatches_tester=opt_swatches
                )

                if ok_pdf:
                    st.success(f"🎉 {msg}")
                    st.info(f"📁 Mentve a Drive-ra: {out_pdf_path}")
                    st.download_button(
                        "📥 Összefűzött PDF Letöltése",
                        data=pdf_bytes,
                        file_name=f"{pdf_title.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.error(f"Hiba: {msg}")
