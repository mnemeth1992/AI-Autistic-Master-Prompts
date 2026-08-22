"""
Core Component: Gemini & NotebookLM Asynchronous Sidecar Dock & Built-in Chat Bridge
====================================================================================
Provides an always-accessible bottom drawer / popup bridge across all workspaces:
1. 1-Click Master Prompt Copier & Web App Window Launcher (NotebookLM / Gemini)
2. Live In-App Gemini Pro / Groq Chat Assistant for prompt refining & conversational editing
100% Bilingual (HU / EN).
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
    is_hu = st.session_state.get("app_global_lang", "HU") == "HU"
    km = get_key_manager()

    title_lbl = "⚡ 🧠 GEMINI & NOTEBOOKLM GYORS-HÍD & BEÉPÍTETT AI CSEVEGŐ" if is_hu else "⚡ 🧠 GEMINI & NOTEBOOKLM FAST BRIDGE & IN-APP CHAT"
    with st.expander(title_lbl, expanded=False):
        tab_bridge, tab_live_chat = st.tabs([
            "📋 1. Prompt Másoló & Lebegő Ablakok" if is_hu else "📋 1. Prompt Copier & Floating Windows",
            "💬 2. Beépített Élő Csevegő (Helyben)" if is_hu else "💬 2. In-App Live AI Chat Assistant"
        ])

        # ─────────────────────────────────────────────────────────
        # TAB 1: VÁGÓLAPRA MÁSOLÁS & LEBEGŐ ABLAKOK
        # ─────────────────────────────────────────────────────────
        with tab_bridge:
            st.markdown(f"##### 🚀 {'1-Kattintásos Prompt Kiválasztás & Webes Indítás' if is_hu else '1-Click Prompt Picker & Web Launcher'}")
            st.caption("Válaszd ki a feladatot, kattints a másolásra, majd nyisd meg az alkalmazást tiszta lebegő ablakban. Csak egy Ctrl+V-t kell nyomnod!" if is_hu else "Pick a task, copy prompt, launch web app in distraction-free window, and paste (Ctrl+V)!")

            c_b1, c_b2 = st.columns([1.2, 1.0])

            with c_b1:
                prompt_options_hu = [
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
                ]
                prompt_options_en = [
                    "📖 NotebookLM: KJV 30 Scenes & Scripture Mining (Monday)",
                    "📑 NotebookLM: 30-Day Theological Matrix Building (Tuesday)",
                    "⭐ NotebookLM: Competitor Review Mining (Wednesday)",
                    "🎙️ NotebookLM: Deep Dive Audio Overview Podcast ($39)",
                    "🎨 Gemini: Track 1 KDP 4K Line Art Coloring Page",
                    "📘 Gemini: Track 1 KDP 17.412:11.25 Wrap-Around Cover",
                    "🖼️ Gemini: Track 2 Etsy Scandinavian Eucalyptus Wall Art",
                    "✂️ Gemini: Track 2 Etsy Chibi Clipart (White BG)",
                    "✨ Gemini: Track 2 Multi-Turn Conversational BG Removal (PNG)",
                    "✍️ Gemini: Track 3 Gumroad 30-Day Devotional Journal"
                ]

                prompt_category = st.selectbox(
                    "Melyik feladat promptját szeretnéd használni?" if is_hu else "Which task prompt would you like to copy?",
                    options=prompt_options_hu if is_hu else prompt_options_en,
                    key="dock_prompt_cat"
                )

                cur_proj = st.session_state.get("wiz_kdp_title", "Noah's Ark Bible Adventures")

                # Build prompt text dynamically based on selection
                if "KJV" in prompt_category or "Jelenet" in prompt_category or "Scenes" in prompt_category:
                    if is_hu:
                        prompt_text = "Gyűjts ki nekem a feltöltött KJV Bibliából 30 olyan ószövetségi jelenetet, amely gyermekek számára könnyen vizualizálható állatokat vagy látványos eseményeket tartalmaz. Mindegyikhez add meg a pontos igehelyet és az exakt idézetet szó szerint, valamint egy tömör, 1 mondatos angol vizuális leírást."
                    else:
                        prompt_text = "Extract 30 sequential Old Testament scenes from the uploaded KJV Bible with visual animals and miracles for children. Provide exact scripture reference, literal quote, and 1-sentence English visual description."
                    target_app = "NotebookLM"
                    target_url = "https://notebooklm.google.com"
                elif "Mátrix" in prompt_category or "Matrix" in prompt_category:
                    if is_hu:
                        prompt_text = f"A feltöltött teológiai források alapján hozz létre egy 30 napos tematikus áhítat-mátrixot '{cur_proj}' témában az alábbi táblázatos szerkezetben: [Nap száma | Fő KJV igehely | Központi tanítás | 3 elgondolkodtató kérdés]."
                    else:
                        prompt_text = f"Based on uploaded theological sources, build a 30-day devotional matrix for '{cur_proj}': [Day Number | Core KJV Scripture | Theological Theme | 3 Reflection Prompts]."
                    target_app = "NotebookLM"
                    target_url = "https://notebooklm.google.com"
                elif "Review Mining" in prompt_category or "Értékelések" in prompt_category:
                    if is_hu:
                        prompt_text = "A feltöltött vásárlói vélemények alapján milyen technikai és tartalmi hibákat említenek a leggyakrabban a vevők (pl. vonalvastagság, túl bonyolult részletek, rossz papírméret, átvérzés), és mi az az 5 konkrét dolog, amivel a mi új termékünk kiemelkedhet?"
                    else:
                        prompt_text = "Based on uploaded customer reviews, identify top recurring complaints (bleed-through, thin lines, paper size) and give 5 actionable ways our new product can solve them."
                    target_app = "NotebookLM"
                    target_url = "https://notebooklm.google.com"
                elif "Audio" in prompt_category or "Podcast" in prompt_category:
                    if is_hu:
                        prompt_text = "Töltsd fel a kész 30 napos kéziratot forrásként a NotebookLM-be, majd a jobb oldali Studio panelen kattints az 'Audio Overview (Deep Dive)' Generálás gombra."
                    else:
                        prompt_text = "Upload complete 30-day devotional manuscript into NotebookLM, then click 'Generate' under Audio Overview (Deep Dive) in the right Studio panel."
                    target_app = "NotebookLM"
                    target_url = "https://notebooklm.google.com"
                elif "Színező" in prompt_category or "Coloring" in prompt_category:
                    prompt_text = build_kdp_coloring_interior_master_prompt("Noah standing on the deck of the ark with two giraffes")
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"
                elif "Borító" in prompt_category or "Cover" in prompt_category:
                    prompt_text = build_kdp_cover_master_prompt("Noah's ark on calm waters with animals", "BIBLE COLORING BOOK FOR KIDS")
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"
                elif "Eukaliptusz" in prompt_category or "Wall Art" in prompt_category:
                    prompt_text = build_etsy_wallart_master_prompt("He restores my soul - Psalm 23:3")
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"
                elif "Clipart" in prompt_category:
                    prompt_text = build_etsy_clipart_master_prompt("young biblical Moses holding the stone tablets")
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"
                elif "Háttéreltávolítás" in prompt_category or "Removal" in prompt_category:
                    prompt_text = build_etsy_bg_removal_prompt()
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"
                else:
                    matrix_sample = st.session_state.get("rag_devotional_matrix", "[Nap 1 | Psalm 23:1-3 | Az Úr gondviselése a belső béke forrása | 1. Miben tapasztaltad ma Isten vezetését?]")
                    prompt_text = build_gumroad_devotional_master_prompt("Reménység a nehéz időkben", 1, matrix_sample.split("\n")[0])
                    target_app = "Gemini"
                    target_url = "https://gemini.google.com"

                st.markdown(f"**{'Másolandó Master Prompt' if is_hu else 'Copyable Master Prompt'} ({target_app}):**")
                st.code(prompt_text, language="text")

            with c_b2:
                flow_step1 = "1. Kattints a webes megnyitás gombra." if is_hu else "1. Click the open button below."
                flow_step2 = "2. A felugró ablakban nyomj <code>Ctrl + V</code>-t." if is_hu else "2. In popup window, press <code>Ctrl + V</code>."
                flow_step3 = "3. Az eredményt azonnal másold vissza a fenti mezőkbe!" if is_hu else "3. Paste results back into the fields above!"

                st.markdown(f"""
                <div style='background: rgba(15, 23, 42, 0.85); border: 1px solid #38bdf8; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px;'>
                    <strong style='color:#38bdf8;'>🎯 {'Cél Alkalmazás' if is_hu else 'Target App'}:</strong> <strong>{target_app}</strong><br>
                    <strong style='color:#34d399;'>⚡ {'Munkafolyamat' if is_hu else 'Workflow'}:</strong><br>
                    {flow_step1}<br>
                    {flow_step2}<br>
                    {flow_step3}
                </div>
                """, unsafe_allow_html=True)

                btn_nlm_text = "🚀 NotebookLM Megnyitása App-Ablakban" if is_hu else "🚀 Open NotebookLM App Window"
                btn_gem_text = "💎 Gemini Advanced Megnyitása App-Ablakban" if is_hu else "💎 Open Gemini App Window"

                js_launcher_html = f"""
                <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 8px;">
                    <a href="https://notebooklm.google.com" target="_blank" 
                       onclick="window.open('https://notebooklm.google.com', 'NotebookLM_Window', 'width=780,height=900,left=800,top=50,resizable=yes,scrollbars=yes'); return false;"
                       style="display: block; text-align: center; background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #38bdf8; color: #38bdf8; font-weight: bold; padding: 10px 14px; border-radius: 8px; text-decoration: none; font-size: 0.95rem;">
                        {btn_nlm_text}
                    </a>
                    <a href="https://gemini.google.com" target="_blank" 
                       onclick="window.open('https://gemini.google.com', 'Gemini_Window', 'width=780,height=900,left=800,top=50,resizable=yes,scrollbars=yes'); return false;"
                       style="display: block; text-align: center; background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #a855f7; color: #c084fc; font-weight: bold; padding: 10px 14px; border-radius: 8px; text-decoration: none; font-size: 0.95rem;">
                        {btn_gem_text}
                    </a>
                </div>
                """
                components.html(js_launcher_html, height=110)

        # ─────────────────────────────────────────────────────────
        # TAB 2: BEÉPÍTETT GEMINI / GROQ ÉLŐ CSEVEGŐ
        # ─────────────────────────────────────────────────────────
        with tab_live_chat:
            st.markdown(f"##### 💬 {'Beépített Élő AI Asszisztens (Helyben, Ablakváltás Nélkül)' if is_hu else 'In-App Live AI Assistant (No Context Switching)'}")
            st.caption("Használd ezt a közvetlen csevegőt szövegek finomhangolására vagy prompt átalakításra." if is_hu else "Use this chat for instant prompt rewriting or devotional copy tweaks.")

            if "sidecar_messages" not in st.session_state:
                welcome_msg = "Szia! Én vagyok a beépített Keresztény AI asszisztensed. Miben segíthetek a jelenlegi projektedben?" if is_hu else "Hello! I am your in-app Christian AI assistant. How can I help with your project today?"
                st.session_state["sidecar_messages"] = [
                    {"role": "assistant", "content": welcome_msg}
                ]

            for msg in st.session_state["sidecar_messages"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            chat_placeholder = "Írj az AI asszisztensnek (pl. 'Tedd még melegebb hangvételűvé az imát')..." if is_hu else "Chat with AI assistant (e.g. 'Make the prayer tone warmer')..."
            user_msg = st.chat_input(chat_placeholder, key="sidecar_chat_input")
            if user_msg:
                st.session_state["sidecar_messages"].append({"role": "user", "content": user_msg})
                with st.chat_message("user"):
                    st.markdown(user_msg)

                with st.chat_message("assistant"):
                    with st.spinner("AI gondolkodik..." if is_hu else "AI thinking..."):
                        sys_inst = "Te egy kedves, empatikus, teológiailag hiteles keresztény digitális termékfejlesztő asszisztens vagy." if is_hu else "You are an empathetic, authentic Christian digital product creator assistant."
                        ok_c, resp_c = km.generate_text_with_fallback(
                            prompt=user_msg,
                            system_instruction=sys_inst,
                            model_name="groq-llama-3.3-70b"
                        )
                        if not ok_c or not resp_c:
                            resp_c = "Sajnálom, nem sikerült kapcsolatba lépni az AI motorral." if is_hu else "Sorry, could not connect to AI engine."

                        st.markdown(resp_c)
                        st.session_state["sidecar_messages"].append({"role": "assistant", "content": resp_c})
