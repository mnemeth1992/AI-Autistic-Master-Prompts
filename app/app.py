"""
Keresztény AI Promptkészítő & Digitális Termékgenerátor Munkaállomás (Streamlit / Python)
========================================================================================
Fő belépési pont, konfiguráció, mobil CSS injektálás, fül- és sávnavigáció,
AuDHD Pomodoro fókusz követő, F5-biztos projektkezelő és a 9 önálló munkaterület vezérlője.
"""

import os
import sys
import json
import streamlit as st
from PIL import Image

# Add current and parent directory to sys.path for clean modular imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Page configuration
st.set_page_config(
    page_title="Keresztény AI Termékgenerátor & Munkaállomás",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core & Module imports (supports both direct and package paths)
try:
    from core.key_manager import get_key_manager
    from core.audhd_tracker import render_audhd_tracker
    from core.project_manager import list_saved_projects, save_project, load_project, auto_save_current_project
    from core.drive_sync import get_drive_root, resolve_drive_folder, get_service_account_info
    from core.prompts_bank import NICHE_CATEGORIES, get_niche_prompt_context

    from modules.kdp_coloring import render_kdp_coloring_module
    from modules.kdp_storybook import render_kdp_storybook_module
    from modules.kdp_cover import render_kdp_cover_module
    from modules.niche_generator import render_niche_generator_module
    from modules.etsy_art_clipart import render_etsy_art_clipart_module
    from modules.gumroad_devotional import render_gumroad_devotional_module
    from modules.vision_lab import render_vision_lab_module
    from modules.pdf_gallery_hub import render_pdf_gallery_hub_module
    from modules.ffc_marketing import render_ffc_marketing_module
except (ModuleNotFoundError, ImportError):
    from app.core.key_manager import get_key_manager
    from app.core.audhd_tracker import render_audhd_tracker
    from app.core.project_manager import list_saved_projects, save_project, load_project, auto_save_current_project
    from app.core.drive_sync import get_drive_root, resolve_drive_folder, get_service_account_info
    from app.core.prompts_bank import NICHE_CATEGORIES, get_niche_prompt_context

    from app.modules.kdp_coloring import render_kdp_coloring_module
    from app.modules.kdp_storybook import render_kdp_storybook_module
    from app.modules.kdp_cover import render_kdp_cover_module
    from app.modules.niche_generator import render_niche_generator_module
    from app.modules.etsy_art_clipart import render_etsy_art_clipart_module
    from app.modules.gumroad_devotional import render_gumroad_devotional_module
    from app.modules.vision_lab import render_vision_lab_module
    from app.modules.pdf_gallery_hub import render_pdf_gallery_hub_module
    from app.modules.ffc_marketing import render_ffc_marketing_module




def inject_custom_css():
    """Loads and injects assets/style.css with mobile responsive rules."""
    css_path = os.path.join(current_dir, "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        # Fallback inline CSS for mobile touch & responsive targets
        st.markdown("""
        <style>
        @media (max-width: 768px) {
            .stButton button {
                width: 100% !important;
                min-height: 48px !important;
                font-size: 1.05rem !important;
                margin-bottom: 6px;
            }
            .stTextInput input, .stTextArea textarea, .stSelectbox select {
                font-size: 16px !important;
            }
            .block-container {
                padding: 1rem 0.5rem 2rem 0.5rem !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)


def main():
    inject_custom_css()
    km = get_key_manager()

    # ── SIDEBAR: PROJEKT & RENDSZERBEÁLLÍTÁSOK ──
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 6px 0 12px 0;'>
            <div style='font-size: 2rem;'>✝️ ✨</div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #f1f5f9; letter-spacing: 0.5px;'>
                Keresztény AI Munkaállomás
            </div>
            <div style='font-size: 0.8rem; color: #94a3b8;'>
                Amazon KDP · Etsy · Gumroad · FFC
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 1. F5-Biztos Projektkezelő ──
        st.markdown("##### 📁 Projekt Menedzser (F5-Biztos)")
        saved_projs = list_saved_projects()
        cur_proj = st.session_state.get("current_project_name", "Noah's_Ark_Adventures")

        proj_options = list(set([cur_proj] + saved_projs))
        chosen_proj = st.selectbox(
            "Aktív Projekt:",
            options=proj_options,
            index=proj_options.index(cur_proj) if cur_proj in proj_options else 0,
            key="sb_proj_select"
        )

        c_p1, c_p2 = st.columns(2)
        with c_p1:
            if st.button("📂 Betöltés", use_container_width=True):
                ok_l, msg_l = load_project(chosen_proj)
                if ok_l:
                    st.success("✅ Betöltve!")
                    st.rerun()
                else:
                    st.error(msg_l)
        with c_p2:
            if st.button("💾 Mentés", use_container_width=True):
                ok_s, msg_s = save_project(chosen_proj)
                if ok_s:
                    st.success("✅ Mentve!")
                else:
                    st.error(msg_s)

        new_proj_name = st.text_input("Új Projekt Neve:", placeholder="pl. Psalms_Devotional_2026", key="sb_new_proj_input")
        if st.button("➕ Új Projekt Létrehozása", use_container_width=True):
            if new_proj_name.strip():
                save_project(new_proj_name.strip())
                st.session_state["current_project_name"] = new_proj_name.strip()
                st.success(f"Új projekt létrehozva: {new_proj_name}")
                st.rerun()

        st.markdown("---")

        # ── 2. Niche Kategória Kiválasztása ──
        st.markdown("##### 🎯 Cél Niche Kategória (22 Piac)")
        niche_keys = list(NICHE_CATEGORIES.keys())
        chosen_niche = st.selectbox(
            "Alapértelmezett Niche:",
            options=niche_keys,
            index=0,
            key="sb_niche_select"
        )
        st.session_state["selected_niche"] = chosen_niche

        st.markdown("---")

        # ── 3. Fő Munkaterület Navigáció ──
        st.markdown("""
        <div class='nav-title-box'>
            <span class='nav-title-text'>🧭 FŐMENÜ & MUNKATERÜLETEK</span>
        </div>
        """, unsafe_allow_html=True)

        workspace_options = [
            "🎨 1. Amazon KDP Színező & PDF Összeállító",
            "📖 2. Amazon KDP Illusztrált Mesekönyv",
            "🎨 3. Amazon KDP Borító & Gerinc Mester",
            "💡 4. 30 Téma & Niche Ötletműhely",
            "🎨 5. Etsy Igés Faliképek & Clipartok",
            "✍️ 6. Gumroad Áhítatok & Értékesítési Szövegek",
            "📷 7. AI Vision Multimodális Lab",
            "🖼️ 8. Képbegyűjtő, Flipbook & PDF Központ",
            "🚀 9. FFC Marketing, Brunson Copywriting & Sites",
            "⚙️ 10. Rendszerbeállítások & API Kulcsok"
        ]

        active_workspace = st.radio(
            "Válassz munkaterületet:",
            options=workspace_options,
            index=0,
            key="main_workspace_radio",
            label_visibility="collapsed"
        )

        st.markdown("---")

        # ── 4. Rendszer & AI Állapot ──
        st.markdown("##### ⚡ Rendszer & AI Állapot")
        summary = km.get_summary()
        prov_info = []
        if summary.get("has_groq"):
            prov_info.append("🚀 Groq")
        if summary.get("has_openrouter"):
            prov_info.append("🌐 OpenRouter")
        if summary.get("has_gemini"):
            prov_info.append("💎 Gemini")

        if prov_info:
            st.markdown(f"📝 **Szöveg AI:** 🟢 {' ➔ '.join(prov_info)}")
        else:
            st.markdown("📝 **Szöveg AI:** 🛡️ Beépített 0-API Sablon Motor")

        st.markdown("🖼️ **Képmotor:** ⚡ 100% Ingyenes Pollinations FLUX (300 DPI)")

        sa_info = get_service_account_info()
        drive_path = get_drive_root()
        if sa_info:
            st.markdown("📁 **Drive:** ☁️ Cloud API Csatlakoztatva")
        elif os.path.exists(drive_path):
            st.markdown("📁 **Drive:** 🟢 Helyi mappa (Laptop)")
        else:
            st.markdown("📁 **Drive:** 🟡 Helyi letöltés / Fallback")

        if st.button("🔄 Kulcsok Resetelése", use_container_width=True):
            km.reset_all_keys()
            st.success("🟢 Kulcsok resetelve!")
            st.rerun()

        st.caption("Keresztény AI Munkaállomás · v4.0 Moduláris")

    # ── FŐTERÜLET: AUDHD POMODORO FÓKUSZ KÖVETŐ ──
    render_audhd_tracker()

    # ── MUNKATERÜLET ROUTER ──
    if "1. Amazon KDP Színező" in active_workspace:
        render_kdp_coloring_module()
    elif "2. Amazon KDP Illusztrált Mesekönyv" in active_workspace:
        render_kdp_storybook_module()
    elif "3. Amazon KDP Borító" in active_workspace:
        render_kdp_cover_module()
    elif "4. 30 Téma" in active_workspace:
        render_niche_generator_module()
    elif "5. Etsy Igés Faliképek" in active_workspace:
        render_etsy_art_clipart_module()
    elif "6. Gumroad Áhítatok" in active_workspace:
        render_gumroad_devotional_module()
    elif "7. AI Vision" in active_workspace:
        render_vision_lab_module()
    elif "8. Képbegyűjtő" in active_workspace:
        render_pdf_gallery_hub_module()
    elif "9. FFC Marketing" in active_workspace:
        render_ffc_marketing_module()
    elif "10. Rendszerbeállítások" in active_workspace:
        render_settings_module(km)


def render_settings_module(km):
    """Workspace 10: System Settings, API Keys & Preferences."""
    st.markdown("<div class='path-badge'>⚙️ 10. Rendszerbeállítások & AI Motorok</div>", unsafe_allow_html=True)

    st.markdown("#### 🔑 AI Szolgáltatók & API Kulcsok")
    st.caption("A rendszer a leggyorsabb és legolcsóbb motorokat részesíti előnyben: 1. Groq (Ingyenes) ➔ 2. OpenRouter (Ingyenes) ➔ 3. Gemini (Fizetős) ➔ 4. Offline Sablonok.")

    c_s1, c_s2 = st.columns(2)
    with c_s1:
        st.markdown("##### 🚀 1. Groq Cloud API (Elsődleges Szövegmotor)")
        groq_k = st.text_input("Groq API Kulcs (Llama 3.3 70B - Villámgyors):", value=km.groq_key, type="password", key="set_groq_key")
        st.caption("Ingyenesen beszerezhető: https://console.groq.com")

        st.markdown("##### 🌐 2. OpenRouter API (Másodlagos Tartalék)")
        openrouter_k = st.text_input("OpenRouter API Kulcs (:free modellek):", value=km.openrouter_key, type="password", key="set_or_key")
        st.caption("Ingyenesen beszerezhető: https://openrouter.ai/keys")

    with c_s2:
        st.markdown("##### 💎 3. Google Gemini Pro API (Harmadlagos Tartalék)")
        gemini_k = st.text_input("Google Gemini Fizetős API Kulcs:", value=km.paid_key, type="password", key="set_gem_key")
        st.caption("Beszerezhető: https://aistudio.google.com/app/apikey")

        st.markdown("##### 🛍️ Gumroad API Access Token")
        gumroad_tok = st.text_input("Gumroad Access Token (Termékpublikáláshoz):", type="password", key="set_gum_token")
        st.caption("Beszerezhető: https://gumroad.com/settings/developer")

    st.markdown("---")
    st.markdown("#### ☁️ Google Drive Felhő Integráció (Streamlit Cloudhoz)")
    st.caption("Ha a laptopod ki van kapcsolva, a rendszer a Google Service Account segítségével közvetlenül a Google Drive felhődbe menti a fájlokat.")

    sa_existing = get_service_account_info()
    if sa_existing:
        st.success(f"🟢 Google Drive Cloud API Csatlakoztatva! (Service Account: `{sa_existing.get('client_email', 'Aktív')}`)")
    else:
        st.info("💡 Helyi módban automatikusan a laptop meghajtóját használja. Streamlit Cloudhoz illeszd be a Google Service Account JSON kulcsodat:")

    current_sa_text = json.dumps(sa_existing, indent=2) if sa_existing else ""
    sa_json_input = st.text_area(
        "Google Service Account JSON Kulcs (opcionális felhőhöz):",
        value=current_sa_text,
        height=100,
        placeholder='{"type": "service_account", "project_id": "...", ...}',
        key="set_sa_json"
    )

    st.markdown("##### 📁 Helyi Google Drive Gyökérmappa Útvonal (Laptophoz)")
    drive_in = st.text_input("Saját Meghajtó Mappa Útvonala:", value=get_drive_root(), key="set_drive_path")

    st.markdown("---")
    st.markdown("##### 🎨 Képmotor Preferencia")
    img_eng = st.radio(
        "Alapértelmezett Képgeneráló Motor:",
        [
            "pollinations_flux (100% Ingyenes, Korlátlan, 300 DPI FLUX.1 - Ajánlott)",
            "imagen (Google Imagen 3 - Csak érvényes fizetős Gemini kulccsal)"
        ],
        index=0,
        key="set_img_engine"
    )
    clean_img_eng = "pollinations_flux" if "pollin" in img_eng else "imagen"

    if st.button("💾 Beállítások Mentése", use_container_width=True, type="primary"):
        km.save_configuration(
            paid_key=gemini_k,
            groq_key=groq_k,
            openrouter_key=openrouter_k,
            image_engine=clean_img_eng
        )
        cfg_path = os.path.join(parent_dir, "config.json")
        try:
            cfg = {}
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            cfg["drive_root_path"] = drive_in.strip()
            if gumroad_tok.strip():
                cfg["gumroad_access_token"] = gumroad_tok.strip()
            if sa_json_input.strip():
                try:
                    cfg["google_service_account_json"] = json.loads(sa_json_input.strip())
                except Exception:
                    cfg["google_service_account_json"] = sa_json_input.strip()
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
            st.success("✅ Rendszerbeállítások és kulcsok sikeresen mentve a config.json fájlba!")
            st.rerun()
        except Exception as e:
            st.error(f"Mentési hiba: {e}")



if __name__ == "__main__":
    main()
