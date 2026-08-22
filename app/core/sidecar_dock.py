"""
Core Component: Gemini & NotebookLM Asynchronous Sidecar Dock & Built-in Chat Bridge
====================================================================================
Provides an always-accessible bottom drawer / popup bridge across all workspaces:
1. 1-Click Master Prompt Copier & Web App Window Launcher (NotebookLM / Gemini)
2. Live In-App Gemini Pro / Groq Chat Assistant for prompt refining & conversational editing
"""

import os
import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, Any, List

try:
    from core.key_manager import get_key_manager
    from core.prompts_bank import (
        build_kdp_coloring_interior_master_prompt,
        build_kdp_cover_master_prompt,
        build_etsy_wallart_master_prompt,
        build_etsy_clipart_master_prompt,
        build_etsy_bg_removal_prompt,
        build_gumroad_devotional_master_prompt
    )
except (ModuleNotFoundError, ImportError):
    from app.core.key_manager import get_key_manager
    from app.core.prompts_bank import (
        build_kdp_coloring_interior_master_prompt,
        build_kdp_cover_master_prompt,
        build_etsy_wallart_master_prompt,
        build_etsy_clipart_master_prompt,
        build_etsy_bg_removal_prompt,
        build_gumroad_devotional_master_prompt
    )


def render_sidecar_dock():
    """Renders the persistent bottom drawer with 1-Click Clipboard Bridge and Live AI Chat."""
    km = get_key_manager()

    with st.expander("⚡ 🧠 GEMINI & NOTEBOOKLM GYORS-HÍD & BEÉPÍTETT AI CSEVEGŐ", expanded=False):
        tab_bridge, tab_live_chat = st.tabs([
            "📋 1. Prompt Vágólapra Másoló & Lebegő Webes Ablakok",
            "💬 2. Beépített Gemini / Groq Élő Csevegő (Helyben)"
        ])

        # ─────────────────────────────────────────────────────────
        # TAB 1: VÁGÓLAPRA MÁSOLÁS & LEBEGŐ ABLAKOK
        # ─────────────────────────────────────────────────────────
        with tab_bridge:
            st.markdown("##### 🚀 1-Kattintásos Prompt Kiválasztás & Webes Indítás")
            st.caption("Válaszd ki a feladatot, kattints a másolásra, majd nyisd meg az alkalmazást tiszta lebegő ablakban (menüsávok nélkül). Csak egy `Ctrl + V`-t kell nyomnod!")

            c_b1, c_b2 = st.columns([1.2, 1.0])

            with c_b1:
                prompt_category = st.selectbox(
                    "Melyik feladat promptját szeretnéd használni?",
                    [
                        "📖 NotebookLM: KJV 30 Jelenet & Igehely Kutatás (Hétfő)",
                        "📑 NotebookLM: 30 Napos Teológiai Mátrixépítés (Kedd)",
                        "⭐ NotebookLM: Versenytársi Értékelések (Review Mining)",
                        "🎙️ NotebookLM: Deep Dive Audio Overview Podcast Upsell ($39)",
                        "🎨 Gemini: 1. út KDP 4K Fekete-Fehér Színező Belső Oldal",
                        "📘 Gemini: 1. út KDP 17.412:11.25 Gyerekkönyv Borító",
                        "🖼️ Gemini: 2. út Etsy Skandináv Eukaliptusz Igés Falikép",
                        "✂️ Gemini: 2. út Etsy Clipart Csomag (Fehér Háttéren)",
                        "✨ Gemini: 2. út Többkörös Beszélgetős Háttéreltávolítás (PNG)",
                        "✍️ Gemini: 3. út Gumroad 30 Napos Áhítat Napló Kifejtés"
                    ],
                    key="dock_prompt_cat"
                )

                cur_proj = st.session_state.get("current_project_name", "Noah's Ark Bible Adventures")

                # Build prompt text dynamically based on selection
                if "KJV 30 Jelenet" in prompt_category:
                    prompt_text = "Gyűjts ki nekem a feltöltött KJV Bibliából 30 olyan ószövetségi jelenetet, amely gyermekek számára könnyen vizualizálható állatokat vagy látványos eseményeket tartalmaz. Mindegyikhez add meg a pontos igehelyet és az exakt idézetet szó szerint, valamint egy tömör, 1 mondatos angol vizuális leírást."
                    target_app = "NotebookLM"
                    target_url = "https://notebooklm.google.com"
                elif "30 Napos Teológiai Mátrix" in prompt_category:
                    prompt_text = f"A feltöltött teológiai források alapján hozz létre egy 30 napos tematikus áhítat-mátrixot '{cur_proj}' témában az alábbi táblázatos szerkezetben: [Nap száma | Fő KJV igehely | Központi tanítás | 3 elgondolkodtató kérdés]."
                    target_app = "NotebookLM"
                    target_url = "https://notebooklm.google.com"
                elif "Review Mining" in prompt_category:
                    prompt_text = "A feltöltött vásárlói vélemények alapján milyen technikai és tartalmi hibákat említenek a leggyakrabban a vevők (pl. vonalvastagság, túl bonyolult részletek, rossz papírméret, átvérzés), és mi az az 5 konkrét dolog, amivel a mi új termékünk kiemelkedhet?"
                    target_app = "NotebookLM"
                    target_url = "https://notebooklm.google.com"
                elif "Deep Dive Audio" in prompt_category:
                    prompt_text = "Töltsd fel a kész 30 napos kéziratot forrásként a NotebookLM-be, majd a jobb oldali Studio panelen kattints az 'Audio Overview (Deep Dive)' Generálás gombra."
                    target_app = "NotebookLM"
                    target_url = "https://notebooklm.google.com"
                elif "KDP 4K Fekete-Fehér Színező" in prompt_category:
                    prompt_text = build_kdp_coloring_interior_master_prompt("Noah standing on the deck of the ark with two giraffes")
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"
                elif "KDP 17.412:11.25" in prompt_category:
                    prompt_text = build_kdp_cover_master_prompt("Noah's ark on calm waters with animals", "BIBLE COLORING BOOK FOR KIDS")
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"
                elif "Skandináv Eukaliptusz" in prompt_category:
                    prompt_text = build_etsy_wallart_master_prompt("He restores my soul - Psalm 23:3")
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"
                elif "Clipart Csomag" in prompt_category:
                    prompt_text = build_etsy_clipart_master_prompt("young biblical Moses holding the stone tablets")
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"
                elif "Háttéreltávolítás" in prompt_category:
                    prompt_text = build_etsy_bg_removal_prompt()
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"
                else:
                    matrix_sample = st.session_state.get("rag_devotional_matrix", "[Nap 1 | Psalm 23:1-3 | Az Úr gondviselése a belső béke forrása | 1. Miben tapasztaltad ma Isten vezetését?]")
                    prompt_text = build_gumroad_devotional_master_prompt("Reménység a nehéz időkben", 1, matrix_sample.split("\n")[0])
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"

                st.markdown(f"**Másolandó Master Prompt ({target_app}):**")
                st.code(prompt_text, language="text")

            with c_b2:
                st.markdown(f"""
                <div style='background: rgba(15, 23, 42, 0.85); border: 1px solid #38bdf8; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px;'>
                    <strong style='color:#38bdf8;'>🎯 Cél Alkalmazás:</strong> <strong>{target_app}</strong><br>
                    <strong style='color:#34d399;'>⚡ Munkafolyamat:</strong><br>
                    1. Kattints a webes megnyitás gombra.<br>
                    2. A felugró ablakban nyomj <code>Ctrl + V</code>-t.<br>
                    3. Az eredményt azonnal másold vissza a fenti mezőkbe!
                </div>
                """, unsafe_allow_html=True)

                # HTML / JS Popup button for distraction-free app window
                js_launcher_html = f"""
                <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 8px;">
                    <a href="https://notebooklm.google.com" target="_blank" 
                       onclick="window.open('https://notebooklm.google.com', 'NotebookLM_Window', 'width=780,height=900,left=800,top=50,resizable=yes,scrollbars=yes'); return false;"
                       style="display: block; text-align: center; background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #38bdf8; color: #38bdf8; font-weight: bold; padding: 10px 14px; border-radius: 8px; text-decoration: none; font-size: 0.95rem;">
                        🚀 NotebookLM Megnyitása App-Ablakban
                    </a>
                    <a href="https://gemini.google.com" target="_blank" 
                       onclick="window.open('https://gemini.google.com', 'Gemini_Window', 'width=780,height=900,left=800,top=50,resizable=yes,scrollbars=yes'); return false;"
                       style="display: block; text-align: center; background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #a855f7; color: #c084fc; font-weight: bold; padding: 10px 14px; border-radius: 8px; text-decoration: none; font-size: 0.95rem;">
                        💎 Gemini Advanced Megnyitása App-Ablakban
                    </a>
                </div>
                """
                components.html(js_launcher_html, height=110)

        # ─────────────────────────────────────────────────────────
        # TAB 2: BEÉPÍTETT GEMINI / GROQ ÉLŐ CSEVEGŐ
        # ─────────────────────────────────────────────────────────
        with tab_live_chat:
            st.markdown("##### 💬 Beépített Élő AI Asszisztens (Helyben, Ablakváltás Nélkül)")
            st.caption("Használd ezt a közvetlen csevegőt szövegek finomhangolására, teológiai kérdésekre vagy prompt átalakításra.")

            if "sidecar_messages" not in st.session_state:
                st.session_state["sidecar_messages"] = [
                    {"role": "assistant", "content": "Szia! Én vagyok a beépített Keresztény AI asszisztensed. Miben segíthetek a jelenlegi projektedben?"}
                ]

            for msg in st.session_state["sidecar_messages"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            user_msg = st.chat_input("Írj az AI asszisztensnek (pl. 'Tedd még melegebb hangvételűvé az imát', 'Írj 3 új falikép témát')...", key="sidecar_chat_input")
            if user_msg:
                st.session_state["sidecar_messages"].append({"role": "user", "content": user_msg})
                with st.chat_message("user"):
                    st.markdown(user_msg)

                with st.chat_message("assistant"):
                    with st.spinner("AI gondolkodik..."):
                        ok_c, resp_c = km.generate_text_with_fallback(
                            prompt=user_msg,
                            system_instruction="Te egy kedves, empatikus, teológiailag művelt és kreatív keresztény digitális termékfejlesztő AI asszisztens vagy.",
                            model_name="groq-llama-3.3-70b"
                        )
                        if not ok_c or not resp_c:
                            resp_c = "Sajnálom, nem sikerült kapcsolatba lépni az AI motorral. Kérlek, ellenőrizd az API kulcsaidat a Rendszerbeállítások fülön."

                        st.markdown(resp_c)
                        st.session_state["sidecar_messages"].append({"role": "assistant", "content": resp_c})
