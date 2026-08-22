"""
Workspace 7: AI Vision Multimodal Lab & Reverse-Prompting
========================================================
Features:
- Image upload (sketches, existing book pages, reference art, photos)
- Multimodal analysis of artistic style, line weight, composition, and character traits
- Reverse-engineering of image prompts for Google Imagen & Gemini Web
- 100% Bilingual (HU / EN).
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
    is_hu = st.session_state.get("app_global_lang", "HU") == "HU"

    st.markdown(f"<div class='path-badge'>📷 {'4. AI Vision Multimodális Lab & Reverse-Prompting' if is_hu else '4. AI Vision Multimodal Lab & Reverse-Prompting'}</div>", unsafe_allow_html=True)

    km = get_key_manager()

    st.markdown(f"##### 🔍 {'Képfeltöltés, Stíluselemzés & Reverse Prompting' if is_hu else 'Image Upload, Style Analysis & Reverse Prompting'}")
    st.caption("Tölts fel egy vázlatot, meglévő színező oldalt, borítót vagy illusztrációt, és az AI azonnal kinyeri a művészeti stílust és legenerálja az újrakészíthető képpromptot." if is_hu else "Upload reference art, book covers or line art to extract prompt formulas.")

    uploaded_file = st.file_uploader(
        "Válassz egy képet elemzésre (PNG, JPG, WEBP):" if is_hu else "Upload Reference Image (PNG, JPG, WEBP):",
        type=["png", "jpg", "jpeg", "webp"],
        key="vision_file_uploader"
    )

    if uploaded_file is not None:
        img_bytes = uploaded_file.read()
        pil_img = Image.open(io.BytesIO(img_bytes))

        c_v1, c_v2 = st.columns([1.0, 1.4])
        with c_v1:
            st.image(pil_img, caption="Feltöltött Referencia Kép" if is_hu else "Uploaded Reference Art", use_container_width=True)

        with c_v2:
            analysis_focus = st.selectbox(
                "Elemzés Fókusza:" if is_hu else "Analysis Focus:",
                [
                    "🎨 KDP Színező Oldal Reverse-Prompting (Vonalrajz, kontúrok, kompozíció)" if is_hu else "🎨 KDP Coloring Page (Clean line art, outline weight, composition)",
                    "📖 Mesekönyv Illusztráció Stíluselemzés (3D/Akvarell/Fények)" if is_hu else "📖 Storybook Illustration (Watercolor, lights, character styling)",
                    "🖼️ Falikép / Poszter Tipográfia & Elrendezés" if is_hu else "🖼️ Wall Art Poster (Typography, frame arrangement)",
                    "🔍 Általános Részletes Multimodális Leírás" if is_hu else "🔍 General Detailed Multimodal Description"
                ]
            )

            if st.button("🚀 " + ("Képelemzés & Reverse Prompt Generálása" if is_hu else "Analyze Image & Reverse Engineer Prompt"), use_container_width=True, type="primary"):
                with st.spinner("AI Vision elemzi a képet..." if is_hu else "AI Vision analyzing style..."):
                    custom_prompt = (
                        f"Analyze this image thoroughly with focus on: {analysis_focus}. "
                        f"Extract the exact art style, stroke weight, character details, composition, background elements, and lighting. "
                        f"Then, create an optimized, affirmative English image prompt for Google Imagen that can recreate this exact style."
                    )
                    ok_v, analysis_result = km.analyze_image_vision(img_bytes, custom_prompt)

                    if ok_v and analysis_result:
                        st.session_state["vision_analysis_result"] = analysis_result
                        st.success("✅ " + ("Elemzés sikeresen befejeződött!" if is_hu else "Analysis finished successfully!"))
                    else:
                        st.error("Nem sikerült az elemzés." if is_hu else "Analysis failed.")

        if "vision_analysis_result" in st.session_state:
            st.markdown("---")
            st.markdown(f"##### 📋 {'AI Vision Elemzési Eredmény & Reverse Prompt' if is_hu else 'AI Vision Analysis & Reverse Prompt'}")
            st.markdown(st.session_state["vision_analysis_result"])
    else:
        st.info("Kérlek tölts fel egy képet a fenti feltöltővel a reverse-prompting elindításához." if is_hu else "Please upload an image above to start reverse-prompting.")
