"""
Keresztény AI Munkaállomás · Zen & Flow Edition (AuDHD Optimalizált)
===================================================================
3 Zárt Pipeline (Wizard) + 1 Központi Vezérlőközpont & Adótervező Hub:
- 📘 1. Útvonal: Amazon KDP Könyv Pipeline (Niche -> Vázlat -> Gemini Custom Gem & 4K Promptek -> Borító & Gerinc -> Nyomdai PDF)
- 🖼️ 2. Útvonal: Etsy Wall Art & Clipart Pipeline (Koncepció -> Gemini Custom Gem & Művészi Promptek -> Háttéreltávolítás -> 2026 SEO & CSV)
- 🎙️ 3. Útvonal: Gumroad Áhítat & Podcast Pipeline (NotebookLM RAG -> 30 Napos Kézirat -> Sales Letter & Audio Upsell -> API Publikálás)
- ⚙️ 0. Hub: Vezérlőközpont, AuDHD Időzítő, 2026 Adótervező, FFC Marketing, Termék Analytics, Mentett Dolgok & Beállítások
"""

import os
import io
import sys
import json
import time
import datetime
import uuid
import re
from typing import List, Dict, Any
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
from key_manager import get_key_manager
import prompts

try:
    from prompts import (
        CHRISTIAN_SUB_NICHES,
        KDP_TASK_STYLES,
        ETSY_TASK_STYLES,
        GUMROAD_TASK_STYLES,
        build_gemini_custom_gem_instructions,
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
except ImportError:
    CHRISTIAN_SUB_NICHES = getattr(prompts, "CHRISTIAN_SUB_NICHES", {
        "👶 Gyermekek & Családok (Bible Stories & Coloring)": {
            "default_kdp_title_en": "Noah's Ark Bible Adventures",
            "default_kdp_title_hu": "Noé Bárkája Bibliai Kalandok",
            "default_kdp_sub_en": "Inspiring Bible Verse Coloring Book for Children",
            "default_kdp_sub_hu": "Inspiráló Bibliai Igés Színezőkönyv Gyermekeknek"
        }
    })
    KDP_TASK_STYLES = getattr(prompts, "KDP_TASK_STYLES", {
        "👶 Gyermek Vonalrajz (Section 5.1)": {"prompt_mod": "clean bold black line art, pure white background", "is_adult": False}
    })
    ETSY_TASK_STYLES = getattr(prompts, "ETSY_TASK_STYLES", {
        "🌿 Skandináv Eukaliptusz Minimalista (Section 5.2)": {"prompt_mod": "minimalist watercolor eucalyptus", "tags_addon": ["scandinavian art"]}
    })
    GUMROAD_TASK_STYLES = getattr(prompts, "GUMROAD_TASK_STYLES", {
        "🕊️ Meleg, Bátorító Lelkigondozói (Section 5.3)": {"instruction": "Írj meleg, mélyen bátorító tónusban."}
    })
    build_gemini_custom_gem_instructions = getattr(prompts, "build_gemini_custom_gem_instructions", lambda *a, **k: "")
    IMAGE_MODEL_PROFILES = getattr(prompts, "IMAGE_MODEL_PROFILES", {})
    build_kdp_autopilot_manifest_prompt = getattr(prompts, "build_kdp_autopilot_manifest_prompt", lambda **k: "")
    parse_kdp_autopilot_manifest_json = getattr(prompts, "parse_kdp_autopilot_manifest_json", lambda r: [])
    build_strict_etsy_seo_prompt = getattr(prompts, "build_strict_etsy_seo_prompt", lambda t, c: "")
    parse_strict_etsy_seo_output = getattr(prompts, "parse_strict_etsy_seo_output", lambda r: {})
    build_pinterest_pin_seo_prompt = getattr(prompts, "build_pinterest_pin_seo_prompt", lambda t, c: "")
    build_kdp_coloring_interior_master_prompt = getattr(prompts, "build_kdp_coloring_interior_master_prompt", lambda s: s)
    build_kdp_cover_master_prompt = getattr(prompts, "build_kdp_cover_master_prompt", lambda s, t: s)
    build_etsy_wallart_master_prompt = getattr(prompts, "build_etsy_wallart_master_prompt", lambda q: q)
    build_etsy_clipart_master_prompt = getattr(prompts, "build_etsy_clipart_master_prompt", lambda s: s)
    build_etsy_bg_removal_prompt = getattr(prompts, "build_etsy_bg_removal_prompt", lambda: "")
    build_gumroad_devotional_master_prompt = getattr(prompts, "build_gumroad_devotional_master_prompt", lambda t, d, m: f"{t} Day {d}")

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
    from app.modules.ev_accounting import render_ev_accounting_module
    render_tax_calculator_2026_module = render_ev_accounting_module
    from app.core.sidecar_dock import render_sidecar_dock
    from app.modules.ffc_marketing import render_ffc_marketing_module
    from app.modules.vision_lab import render_vision_lab_module
    from app.modules.product_analytics import render_product_analytics_module
    from app.modules.saved_vault import render_saved_vault_module, add_to_saved_vault
except (ModuleNotFoundError, ImportError):
    try:
        from core.audhd_tracker import render_audhd_tracker
        from modules.notebooklm_rag import render_notebooklm_rag_module
        from modules.ev_accounting import render_ev_accounting_module
        render_tax_calculator_2026_module = render_ev_accounting_module
        from core.sidecar_dock import render_sidecar_dock
        from modules.ffc_marketing import render_ffc_marketing_module
        from modules.vision_lab import render_vision_lab_module
        from modules.product_analytics import render_product_analytics_module
        from modules.saved_vault import render_saved_vault_module, add_to_saved_vault
    except Exception:
        render_audhd_tracker = None
        render_notebooklm_rag_module = None
        render_ev_accounting_module = None
        render_tax_calculator_2026_module = None
        render_sidecar_dock = None
        render_ffc_marketing_module = None
        render_vision_lab_module = None
        render_product_analytics_module = None
        render_saved_vault_module = None
        add_to_saved_vault = lambda *a, **k: False

CONFIG_FILE = os.path.join(current_dir, "config.json")
TIME_LOG_FILE = os.path.join(current_dir, "time_log.json")
PROJECTS_DIR = os.path.join(current_dir, "projects")
os.makedirs(PROJECTS_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# BIBLIAI JELENET TÁR & PONTOS OLDALSZÁM BIZTOSÍTÓ
# ─────────────────────────────────────────────────────────────

BIBLICAL_SCENES_POOL = [
    {"title_en": "Noah Building the Wooden Ark", "title_hu": "Noé építi a fából készült bárkát", "ref": "Genesis 6:14", "verse_en": "Make thee an ark of gopher wood...", "verse_hu": "Csinálj magadnak bárkát gófer-fából...", "visual_desc": "Noah holding carpentry tools standing before the giant wooden ark in a sunny meadow"},
    {"title_en": "Animals Entering the Ark Two by Two", "title_hu": "Az állatok megérkezése a bárkához", "ref": "Genesis 7:9", "verse_en": "There went in two and two unto Noah into the ark...", "verse_hu": "Kettő-kettő ment be Noéhoz a bárkába...", "visual_desc": "Pairs of giraffes, lions, elephants and lambs peacefully walking up the ark wooden ramp"},
    {"title_en": "The Dove Returning with Olive Leaf", "title_hu": "A galamb visszatér az olajfa levéllel", "ref": "Genesis 8:11", "verse_en": "And the dove came in to him in the evening; and, lo, in her mouth was an olive leaf...", "verse_hu": "És megjöve ő hozzá a galamb estenden, és ímé leszakasztott olajfalevél vala annak szájában...", "visual_desc": "A gentle white dove flying toward Noah holding a green olive leaf in its beak over calm waters"},
    {"title_en": "The Rainbow of God's Promise", "title_hu": "A szövetség szivárványa", "ref": "Genesis 9:13", "verse_en": "I do set my bow in the cloud, and it shall be for a token of a covenant...", "verse_hu": "Ívemet helyezem a felhőkbe, és az lesz a szövetség jele...", "visual_desc": "Noah and his family joyfully praying with hands lifted under a magnificent colorful rainbow"},
    {"title_en": "David the Shepherd Protecting His Flock", "title_hu": "Dávid a pásztorfiú megvédi nyáját", "ref": "Psalm 23:1", "verse_en": "The Lord is my shepherd; I shall not want.", "verse_hu": "Az Úr az én pásztorom; nem szűkölködöm.", "visual_desc": "Young David holding a wooden staff playing a harp beside fluffy white sheep in green pastures"},
    {"title_en": "David and Goliath with Faith in God", "title_hu": "Dávid hittel szembeszáll Góliáttal", "ref": "1 Samuel 17:45", "verse_en": "I come to thee in the name of the Lord of hosts...", "verse_hu": "Én a Seregek Urának nevében megyek ellened...", "visual_desc": "Brave young David holding a smooth stone and sling with confident faith"},
    {"title_en": "Daniel Safe in the Lions' Den", "title_hu": "Dániel biztonságban az oroszlánok vermében", "ref": "Daniel 6:22", "verse_en": "My God hath sent his angel, and hath shut the lions' mouths...", "verse_hu": "Az én Istenem elküldte az ő angyalát, és bezárta az oroszlánok száját...", "visual_desc": "Daniel kneeling peacefully in prayer with friendly gentle lions resting calmly around him"},
    {"title_en": "Jesus Calming the Raging Storm", "title_hu": "Jézus lecsendesíti a vihart", "ref": "Mark 4:39", "verse_en": "Peace, be still. And the wind ceased, and there was a great calm.", "verse_hu": "Hallgass, némulj el! És elállt a szél, és lőn nagy csendesség.", "visual_desc": "Jesus standing on the wooden fishing boat raising his hand as storm clouds part and waves calm"},
    {"title_en": "The Good Shepherd Carrying the Lost Sheep", "title_hu": "A Jó Pásztor a vállán viszi a megkerült bárányt", "ref": "Luke 15:5", "verse_en": "And when he hath found it, he layeth it on his shoulders, rejoicing.", "verse_hu": "És ha megtalálta, felveszi az ő vállára örvendezve.", "visual_desc": "Jesus as the caring Good Shepherd carrying a little fluffy lamb gently on his shoulders"},
    {"title_en": "Moses and the Burning Bush", "title_hu": "Mózes az égő csipkebokornál", "ref": "Exodus 3:2", "verse_en": "And the angel of the Lord appeared unto him in a flame of fire...", "verse_hu": "És megjelenék néki az Úrnak angyala tűzlángban egy csipkebokor közepéből...", "visual_desc": "Moses respectfully removing his sandals kneeling before the radiant burning bush"},
    {"title_en": "Parting of the Red Sea", "title_hu": "Átkelés a Vörös-tengeren", "ref": "Exodus 14:21", "verse_en": "And Moses stretched out his hand over the sea; and the Lord caused the sea to go back...", "verse_hu": "És kinyújtá Mózes az ő kezét a tengerre, és az Úr elhajtá a tengert...", "visual_desc": "Moses lifting his staff as towering blue water walls stand firm on left and right"},
    {"title_en": "The Star of Bethlehem and Wise Men", "title_hu": "A betlehemi csillag és a bölcsek", "ref": "Matthew 2:10", "verse_en": "When they saw the star, they rejoiced with exceeding great joy.", "verse_hu": "Mikor pedig látták a csillagot, igen nagy örömmel örvendezének.", "visual_desc": "Three wise men with gifts gazing up at a radiant bright golden star over Bethlehem"},
    {"title_en": "Jonah Praying by the Seashore", "title_hu": "Jónás hálát ad Istennek a tengerparton", "ref": "Jonah 2:9", "verse_en": "Salvation is of the Lord.", "verse_hu": "Az Úré a szabadítás!", "visual_desc": "Jonah kneeling in grateful prayer on a sunlit golden sand beach as a big friendly whale swims away"},
    {"title_en": "Jesus Blessing the Little Children", "title_hu": "Jézus megáldja a gyermekeket", "ref": "Mark 10:14", "verse_en": "Suffer the little children to come unto me, and forbid them not...", "verse_hu": "Engedjétek hozzám jönni a kisgyermekeket, és ne tiltsátok el őket...", "visual_desc": "Jesus smiling with open arms surrounded by happy joyful children laughing together"},
    {"title_en": "Creation: Sun, Moon and Bright Stars", "title_hu": "A teremtés: Nap, Hold és a ragyogó csillagok", "ref": "Genesis 1:16", "verse_en": "And God made two great lights; the greater light to rule the day...", "verse_hu": "Teremté tehát Isten a két nagy világító testet...", "visual_desc": "A beautiful celestial landscape with golden smiling sun, silver crescent moon, and sparkling stars"}
]


def ensure_exact_page_count(scenes: List[Dict[str, Any]], target_count: int, is_hu: bool, style_mod: str) -> List[Dict[str, Any]]:
    """Guarantees that the scenes list has EXACTLY target_count pages (e.g. 10 pages = 10 scenes)."""
    clean_scenes = []
    
    # Keep existing valid scenes
    for idx, sc in enumerate(scenes[:target_count]):
        page_num = idx + 1
        t_hu = sc.get("title_hu", sc.get("title", f"{page_num}. Jelenet"))
        t_en = sc.get("title", f"Scene {page_num}")
        cur_title = t_hu if is_hu else t_en
        ref = sc.get("scripture_reference", "Bible Verse")
        verse = sc.get("scripture_text", "")
        v_prompt = sc.get("visual_prompt", f"Bible coloring page of {cur_title}, {style_mod}")
        if style_mod and style_mod not in v_prompt:
            v_prompt = f"{v_prompt}, {style_mod}"
        
        clean_scenes.append({
            "page_number": page_num,
            "title": cur_title,
            "title_en": t_en,
            "title_hu": t_hu,
            "scripture_reference": ref,
            "scripture_text": verse,
            "visual_prompt": v_prompt
        })

    # If AI returned fewer scenes than target_count, complement from the rich biblical scenes pool
    current_len = len(clean_scenes)
    if current_len < target_count:
        for i in range(current_len, target_count):
            pool_idx = i % len(BIBLICAL_SCENES_POOL)
            p_data = BIBLICAL_SCENES_POOL[pool_idx]
            page_num = i + 1
            cur_title = p_data["title_hu"] if is_hu else p_data["title_en"]
            cur_verse = p_data["verse_hu"] if is_hu else p_data["verse_en"]
            v_prompt = f"Coloring book page illustration of {p_data['visual_desc']}, {style_mod}"
            
            clean_scenes.append({
                "page_number": page_num,
                "title": cur_title,
                "title_en": p_data["title_en"],
                "title_hu": p_data["title_hu"],
                "scripture_reference": p_data["ref"],
                "scripture_text": cur_verse,
                "visual_prompt": v_prompt
            })

    return clean_scenes[:target_count]


# ─────────────────────────────────────────────────────────────
# ZEN & FLOW CUSTOM CSS INJECTION
# ─────────────────────────────────────────────────────────────

def inject_zen_css():
    st.markdown("""
    <style>
    /* Felső felesleges Streamlit sáv, Share gomb, menü és toolbar teljes elrejtése */
    header[data-testid="stHeader"],
    .stAppHeader,
    #MainMenu,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    .viewerBadge_container,
    footer {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        min-height: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* Tiszta, fentről induló tartalom (eltünteti a felesleges felső üres helyet) */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
    }

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

    /* Paraméter visszajelző sáv */
    .param-badge {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 4px 12px;
        border-radius: 14px;
        font-weight: 700;
        font-size: 0.84rem;
        display: inline-block;
        margin-right: 6px;
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


def render_stepper(steps: list, current_step_idx: int, pipeline_key: str = "kdp"):
    """Interactive visual progress stepper allowing both direct step jumping and feedback."""
    cols = st.columns(len(steps))
    for idx, name in enumerate(steps):
        with cols[idx]:
            is_active = (idx == current_step_idx)
            is_done = (idx < current_step_idx)
            icon = "👉" if is_active else ("✅" if is_done else "⚪")
            btn_label = f"{icon} {name}"
            
            if st.button(btn_label, key=f"step_btn_{pipeline_key}_{idx}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state[f"{pipeline_key}_step"] = idx
                st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)


def render_ai_tool_badge(tool_type: str, note: str = ""):
    """Renders a large, prominent visual badge indicating the exact AI tool to use."""
    t_lower = tool_type.lower()
    if "notebooklm" in t_lower:
        bg = "linear-gradient(135deg, #4c1d95 0%, #6d28d9 100%)"
        border = "#a78bfa"
        icon = "📓"
        name = "GOOGLE NOTEBOOKLM (RAG Forrásalapú Kutató & Podcast)"
        action_url = "https://notebooklm.google.com"
        btn_text = "🚀 NotebookLM Megnyitása"
    elif "gemini" in t_lower or "web" in t_lower:
        bg = "linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%)"
        border = "#60a5fa"
        icon = "💎"
        name = "GOOGLE GEMINI ADVANCED (Webes Képgeneráló & Custom Gem)"
        action_url = "https://gemini.google.com"
        btn_text = "🚀 Gemini Megnyitása"
    elif "reportlab" in t_lower or "pdf" in t_lower:
        bg = "linear-gradient(135deg, #78350f 0%, #d97706 100%)"
        border = "#fbbf24"
        icon = "🖨️"
        name = "REPORTLAB NYOMDAI MOTOR (Automatikus KDP PDF)"
        action_url = None
        btn_text = ""
    else:
        bg = "linear-gradient(135deg, #1e293b 0%, #334155 100%)"
        border = "#94a3b8"
        icon = "🛠️"
        name = tool_type.upper()
        action_url = None
        btn_text = ""

    html = f"""
    <div style='background: {bg}; border: 2px solid {border}; border-radius: 12px; padding: 12px 18px; margin: 10px 0 16px 0; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 14px rgba(0,0,0,0.35);'>
        <div style='display:flex; align-items:center; gap: 14px;'>
            <span style='font-size: 2.2rem;'>{icon}</span>
            <div>
                <div style='font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.85); font-weight: 800;'>🎯 HASZNÁLANDÓ AI ESZKÖZ / RECOMMENDED AI TOOL</div>
                <div style='font-size: 1.15rem; font-weight: 900; color: #ffffff;'>{name}</div>
                {f"<div style='font-size:0.84rem; color:rgba(255,255,255,0.95); margin-top:3px;'>💡 {note}</div>" if note else ""}
            </div>
        </div>
        {f"<a href='{action_url}' target='_blank' style='background: rgba(255,255,255,0.22); border: 1.5px solid rgba(255,255,255,0.5); color: #ffffff; text-decoration: none; padding: 8px 16px; border-radius: 20px; font-weight: 800; font-size: 0.85rem; white-space: nowrap; box-shadow: 0 2px 6px rgba(0,0,0,0.2);'>{btn_text} ↗</a>" if action_url else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# GLOBÁLIS PRÉMIUM KÉTNYELVŰ RENDSZER (SZINKRONIZÁCIÓ & VÁLTÓ)
# ─────────────────────────────────────────────────────────────

def sync_all_language_defaults(lang: str):
    """Synchronizes all input fields and prompts across all modules upon language change."""
    niche_key = st.session_state.get("zen_niche_sel", list(CHRISTIAN_SUB_NICHES.keys())[0])
    niche_data = CHRISTIAN_SUB_NICHES.get(niche_key, CHRISTIAN_SUB_NICHES[list(CHRISTIAN_SUB_NICHES.keys())[0]])

    if lang == "HU":
        st.session_state["wiz_kdp_title"] = niche_data.get("default_kdp_title_hu", "Noé Bárkája Bibliai Kalandok")
        st.session_state["wiz_kdp_sub"] = niche_data.get("default_kdp_sub_hu", "Inspiráló Bibliai Igés Színezőkönyv Gyermekeknek")
        st.session_state["wiz_etsy_ref"] = "Zsoltárok 23:3"
        st.session_state["wiz_etsy_verse"] = "Lelkemet megvidámítja, az igazság ösvényein vezet engem az ő nevéért."
        st.session_state["wiz_gum_title"] = "30 Napos Békesség a Viharban Áhítat"
        st.session_state["wiz_gum_matrix"] = "[1. Nap | Filippi 4:6-7 | Isten békessége megőrzi a szíveteket | 1. Mi aggaszt ma? 2. Hogyan adod át Istennek? 3. Miért lehetsz hálás ma?]"
    else:
        st.session_state["wiz_kdp_title"] = niche_data.get("default_kdp_title_en", "Noah's Ark Bible Adventures")
        st.session_state["wiz_kdp_sub"] = niche_data.get("default_kdp_sub_en", "Inspiring Bible Verse Coloring Book for Children")
        st.session_state["wiz_etsy_ref"] = "Psalm 23:3"
        st.session_state["wiz_etsy_verse"] = "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake."
        st.session_state["wiz_gum_title"] = "30 Days of Peace in the Storm Devotional Journal"
        st.session_state["wiz_gum_matrix"] = "[Day 1 | Philippians 4:6-7 | God's peace guards hearts | 1. What worries you today? 2. How do you surrender it? 3. What can you thank God for?]"


def on_niche_change():
    """Callback triggered when Christian sub-niche changes in sidebar."""
    cur_lang = st.session_state.get("app_global_lang", "HU")
    sync_all_language_defaults(cur_lang)


def render_sleek_language_bar(key_suffix: str = "") -> bool:
    """Renders dual interactive language buttons with instant, collision-free global sync."""
    if "app_global_lang" not in st.session_state:
        st.session_state["app_global_lang"] = "HU"

    cur_lang = st.session_state["app_global_lang"]
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        is_hu_active = (cur_lang == "HU")
        if st.button("🇭🇺 Magyar", key=f"btn_lang_hu_{key_suffix}", type="primary" if is_hu_active else "secondary", use_container_width=True):
            if cur_lang != "HU":
                st.session_state["app_global_lang"] = "HU"
                sync_all_language_defaults("HU")
                st.rerun()
    with col_l2:
        is_en_active = (cur_lang == "EN")
        if st.button("🇺🇸 English", key=f"btn_lang_en_{key_suffix}", type="primary" if is_en_active else "secondary", use_container_width=True):
            if cur_lang != "EN":
                st.session_state["app_global_lang"] = "EN"
                sync_all_language_defaults("EN")
                st.rerun()

    return st.session_state["app_global_lang"] == "HU"


# ─────────────────────────────────────────────────────────────
# 1. ÚTVONAL: AMAZON KDP KÖNYV PIPELINE (5-LÉPÉSES WIZARD)
# ─────────────────────────────────────────────────────────────

def render_kdp_pipeline_wizard(km):
    if "kdp_page_count" not in st.session_state:
        st.session_state["kdp_page_count"] = 10
    if "kdp_trim" not in st.session_state:
        st.session_state["kdp_trim"] = "8.5x11"
    
    current_pages = st.session_state.get("kdp_page_count", 10)
    current_trim = st.session_state.get("kdp_trim", "8.5x11")
    current_title = st.session_state.get("kdp_title", st.session_state.get("wiz_kdp_title", "Noah's Ark Bible Adventures"))

    # ── Fejléc és Nyelvválasztó Sáv ──
    h_col1, h_col2 = st.columns([1.6, 1.4])
    with h_col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(2, 132, 199, 0.15), rgba(15, 23, 42, 0.9)); border: 1px solid #0284c7; border-radius: 12px; padding: 12px 18px; margin-bottom: 14px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <h3 style='margin:0; color:#38bdf8; font-size:1.25rem;'>📘 1. Útvonal: Amazon KDP Könyv Pipeline</h3>
                <div>
                    <span class='param-badge'>📖 {current_pages} Oldal</span>
                    <span class='param-badge'>📐 {current_trim}</span>
                </div>
            </div>
            <p style='margin:3px 0 0 0; color:#94a3b8; font-size:0.84rem;'>Projekt: <strong>{current_title}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div style='font-size:0.78rem; font-weight:700; color:#38bdf8; margin-bottom:4px;'>🌐 KIADVÁNY NYELVE / LANGUAGE:</div>", unsafe_allow_html=True)
        is_hu = render_sleek_language_bar("kdp")

    if "wiz_kdp_title" not in st.session_state:
        st.session_state["wiz_kdp_title"] = "Noé Bárkája Bibliai Kalandok" if is_hu else "Noah's Ark Bible Adventures"
    if "wiz_kdp_sub" not in st.session_state:
        st.session_state["wiz_kdp_sub"] = "Inspiráló Bibliai Igés Színezőkönyv Gyermekeknek" if is_hu else "Inspiring Bible Verse Coloring Book for Children"

    kdp_steps = [
        f"1. Cél ({current_pages}p)" if is_hu else f"1. Goal ({current_pages}p)",
        f"2. Vázlat ({current_pages}p)" if is_hu else f"2. Outline ({current_pages}p)",
        f"3. Promptek ({current_pages}p)" if is_hu else f"3. Prompts ({current_pages}p)",
        "4. Borító" if is_hu else "4. Cover",
        "5. Nyomdai PDF" if is_hu else "5. Print PDF"
    ]

    if "kdp_step" not in st.session_state:
        st.session_state["kdp_step"] = 0

    cur_step = st.session_state["kdp_step"]
    render_stepper(kdp_steps, cur_step, "kdp")

    # ── 1. LÉPÉS: NICHE, OLDALSZÁM & FELADAT-SPECIFIKUS STÍLUS ──
    if cur_step == 0:
        render_ai_tool_badge("gemini", "A könyvcím, alcím és illusztrációs stílus meghatározásához használd a Geminit vagy az alábbi KDP stílusokat." if is_hu else "Use Gemini or the presets below to fine-tune your book title, subtitle, and art style.")
        st.markdown(f"#### 🎯 1. Lépés: Könyv Cél, Cím, Stílus és Oldalszám Beállítása" if is_hu else "#### 🎯 Step 1: Book Goal, Title, Style & Page Count")
        
        c1, c2 = st.columns([1.2, 1.0])
        with c1:
            title = st.text_input("Könyv Főcíme:" if is_hu else "Main Book Title:", key="wiz_kdp_title")
            subtitle = st.text_input("Alcím:" if is_hu else "Subtitle:", key="wiz_kdp_sub")
            
            kdp_style = st.selectbox(
                "🎨 KDP Művészeti & Vizuális Stílus:" if is_hu else "🎨 KDP Artistic & Visual Style:",
                options=list(KDP_TASK_STYLES.keys()),
                key="wiz_kdp_style_select"
            )
            st.session_state["kdp_chosen_style"] = kdp_style
            st.session_state["kdp_is_adult"] = KDP_TASK_STYLES[kdp_style]["is_adult"]

        with c2:
            trim = st.selectbox("KDP Formátum (Trim Size):", ["8.5x11", "8.5x8.5", "8x10", "6x9"], index=0, key="wiz_kdp_trim")
            page_count = st.slider("Színező / Illusztrált Oldalak Száma:" if is_hu else "Number of Coloring / Illustrated Pages:", 4, 30, value=st.session_state.get("kdp_page_count", 10), key="wiz_kdp_pages")
            
            st.markdown(f"""
            <div class='zen-card'>
                <strong style='color:#38bdf8;'>📖 {'Beállított Paraméterek' if is_hu else 'Configured Parameters'}:</strong><br>
                • <strong>{'Tervezett terjedelem' if is_hu else 'Target Volume'}:</strong> <span style='color:#10b981; font-weight:800;'>{page_count} {'egyedi illusztrált oldal' if is_hu else 'unique illustrated pages'}</span><br>
                • <strong>{'Kiválasztott stílus' if is_hu else 'Chosen Style'}:</strong> <code>{KDP_TASK_STYLES[kdp_style]['prompt_mod']}</code>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Mentés és Tovább a Vázlathoz ➔" if is_hu else "Save & Continue to Outline ➔", type="primary", use_container_width=True):
            st.session_state["kdp_title"] = title
            st.session_state["kdp_subtitle"] = subtitle
            st.session_state["kdp_trim"] = trim
            st.session_state["kdp_page_count"] = page_count
            st.session_state["kdp_step"] = 1
            st.rerun()

    # ── 2. LÉPÉS: VÁZLAT & KJV IGÉK (PONTOS OLDALSZÁM BIZTOSÍTÁSÁVAL) ──
    elif cur_step == 1:
        render_ai_tool_badge("notebooklm", "A KJV Biblia feltöltve a NotebookLM-be hallucinációmentes igehelyeket és jeleneteket biztosít ➔ ezt fejtjük ki a Geminivel." if is_hu else "Upload KJV Bible into NotebookLM for hallucination-free scriptures ➔ expand scenes with Gemini.")
        st.markdown(f"#### 📖 2. Lépés: '{st.session_state.get('kdp_title', current_title)}' Sorszámozott Vázlata ({current_pages} Oldal)" if is_hu else f"#### 📖 Step 2: '{st.session_state.get('kdp_title', current_title)}' Sequential Outline ({current_pages} Pages)")
        st.caption(f"Az AI pontosan {current_pages} db bibliai igehelyet és 4K képgeneráló promptot készít ({'Magyarul' if is_hu else 'Angolul'}).")

        target_p = st.session_state.get("kdp_page_count", 10)
        style_choice = st.session_state.get("kdp_chosen_style", list(KDP_TASK_STYLES.keys())[0])
        style_mod = KDP_TASK_STYLES.get(style_choice, {}).get("prompt_mod", "")

        btn_txt = f"✨ Pontosan {target_p} Oldalas Vázlat Generálása (AI)" if is_hu else f"✨ Generate Exactly {target_p}-Page Outline (AI)"
        if st.button(btn_txt, use_container_width=True, type="primary"):
            with st.spinner(f"AI generálja a pontosan {target_p} oldalas könyvvázlatot..."):
                prompt = build_kdp_autopilot_manifest_prompt(
                    book_title=st.session_state.get("kdp_title", current_title),
                    theme=st.session_state.get("kdp_title", current_title),
                    target_audience="Adult" if st.session_state.get("kdp_is_adult") else "Child",
                    page_count=target_p,
                    is_adult=st.session_state.get("kdp_is_adult", False)
                )
                lang_sys = f"Kizárólag magyar nyelven válaszolj, és pontosan {target_p} db sorszámozott jelenetet készíts." if is_hu else f"Respond strictly in English with exactly {target_p} sequential biblical scenes."
                ok, resp = km.generate_text_with_fallback(prompt=prompt, system_instruction=f"Te egy KDP kiadói szakértő vagy. {lang_sys}", model_name="groq-llama-3.3-70b")
                
                raw_scenes = parse_kdp_autopilot_manifest_json(resp)
                exact_scenes = ensure_exact_page_count(raw_scenes, target_p, is_hu, style_mod)
                st.session_state["kdp_scenes_manifest"] = exact_scenes
                st.success(f"✅ Sorszámozott könyvvázlat sikeresen elkészült mind a(z) {len(exact_scenes)} oldalhoz!" if is_hu else f"✅ Sequential outline generated for all {len(exact_scenes)} pages!")

        scenes = st.session_state.get("kdp_scenes_manifest", [])
        if scenes:
            st.markdown(f"**{'Legenerált Jelenetek' if is_hu else 'Generated Scenes'} ({len(scenes)} / {target_p} {'oldal' if is_hu else 'pages'}):**")
            for sc in scenes:
                st.info(f"**{'Oldal' if is_hu else 'Page'} {sc.get('page_number')}: {sc.get('title')}** (`{sc.get('scripture_reference')}`)\n\n*Ige:* \"{sc.get('scripture_text', '')}\"\n\n*Prompt:* {sc.get('visual_prompt')}")

            # 💾 Save to Vault Button
            v_content_text = "\n\n".join([f"Page {s['page_number']}: {s['title']} ({s['scripture_reference']})\nVerse: {s['scripture_text']}\nPrompt: {s['visual_prompt']}" for s in scenes])
            if st.button("💾 Vázlat Mentése a Mentett Dolgokba (Vault)" if is_hu else "💾 Save Outline to Vault", use_container_width=True):
                add_to_saved_vault(
                    title=f"KDP Vázlat ({len(scenes)}p): {st.session_state.get('kdp_title', current_title)}",
                    category="💡 Témák & Vázlatok",
                    content=v_content_text,
                    pipeline="Amazon KDP"
                )
                st.success("✅ Vázlat sikeresen elmentve a Vezérlő Hub Mentett Dolgok tárába!" if is_hu else "✅ Outline saved to Control Hub Vault!")

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Címhez" if is_hu else "⬅️ Back to Title", use_container_width=True):
                st.session_state["kdp_step"] = 0
                st.rerun()
        with c_b2:
            if st.button(f"Tovább a Gemini Gemhez & {target_p} db Promptekhez ➔" if is_hu else f"Continue to Gemini Gem & {target_p} Prompts ➔", type="primary", use_container_width=True):
                st.session_state["kdp_step"] = 2
                st.rerun()

    # ── 3. LÉPÉS: GEMINI CUSTOM GEM & 4K PROMPTEK (MINDEN OLDALHOZ) ──
    elif cur_step == 2:
        render_ai_tool_badge("gemini", "A 4K képeket mindig a Gemini webes felületén hozzuk létre a lenti Custom Gem leírással, így a stílus és a karakterek 100%-ban azonosak maradnak." if is_hu else "Generate 4K images on Gemini Web using the Custom Gem instruction below for 100% character and style consistency.")
        
        target_p = st.session_state.get("kdp_page_count", 10)
        book_title = st.session_state.get('kdp_title', current_title)
        style_choice = st.session_state.get("kdp_chosen_style", list(KDP_TASK_STYLES.keys())[0])
        style_prompt = KDP_TASK_STYLES.get(style_choice, {}).get("prompt_mod", "")

        gem_instruction = build_gemini_custom_gem_instructions(
            gem_type="kdp_coloring",
            project_title=book_title,
            style_name=style_prompt
        )

        st.markdown(f"#### 💎 Gemini Custom Gem {'Rendszerutasítás' if is_hu else 'System Instruction'} ({target_p} {'Oldalas Kiadványhoz' if is_hu else 'Pages'})")
        st.caption("Másold be ezt az utasítást a Gemini 'Custom Gems' létrehozó felületére a garantált stílus- és karakterkonzisztenciához:" if is_hu else "Copy this instruction into Gemini Custom Gems creator for guaranteed style consistency:")
        st.code(gem_instruction, language="markdown")

        st.markdown("---")
        st.markdown(f"#### 📋 {'Mind a(z)' if is_hu else 'All'} {target_p} {'Oldal 4K Képpromptja a Gemini Webhez:' if is_hu else 'Page 4K Image Prompts for Gemini Web:'}")

        raw_scenes = st.session_state.get("kdp_scenes_manifest", [])
        scenes = ensure_exact_page_count(raw_scenes, target_p, is_hu, style_prompt)

        for sc in scenes:
            with st.expander(f"🖼️ {'Oldal' if is_hu else 'Page'} {sc.get('page_number')} / {target_p}: {sc.get('title')} ({sc.get('scripture_reference', '')})", expanded=False):
                st.text_area(f"{'Másolható Prompt' if is_hu else 'Copyable Prompt'} ({'Oldal' if is_hu else 'Page'} {sc.get('page_number')}):", value=sc.get('visual_prompt', ''), height=75, key=f"kdp_sc_p_{sc.get('page_number')}")

        # 💾 Save Prompts & Gem to Vault Button
        full_prompts_payload = f"=== GEMINI CUSTOM GEM INSTRUCTION ===\n{gem_instruction}\n\n=== 4K IMAGE PROMPTS ({len(scenes)} PAGES) ===\n" + "\n".join([f"Page {s['page_number']}: {s['visual_prompt']}" for s in scenes])
        if st.button("💾 Gemini Custom Gem & 4K Promptek Mentése a Vaultba" if is_hu else "💾 Save Gem & 4K Prompts to Vault", use_container_width=True):
            add_to_saved_vault(
                title=f"KDP Promptek ({len(scenes)}p): {book_title}",
                category="🖼️ 4K Gemini Promptek",
                content=full_prompts_payload,
                pipeline="Amazon KDP"
            )
            st.success("✅ Promptek és Gem utasítás sikeresen mentve a Mentett Dolgokba!" if is_hu else "✅ Prompts & Gem saved to Vault!")

        st.markdown("---")
        st.markdown(f"#### 📥 {'Gemini Webről Letöltött Képek Feltöltése (Opcionális - Nyomdai PDF-hez)' if is_hu else 'Upload Downloaded Images from Gemini Web (Optional - for Print PDF)'}")
        st.caption(f"Ha a Gemini Webes felületén letöltötted a kész 4K képeket ({target_p} db), húzd be őket ide, és az 5. lépésben a ReportLab automatikusan összefűzi a nyomdakész PDF-et:" if is_hu else f"Upload your {target_p} images saved from Gemini Web for automatic ReportLab PDF assembly:")
        uploaded_imgs = st.file_uploader(f"{'Kész képek feltöltése' if is_hu else 'Upload finished images'} ({target_p} {'oldalhoz' if is_hu else 'pages'}):", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="kdp_user_uploaded_images")
        if uploaded_imgs:
            st.session_state["kdp_uploaded_images_list"] = uploaded_imgs
            st.success(f"✅ {len(uploaded_imgs)} db kép feltöltve a {target_p} oldalas kiadványhoz!" if is_hu else f"✅ {len(uploaded_imgs)} images uploaded for {target_p}-page book!")

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Vázlathoz" if is_hu else "⬅️ Back to Outline", use_container_width=True):
                st.session_state["kdp_step"] = 1
                st.rerun()
        with c_b2:
            if st.button("Tovább a Borító & Gerinc Kalkulációhoz ➔" if is_hu else "Continue to Cover & Spine Math ➔", type="primary", use_container_width=True):
                st.session_state["kdp_step"] = 3
                st.rerun()

    # ── 4. LÉPÉS: BORÍTÓ & GERINC (PONTOS OLDALSZÁMBÓL SZÁMÍTVA) ──
    elif cur_step == 3:
        render_ai_tool_badge("gemini", "A mértani 17.412:11.25 Wrap-Around borítót a beépített KDP kalkulátor méretezi és a Gemini Web Imagen motorjával generálod." if is_hu else "The wrap-around cover is calculated with KDP math and generated on Gemini Web.")
        
        target_p = st.session_state.get("kdp_page_count", 10)
        cov_calc = calculate_kdp_cover_dimensions(page_count=target_p, trim_size_str="8.5x11", paper_type="white")

        st.markdown(f"#### 📐 4. Lépés: KDP Wrap-Around Borító & Gerincvastagság ({target_p} Oldalas Kiadvány)" if is_hu else f"#### 📐 Step 4: KDP Wrap-Around Cover & Spine Dimensions ({target_p} Pages)")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class='zen-card'>
                <strong style='color:#38bdf8;'>📐 {'Nyomdai Méretek' if is_hu else 'Print Dimensions'} (8.5×11 Bleed, {target_p} {'oldal' if is_hu else 'pages'}):</strong><br>
                • <strong>{'Belső terjedelme' if is_hu else 'Interior Volume'}:</strong> <span style='color:#10b981; font-weight:800;'>{target_p} {'oldal' if is_hu else 'pages'}</span><br>
                • <strong>{'Teljes borítószélesség' if is_hu else 'Total Cover Width'}:</strong> {cov_calc['total_width_in']:.3f} in ({cov_calc['pixel_width_300dpi']} px)<br>
                • <strong>{'Teljes borítómagasság' if is_hu else 'Total Cover Height'}:</strong> {cov_calc['total_height_in']:.3f} in ({cov_calc['pixel_height_300dpi']} px)<br>
                • <strong>{'Számított gerincvastagság' if is_hu else 'Spine Thickness'}:</strong> <span style='color:#f59e0b; font-weight:800;'>{cov_calc['spine_width_in']:.4f} in</span><br>
                • <strong>{'Képarány' if is_hu else 'Aspect Ratio'}:</strong> <code>17.412:11.25</code>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            cov_prompt = build_kdp_cover_master_prompt(f"{st.session_state.get('kdp_title', current_title)} on calm waters with animals", st.session_state.get('kdp_title', 'BIBLE COLORING BOOK'))
            st.markdown(f"**{'Master Prompt Borítóhoz a Gemini Webre:' if is_hu else 'Master Prompt for Cover on Gemini Web:'}**")
            st.code(cov_prompt, language="text")

            # 💾 Save Cover Prompt to Vault
            if st.button("💾 Borító Prompt Mentése a Vaultba" if is_hu else "💾 Save Cover Prompt to Vault", use_container_width=True):
                add_to_saved_vault(
                    title=f"KDP Borító: {st.session_state.get('kdp_title', current_title)}",
                    category="🖼️ 4K Gemini Promptek",
                    content=cov_prompt,
                    pipeline="Amazon KDP"
                )
                st.success("✅ Borító prompt elmentve a Vaultba!" if is_hu else "✅ Cover prompt saved to Vault!")

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Promptekhez" if is_hu else "⬅️ Back to Prompts", use_container_width=True):
                st.session_state["kdp_step"] = 2
                st.rerun()
        with c_b2:
            if st.button("Tovább a Nyomdai PDF Összeállításhoz ➔" if is_hu else "Continue to Print PDF Assembly ➔", type="primary", use_container_width=True):
                st.session_state["kdp_step"] = 4
                st.rerun()

    # ── 5. LÉPÉS: NYOMDAI PDF ÖSSZEÁLLÍTÁS (REPORTLAB) ──
    elif cur_step == 4:
        render_ai_tool_badge("reportlab", "A ReportLab motor automatikusan összefűzi a feltöltött képeket a bal oldali igés oldalakkal, és kész nyomdai KDP PDF-et generál." if is_hu else "ReportLab engine compiles full print-ready KDP interior PDF.")
        st.markdown(f"#### 🖨️ 5. Lépés: Kész Nyomdakész KDP Belső PDF Összeállítása ({current_pages} Oldal)" if is_hu else f"#### 🖨️ Step 5: Print-Ready KDP Interior PDF Assembly ({current_pages} Pages)")

        uploaded_list = st.session_state.get("kdp_uploaded_images_list", [])
        st.write(f"**{'Feltöltött Képek Állapota' if is_hu else 'Uploaded Images Status'}:** {len(uploaded_list)} / {current_pages} {'db kép rendelkezésre áll' if is_hu else 'images available'}")

        if st.button(f"🚀 {'Nyomdai KDP Belső PDF Generálása' if is_hu else 'Generate Print-Ready KDP Interior PDF'} ({current_pages}p)", type="primary", use_container_width=True):
            with st.spinner("ReportLab motor fordítja a nyomdai PDF-et..."):
                scenes = st.session_state.get("kdp_scenes_manifest", [])
                pdf_bytes = build_kdp_book_pdf(
                    book_title=st.session_state.get('kdp_title', current_title),
                    scenes=scenes,
                    uploaded_images=uploaded_list,
                    trim_size_str="8.5x11",
                    is_hu=is_hu
                )
                st.session_state["kdp_final_pdf_bytes"] = pdf_bytes
                st.success(f"🎉 {'Nyomdakész KDP Belső PDF sikeresen elkészült!' if is_hu else 'Print-ready KDP Interior PDF successfully generated!'}")

        if "kdp_final_pdf_bytes" in st.session_state:
            st.download_button(
                f"📥 {'Nyomdakész KDP Belső PDF Letöltése' if is_hu else 'Download Print-Ready KDP Interior PDF'} (8.5x11)",
                data=st.session_state["kdp_final_pdf_bytes"],
                file_name=f"{st.session_state.get('kdp_title', 'KDP_Book').replace(' ', '_')}_{current_pages}p_Interior.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Borítóhoz" if is_hu else "⬅️ Back to Cover", use_container_width=True):
                st.session_state["kdp_step"] = 3
                st.rerun()
        with c_b2:
            if st.button("🔄 Új KDP Könyv Indítása (Reset)" if is_hu else "🔄 Start New KDP Book (Reset)", use_container_width=True):
                st.session_state["kdp_step"] = 0
                st.rerun()


# ─────────────────────────────────────────────────────────────
# 2. ÚTVONAL: ETSY WALL ART & CLIPART PIPELINE (4-LÉPÉSES WIZARD)
# ─────────────────────────────────────────────────────────────

def render_etsy_pipeline_wizard(km):
    h_col1, h_col2 = st.columns([1.6, 1.4])
    with h_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(15, 23, 42, 0.9)); border: 1px solid #10b981; border-radius: 12px; padding: 12px 18px; margin-bottom: 14px;'>
            <h3 style='margin:0; color:#34d399; font-size:1.25rem;'>🖼️ 2. Útvonal: Etsy Wall Art & Clipart Stúdió</h3>
            <p style='margin:3px 0 0 0; color:#94a3b8; font-size:0.84rem;'>Zárt 4-lépéses munkafolyamat: Koncepció ➔ Gemini Custom Gem ➔ Háttéreltávolítás ➔ 2026 SEO & CSV</p>
        </div>
        """, unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div style='font-size:0.78rem; font-weight:700; color:#34d399; margin-bottom:4px;'>🌐 ETSY NYELV / LANGUAGE:</div>", unsafe_allow_html=True)
        is_hu = render_sleek_language_bar("etsy")

    if "wiz_etsy_ref" not in st.session_state:
        st.session_state["wiz_etsy_ref"] = "Zsoltárok 23:3" if is_hu else "Psalm 23:3"
    if "wiz_etsy_verse" not in st.session_state:
        st.session_state["wiz_etsy_verse"] = "Lelkemet megvidámítja, az igazság ösvényein vezet engem az ő nevéért." if is_hu else "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake."

    etsy_steps = [
        "1. Koncepció & Stílus" if is_hu else "1. Concept & Style",
        "2. Gemini Gem & Promptek" if is_hu else "2. Gemini Gem & Prompts",
        "3. Háttéreltávolítás" if is_hu else "3. Background Removal",
        "4. 2026 SEO & CSV"
    ]

    if "etsy_step" not in st.session_state:
        st.session_state["etsy_step"] = 0

    cur_step = st.session_state["etsy_step"]
    render_stepper(etsy_steps, cur_step, "etsy")

    # ── 1. LÉPÉS: KONCEPCIÓ & FELADAT-SPECIFIKUS STÍLUS ──
    if cur_step == 0:
        render_ai_tool_badge("notebooklm", "A szó szerinti, pontos bibliai igéket a forrásalapú NotebookLM jegyzetfüzetből emeljük át." if is_hu else "Extract literal scripture verses from NotebookLM RAG.")
        st.markdown(f"#### 🌿 1. Lépés: Terméktípus, Igehely és Művészeti Stílus" if is_hu else "#### 🌿 Step 1: Product Type, Scripture Verse & Art Style")
        
        p_type = st.radio("Terméktípus:" if is_hu else "Product Type:", ["🖼️ Skandináv Igés Falikép (4:5 Wall Art)" if is_hu else "🖼️ Scandinavian Scripture Wall Art (4:5)", "✂️ Chibi / Akvarell Clipart Csomag (Fehér Háttér)" if is_hu else "✂️ Chibi / Watercolor Clipart Bundle (1:1 White BG)"], key="wiz_etsy_ptype")
        st.session_state["etsy_is_clipart"] = "Clipart" in p_type

        c1, c2 = st.columns([1.2, 1.0])
        with c1:
            ref = st.text_input("Igehely:" if is_hu else "Scripture Reference:", key="wiz_etsy_ref")
            verse = st.text_area("Szó szerinti Ige:" if is_hu else "Literal Verse Text:", height=70, key="wiz_etsy_verse")
            
            etsy_style = st.selectbox(
                "🎨 Etsy Művészeti & Dekor Stílus:" if is_hu else "🎨 Etsy Art & Decor Style:",
                options=list(ETSY_TASK_STYLES.keys()),
                key="wiz_etsy_style_select"
            )
            st.session_state["etsy_chosen_style"] = etsy_style

        with c2:
            st.markdown(f"""
            <div class='zen-card'>
                <strong style='color:#34d399;'>🎨 {'Kiválasztott Stílus Módosító' if is_hu else 'Selected Style Modifier'}:</strong><br>
                <code>{ETSY_TASK_STYLES[etsy_style]['prompt_mod']}</code><br><br>
                <strong style='color:#cbd5e1;'>🏷️ {'SEO Címkék kiegészítése' if is_hu else 'SEO Tags Addon'}:</strong><br>
                <code>{', '.join(ETSY_TASK_STYLES[etsy_style]['tags_addon'])}</code>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Mentés és Tovább a Gemini Promptekhez ➔" if is_hu else "Save & Continue to Gemini Prompts ➔", type="primary", use_container_width=True):
            st.session_state["etsy_ref"] = ref
            st.session_state["etsy_verse"] = verse
            st.session_state["etsy_step"] = 1
            st.rerun()

    # ── 2. LÉPÉS: GEMINI CUSTOM GEM & 4K PROMPTEK ──
    elif cur_step == 1:
        render_ai_tool_badge("gemini", "A 4K faliképeket és clipartokat a Gemini webes felületén hozzuk létre a lenti Custom Gem és prompt segítségével." if is_hu else "Create 4K wall art and cliparts on Gemini Web with the Custom Gem and prompts below.")
        
        is_clipart = st.session_state.get("etsy_is_clipart", False)
        style_info = ETSY_TASK_STYLES.get(st.session_state.get("etsy_chosen_style", list(ETSY_TASK_STYLES.keys())[0]), {})
        style_prompt = style_info.get("prompt_mod", "")

        etsy_gem_instruction = build_gemini_custom_gem_instructions(
            gem_type="etsy_clipart" if is_clipart else "etsy_wallart",
            project_title=st.session_state.get("etsy_ref", "Etsy Collection"),
            style_name=style_prompt
        )

        st.markdown(f"#### 💎 Gemini Custom Gem {'Rendszerutasítás (Etsy Stílus)' if is_hu else 'System Instruction (Etsy Style)'}")
        st.caption("Másold be ezt a Gemini Custom Gembe a garantáltan egységes skandináv falikép vagy chibi clipart stílushoz:" if is_hu else "Copy into Gemini Custom Gems for 100% consistent art style:")
        st.code(etsy_gem_instruction, language="markdown")

        st.markdown("---")
        st.markdown(f"#### 📋 {'Másolható 4K Master Prompt a Gemini Webhez:' if is_hu else 'Copyable 4K Master Prompt for Gemini Web:'}")

        if is_clipart:
            subject = "young biblical Moses holding the stone tablets" if not is_hu else "fiatal bibliai Mózes a kőtáblákkal"
            prompt_in = f"{build_etsy_clipart_master_prompt(subject)}, {style_prompt}"
        else:
            quote_text = f"{st.session_state.get('etsy_verse', st.session_state.get('wiz_etsy_verse', ''))} - {st.session_state.get('etsy_ref', st.session_state.get('wiz_etsy_ref', ''))}"
            prompt_in = f"An elegant Christian wall art with scripture quote: '{quote_text}', {style_prompt}"

        st.code(prompt_in, language="text")

        # 💾 Save Etsy Prompts to Vault
        if st.button("💾 Etsy Promptek & Gem Mentése a Vaultba" if is_hu else "💾 Save Etsy Prompts & Gem to Vault", use_container_width=True):
            add_to_saved_vault(
                title=f"Etsy Prompt: {st.session_state.get('etsy_ref', 'Etsy Art')}",
                category="🖼️ 4K Gemini Promptek",
                content=f"=== GEMINI CUSTOM GEM ===\n{etsy_gem_instruction}\n\n=== 4K PROMPT ===\n{prompt_in}",
                pipeline="Etsy Wall Art & Clipart"
            )
            st.success("✅ Etsy promptek sikeresen elmentve a Vaultba!" if is_hu else "✅ Etsy prompts saved to Vault!")

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Koncepcióhoz" if is_hu else "⬅️ Back to Concept", use_container_width=True):
                st.session_state["etsy_step"] = 0
                st.rerun()
        with c_b2:
            if st.button("Tovább a Háttéreltávolításhoz ➔" if is_hu else "Continue to BG Removal ➔", type="primary", use_container_width=True):
                st.session_state["etsy_step"] = 2
                st.rerun()

    # ── 3. LÉPÉS: HÁTTÉRELTÁVOLÍTÁS ──
    elif cur_step == 2:
        render_ai_tool_badge("gemini", "A többkörös beszélgetős háttéreltávolításhoz (Transparent PNG) a Gemini Web képszerkesztőjét használjuk." if is_hu else "Use Gemini Web Multi-Turn Conversational Editing to make backgrounds transparent PNG.")
        st.markdown(f"#### ✨ 3. Lépés: Többkörös Beszélgetős Háttéreltávolítás (PNG)" if is_hu else "#### ✨ Step 3: Conversational Background Removal (PNG)")
        st.caption("Használd a Gemini Conversational Editing funkciót a fehér háttér azonnali átlátszóvá tételéhez." if is_hu else "Use conversational commands in Gemini to remove white background instantly.")

        st.markdown(f"""
        <div class='zen-card'>
            <strong style='color:#38bdf8;'>💬 {'Gemini Másolható Utasítás' if is_hu else 'Gemini Copyable Command'}:</strong><br>
            <code>{'Kérlek, távolítsd el a fehér hátteret a fenti grafikák mögül, és tegyed őket teljesen átlátszóvá (transparent PNG format).' if is_hu else 'Please remove the white background behind these illustrations and make them completely transparent (PNG format).'}</code>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Promptekhez" if is_hu else "⬅️ Back to Prompts", use_container_width=True):
                st.session_state["etsy_step"] = 1
                st.rerun()
        with c_b2:
            if st.button("Tovább a 2026 SEO & CSV-hez ➔" if is_hu else "Continue to 2026 SEO & CSV ➔", type="primary", use_container_width=True):
                st.session_state["etsy_step"] = 3
                st.rerun()

    # ── 4. LÉPÉS: 2026 SEO & CSV ──
    elif cur_step == 3:
        render_ai_tool_badge("gemini", "A szigorú 2026-os Etsy SEO címeket (140 kar) és a 13 tag-et a Gemini / Groq és a beépített CSV motor készíti." if is_hu else "Strict 2026 Etsy SEO titles (140 chars) and 13 tags generated with CSV export.")
        st.markdown("#### 🛍️ 4. Lépés: Szigorú 2026-os Etsy SEO & 1-Kattintásos CSV Export" if is_hu else "#### 🛍️ Step 4: Strict 2026 Etsy SEO & 1-Click CSV Export")
        st.caption(f"Cím <= 140 karakter, pontosan 13 tag (egyenként <= 20 karakter!), FFC leírás Drive szállítással ({'Magyarul' if is_hu else 'Angolul'}).")

        cur_ref = st.session_state.get("etsy_ref", st.session_state.get("wiz_etsy_ref", "Psalm 23:3"))
        if is_hu:
            prod_title = f"{cur_ref} Keresztény Falikép Nyomtatható Skandináv Minimalista Igés Poszter"
        else:
            prod_title = f"{cur_ref} Christian Wall Art Printable Scandinavian Minimalist Scripture Poster"

        btn_seo_txt = "✨ 2026-os Etsy SEO Generálása & CSV Előállítása" if is_hu else "✨ Generate 2026 Etsy SEO & Official CSV"
        if st.button(btn_seo_txt, type="primary", use_container_width=True):
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
                st.success("✅ Etsy SEO készlet és CSV elkészült!" if is_hu else "✅ Etsy SEO listing & CSV prepared successfully!")

        seo_res = st.session_state.get("etsy_seo_result", {})
        if seo_res:
            st.markdown(f"**{'Cím' if is_hu else 'Title'} ({len(seo_res.get('title', ''))}/140 {'kar' if is_hu else 'chars'}):** `{seo_res.get('title')}`")
            st.markdown(f"**13 {'Címke' if is_hu else 'Tags'}:** {', '.join([f'`{t}`' for t in seo_res.get('tags', [])])}")
            
            csv_bytes = generate_etsy_csv([{"title": seo_res.get('title'), "description": "High resolution printable digital download.", "price": "6.99", "quantity": "999", "tags": seo_res.get('tags', [])}])
            
            c_e1, c_e2 = st.columns(2)
            with c_e1:
                st.download_button(f"📊 {'Hivatalos Etsy CSV Letöltése' if is_hu else 'Download Official Etsy CSV'}", data=csv_bytes, file_name="Etsy_Listing_2026.csv", mime="text/csv", use_container_width=True)
            with c_e2:
                # 💾 Save SEO to Vault
                if st.button("💾 Etsy 2026 SEO Készlet Mentése a Vaultba" if is_hu else "💾 Save Etsy SEO Set to Vault", use_container_width=True):
                    add_to_saved_vault(
                        title=f"Etsy SEO: {seo_res.get('title', prod_title)[:30]}...",
                        category="🛍️ Etsy SEO Készletek",
                        content=f"Title: {seo_res.get('title')}\nTags: {', '.join(seo_res.get('tags', []))}",
                        pipeline="Etsy Wall Art & Clipart"
                    )
                    st.success("✅ SEO adatok elmentve a Vaultba!" if is_hu else "✅ SEO data saved to Vault!")

        st.markdown("---")
        if st.button("🔄 Új Etsy Termék Indítása (Reset)" if is_hu else "🔄 Start New Etsy Product (Reset)", use_container_width=True):
            st.session_state["etsy_step"] = 0
            st.rerun()


# ─────────────────────────────────────────────────────────────
# 3. ÚTVONAL: GUMROAD ÁHÍTAT & PODCAST PIPELINE (4-LÉPÉSES WIZARD)
# ─────────────────────────────────────────────────────────────

def render_gumroad_pipeline_wizard(km):
    h_col1, h_col2 = st.columns([1.6, 1.4])
    with h_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(15, 23, 42, 0.9)); border: 1px solid #a855f7; border-radius: 12px; padding: 12px 18px; margin-bottom: 14px;'>
            <h3 style='margin:0; color:#c084fc; font-size:1.25rem;'>🎙️ 3. Útvonal: Gumroad Áhítat & Podcast Gyár</h3>
            <p style='margin:3px 0 0 0; color:#94a3b8; font-size:0.84rem;'>Zárt 4-lépéses munkafolyamat: RAG Mátrix ➔ 30 Napos Kézirat ➔ Sales Copy & Audio Upsell ($39) ➔ API</p>
        </div>
        """, unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div style='font-size:0.78rem; font-weight:700; color:#c084fc; margin-bottom:4px;'>🌐 GUMROAD NYELV / LANGUAGE:</div>", unsafe_allow_html=True)
        is_hu = render_sleek_language_bar("gum")

    if "wiz_gum_title" not in st.session_state:
        st.session_state["wiz_gum_title"] = "30 Napos Békesség a Viharban Áhítat" if is_hu else "30 Days of Peace in the Storm Devotional Journal"
    if "wiz_gum_matrix" not in st.session_state:
        st.session_state["wiz_gum_matrix"] = "[1. Nap | Filippi 4:6-7 | Isten békessége megőrzi a szíveteket | 1. Mi aggaszt ma? 2. Hogyan adod át Istennek? 3. Miért lehetsz hálás ma?]" if is_hu else "[Day 1 | Philippians 4:6-7 | God's peace guards hearts | 1. What worries you today? 2. How do you surrender it? 3. What can you thank God for?]"

    gum_steps = [
        "1. NotebookLM RAG",
        "2. Napi Kézirat & Stílus" if is_hu else "2. Daily Manuscript & Tone",
        "3. Copy & Audio ($39)" if is_hu else "3. Copy & Audio ($39)",
        "4. Gumroad Publikálás" if is_hu else "4. Gumroad Publish"
    ]

    if "gum_step" not in st.session_state:
        st.session_state["gum_step"] = 0

    cur_step = st.session_state["gum_step"]
    render_stepper(gum_steps, cur_step, "gum")

    # ── 1. LÉPÉS: NOTEBOOKLM RAG ──
    if cur_step == 0:
        render_ai_tool_badge("notebooklm", "A 30 napos teológiai mátrix táblázatot [Nap | Ige | Tanítás | 3 Kérdés] a forrásalapú NotebookLM építi fel." if is_hu else "Build your 30-day theological matrix table in NotebookLM RAG.")
        st.markdown(f"#### 📓 1. Lépés: Forrásalapú Teológiai Mátrix & KJV Kutatás" if is_hu else "#### 📓 Step 1: Source-Based Theological Matrix & KJV Research")
        c1, c2 = st.columns([1.2, 1.0])
        with c1:
            dev_title = st.text_input("Áhítatos Kötet Címe:" if is_hu else "Devotional Book Title:", key="wiz_gum_title")
            day_num = st.slider("Nap Száma:" if is_hu else "Day Number:", 1, 30, value=st.session_state.get("gum_day", 1), key="wiz_gum_day")
            matrix_row = st.text_area("NotebookLM Mátrix Sor (RAG Forrás):" if is_hu else "NotebookLM Matrix Row (RAG Source):", height=70, key="wiz_gum_matrix")
        with c2:
            st.markdown(f"""
            <div class='zen-card'>
                <strong style='color:#a855f7;'>🧠 {'RAG Előny' if is_hu else 'RAG Advantage'}:</strong><br>
                {'A NotebookLM jegyzetfüzetbe feltöltött KJV Biblia és teológiai jegyzetek megszüntetik a téves idézeteket és a közhelyes AI szövegeket.' if is_hu else 'NotebookLM grounded in KJV scriptures eliminates hallucinated quotes and generic text.'}
            </div>
            """, unsafe_allow_html=True)

            # 💾 Save Matrix to Vault
            if st.button("💾 30 Napos Mátrix Mentése a Vaultba" if is_hu else "💾 Save 30-Day Matrix to Vault", use_container_width=True):
                add_to_saved_vault(
                    title=f"Áhítat Mátrix: {dev_title} (Nap #{day_num})",
                    category="💡 Témák & Vázlatok",
                    content=matrix_row,
                    pipeline="Gumroad Devotionals"
                )
                st.success("✅ Mátrix sor elmentve a Vaultba!" if is_hu else "✅ Matrix row saved to Vault!")

        st.markdown("---")
        if st.button("Mentés és Tovább a Kézirathoz ➔" if is_hu else "Save & Continue to Manuscript ➔", type="primary", use_container_width=True):
            st.session_state["gum_dev_title"] = dev_title
            st.session_state["gum_day"] = day_num
            st.session_state["gum_matrix_row"] = matrix_row
            st.session_state["gum_step"] = 1
            st.rerun()

    # ── 2. LÉPÉS: NAPI KÉZIRAT & FELADAT-SPECIFIKUS TÓNUS STÍLUS ──
    elif cur_step == 1:
        render_ai_tool_badge("gemini", "A 200 szavas mély lelkigondozói reflexiókat, imákat és naplókérdéseket a Gemini Advanced Master Prompt fejti ki." if is_hu else "Expand 200-word pastoral reflections, prayers and journal prompts with Gemini Advanced.")
        st.markdown(f"#### ✍️ 2. Lépés: {st.session_state.get('gum_day', 1)}. Napi Áhítat Kifejtése (Gemini Master Prompt)" if is_hu else f"#### ✍️ Step 2: Day {st.session_state.get('gum_day', 1)} Devotional Manuscript (Gemini Master Prompt)")
        
        gum_style = st.selectbox(
            "✍️ Lelkigondozói & Irodalmi Hangvétel Stílus:" if is_hu else "✍️ Pastoral & Devotional Tone Style:",
            options=list(GUMROAD_TASK_STYLES.keys()),
            key="wiz_gum_style_select"
        )
        st.session_state["gum_chosen_style"] = gum_style
        tone_instruction = GUMROAD_TASK_STYLES[gum_style]["instruction"]

        btn_dev_txt = f"✨ Napi Áhítat Generálása ({'Magyarul' if is_hu else 'Angolul'})" if is_hu else f"✨ Generate Daily Devotional ({'Hungarian' if is_hu else 'English'})"
        if st.button(btn_dev_txt, type="primary", use_container_width=True):
            with st.spinner("AI írja a mély, lelkigondozói szöveget..."):
                base_prompt = build_gumroad_devotional_master_prompt(
                    st.session_state.get("gum_dev_title", st.session_state.get("wiz_gum_title", "Áhítat")),
                    st.session_state.get("gum_day", 1),
                    st.session_state.get("gum_matrix_row", st.session_state.get("wiz_gum_matrix", ""))
                )
                lang_sys = f"Kizárólag mély, hiteles magyar nyelven írj. Stílusutasítás: {tone_instruction}" if is_hu else f"Write strictly in deep, authentic English devotional tone. Style instruction: {tone_instruction}"
                ok, resp = km.generate_text_with_fallback(prompt=base_prompt, system_instruction=lang_sys, model_name="groq-llama-3.3-70b")
                st.session_state["gum_dev_text"] = resp
                st.success("✅ Napi áhítat elkészült!" if is_hu else "✅ Daily devotional text generated!")

        dev_t = st.session_state.get("gum_dev_text", "")
        if dev_t:
            st.markdown("---")
            st.markdown(dev_t)
            c_d1, c_d2 = st.columns(2)
            with c_d1:
                st.download_button(f"📥 {'Kézirat Letöltése' if is_hu else 'Download Manuscript'} (.txt)", data=dev_t, file_name=f"Devotional_Day_{st.session_state.get('gum_day', 1):02d}.txt", mime="text/plain", use_container_width=True)
            with c_d2:
                # 💾 Save Devotional to Vault
                if st.button("💾 Napi Áhítat Mentése a Vaultba" if is_hu else "💾 Save Devotional to Vault", use_container_width=True):
                    add_to_saved_vault(
                        title=f"Kézirat #{st.session_state.get('gum_day', 1)}: {st.session_state.get('gum_dev_title', 'Áhítat')}",
                        category="✍️ Kéziratok & Sales Copy",
                        content=dev_t,
                        pipeline="Gumroad Devotionals"
                    )
                    st.success("✅ Kézirat sikeresen mentve a Vaultba!" if is_hu else "✅ Manuscript saved to Vault!")

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Mátrixhoz" if is_hu else "⬅️ Back to Matrix", use_container_width=True):
                st.session_state["gum_step"] = 0
                st.rerun()
        with c_b2:
            if st.button("Tovább az Értékesítési Szöveghez & Audio Upsellhez ➔" if is_hu else "Continue to Sales Letter & Audio Upsell ➔", type="primary", use_container_width=True):
                st.session_state["gum_step"] = 2
                st.rerun()

    # ── 3. LÉPÉS: SALES COPY & AUDIO UPSELL ($39) ──
    elif cur_step == 2:
        render_ai_tool_badge("notebooklm", "A 10-15 perces Deep Dive Audio Overview (két műsorvezetős MP3 podcast) bónuszt a NotebookLM generálja ($39 upsell)." if is_hu else "Generate 10-15 min Deep Dive Audio Overview podcast in NotebookLM ($39 upsell).")
        st.markdown(f"#### 📜 3. Lépés: Russell Brunson Sales Letter & Audio Upsell ($39)" if is_hu else f"#### 📜 Step 3: Russell Brunson Sales Letter & Audio Upsell ($39)")
        st.caption("A NotebookLM Deep Dive Audio Overview (15 perces MP3 podcast) bónusz $29-ról $39-ra emeli a csomagárat (+$10 tiszta profit)." if is_hu else "NotebookLM Audio Overview companion lifts package value from $29 to $39 (+$10 pure profit).")

        value_stack_content = f"""• {'30 Napos Vezetett Áhítat Napló (PDF): $47 érték' if is_hu else '30-Day Guided Devotional Journal (PDF): $47 Value'}
• {'BÓNUSZ: Deep Dive Audio Overview Podcast (MP3): $19 érték' if is_hu else 'BONUS: Deep Dive Audio Overview Podcast (MP3): $19 Value'}
• {'Nyomtatható Imakártyák: $15 érték' if is_hu else 'Printable Scripture Prayer Cards: $15 Value'}
➔ {'Teljes Prémium Csomag Ár: $39' if is_hu else 'Full Premium Bundle Price: $39'}"""

        st.markdown(f"""
        <div class='zen-card'>
            <strong style='color:#10b981;'>💰 {'Értékhalom (Value Stack)' if is_hu else 'Value Stack'}:</strong><br>
            {value_stack_content.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

        if st.button("💾 Sales Letter & Értékhalom Mentése a Vaultba" if is_hu else "💾 Save Sales Stack to Vault", use_container_width=True):
            add_to_saved_vault(
                title=f"Gumroad Sales Stack: {st.session_state.get('gum_dev_title', 'Áhítat')}",
                category="✍️ Kéziratok & Sales Copy",
                content=value_stack_content,
                pipeline="Gumroad Devotionals"
            )
            st.success("✅ Értékhalom elmentve a Vaultba!" if is_hu else "✅ Sales stack saved to Vault!")

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza a Kézirathoz" if is_hu else "⬅️ Back to Manuscript", use_container_width=True):
                st.session_state["gum_step"] = 1
                st.rerun()
        with c_b2:
            if st.button("Tovább a Gumroad Publikáláshoz ➔" if is_hu else "Continue to Gumroad Publish ➔", type="primary", use_container_width=True):
                st.session_state["gum_step"] = 3
                st.rerun()

    # ── 4. LÉPÉS: GUMROAD PUBLIKÁLÁS ──
    elif cur_step == 3:
        render_ai_tool_badge("gemini", "A termék 1-kattintással közvetlenül publikálható a Gumroad API v2-n keresztül." if is_hu else "Publish product directly via Gumroad API v2.")
        st.markdown(f"#### 🚀 4. Lépés: 1-Kattintásos Gumroad API Publikálás" if is_hu else "#### 🚀 Step 4: 1-Click Gumroad API Publishing")
        p_title = st.session_state.get("gum_dev_title", st.session_state.get("wiz_gum_title", "30 Napos Keresztény Áhítat Csomag"))
        p_price = st.number_input("Termék Ára ($ USD):" if is_hu else "Product Price ($ USD):", min_value=9, max_value=99, value=39)
        p_drive_url = st.text_input("Google Drive Kézbesítési Mappa URL:" if is_hu else "Google Drive Delivery Folder URL:", value="https://drive.google.com/drive/folders/...")

        btn_pub_txt = "🚀 Termék Publikálása Gumroadra (API)" if is_hu else "🚀 Publish Product to Gumroad (API)"
        if st.button(btn_pub_txt, type="primary", use_container_width=True):
            with st.spinner("Publikálás a Gumroad fiókodba..."):
                ok_g, g_url, raw = publish_to_gumroad(product_name=p_title, price_usd=str(p_price), description=f"30-Day Christian Devotional with Bonus MP3 Audio Companion.", drive_delivery_url=p_drive_url)
                if ok_g:
                    st.success(f"🎉 {'Termék sikeresen publikálva! Élő URL:' if is_hu else 'Product published successfully! Live URL:'} {g_url}")
                else:
                    st.error(f"Eredmény: {g_url}")

        st.markdown("---")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("⬅️ Vissza az Értékesítési Szöveghez" if is_hu else "⬅️ Back to Sales Letter", use_container_width=True):
                st.session_state["gum_step"] = 2
                st.rerun()
        with c_b2:
            if st.button("🔄 Új Gumroad Termék Indítása (Reset)" if is_hu else "🔄 Start New Gumroad Project (Reset)", use_container_width=True):
                st.session_state["gum_step"] = 0
                st.rerun()


# ─────────────────────────────────────────────────────────────
# 0. HUB: VEZÉRLŐKÖZPONT, ADÓTERVEZŐ & RENDSZERBEÁLLÍTÁSOK
# ─────────────────────────────────────────────────────────────

def render_central_hub(km):
    h_col1, h_col2 = st.columns([1.6, 1.4])
    with h_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95)); border: 1.5px solid #38bdf8; border-radius: 12px; padding: 14px 18px; margin-bottom: 14px;'>
            <h3 style='margin:0; color:#38bdf8; font-size:1.25rem;'>🏢 0. EV Pénzügyi, Bizonylattár & Központi Hub</h3>
            <p style='margin:3px 0 0 0; color:#94a3b8; font-size:0.84rem;'>2026-os átalányadó tervező, bizonylattár, könyvelői ZIP export, RAG, termék analytics és mentett ötlettár.</p>
        </div>
        """, unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div style='font-size:0.78rem; font-weight:700; color:#f1f5f9; margin-bottom:4px;'>🌐 VEZÉRLŐPULT NYELVE / LANGUAGE:</div>", unsafe_allow_html=True)
        is_hu = render_sleek_language_bar("hub")

    tab_tax, tab_rag, tab_mktg, tab_vision, tab_analytics, tab_vault, tab_settings = st.tabs([
        "🏢 1. EV Pénzügy & Adó" if is_hu else "🏢 1. EV Accounting & Tax",
        "📓 2. NotebookLM RAG" if is_hu else "📓 2. NotebookLM RAG",
        "📌 3. FFC & Pinterest SEO",
        "📷 4. AI Vision Lab",
        "📈 5. Termék & Eladások" if is_hu else "📈 5. Products & Sales",
        "💾 6. Mentett Dolgok (Vault)" if is_hu else "💾 6. Saved Vault",
        "🔑 7. Beállítások & API" if is_hu else "🔑 7. Settings & API Keys"
    ])

    with tab_tax:
        if render_ev_accounting_module:
            render_ev_accounting_module()
        elif render_tax_calculator_2026_module:
            render_tax_calculator_2026_module()
        else:
            st.info("EV Pénzügyi és Adó modul aktív.")

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

    with tab_analytics:
        if render_product_analytics_module:
            render_product_analytics_module()
        else:
            st.info("Termék Analytics modul aktív.")

    with tab_vault:
        if render_saved_vault_module:
            render_saved_vault_module(is_hu)
        else:
            st.info("Mentett Dolgok Tára aktív.")

    with tab_settings:
        st.markdown(f"#### 🔑 {'AI Szolgáltatók & API Kulcsok' if is_hu else 'AI Providers & API Configuration'}")
        st.caption("Automatikus szöveges AI motorok: 1. Groq (Ingyenes) ➔ 2. OpenRouter ➔ 3. Gemini ➔ 4. Offline Sablonok." if is_hu else "Multi-provider AI fallback: 1. Groq (Free) ➔ 2. OpenRouter ➔ 3. Gemini ➔ 4. Offline Templates.")

        cg1, cg2 = st.columns(2)
        with cg1:
            groq_k = st.text_input("Groq API Kulcs (Llama 3.3 70B):", value=km.groq_key, type="password", key="zen_groq_k")
            openr_k = st.text_input("OpenRouter API Kulcs:", value=km.openrouter_key, type="password", key="zen_or_k")
        with cg2:
            gem_k = st.text_input("Google Gemini Fizetős API Kulcs:", value=km.paid_key, type="password", key="zen_gem_k")
            gum_t = st.text_input("Gumroad Access Token:", type="password", key="zen_gum_t")

        if st.button("💾 Kulcsok & Beállítások Mentése" if is_hu else "💾 Save Keys & Configuration", type="primary", use_container_width=True):
            km.save_configuration(paid_key=gem_k, groq_key=groq_k, openrouter_key=openr_k)
            st.success("✅ Beállítások sikeresen mentve!" if is_hu else "✅ Configuration saved successfully!")


# ─────────────────────────────────────────────────────────────
# FŐVEZÉRLŐ ROUTER
# ─────────────────────────────────────────────────────────────

def main():
    inject_zen_css()
    km = get_key_manager()

    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 6px 0 10px 0;'>
            <div style='font-size: 2.2rem;'>✝️</div>
            <h2 style='margin:0; font-size:1.15rem; font-weight:800; color:#f1f5f9;'>Keresztény Munkaállomás</h2>
            <span style='font-size:0.78rem; color:#94a3b8;'>Zen & Flow Pipeline Hub</span>
        </div>
        """, unsafe_allow_html=True)

        # ── Globális Nyelvváltó az Oldalsáv Tetején ──
        st.markdown("<div style='font-size:0.78rem; font-weight:800; color:#38bdf8; margin-bottom:4px;'>🌐 GLOBÁLIS NYELV / LANGUAGE:</div>", unsafe_allow_html=True)
        is_global_hu = render_sleek_language_bar("sidebar")

        st.markdown("---")
        # ── Keresztény Célcsoport & Alkategória Választó ──
        christian_niche_keys = list(CHRISTIAN_SUB_NICHES.keys())
        chosen_niche = st.selectbox(
            "🎯 Keresztény Célcsoport:" if is_global_hu else "🎯 Christian Target Audience:",
            options=christian_niche_keys,
            index=0,
            key="zen_niche_sel",
            on_change=on_niche_change
        )
        st.session_state["active_niche_choice"] = chosen_niche

        st.markdown("---")
        st.markdown("<div style='font-weight:700; color:#38bdf8; font-size:0.85rem; margin-bottom:6px;'>🧭 VÁLASSZ PIPELINE-T:</div>" if is_global_hu else "<div style='font-weight:700; color:#38bdf8; font-size:0.85rem; margin-bottom:6px;'>🧭 SELECT PIPELINE:</div>", unsafe_allow_html=True)

        # ── A 3 Fő Pipeline + 1 Hub (Stabil Kulcsokkal) ──
        nav_keys = ["kdp", "etsy", "gumroad", "hub"]
        nav_labels_hu = {
            "kdp": "📘 1. Amazon KDP Könyv Pipeline",
            "etsy": "🖼️ 2. Etsy Wall Art & Clipart",
            "gumroad": "🎙️ 3. Gumroad Áhítat & Podcast",
            "hub": "🏢 0. EV Pénzügy & Vezérlőközpont Hub"
        }
        nav_labels_en = {
            "kdp": "📘 1. Amazon KDP Book Pipeline",
            "etsy": "🖼️ 2. Etsy Wall Art & Clipart",
            "gumroad": "🎙️ 3. Gumroad Devotional & Podcast",
            "hub": "🏢 0. EV Accounting & Control Hub"
        }

        if "app_active_pipeline_key" not in st.session_state:
            st.session_state["app_active_pipeline_key"] = "kdp"

        cur_saved_nav = st.session_state.get("app_active_pipeline_key", "kdp")
        if cur_saved_nav not in nav_keys:
            cur_saved_nav = "kdp"

        selected_nav = st.radio(
            "Navigáció:",
            options=nav_keys,
            index=nav_keys.index(cur_saved_nav),
            format_func=lambda k: nav_labels_hu[k] if is_global_hu else nav_labels_en[k],
            label_visibility="collapsed",
            key="app_main_nav_radio"
        )
        st.session_state["app_active_pipeline_key"] = selected_nav

        st.markdown("---")
        summary = km.get_summary()
        st.caption(f"⚡ Szöveges AI: {'Groq (Aktív)' if summary.get('has_groq') else 'Offline Sablonok'}")

    # ── Permanens AuDHD 120-Perces Időzítő a legfelső fejlécben ──
    if render_audhd_tracker:
        render_audhd_tracker()

    # ── Munkaterület Routing (Stabil Kulcsok Alapján) ──
    active_nav = st.session_state.get("app_active_pipeline_key", "kdp")
    if active_nav == "kdp":
        render_kdp_pipeline_wizard(km)
    elif active_nav == "etsy":
        render_etsy_pipeline_wizard(km)
    elif active_nav == "gumroad":
        render_gumroad_pipeline_wizard(km)
    elif active_nav == "hub":
        render_central_hub(km)

    # ── Minden oldalon diszkréten elérhető Alsó Gyors-Híd ──
    if render_sidecar_dock:
        st.markdown("---")
        render_sidecar_dock()


if __name__ == "__main__":
    main()
