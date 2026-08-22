"""
Keresztény AI Munkaállomás · Zen & Flow Edition (AuDHD Optimalizált)
===================================================================
3 Zárt Pipeline (Wizard) + 1 Központi Vezérlőközpont & Adótervező Hub:
- 📘 1. Útvonal: Amazon KDP Könyv Pipeline (Niche -> Vázlat -> Képek -> Borító -> Nyomdai PDF)
- 🖼️ 2. Útvonal: Etsy Wall Art & Clipart Pipeline (Koncepció -> FLUX 300 DPI -> Háttéreltávolítás -> 2026 SEO & CSV)
- 🎙️ 3. Útvonal: Gumroad Áhítat & Podcast Pipeline (NotebookLM RAG -> 30 Napos Kézirat -> Sales Letter & Audio Upsell -> API Publikálás)
- ⚙️ 0. Hub: Vezérlőközpont, AuDHD Időzítő, 2026 Adótervező, FFC Marketing & Beállítások
"""

import os
import io
import sys
import json
import time
import datetime
import uuid
import re
import streamlit as st
import streamlit.components.v1 as components
import dotenv
from PIL import Image

# Word (.docx) document support
try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

dotenv.load_dotenv()

# Add module paths
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "app")
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Page configuration
st.set_page_config(
    page_title="Keresztény AI Munkaállomás · Zen & Flow",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core engine imports
import key_manager
from key_manager import get_key_manager, generate_image_with_fallback
import prompts
from prompts import (
    NICHE_CATEGORIES,
    get_niche_prompt_context,
    IMAGE_MODEL_PROFILES,
    build_kdp_autopilot_manifest_prompt,
    parse_kdp_autopilot_manifest_json,
    build_strict_etsy_seo_prompt,
    parse_strict_etsy_seo_output,
    build_pinterest_pin_seo_prompt,
    build_kdp_coloring_interior_master_prompt,
    build_kdp_cover_master_prompt,
    build_etsy_wallart_master_prompt,
    build_etsy_clipart_master_prompt,
    build_etsy_bg_removal_prompt,
    build_gumroad_devotional_master_prompt
)
import kdp_math
from kdp_math import calculate_kdp_cover_dimensions, TRIM_SIZES, PAPER_MULTIPLIERS
import kdp_pdf_engine
from kdp_pdf_engine import build_kdp_book_pdf
import etsy_csv_engine
from etsy_csv_engine import sanitize_etsy_title, sanitize_etsy_tags, build_etsy_ffc_description, generate_etsy_csv
import gumroad_publisher
from gumroad_publisher import publish_to_gumroad

# Research, RAG & Tracker Modules
try:
    from app.core.audhd_tracker import render_audhd_tracker
    from app.modules.notebooklm_rag import render_notebooklm_rag_module
    from app.modules.tax_calculator_2026 import render_tax_calculator_2026_module
    from app.core.sidecar_dock import render_sidecar_dock
    from app.modules.ffc_marketing import render_ffc_marketing_module
    from app.modules.vision_lab import render_vision_lab_module
except (ModuleNotFoundError, ImportError):
    try:
        from core.audhd_tracker import render_audhd_tracker
        from modules.notebooklm_rag import render_notebooklm_rag_module
        from modules.tax_calculator_2026 import render_tax_calculator_2026_module
        from core.sidecar_dock import render_sidecar_dock
        from modules.ffc_marketing import render_ffc_marketing_module
        from modules.vision_lab import render_vision_lab_module
    except Exception:
        render_audhd_tracker = None
        render_notebooklm_rag_module = None
        render_tax_calculator_2026_module = None
        render_sidecar_dock = None
        render_ffc_marketing_module = None
        render_vision_lab_module = None

CONFIG_FILE = os.path.join(current_dir, "config.json")
TIME_LOG_FILE = os.path.join(current_dir, "time_log.json")
PROJECTS_DIR = os.path.join(current_dir, "projects")
os.makedirs(PROJECTS_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# ZEN & FLOW CUSTOM CSS INJECTION
# ─────────────────────────────────────────────────────────────

def inject_zen_css():
    st.markdown("""
    <style>
    /* Alap háttér és betűtípus */
    .stApp {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }

    /* Sidebar letisztítása */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155 !important;
    }

    /* Kártya konténerek */
    .zen-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }

    /* Lépésjelző sáv (Stepper) */
    .step-badge-active {
        background: linear-gradient(135deg, #0284c7, #0369a1);
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
    .step-badge-done {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid #10b981;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .step-badge-idle {
        background: #0f172a;
        color: #64748b;
        border: 1px solid #334155;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.85rem;
        display: inline-block;
    }

    /* Gombok finomítása */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        min-height: 44px !important;
        transition: transform 0.1s ease, box-shadow 0.1s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2) !important;
    }

    button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7, #0369a1) !important;
        border: none !important;
        color: #ffffff !important;
    }

    /* Input mezők stílusa */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        color: #f1f5f9 !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 1px #38bdf8 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_stepper(steps: list, current_step_idx: int):
    """Visual progress stepper for dopamine feedback and flow state."""
    cols = st.columns(len(steps))
    for idx, name in enumerate(steps):
        with cols[idx]:
            if idx < current_step_idx:
                st.markdown(f"<div style='text-align:center;'><span class='step-badge-done'>✅ {name}</span></div>", unsafe_allow_html=True)
            elif idx == current_step_idx:
                st.markdown(f"<div style='text-align:center;'><span class='step-badge-active'>👉 {name}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:center;'><span class='step-badge-idle'>⚪ {name}</span></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# NYELVVÁLTÁSI CALLBACK FÜGGVÉNYEK (AZONNALI MEZŐFRISSÍTÉS)
# ─────────────────────────────────────────────────────────────

def on_kdp_lang_change():
    """Callback triggered immediately when KDP language radio changes."""
    lang = st.session_state.get("kdp_lang_radio", "")
    if "Magyar" in lang:
        st.session_state["wiz_kdp_title"] = "Noé Bárkája Bibliai Kalandok"
        st.session_state["wiz_kdp_sub"] = "Inspiráló Bibliai Igés Színezőkönyv Gyermekeknek"
    else:
        st.session_state["wiz_kdp_title"] = "Noah's Ark Bible Adventures"
        st.session_state["wiz_kdp_sub"] = "Inspiring Bible Verse Coloring Book for Children"


def on_etsy_lang_change():
    """Callback triggered immediately when Etsy language radio changes."""
    lang = st.session_state.get("etsy_lang_radio", "")
    if "Magyar" in lang:
        st.session_state["wiz_etsy_ref"] = "Zsoltárok 23:3"
        st.session_state["wiz_etsy_verse"] = "Lelkemet megvidámítja, az igazság ösvényein vezet engem az ő nevéért."
    else:
        st.session_state["wiz_etsy_ref"] = "Psalm 23:3"
        st.session_state["wiz_etsy_verse"] = "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake."


def on_gum_lang_change():
    """Callback triggered immediately when Gumroad language radio changes."""
    lang = st.session_state.get("gum_lang_radio", "")
    if "Magyar" in lang:
        st.session_state["wiz_gum_title"] = "30 Napos Békesség a Viharban Áhítat"
        st.session_state["wiz_gum_matrix"] = "[1. Nap | Filippi 4:6-7 | Isten békessége megőrzi a szíveteket | 1. Mi aggaszt ma? 2. Hogyan adod át Istennek? 3. Miért lehetsz hálás ma?]"
    else:
        st.session_state["wiz_gum_title"] = "30 Days of Peace in the Storm Devotional Journal"
        st.session_state["wiz_gum_matrix"] = "[Day 1 | Philippians 4:6-7 | God's peace guards hearts | 1. What worries you today? 2. How do you surrender it? 3. What can you thank God for?]"


# ─────────────────────────────────────────────────────────────
# 1. ÚTVONAL: AMAZON KDP KÖNYV PIPELINE (5-LÉPÉSES WIZARD)
# ─────────────────────────────────────────────────────────────

def render_kdp_pipeline_wizard(km):
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(2, 132, 199, 0.15), rgba(15, 23, 42, 0.9)); border: 1px solid #0284c7; border-radius: 12px; padding: 14px 20px; margin-bottom: 20px;'>
        <h3 style='margin:0; color:#38bdf8; font-size:1.3rem;'>📘 1. Útvonal: Amazon KDP Könyv Pipeline</h3>
        <p style='margin:4px 0 0 0; color:#94a3b8; font-size:0.88rem;'>Zárt, 5-lépéses munkafolyamat: Niche & Ötlet ➔ Vázlat & Igék ➔ 4K Képgenerálás ➔ Borító & Gerinc ➔ Nyomdai PDF</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Nyelvválasztó ──
    lang_col1, lang_col2 = st.columns([1.6, 2.4])
    with lang_col1:
        kdp_lang = st.radio(
            "🌐 KDP Nyelv / Language:",
            ["🇺🇸 Angol (US Market / KDP)", "🇭🇺 Magyar (Hazai piac)"],
            horizontal=True,
            key="kdp_lang_radio",
            on_change=on_kdp_lang_change
        )
    is_hu = "Magyar" in kdp_lang

    # Alapértékek inicializálása ha még nincsenek beállítva
    if "wiz_kdp_title" not in st.session_state:
        st.session_state["wiz_kdp_title"] = "Noé Bárkája Bibliai Kalandok" if is_hu else "Noah's Ark Bible Adventures"
    if "wiz_kdp_sub" not in st.session_state:
        st.session_state["wiz_kdp_sub"] = "Inspiráló Bibliai Igés Színezőkönyv Gyermekeknek" if is_hu else "Inspiring Bible Verse Coloring Book for Children"

    kdp_steps = [
        "1. Niche & Ötlet",
        "2. Vázlat & Igék",
        "3. Képgenerálás",
        "4. Borító & Gerinc",
        "5. Nyomdai PDF"
    ]

    if "kdp_step" not in st.session_state:
        st.session_state["kdp_step"] = 0

    cur_step = st.session_state["kdp_step"]
    render_stepper(kdp_steps, cur_step)

    # ── 1. LÉPÉS: NICHE & ÖTLET ──
    if cur_step == 0:
        st.markdown("#### 🎯 1. Lépés: Könyv Cél, Cím és Formátum")
        c1, c2 = st.columns([1.2, 1.0])
        with c1:
            title = st.text_input("Könyv Főcíme:", key="wiz_kdp_title")
            subtitle = st.text_input("Alcím:", key="wiz_kdp_sub")
            aud_choice = st.selectbox(
                "Célközönség & Stílus:",
                ["👶 Gyermek (Vastag fekete vonalak, cuki formák, tiszta fehér háttér)", "🧘 Felnőtt (Intrikát mandala, zentangle vonalrajz)"],
                key="wiz_kdp_aud"
            )
        with c2:
            trim = st.selectbox("KDP Formátum (Trim Size):", ["8.5x11", "8.5x8.5", "8x10", "6x9"], index=0, key="wiz_kdp_trim")
            page_count = st.slider("Színező Oldalak Száma:", 4, 30, value=st.session_state.get("kdp_page_count", 10), key="wiz_kdp_pages")
            st.session_state["kdp_is_adult"] = "Felnőtt" in aud_choice

        st.markdown("---")
        if st.button("Mentés és Tovább a Vázlathoz ➔", type="primary", use_container_width=True):
            st.session_state["kdp_title"] = title
            st.session_state["kdp_subtitle"] = subtitle
            st.session_state["kdp_trim"] = trim
            st.session_state["kdp_page_count"] = page_count
            st.session_state["kdp_step"] = 1
            st.rerun()

    # ── 2. LÉPÉS: VÁZLAT & KJV IGÉK ──
    elif cur_step == 1:
        st.markdown(f"#### 📖 2. Lépés: '{st.session_state.get('kdp_title', st.session_state.get('wiz_kdp_title'))}' Sorszámozott Vázlata")
        st.caption(f"AI generálja a pontos bibliai igehelyeket és 4K képgeneráló promptokat ({'Magyarul' if is_hu else 'Angolul'}).")

        if st.button("✨ Vázlat & Prompt Készlet Generálása (AI)", use_container_width=True, type="primary"):
            with st.spinner("AI készíti a sorszámozott könyvvázlatot..."):
                prompt = build_kdp_autopilot_manifest_prompt(
                    book_title=st.session_state.get("kdp_title", st.session_state.get("wiz_kdp_title", "")),
                    target_audience="Adult" if st.session_state.get("kdp_is_adult") else "Child",
                    page_count=st.session_state.get("kdp_page_count", 10),
                    is_adult=st.session_state.get("kdp_is_adult", False)
                )
                lang_sys = "Kizárólag magyar nyelven válaszolj, a címek és igék magyarul legyenek." if is_hu else "Respond strictly in English with literal KJV scriptures."
                ok, resp = km.generate_text_with_fallback(prompt=prompt, system_instruction=f"Te egy KDP kiadói szakértő vagy. {lang_sys}", model_name="groq-llama-3.3-70b")
                scenes = parse_kdp_autopilot_manifest_json(resp)
                if not scenes:
                    if is_hu:
                        scenes = [
                            {"page_number": 1, "title": "Noé építi a bárkát", "scripture_reference": "1Mózes 6:14", "scripture_text": "Csinálj magadnak bárkát gófer-fából...", "visual_prompt": build_kdp_coloring_interior_master_prompt("Noé építi a fából készült bárkát szerszámokkal")},
                            {"page_number": 2, "title": "Az állatok megérkezése", "scripture_reference": "1Mózes 7:9", "scripture_text": "Kettő-kettő ment be Noéhoz a bárkába...", "visual_prompt": build_kdp_coloring_interior_master_prompt("Két zsiráf és két oroszlán sétál a bárka felé")},
                            {"page_number": 3, "title": "A szövetség szivárványa", "scripture_reference": "1Mózes 9:13", "scripture_text": "Ívemet helyezem a felhőkbe...", "visual_prompt": build_kdp_coloring_interior_master_prompt("Noé és családja imádkozik egy hatalmas szivárvány alatt")}
                        ]
                    else:
                        scenes = [
                            {"page_number": 1, "title": "Noah building the ark", "scripture_reference": "Genesis 6:14", "scripture_text": "Make thee an ark of gopher wood...", "visual_prompt": build_kdp_coloring_interior_master_prompt("Noah building the wooden ark with tools")},
                            {"page_number": 2, "title": "Animals arriving two by two", "scripture_reference": "Genesis 7:9", "scripture_text": "There went in two and two unto Noah...", "visual_prompt": build_kdp_coloring_interior_master_prompt("Two giraffes and two lions walking toward the ark")},
                            {"page_number": 3, "title": "The rainbow of promise", "scripture_reference": "Genesis 9:13", "scripture_text": "I do set my bow in the cloud...", "visual_prompt": build_kdp_coloring_interior_master_prompt("Noah praying with family under a big rainbow")}
                        ]
                st.session_state["kdp_scenes_manifest"] = scenes
                st.success("✅ Könyvvázlat sikeresen elkészült!")

        scenes = st.session_state.get("kdp_scenes_manifest", [])
        if scenes:
            st.markdown(f"**Legenerált Jelenetek ({len(scenes)} oldal):**")
            for sc in scenes[:4]:
                st.info(f"**Oldal {sc.get('page_number')}: {sc.get('title')}** (`{sc.get('scripture_reference')}`)\n\n*Prompt:* {sc.get('visual_prompt')}")

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Címhez", use_container_width=True):
                st.session_state["kdp_step"] = 0
                st.rerun()
        with c_b2:
            if st.button("Tovább a Képgeneráláshoz ➔", type="primary", use_container_width=True):
                st.session_state["kdp_step"] = 2
                st.rerun()

    # ── 3. LÉPÉS: KÉPGENERÁLÁS ──
    elif cur_step == 2:
        st.markdown("#### 🎨 3. Lépés: 4K Színező Képek Generálása (FLUX / Gemini)")
        scenes = st.session_state.get("kdp_scenes_manifest", [{"visual_prompt": build_kdp_coloring_interior_master_prompt("Noah with animals")}])
        
        sel_page = st.selectbox("Válassz jelenetet teszteléshez / generáláshoz:", [f"Oldal {sc.get('page_number', i+1)}: {sc.get('title', 'Jelenet')}" for i, sc in enumerate(scenes)])
        sel_idx = int(sel_page.split()[1].replace(":", "")) - 1 if "Oldal" in sel_page else 0
        cur_sc = scenes[min(sel_idx, len(scenes)-1)]

        prompt_in = st.text_area("4K Master Prompt (Section 5.1 szerint):", value=cur_sc.get("visual_prompt", ""), height=100)

        if st.button("🚀 Kép Generálása (Pollinations FLUX 300 DPI)", type="primary", use_container_width=True):
            with st.spinner("4K Fekete-fehér színező oldal generálása..."):
                ok_img, imgs, err = km.generate_image_with_fallback(prompt=prompt_in, aspect_ratio="3:4", model_name="flux")
                if ok_img and imgs:
                    st.session_state["last_kdp_coloring_img"] = imgs[0]
                    st.success("✅ Színező oldal sikeresen legenerálva!")
                else:
                    st.error(f"Hiba: {err}")

        if "last_kdp_coloring_img" in st.session_state:
            st.image(st.session_state["last_kdp_coloring_img"], caption="Legenerált KDP színező oldal (300 DPI)", width=350)

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Vázlathoz", use_container_width=True):
                st.session_state["kdp_step"] = 1
                st.rerun()
        with c_b2:
            if st.button("Tovább a Borító & Gerinc Kalkulációhoz ➔", type="primary", use_container_width=True):
                st.session_state["kdp_step"] = 3
                st.rerun()

    # ── 4. LÉPÉS: BORÍTÓ & GERINC ──
    elif cur_step == 3:
        st.markdown("#### 📐 4. Lépés: KDP Wrap-Around Borító & Gerincvastagság")
        p_count = st.session_state.get("kdp_page_count", 24)
        cov_calc = calculate_kdp_cover_dimensions(page_count=p_count, trim_size_str="8.5x11", paper_type="white")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class='zen-card'>
                <strong style='color:#38bdf8;'>📐 Nyomdai Méretek (8.5×11 Bleed):</strong><br>
                • <strong>Teljes szélesség:</strong> {cov_calc['total_width_in']:.3f} hüvelyk ({cov_calc['pixel_width_300dpi']} px)<br>
                • <strong>Teljes magasság:</strong> {cov_calc['total_height_in']:.3f} hüvelyk ({cov_calc['pixel_height_300dpi']} px)<br>
                • <strong>Gerincvastagság:</strong> {cov_calc['spine_width_in']:.4f} hüvelyk<br>
                • <strong>Képarány:</strong> <code>17.412:11.25</code>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            cov_prompt = build_kdp_cover_master_prompt(f"{st.session_state.get('kdp_title', 'Noah ark')} on calm waters with animals", st.session_state.get('kdp_title', 'BIBLE COLORING BOOK'))
            st.markdown("**Master Prompt Borítóhoz (Section 5.1):**")
            st.code(cov_prompt, language="text")

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Képekhez", use_container_width=True):
                st.session_state["kdp_step"] = 2
                st.rerun()
        with c_b2:
            if st.button("Tovább a Nyomdai PDF Összefűzéshez ➔", type="primary", use_container_width=True):
                st.session_state["kdp_step"] = 4
                st.rerun()

    # ── 5. LÉPÉS: NYOMDAI PDF & FLIPBOOK ──
    elif cur_step == 4:
        st.markdown("#### 🖨️ 5. Lépés: KDP Nyomdakész Belső PDF Összeállítása")
        st.caption("ReportLab nyomdai motor: margók (0.50\"), filcátütés-gátló oldalak, színtesztelő paletta.")

        scenes = st.session_state.get("kdp_scenes_manifest", [])
        if st.button("🚀 Nyomdakész KDP Belső PDF Összefűzése (ReportLab)", type="primary", use_container_width=True):
            with st.spinner("PDF összeállítása margókkal és kísérő oldalakkal..."):
                pdf_bytes = build_kdp_book_pdf(
                    scenes=scenes,
                    book_title=st.session_state.get("kdp_title", "Coloring Book"),
                    margin_in=0.5,
                    show_frame=True,
                    show_swatches=True,
                    include_bleed=True
                )
                if pdf_bytes:
                    st.session_state["final_kdp_pdf_bytes"] = pdf_bytes
                    st.success("🎉 Nyomdakész PDF sikeresen elkészült!")

        if "final_kdp_pdf_bytes" in st.session_state:
            st.download_button(
                "📥 Nyomdakész KDP PDF Letöltése (.pdf)",
                data=st.session_state["final_kdp_pdf_bytes"],
                file_name=f"{st.session_state.get('kdp_title', 'Coloring_Book').replace(' ', '_')}_KDP_Interior.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        st.markdown("---")
        if st.button("🔄 Új KDP Könyv Indítása (Reset)", use_container_width=True):
            st.session_state["kdp_step"] = 0
            st.rerun()


# ─────────────────────────────────────────────────────────────
# 2. ÚTVONAL: ETSY WALL ART & CLIPART PIPELINE (4-LÉPÉSES WIZARD)
# ─────────────────────────────────────────────────────────────

def render_etsy_pipeline_wizard(km):
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(15, 23, 42, 0.9)); border: 1px solid #10b981; border-radius: 12px; padding: 14px 20px; margin-bottom: 20px;'>
        <h3 style='margin:0; color:#34d399; font-size:1.3rem;'>🖼️ 2. Útvonal: Etsy Wall Art & Clipart Stúdió</h3>
        <p style='margin:4px 0 0 0; color:#94a3b8; font-size:0.88rem;'>Zárt, 4-lépéses munkafolyamat: Koncepció & Ige ➔ FLUX 300 DPI Kép ➔ Háttéreltávolítás ➔ 2026 SEO & CSV Export</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Nyelvválasztó ──
    lang_col1, lang_col2 = st.columns([1.6, 2.4])
    with lang_col1:
        etsy_lang = st.radio(
            "🌐 Etsy Nyelv / Language:",
            ["🇺🇸 Angol (Global Etsy)", "🇭🇺 Magyar (Hazai piac)"],
            horizontal=True,
            key="etsy_lang_radio",
            on_change=on_etsy_lang_change
        )
    is_hu = "Magyar" in etsy_lang

    # Alapértékek inicializálása ha még nincsenek beállítva
    if "wiz_etsy_ref" not in st.session_state:
        st.session_state["wiz_etsy_ref"] = "Zsoltárok 23:3" if is_hu else "Psalm 23:3"
    if "wiz_etsy_verse" not in st.session_state:
        st.session_state["wiz_etsy_verse"] = "Lelkemet megvidámítja, az igazság ösvényein vezet engem az ő nevéért." if is_hu else "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake."

    etsy_steps = [
        "1. Koncepció & Ige",
        "2. Vizuális Generálás",
        "3. Háttéreltávolítás",
        "4. 2026 SEO & CSV"
    ]

    if "etsy_step" not in st.session_state:
        st.session_state["etsy_step"] = 0

    cur_step = st.session_state["etsy_step"]
    render_stepper(etsy_steps, cur_step)

    # ── 1. LÉPÉS: KONCEPCIÓ & IGE ──
    if cur_step == 0:
        st.markdown("#### 🌿 1. Lépés: Terméktípus és Bibliai Igehely")
        p_type = st.radio("Terméktípus:", ["🖼️ Skandináv Igés Falikép (4:5 Wall Art)", "✂️ Chibi / Akvarell Clipart Csomag (Fehér Háttér)"], key="wiz_etsy_ptype")
        st.session_state["etsy_is_clipart"] = "Clipart" in p_type

        c1, c2 = st.columns([1.2, 1.0])
        with c1:
            ref = st.text_input("Igehely:", key="wiz_etsy_ref")
            verse = st.text_area("Szó szerinti Ige:", height=70, key="wiz_etsy_verse")
        with c2:
            st.markdown("""
            <div class='zen-card'>
                <strong style='color:#34d399;'>🎨 Section 5.2 Stíluskövetelmény:</strong><br>
                • <strong>Falikép:</strong> Elegáns minimalista akvarell eukaliptusz levelekkel keretezett tiszta idézet (4:5 arány).<br>
                • <strong>Clipart:</strong> Izolált tiszta fehér háttér, egységes chibi stílus.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Mentés és Tovább a Képgeneráláshoz ➔", type="primary", use_container_width=True):
            st.session_state["etsy_ref"] = ref
            st.session_state["etsy_verse"] = verse
            st.session_state["etsy_step"] = 1
            st.rerun()

    # ── 2. LÉPÉS: VIZUÁLIS GENERÁLÁS ──
    elif cur_step == 1:
        st.markdown("#### 🎨 2. Lépés: FLUX 300 DPI Képgenerálás")
        is_clipart = st.session_state.get("etsy_is_clipart", False)
        
        if is_clipart:
            subject = "fiatal bibliai Mózes a kőtáblákkal" if is_hu else "young biblical Moses holding the stone tablets"
            prompt_in = build_etsy_clipart_master_prompt(subject)
            ratio = "1:1"
        else:
            quote_text = f"{st.session_state.get('etsy_verse', st.session_state.get('wiz_etsy_verse', ''))} - {st.session_state.get('etsy_ref', st.session_state.get('wiz_etsy_ref', ''))}"
            prompt_in = build_etsy_wallart_master_prompt(quote_text)
            ratio = "4:5"

        st.markdown("**Generálandó Master Prompt:**")
        st.code(prompt_in, language="text")

        if st.button("🚀 Kép Generálása (Pollinations FLUX 300 DPI)", type="primary", use_container_width=True):
            with st.spinner("Művészi kép előállítása..."):
                ok_img, imgs, err = km.generate_image_with_fallback(prompt=prompt_in, aspect_ratio=ratio, model_name="flux")
                if ok_img and imgs:
                    st.session_state["last_etsy_img"] = imgs[0]
                    st.success("✅ Művészi grafika sikeresen elkészült!")
                else:
                    st.error(f"Hiba: {err}")

        if "last_etsy_img" in st.session_state:
            st.image(st.session_state["last_etsy_img"], caption="Elkészült Etsy grafika", width=350)

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Koncepcióhoz", use_container_width=True):
                st.session_state["etsy_step"] = 0
                st.rerun()
        with c_b2:
            if st.button("Tovább a Háttéreltávolításhoz ➔", type="primary", use_container_width=True):
                st.session_state["etsy_step"] = 2
                st.rerun()

    # ── 3. LÉPÉS: HÁTTÉRELTÁVOLÍTÁS ──
    elif cur_step == 2:
        st.markdown("#### ✨ 3. Lépés: Többkörös Beszélgetős Háttéreltávolítás (PNG)")
        st.caption("Használd a Gemini Conversational Editing funkciót a fehér háttér azonnali átlátszóvá tételéhez.")

        st.markdown("""
        <div class='zen-card'>
            <strong style='color:#38bdf8;'>💬 Gemini Másolható Utasítás:</strong><br>
            <code>Kérlek, távolítsd el a fehér hátteret a fenti grafikák mögül, és tegyed őket teljesen átlátszóvá (transparent PNG format).</code>
        </div>
        """, unsafe_allow_html=True)

        if "last_etsy_img" in st.session_state:
            st.download_button("📥 Kép Letöltése Háttéreltávolításhoz / Canva-hoz (PNG)", data=st.session_state["last_etsy_img"], file_name="Etsy_Artwork.png", mime="image/png", use_container_width=True)

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Képhez", use_container_width=True):
                st.session_state["etsy_step"] = 1
                st.rerun()
        with c_b2:
            if st.button("Tovább a 2026 SEO & CSV-hez ➔", type="primary", use_container_width=True):
                st.session_state["etsy_step"] = 3
                st.rerun()

    # ── 4. LÉPÉS: 2026 SEO & CSV ──
    elif cur_step == 3:
        st.markdown("#### 🛍️ 4. Lépés: Szigorú 2026-os Etsy SEO & 1-Kattintásos CSV Export")
        st.caption(f"Cím <= 140 karakter, pontosan 13 tag (egyenként <= 20 karakter!), FFC leírás Drive szállítással ({'Magyarul' if is_hu else 'Angolul'}).")

        cur_ref = st.session_state.get("etsy_ref", st.session_state.get("wiz_etsy_ref", "Psalm 23:3"))
        if is_hu:
            prod_title = f"{cur_ref} Keresztény Falikép Nyomtatható Skandináv Minimalista Igés Poszter"
        else:
            prod_title = f"{cur_ref} Christian Wall Art Printable Scandinavian Minimalist Scripture Poster"

        if st.button("✨ 2026-os Etsy SEO Generálása & CSV Előállítása", type="primary", use_container_width=True):
            with st.spinner("AI generálja a szigorú Etsy SEO címkéket..."):
                prompt = build_strict_etsy_seo_prompt(prod_title, "Christian Wall Art Decor")
                lang_sys = "Kizárólag magyar nyelven válaszolj, a címkék magyar ékezetmentes kulcsszavak legyenek." if is_hu else "Respond strictly in English."
                ok, resp = km.generate_text_with_fallback(prompt=prompt, system_instruction=lang_sys, model_name="groq-llama-3.3-70b")
                seo_data = parse_strict_etsy_seo_output(resp)
                if not seo_data:
                    if is_hu:
                        seo_data = {
                            "title": sanitize_etsy_title(prod_title, 140),
                            "tags": ["kereszteny falikep", "zsoltarok 23", "bibliai idezet", "skandinav poszter", "nyomtathato kep", "azonnali letoltes", "kereszteny ajandek", "eukaliptusz dekor", "hitalapu otthon", "digitalis falikep", "minimalista poszter", "igevers dekoracio", "magyar falikep"]
                        }
                    else:
                        seo_data = {
                            "title": sanitize_etsy_title(prod_title, 140),
                            "tags": ["christian wall art", "psalm 23 print", "bible verse decor", "scandinavian art", "scripture print", "printable wall art", "instant download", "faith home decor", "minimalist poster", "digital wall art", "christian gift", "eucalyptus print", "300 dpi printable"]
                        }
                st.session_state["etsy_seo_result"] = seo_data
                st.success("✅ Etsy SEO készlet és CSV elkészült!")

        seo_res = st.session_state.get("etsy_seo_result", {})
        if seo_res:
            st.markdown(f"**Cím ({len(seo_res.get('title', ''))}/140 kar):** `{seo_res.get('title')}`")
            st.markdown(f"**13 Címke:** {', '.join([f'`{t}`' for t in seo_res.get('tags', [])])}")
            
            csv_bytes = generate_etsy_csv([{"title": seo_res.get('title'), "description": "High resolution printable digital download.", "price": "6.99", "quantity": "999", "tags": seo_res.get('tags', [])}])
            st.download_button("📊 Hivatalos Etsy CSV Letöltése", data=csv_bytes, file_name="Etsy_Listing_2026.csv", mime="text/csv", use_container_width=True)

        st.markdown("---")
        if st.button("🔄 Új Etsy Termék Indítása (Reset)", use_container_width=True):
            st.session_state["etsy_step"] = 0
            st.rerun()


# ─────────────────────────────────────────────────────────────
# 3. ÚTVONAL: GUMROAD ÁHÍTAT & PODCAST PIPELINE (4-LÉPÉSES WIZARD)
# ─────────────────────────────────────────────────────────────

def render_gumroad_pipeline_wizard(km):
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(15, 23, 42, 0.9)); border: 1px solid #a855f7; border-radius: 12px; padding: 14px 20px; margin-bottom: 20px;'>
        <h3 style='margin:0; color:#c084fc; font-size:1.3rem;'>🎙️ 3. Útvonal: Gumroad Áhítat & Podcast Gyár</h3>
        <p style='margin:4px 0 0 0; color:#94a3b8; font-size:0.88rem;'>Zárt, 4-lépéses munkafolyamat: NotebookLM RAG ➔ 30 Napos Kézirat ➔ Sales Letter & Audio Upsell ($39) ➔ API Publikálás</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Nyelvválasztó ──
    lang_col1, lang_col2 = st.columns([1.6, 2.4])
    with lang_col1:
        gum_lang = st.radio(
            "🌐 Gumroad Nyelv / Language:",
            ["🇺🇸 Angol (Global Gumroad)", "🇭🇺 Magyar (Hazai piac)"],
            horizontal=True,
            key="gum_lang_radio",
            on_change=on_gum_lang_change
        )
    is_hu = "Magyar" in gum_lang

    # Alapértékek inicializálása ha még nincsenek beállítva
    if "wiz_gum_title" not in st.session_state:
        st.session_state["wiz_gum_title"] = "30 Napos Békesség a Viharban Áhítat" if is_hu else "30 Days of Peace in the Storm Devotional Journal"
    if "wiz_gum_matrix" not in st.session_state:
        st.session_state["wiz_gum_matrix"] = "[1. Nap | Filippi 4:6-7 | Isten békessége megőrzi a szíveteket | 1. Mi aggaszt ma? 2. Hogyan adod át Istennek? 3. Miért lehetsz hálás ma?]" if is_hu else "[Day 1 | Philippians 4:6-7 | God's peace guards hearts | 1. What worries you today? 2. How do you surrender it? 3. What can you thank God for?]"

    gum_steps = [
        "1. NotebookLM RAG",
        "2. Napi Kézirat & Ima",
        "3. Copy & Audio Upsell ($39)",
        "4. Gumroad Publikálás"
    ]

    if "gum_step" not in st.session_state:
        st.session_state["gum_step"] = 0

    cur_step = st.session_state["gum_step"]
    render_stepper(gum_steps, cur_step)

    # ── 1. LÉPÉS: NOTEBOOKLM RAG ──
    if cur_step == 0:
        st.markdown("#### 📓 1. Lépés: Forrásalapú Teológiai Mátrix & KJV Kutatás")
        c1, c2 = st.columns([1.2, 1.0])
        with c1:
            dev_title = st.text_input("Áhítatos Kötet Címe:", key="wiz_gum_title")
            day_num = st.slider("Nap Száma:", 1, 30, value=st.session_state.get("gum_day", 1), key="wiz_gum_day")
            matrix_row = st.text_area("NotebookLM Mátrix Sor (RAG Forrás):", height=70, key="wiz_gum_matrix")
        with c2:
            st.markdown("""
            <div class='zen-card'>
                <strong style='color:#a855f7;'>🧠 RAG Előny:</strong><br>
                A NotebookLM jegyzetfüzetbe feltöltött KJV Biblia és teológiai jegyzetek megszüntetik a téves idézeteket és a közhelyes AI szövegeket.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Mentés és Tovább a Kézirathoz ➔", type="primary", use_container_width=True):
            st.session_state["gum_dev_title"] = dev_title
            st.session_state["gum_day"] = day_num
            st.session_state["gum_matrix_row"] = matrix_row
            st.session_state["gum_step"] = 1
            st.rerun()

    # ── 2. LÉPÉS: NAPI KÉZIRAT & IMA ──
    elif cur_step == 1:
        st.markdown(f"#### ✍️ 2. Lépés: {st.session_state.get('gum_day', 1)}. Napi Áhítat Kifejtése (Gemini Master Prompt)")
        
        if st.button(f"✨ Napi Áhítat Generálása ({'Magyarul' if is_hu else 'Angolul'})", type="primary", use_container_width=True):
            with st.spinner("AI írja a mély, lelkigondozói szöveget..."):
                prompt = build_gumroad_devotional_master_prompt(
                    st.session_state.get("gum_dev_title", st.session_state.get("wiz_gum_title", "Áhítat")),
                    st.session_state.get("gum_day", 1),
                    st.session_state.get("gum_matrix_row", st.session_state.get("wiz_gum_matrix", ""))
                )
                lang_sys = "Kizárólag mély, hiteles magyar nyelven írj, meleg lelkigondozói tónusban." if is_hu else "Write strictly in deep, authentic English devotional tone."
                ok, resp = km.generate_text_with_fallback(prompt=prompt, system_instruction=lang_sys, model_name="groq-llama-3.3-70b")
                st.session_state["gum_dev_text"] = resp
                st.success("✅ Napi áhítat elkészült!")

        dev_t = st.session_state.get("gum_dev_text", "")
        if dev_t:
            st.markdown("---")
            st.markdown(dev_t)
            st.download_button("📥 Kézirat Letöltése (.txt)", data=dev_t, file_name=f"Devotional_Day_{st.session_state.get('gum_day', 1):02d}.txt", mime="text/plain", use_container_width=True)

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Mátrixhoz", use_container_width=True):
                st.session_state["gum_step"] = 0
                st.rerun()
        with c_b2:
            if st.button("Tovább az Értékesítési Szöveghez & Audio Upsellhez ➔", type="primary", use_container_width=True):
                st.session_state["gum_step"] = 2
                st.rerun()

    # ── 3. LÉPÉS: SALES COPY & AUDIO UPSELL ($39) ──
    elif cur_step == 2:
        st.markdown("#### 📜 3. Lépés: Russell Brunson Sales Letter & Audio Upsell ($39)")
        st.caption("A NotebookLM Deep Dive Audio Overview (15 perces MP3 podcast) bónusz $29-ról $39-ra emeli a csomagárat (+$10 tiszta profit).")

        st.markdown("""
        <div class='zen-card'>
            <strong style='color:#10b981;'>💰 Értékhalom (Value Stack):</strong><br>
            • 30 Napos Vezetett Áhítat Napló (PDF): $47 érték<br>
            • <strong>BÓNUSZ: Deep Dive Audio Overview Podcast (MP3):</strong> $19 érték<br>
            • Nyomtatható Imakártyák: $15 érték<br>
            <strong>➔ Teljes Prémium Csomag Ár: $39</strong> (Több mint 60% megtakarítás!)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Kézirathoz", use_container_width=True):
                st.session_state["gum_step"] = 1
                st.rerun()
        with c_b2:
            if st.button("Tovább a Gumroad Publikáláshoz ➔", type="primary", use_container_width=True):
                st.session_state["gum_step"] = 3
                st.rerun()

    # ── 4. LÉPÉS: GUMROAD PUBLIKÁLÁS ──
    elif cur_step == 3:
        st.markdown("#### 🚀 4. Lépés: 1-Kattintásos Gumroad API Publikálás")
        p_title = st.session_state.get("gum_dev_title", st.session_state.get("wiz_gum_title", "30 Napos Keresztény Áhítat Csomag"))
        p_price = st.number_input("Termék Ára ($ USD):", min_value=9, max_value=99, value=39)
        p_drive_url = st.text_input("Google Drive Kézbesítési Mappa URL:", value="https://drive.google.com/drive/folders/...")

        if st.button("🚀 Termék Publikálása Gumroadra (API)", type="primary", use_container_width=True):
            with st.spinner("Publikálás a Gumroad fiókodba..."):
                ok_g, g_url, raw = publish_to_gumroad(product_name=p_title, price_usd=str(p_price), description=f"30-Day Christian Devotional with Bonus MP3 Audio Companion.", drive_delivery_url=p_drive_url)
                if ok_g:
                    st.success(f"🎉 Termék sikeresen publikálva! Élő URL: {g_url}")
                else:
                    st.error(f"Eredmény: {g_url}")

        st.markdown("---")
        if st.button("🔄 Új Gumroad Termék Indítása (Reset)", use_container_width=True):
            st.session_state["gum_step"] = 0
            st.rerun()


# ─────────────────────────────────────────────────────────────
# 0. HUB: VEZÉRLŐKÖZPONT, ADÓTERVEZŐ & RENDSZERBEÁLLÍTÁSOK
# ─────────────────────────────────────────────────────────────

def render_central_hub(km):
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95)); border: 1px solid #334155; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;'>
        <h3 style='margin:0; color:#f1f5f9; font-size:1.3rem;'>⚙️ 0. Központi Vezérlőközpont & Adótervező Hub</h3>
        <p style='margin:4px 0 0 0; color:#94a3b8; font-size:0.88rem;'>2026-os magyar átalányadó kalkulátor, NotebookLM RAG motor, FFC marketing és AI konfiguráció.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_tax, tab_rag, tab_mktg, tab_vision, tab_settings = st.tabs([
        "💰 1. 2026 Adótervező & Kalkulátor",
        "📓 2. NotebookLM RAG Kutatás",
        "📌 3. FFC & Pinterest SEO",
        "📷 4. AI Vision Lab",
        "🔑 5. Rendszer & API Beállítások"
    ])

    with tab_tax:
        if render_tax_calculator_2026_module:
            render_tax_calculator_2026_module()
        else:
            st.info("2026-os Adó kalkulátor modul aktív.")

    with tab_rag:
        if render_notebooklm_rag_module:
            render_notebooklm_rag_module()
        else:
            st.info("NotebookLM RAG modul aktív.")

    with tab_mktg:
        if render_ffc_marketing_module:
            render_ffc_marketing_module()
        else:
            st.info("FFC Marketing & Pinterest SEO modul aktív.")

    with tab_vision:
        if render_vision_lab_module:
            render_vision_lab_module()
        else:
            st.info("AI Vision Lab modul aktív.")

    with tab_settings:
        st.markdown("#### 🔑 AI Szolgáltatók & API Kulcsok")
        st.caption("Automatikus többmotoros fallback: 1. Groq (Ingyenes) ➔ 2. OpenRouter ➔ 3. Gemini ➔ 4. Offline Sablonok.")

        cg1, cg2 = st.columns(2)
        with cg1:
            groq_k = st.text_input("Groq API Kulcs (Llama 3.3 70B):", value=km.groq_key, type="password", key="zen_groq_k")
            openr_k = st.text_input("OpenRouter API Kulcs:", value=km.openrouter_key, type="password", key="zen_or_k")
        with cg2:
            gem_k = st.text_input("Google Gemini Fizetős API Kulcs:", value=km.paid_key, type="password", key="zen_gem_k")
            gum_t = st.text_input("Gumroad Access Token:", type="password", key="zen_gum_t")

        if st.button("💾 Kulcsok & Beállítások Mentése", type="primary", use_container_width=True):
            km.save_configuration(paid_key=gem_k, groq_key=groq_k, openrouter_key=openr_k)
            st.success("✅ Beállítások sikeresen mentve!")


# ─────────────────────────────────────────────────────────────
# FŐVEZÉRLŐ ROUTER
# ─────────────────────────────────────────────────────────────

def main():
    inject_zen_css()
    km = get_key_manager()

    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 6px 0 14px 0;'>
            <div style='font-size: 2.2rem;'>✝️</div>
            <h2 style='margin:0; font-size:1.15rem; font-weight:800; color:#f1f5f9;'>Keresztény Munkaállomás</h2>
            <span style='font-size:0.78rem; color:#94a3b8;'>Zen & Flow Pipeline Hub</span>
        </div>
        """, unsafe_allow_html=True)

        # ── 22 Niche választó ──
        niche_keys = list(NICHE_CATEGORIES.keys())
        chosen_niche = st.selectbox("🎯 Cél Niche (22 Piac):", options=niche_keys, index=0, key="zen_niche_sel")
        st.session_state["active_niche_choice"] = chosen_niche

        st.markdown("---")
        st.markdown("<div style='font-weight:700; color:#38bdf8; font-size:0.85rem; margin-bottom:6px;'>🧭 VÁLASSZ PIPELINE-T:</div>", unsafe_allow_html=True)

        # ── A 3 Fő Pipeline + 1 Hub ──
        selected_nav = st.radio(
            "Navigáció:",
            [
                "📘 1. Amazon KDP Könyv Pipeline",
                "🖼️ 2. Etsy Wall Art & Clipart Pipeline",
                "🎙️ 3. Gumroad Áhítat & Podcast Pipeline",
                "⚙️ 0. Vezérlőközpont & Adó Hub"
            ],
            index=0,
            label_visibility="collapsed",
            key="zen_main_nav"
        )

        st.markdown("---")
        summary = km.get_summary()
        st.caption(f"⚡ AI Motor: {'Groq' if summary.get('has_groq') else 'FLUX / Offline'}")

    # ── AuDHD 120-Perces Időzítő a főoldal legtetején lenyitható panelben ──
    if render_audhd_tracker:
        render_audhd_tracker()

    # ── Munkaterület Routing ──
    if "1. Amazon KDP" in selected_nav:
        render_kdp_pipeline_wizard(km)
    elif "2. Etsy" in selected_nav:
        render_etsy_pipeline_wizard(km)
    elif "3. Gumroad" in selected_nav:
        render_gumroad_pipeline_wizard(km)
    elif "0. Vezérlőközpont" in selected_nav:
        render_central_hub(km)

    # ── Minden oldalon diszkréten elérhető Alsó Gyors-Híd ──
    if render_sidecar_dock:
        st.markdown("---")
        render_sidecar_dock()


if __name__ == "__main__":
    main()
