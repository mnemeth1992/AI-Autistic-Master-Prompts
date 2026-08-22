"""
Központi Mentett Dolgok, Ötletek & Projekttár Modul (Saved Vault)
================================================================
Automatikus és manuális mentési központ: témák, 30 napos vázlatok, 4K Gemini promptek,
Gemini Custom Gem leírások, 2026 Etsy SEO címkék, kéziratok és sales szövegek.
"""

import os
import io
import json
import uuid
import datetime
from typing import List, Dict, Any, Tuple
import streamlit as st

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(CURRENT_DIR)
ROOT_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data", "ev_data")
os.makedirs(DATA_DIR, exist_ok=True)

SAVED_VAULT_FILE = os.path.join(DATA_DIR, "saved_vault.json")


def load_saved_vault() -> List[Dict[str, Any]]:
    """Loads all saved items, ideas, prompts and manuscripts from disk."""
    if os.path.exists(SAVED_VAULT_FILE):
        try:
            with open(SAVED_VAULT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []


def save_saved_vault(vault: List[Dict[str, Any]]):
    """Saves the vault items to local disk."""
    with open(SAVED_VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(vault, f, ensure_ascii=False, indent=2)


def add_to_saved_vault(title: str, category: str, content: str, pipeline: str = "Általános", tags: List[str] = None) -> bool:
    """Adds a new item to the persistent saved items vault."""
    vault = load_saved_vault()
    new_item = {
        "id": f"vault-{str(uuid.uuid4())[:8]}",
        "title": title,
        "category": category,
        "pipeline": pipeline,
        "content": content,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "tags": tags or [pipeline, category]
    }
    vault.insert(0, new_item)
    save_saved_vault(vault)
    return True


def render_saved_vault_module(is_hu: bool = True):
    """Renders the comprehensive Saved Items & Ideas Vault inside the Control Hub."""
    vault = load_saved_vault()

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(15, 23, 42, 0.95)); border: 1.5px solid #f59e0b; border-radius: 14px; padding: 14px 20px; margin-bottom: 18px; box-shadow: 0 4px 16px rgba(0,0,0,0.25);'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;'>
            <div>
                <h3 style='margin:0; color:#fbbf24; font-size:1.3rem;'>💾 {'Mentett Dolgok, Ötletek & Prompt Tár' if is_hu else 'Saved Items, Ideas & Prompts Vault'}</h3>
                <p style='margin:3px 0 0 0; color:#94a3b8; font-size:0.86rem;'>
                    {'Minden elmentett témaötlet, 30 napos vázlat, 4K Gemini képprompt, SEO lista és kézirat egyetlen biztonságos helyen.' if is_hu else 'All saved topic ideas, 30-day outlines, 4K Gemini prompts, SEO sets, and manuscripts in one secure vault.'}
                </p>
            </div>
            <div>
                <span class='param-badge'>📑 {len(vault)} {'Mentett Elem' if is_hu else 'Saved Items'}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action Toolbar
    col_t1, col_t2 = st.columns([1.5, 1.0])
    with col_t1:
        cat_filter = st.selectbox(
            "🔍 Szűrés Kategória Szerint:" if is_hu else "🔍 Filter by Category:",
            options=["Mind / All", "💡 Témák & Vázlatok", "🖼️ 4K Gemini Promptek", "💎 Gemini Custom Gems", "🛍️ Etsy SEO Készletek", "✍️ Kéziratok & Sales Copy", "📓 NotebookLM RAG"],
            key="vault_cat_filter"
        )
    with col_t2:
        if st.button("🗑️ Minden Mentett Elem Törlése" if is_hu else "🗑️ Clear All Vault Items", type="secondary", use_container_width=True):
            save_saved_vault([])
            st.success("✅ A mentett tár teljesen kiürítve!" if is_hu else "✅ Vault cleared successfully!")
            st.rerun()

    # Manual Add Item Expander
    with st.expander("➕ Új Saját Jegyzet / Prompt Mentése Manuálisan" if is_hu else "➕ Manually Save New Note / Prompt", expanded=False):
        with st.form("manual_vault_add_form"):
            ca1, ca2 = st.columns(2)
            with ca1:
                v_title = st.text_input("Cím / Megnevezés:" if is_hu else "Title / Name:", placeholder="Pl. Dániel Oroszlánok Vermében 10 Képprompt")
                v_cat = st.selectbox("Kategória:" if is_hu else "Category:", [
                    "💡 Témák & Vázlatok",
                    "🖼️ 4K Gemini Promptek",
                    "💎 Gemini Custom Gems",
                    "🛍️ Etsy SEO Készletek",
                    "✍️ Kéziratok & Sales Copy",
                    "📓 NotebookLM RAG"
                ])
            with ca2:
                v_pipe = st.selectbox("Kapcsolódó Pipeline:" if is_hu else "Related Pipeline:", ["Amazon KDP", "Etsy Wall Art & Clipart", "Gumroad Devotionals", "Központi Hub / RAG"])

            v_content = st.text_area("Mentendő Tartalom / Prompt / Szöveg:" if is_hu else "Content / Prompt / Text:", height=120)
            
            sub_vault = st.form_submit_button("💾 Mentés a Mentett Dolgokba" if is_hu else "💾 Save to Vault", type="primary", use_container_width=True)
            if sub_vault and v_title and v_content:
                add_to_saved_vault(v_title, v_cat, v_content, v_pipe)
                st.success("✅ Elem sikeresen elmentve!" if is_hu else "✅ Item saved successfully!")
                st.rerun()

    st.markdown("---")

    # Filter Items
    if cat_filter != "Mind / All":
        filtered_vault = [item for item in vault if item.get("category") == cat_filter]
    else:
        filtered_vault = vault

    if not filtered_vault:
        st.info("ℹ️ " + ("Jelenleg nincs mentett elem ebben a nézetben. A pipeline-ok lépéseinél a 'Mentés a Vaultba' gombokkal bármikor ide mentheted a vázlatokat és prompteket!" if is_hu else "No saved items found. Click 'Save to Vault' on any pipeline step to archive outlines, prompts and copy!"))
    else:
        for idx, item in enumerate(filtered_vault):
            with st.expander(f"📌 [{item.get('category', 'Jegyzet')}] {item.get('title')} ({item.get('date', '')})", expanded=(idx == 0)):
                st.markdown(f"**Pipeline:** `{item.get('pipeline', 'Általános')}` · **Dátum:** `{item.get('date', '')}`")
                st.code(item.get("content", ""), language="text")

                c_act1, c_act2 = st.columns([1.5, 1.0])
                with c_act1:
                    clean_fn = re.sub(r'[^a-zA-Z0-9_\.-]', '_', item.get('title', 'Vault_Item'))
                    st.download_button(
                        f"⬇️ Letöltés (.txt)" if is_hu else "⬇️ Download (.txt)",
                        data=item.get("content", ""),
                        file_name=f"{clean_fn}.txt",
                        mime="text/plain",
                        key=f"dl_vault_{item.get('id')}_{idx}"
                    )
                with c_act2:
                    if st.button("🗑️ Elem Törlése" if is_hu else "🗑️ Delete Item", key=f"del_vault_{item.get('id')}_{idx}", type="secondary"):
                        vault = [v for v in vault if v.get("id") != item.get("id")]
                        save_saved_vault(vault)
                        st.success("🗑️ Elem törölve!" if is_hu else "🗑️ Item deleted!")
                        st.rerun()
