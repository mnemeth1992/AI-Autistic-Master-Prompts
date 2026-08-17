"""
Workspace 5: Etsy Wall Art, Clipart Bundles & 2026 Strict SEO Engine
===================================================================
Features:
- Scripture Wall Art prompt engine (4:5, 3:4; Scandinavian, Watercolor, Boho, Gold Foil)
- Clipart bundle generator (Cute chibi stickers on pure white background)
- Strict 2026 Etsy SEO Engine (Title <= 140 chars, 13 tags <= 20 chars each, FFC description)
- Direct image generation with Pollinations FLUX / Google Imagen
- 1-Click Etsy CSV export with Google Drive delivery instructions
"""

import os
import json
import streamlit as st
from PIL import Image
import io

try:
    from core.key_manager import get_key_manager
    from core.prompts_bank import (
        build_etsy_wall_art_prompt,
        build_etsy_clipart_prompt,
        build_strict_etsy_seo_prompt,
        parse_strict_etsy_seo_output
    )
    from core.drive_sync import (
        save_prompts_file_to_drive,
        generate_etsy_csv,
        sanitize_etsy_title,
        sanitize_etsy_tags,
        build_etsy_ffc_description,
        resolve_drive_folder
    )
    from core.project_manager import auto_save_current_project
except (ModuleNotFoundError, ImportError):
    from app.core.key_manager import get_key_manager
    from app.core.prompts_bank import (
        build_etsy_wall_art_prompt,
        build_etsy_clipart_prompt,
        build_strict_etsy_seo_prompt,
        parse_strict_etsy_seo_output
    )
    from app.core.drive_sync import (
        save_prompts_file_to_drive,
        generate_etsy_csv,
        sanitize_etsy_title,
        sanitize_etsy_tags,
        build_etsy_ffc_description,
        resolve_drive_folder
    )
    from app.core.project_manager import auto_save_current_project



def render_etsy_art_clipart_module():
    st.markdown("<div class='path-badge'>🎨 5. Etsy Igés Faliképek, Clipartok & 2026-os SEO motor</div>", unsafe_allow_html=True)

    km = get_key_manager()

    tab_wallart, tab_clipart, tab_seo = st.tabs([
        "🖼️ 1. Igés Faliképek (Wall Art)",
        "✂️ 2. Clipart Matrica Csomagok",
        "🛍️ 3. Szigorú 2026-os Etsy SEO & CSV"
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1: IGÉS FALIKÉPEK
    # ─────────────────────────────────────────────────────────
    with tab_wallart:
        st.markdown("#### 🖼️ Művészi Igés Falikép Tervező & Generáló")

        c_w1, c_w2 = st.columns([1.4, 1.0])
        with c_w1:
            w_ref = st.text_input("Igehely (pl. Philippians 4:13):", value="Philippians 4:13", key="etsy_w_ref")
            w_verse = st.text_area("Ige Szövege:", value="I can do all things through Christ which strengtheneth me.", height=70, key="etsy_w_verse")

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                w_style = st.selectbox(
                    "Művészeti Stílus:",
                    [
                        "Skandináv Minimalista Zsályazöld & Arany",
                        "Gyengéd Akvarell Botanikai Virágkoszorú",
                        "Meleg Boho Földszínek & Absztrakt Formák",
                        "Elegáns Klasszikus Tipográfia & Pergamen"
                    ],
                    key="etsy_w_style"
                )
            with col_s2:
                w_ratio = st.selectbox("Képarány:", ["4:5 (Standard Falikép)", "3:4", "2:3", "1:1"], key="etsy_w_ratio")
                clean_w_ratio = w_ratio.split()[0]

            art_prompt = build_etsy_wall_art_prompt(w_ref, w_verse, w_style)
            st.markdown("**Generált Művészi Prompt:**")
            st.code(art_prompt, language="text")

            if st.button("🚀 Falikép Generálása (Pollinations FLUX 300 DPI)", use_container_width=True, type="primary"):
                with st.spinner("Művészi falikép generálása..."):
                    ok_img, img_list, err = km.generate_image_with_fallback(
                        prompt=art_prompt,
                        aspect_ratio=clean_w_ratio,
                        model_name="flux"
                    )
                    if ok_img and img_list:
                        st.session_state["etsy_wallart_img"] = img_list[0]
                        st.rerun()
                    else:
                        st.error(f"Hiba: {err}")

        with c_w2:
            st.markdown("**Falikép Előnézet:**")
            if "etsy_wallart_img" in st.session_state:
                st.image(st.session_state["etsy_wallart_img"], use_container_width=True)
                st.download_button(
                    "📥 Falikép Letöltése (PNG)",
                    data=st.session_state["etsy_wallart_img"],
                    file_name=f"WallArt_{w_ref.replace(' ', '_')}.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.info("Kattints a fenti generálás gombra az előnézethez.")

    # ─────────────────────────────────────────────────────────
    # TAB 2: CLIPART CSOMAGOK
    # ─────────────────────────────────────────────────────────
    with tab_clipart:
        st.markdown("#### ✂️ Keresztény & Tematikus Clipart Csomagok")

        c_cl1, c_cl2 = st.columns([1.4, 1.0])
        with c_cl1:
            cl_subject = st.text_input(
                "Clipart Fő Témája:",
                value="Cute Bible Animals (Lion, Lamb, Dove, Giraffe) with floral wreaths",
                key="etsy_cl_sub"
            )
            cl_count = st.slider("Elemek száma a csomagban:", min_value=1, max_value=12, value=6, key="etsy_cl_count")

            cl_prompt = build_etsy_clipart_prompt(cl_subject, cl_count)
            st.markdown("**Generált Clipart Prompt:**")
            st.code(cl_prompt, language="text")

            if st.button("🚀 Clipart Csomag Generálása (Fehér Háttér, FLUX)", use_container_width=True, type="primary"):
                with st.spinner("Clipart generálása folyamatban..."):
                    ok_img, img_list, err = km.generate_image_with_fallback(
                        prompt=cl_prompt,
                        aspect_ratio="1:1",
                        model_name="flux"
                    )
                    if ok_img and img_list:
                        st.session_state["etsy_clipart_img"] = img_list[0]
                        st.rerun()
                    else:
                        st.error(f"Hiba: {err}")

        with c_cl2:
            st.markdown("**Clipart Előnézet:**")
            if "etsy_clipart_img" in st.session_state:
                st.image(st.session_state["etsy_clipart_img"], use_container_width=True)
                st.download_button(
                    "📥 Clipart Letöltése (PNG)",
                    data=st.session_state["etsy_clipart_img"],
                    file_name="Clipart_Bundle.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.info("Kattints a generálás gombra a clipart megjelenítéséhez.")

    # ─────────────────────────────────────────────────────────
    # TAB 3: SZIGORÚ 2026-OS ETSY SEO & CSV
    # ─────────────────────────────────────────────────────────
    with tab_seo:
        st.markdown("#### 🛍️ Szigorú 2026-os Etsy SEO & 1-Kattintásos CSV Exportőr")
        st.caption("Etsy 2026-os algoritmus-szabályok: Cím max. 140 karakter, pontosan 13 tag (egyenként max. 20 karakter!), FFC leírás.")

        c_seo1, c_seo2 = st.columns(2)
        with c_seo1:
            seo_prod_title = st.text_input("Termék Neve:", value="Philippians 4:13 Bible Verse Wall Art Printable", key="seo_in_title")
            seo_niche = st.text_input("Niche / Kategória:", value="Christian Home Decor Wall Art", key="seo_in_niche")
            seo_price = st.text_input("Ár ($):", value="6.99", key="seo_in_price")

        with c_seo2:
            st.markdown(f"""
            <div class='metric-card'>
                <strong style='color:#34d399;'>✅ Cím limit:</strong> Max 140 karakter<br>
                <strong style='color:#38bdf8;'>✅ Címkék:</strong> Pontosan 13 db (≤ 20 karakter/tag)<br>
                <strong style='color:#f59e0b;'>✅ Kiszállítás:</strong> Google Drive azonnali letöltés + AI átláthatóság
            </div>
            """, unsafe_allow_html=True)

        if st.button("✨ 2026-os Etsy SEO Metaadatok Generálása", use_container_width=True, type="primary"):
            with st.spinner("AI generálja a kulcsszó-elöltöltött címet és 13 tag-et..."):
                prompt = build_strict_etsy_seo_prompt(seo_prod_title, seo_niche)
                ok, resp = km.generate_text_with_fallback(
                    prompt=prompt,
                    system_instruction="Te egy profi Etsy 2026 SEO szakértő vagy. Szigorú JSON-t adj.",
                    model_name="groq-llama-3.3-70b"
                )
                seo_data = parse_strict_etsy_seo_output(resp)
                if not seo_data:
                    offline_raw = km.generate_offline_content("etsy seo tags")
                    seo_data = parse_strict_etsy_seo_output(offline_raw)

                st.session_state["etsy_seo_data"] = seo_data
                auto_save_current_project()
                st.success("✅ SEO Metaadatok sikeresen legenerálva!")

        seo_res = st.session_state.get("etsy_seo_data", {})
        if seo_res:
            st.markdown("---")
            final_title = sanitize_etsy_title(seo_res.get("title", seo_prod_title), 140)
            final_tags = sanitize_etsy_tags(seo_res.get("tags", []), max_tags=13, max_tag_len=20)
            final_desc = build_etsy_ffc_description(
                product_title=final_title,
                features_bullets=seo_res.get("features", ""),
                emotional_hook=seo_res.get("emotional_hook", "")
            )

            st.markdown(f"**Optimalizált Cím ({len(final_title)}/140 karakter):**")
            st.info(final_title)

            st.markdown(f"**Pontosan 13 db Címke ({len(final_tags)} db, mind ≤ 20 karakter):**")
            st.write(", ".join([f"`{t}`" for t in final_tags]))

            st.markdown("**Termékleírás (FFC + Drive szállítás + AI nyilatkozat):**")
            st.text_area("Leírás:", value=final_desc, height=200, key="seo_desc_view")

            if st.button("📊 Hivatalos Etsy Listing CSV Letöltése", use_container_width=True):
                listing_item = {
                    "title": final_title,
                    "tags": final_tags,
                    "description": final_desc,
                    "price": seo_price,
                    "sku": f"ETSY-WALL-{w_ref.replace(' ', '')}",
                    "drive_url": "Google Drive Instant Delivery Link"
                }
                out_csv_dir = resolve_drive_folder("etsy")
                out_csv_path = os.path.join(out_csv_dir, f"Etsy_Listing_{w_ref.replace(' ', '_')}.csv")
                ok_c, msg_c, csv_bytes = generate_etsy_csv([listing_item], output_path=out_csv_path)

                if ok_c:
                    st.success(f"📁 Mentve a Drive-ra: {out_csv_path}")
                    st.download_button(
                        "📥 Etsy Listing CSV Letöltése",
                        data=csv_bytes,
                        file_name="Etsy_Listing.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.error(f"Hiba: {msg_c}")
