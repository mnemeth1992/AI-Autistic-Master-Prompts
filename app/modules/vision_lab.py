"""
Workspace 7: AI Vision Multimodal Lab & Reverse-Prompting
========================================================
Features:
- Image upload (sketches, existing book pages, reference art, photos)
- Multimodal analysis of artistic style, line weight, composition, and character traits
- Reverse-engineering of image prompts for Pollinations FLUX & Google Imagen
- 1-Click prompt copying and testing
"""

import os
import streamlit as st
from PIL import Image
import io

try:
    from core.key_manager import get_key_manager
    from core.drive_sync import save_prompts_file_to_drive
except (ModuleNotFoundError, ImportError):
    from app.core.key_manager import get_key_manager
    from app.core.drive_sync import save_prompts_file_to_drive



def render_vision_lab_module():
    st.markdown("<div class='path-badge'>📷 7. AI Vision Multimodális Lab & Reverse-Prompting</div>", unsafe_allow_html=True)

    km = get_key_manager()

    st.markdown("##### 🔍 Képfeltöltés, Stíluselemzés & Reverse Prompting")
    st.caption("Tölts fel egy vázlatot, meglévő színező oldalt, borítót vagy illusztrációt, és az AI azonnal kinyeri a művészeti stílust és legenerálja az újrakészíthető képpromptot.")

    uploaded_file = st.file_uploader(
        "Válassz egy képet elemzésre (PNG, JPG, WEBP):",
        type=["png", "jpg", "jpeg", "webp"],
        key="vision_file_uploader"
    )

    if uploaded_file is not None:
        img_bytes = uploaded_file.read()
        pil_img = Image.open(io.BytesIO(img_bytes))

        c_v1, c_v2 = st.columns([1.0, 1.4])
        with c_v1:
            st.image(pil_img, caption="Feltöltött Referencia Kép", use_container_width=True)

        with c_v2:
            analysis_focus = st.selectbox(
                "Elemzés Fókusza:",
                [
                    "🎨 KDP Színező Oldal Reverse-Prompting (Vonalrajz, kontúrok, kompozíció)",
                    "📖 Mesekönyv Illusztráció Stíluselemzés (3D/Akvarell/Fények)",
                    "🖼️ Falikép / Poszter Tipográfia & Elrendezés",
                    "🔍 Általános Részletes Multimodális Leírás"
                ]
            )

            if st.button("🚀 Képelemzés & Reverse Prompt Generálása", use_container_width=True, type="primary"):
                with st.spinner("AI Vision elemzi a kép vizuális elemeit és stílusát..."):
                    custom_prompt = (
                        f"Analyze this image thoroughly with focus on: {analysis_focus}. "
                        f"Extract the exact art style, stroke weight, character details, composition, background elements, and lighting. "
                        f"Then, create an optimized, affirmative English image prompt for Pollinations FLUX and Google Imagen that can recreate this exact style."
                    )
                    ok_v, analysis_result = km.analyze_image_vision(img_bytes, custom_prompt)

                    if ok_v and analysis_result:
                        st.session_state["vision_analysis_result"] = analysis_result
                        st.success("✅ Elemzés sikeresen befejeződött!")
                    else:
                        st.error("Nem sikerült az elemzés.")

        if "vision_analysis_result" in st.session_state:
            st.markdown("---")
            st.markdown("##### 📋 AI Vision Elemzési Eredmény & Reverse Prompt")
            st.markdown(st.session_state["vision_analysis_result"])

            if st.button("💾 Elemzés és Prompt Mentése Drive-ra", use_container_width=True):
                ok_d, d_path = save_prompts_file_to_drive(
                    "kdp",
                    f"Vision_Analysis_{uploaded_file.name[:15]}",
                    st.session_state["vision_analysis_result"],
                    f"AI Vision Elemzés: {uploaded_file.name}"
                )
                if ok_d:
                    st.success(f"📁 Mentve a Drive-ra: {d_path}")
                else:
                    st.error(f"Hiba: {d_path}")
    else:
        st.info("Kérlek tölts fel egy képet a fenti feltöltővel a reverse-prompting elindításához.")
