"""
F5-Proof Project Manager & Session State Persistence
===================================================
Maintains auto-save and 1-click restore functionality across page refreshes
and project switching by persisting state into `projects/<project_name>.json`.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
import streamlit as st

logger = logging.getLogger("ProjectManager")

PROJECTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "projects")
os.makedirs(PROJECTS_DIR, exist_ok=True)

TRACKED_KEYS = [
    # KDP Coloring
    "kdp_book_title", "kdp_book_subtitle", "kdp_target_audience", "kdp_page_count",
    "kdp_trim_size", "kdp_scenes_manifest", "kdp_active_scene_idx", "kdp_generated_images",
    "kdp_character_bible", "kdp_style_mode", "kdp_margin_in", "kdp_show_frame",
    "kdp_show_border", "kdp_show_header", "kdp_show_footer", "kdp_companion_pages",
    "kdp_bleed_protection", "kdp_swatches_tester",
    # KDP Storybook
    "sb_title", "sb_subtitle", "sb_author", "sb_chapters_manifest", "sb_trim_size",
    "sb_target_age", "sb_art_style", "sb_generated_images",
    # KDP Cover
    "cover_page_count", "cover_paper_type", "cover_trim_size", "cover_binding",
    "cover_book_title", "cover_subtitle", "cover_author", "cover_scene_desc",
    "cover_generated_image", "cover_calculated_metrics",
    # Niche & Ideas
    "selected_niche", "custom_topic_prompt", "niche_ideas_list", "bulk_prompts_text",
    # Etsy Wall Art & Clipart
    "etsy_art_title", "etsy_verse_ref", "etsy_verse_text", "etsy_style",
    "etsy_clipart_subject", "etsy_clipart_count", "etsy_seo_data",
    # Gumroad
    "gumroad_product_name", "gumroad_price", "gumroad_devotional_day",
    "gumroad_devotional_text", "gumroad_sales_letter",
    # FFC Marketing
    "ffc_product_name", "ffc_avatar_data", "ffc_hooks_data", "ffc_value_stack_data",
    "ffc_sales_letter_data", "ffc_google_sites_data", "ffc_emails_data", "ffc_social_data"
]


def list_saved_projects() -> List[str]:
    """Returns list of saved project names."""
    if not os.path.exists(PROJECTS_DIR):
        return []
    files = [f[:-5] for f in os.listdir(PROJECTS_DIR) if f.endswith(".json")]
    return sorted(files)


def save_project(project_name: str, extra_state: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    """Serializes current session state into projects/<project_name>.json."""
    if not project_name.strip():
        return False, "A projekt neve nem lehet üres."

    clean_name = "".join(c for c in project_name if c.isalnum() or c in " _-").strip()
    if not clean_name:
        clean_name = "default_project"

    file_path = os.path.join(PROJECTS_DIR, f"{clean_name}.json")

    state_dict = {}
    for k in TRACKED_KEYS:
        if k in st.session_state:
            val = st.session_state[k]
            # Convert non-serializable bytes or complex objects if needed
            if isinstance(val, (bytes, bytearray)):
                continue
            state_dict[k] = val

    if extra_state:
        for k, v in extra_state.items():
            if not isinstance(v, (bytes, bytearray)):
                state_dict[k] = v

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(state_dict, f, ensure_ascii=False, indent=2)
        return True, f"Projekt mentve: {clean_name}"
    except Exception as e:
        logger.error(f"Error saving project {clean_name}: {e}")
        return False, str(e)


def load_project(project_name: str) -> Tuple[bool, str]:
    """Restores session state from projects/<project_name>.json."""
    clean_name = "".join(c for c in project_name if c.isalnum() or c in " _-").strip()
    file_path = os.path.join(PROJECTS_DIR, f"{clean_name}.json")

    if not os.path.exists(file_path):
        return False, f"A '{clean_name}' projektfájl nem található."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in data.items():
            st.session_state[k] = v
        st.session_state["current_project_name"] = clean_name
        return True, f"Projekt sikeresen betöltve: {clean_name}"
    except Exception as e:
        logger.error(f"Error loading project {clean_name}: {e}")
        return False, str(e)


def auto_save_current_project():
    """Silently saves active project state."""
    curr = st.session_state.get("current_project_name", "active_project")
    save_project(curr)
