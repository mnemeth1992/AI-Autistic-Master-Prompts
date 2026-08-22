"""
AuDHD 120-Minute Focus Timer, Phase Tracker & Streak Calendar Engine
===================================================================
Designed specifically for neurodivergent (AuDHD) asynchronous workflows:
  - Permanent, non-collapsing top dashboard with giant real-time ticking LED clock.
  - Emerald Green (< 120m) -> Fiery Red when overtime (> 120m).
  - Synchronous 7-day selector with instant day switching and persistent tasks.
  - Full Hungarian & English bilingual localization.
"""

import os
import json
import time
import datetime
from typing import Dict, Any, List
import streamlit as st
import streamlit.components.v1 as components

TIME_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "time_log.json")

AUDHD_DAY_PLANS_HU = {
    "Hétfő": {
        "title": "🔍 Hétfő: Tiszta Kutatás & RAG Data Mining (NotebookLM & Gemini)",
        "short": "Kutatás & Mining",
        "description": "2 órás mélyfókusz: Amazon/Etsy kulcsszókutatás, 100% pontos KJV igehely- és jelenetkutatás, versenytársi Review Mining.",
        "target_minutes": 120,
        "tasks": [
            "🎯 1. [🌐 Amazon/Etsy] Kulcsszókutatás (High Volume, Low Competition) (30 perc)",
            "📖 2. [📓 NotebookLM] KJV Biblia feltöltése és 30 jelenet/ige kinyerése (30 perc)",
            "⭐ 3. [📓 NotebookLM] Top versenytársak 1-3 csillagos Review Mining elemzése (30 perc)",
            "📁 4. [💾 Drive] Piaci hibák és 5 kiemelkedő termékelőny mentése a projektbe (15 perc)",
            "📋 5. [📓 NotebookLM] Heti termékspecifikációk véglegesítése a RAG fülön (15 perc)"
        ]
    },
    "Kedd": {
        "title": "📑 Kedd: Teológiai Mátrix & Szöveggenerálás (NotebookLM & Gemini)",
        "short": "Mátrix & Szöveg",
        "description": "2 órás mélyfókusz: 30 napos teológiai mátrix felépítése forrásokból, Gemini Advanced Master Prompt futtatás.",
        "target_minutes": 120,
        "tasks": [
            "🕊️ 1. [📓 NotebookLM] Teológiai források feltöltése a jegyzetfüzetbe (20 perc)",
            "📑 2. [📓 NotebookLM] 30 napos táblázatos mátrix legenerálása prompttal (40 perc)",
            "💎 3. [💎 Gemini Advanced] Master Prompt futtatása a mátrix soraihoz (40 perc)",
            "✍️ 4. [💎 Gemini Advanced] 200 szavas reflexiók, imák és 3 kérdés finomhangolása (10 perc)",
            "💾 5. [💾 Drive/Docs] Kész kézirat mentése a 05_GUMROAD mappába (10 perc)"
        ]
    },
    "Szerda": {
        "title": "🎨 Szerda: Vizuális Generálás & Képszerkesztés (Gemini Web)",
        "short": "4K Képek & Clipart",
        "description": "2 órás mélyfókusz: 8.5x11 4K fekete-fehér színezők, 4:5 faliképek, clipart csomagok és többkörös háttéreltávolítás.",
        "target_minutes": 120,
        "tasks": [
            "🎨 1. [💎 Gemini Web] KDP Színező oldalak generálása Custom Gemmel (45 perc)",
            "🖼️ 2. [💎 Gemini Web] Etsy 4:5 Skandináv eukaliptusz faliképek generálása (30 perc)",
            "✂️ 3. [💎 Gemini Web] Clipart illusztrációk generálása fehér háttérrel (25 perc)",
            "✨ 4. [💎 Gemini Web] Többkörös beszélgetős háttéreltávolítás (Transparent PNG) (10 perc)",
            "📁 5. [💾 Drive] Képek mentése és rendszerezése a projektmappákba (10 perc)"
        ]
    },
    "Csütörtök": {
        "title": "📐 Csütörtök: Kiadványszerkesztés & PDF Szerkesztés (ReportLab / Canva)",
        "short": "Kiadvány & PDF",
        "description": "2 órás mélyfókusz: ReportLab nyomdakész KDP belső PDF összeállítása, borító méretezés és Etsy ZIP csomagolás.",
        "target_minutes": 120,
        "tasks": [
            "📖 1. [🖨️ ReportLab] KDP belső PDF összefűzése margókkal és tesztlapokkal (40 perc)",
            "🎨 2. [💎 Gemini / Canva] KDP 17.412:11.25 Wrap-Around borító generálása (35 perc)",
            "🛍️ 3. [📐 Canva / ZIP] Etsy falikép méretcsomagok (4:5, 3:4, 2:3) készítése (25 perc)",
            "📦 4. [📐 ZIP] Clipart PNG csomagok és vásárlói útmutató összeállítása (10 perc)",
            "💾 5. [💾 Drive] Nyomdakész és letöltendő fájlok mentése a Drive-ba (10 perc)"
        ]
    },
    "Péntek": {
        "title": "🚀 Péntek: Automata Publikálás & Audio Upsell (KDP, Etsy, Gumroad)",
        "short": "Publikálás & Audio",
        "description": "2 órás mélyfókusz: Termékfeltöltések, Pinterest passzív SEO leírások és NotebookLM Audio Devotional ($29->$39) generálás.",
        "target_minutes": 120,
        "tasks": [
            "🛍️ 1. [🛍️ KDP / Etsy] Termékek feltöltése 13 SEO taggel és leírással (40 perc)",
            "📌 2. [📌 Pinterest] Passzív SEO címek, leírások és közvetlen linkes pinek (20 perc)",
            "🎙️ 3. [📓 NotebookLM] Audio Overview (Deep Dive MP3 podcast) generálása (35 perc)",
            "💰 4. [🛍️ Gumroad] Termék publikálás + Audio Companion ($39) upsell (15 perc)",
            "🏆 5. [⏱️ Időnapló] Heti fókuszblokkok értékelése és felkészülés a hétvégére (10 perc)"
        ]
    },
    "Szombat": {
        "title": "🌿 Szombat: Pihenés & Regeneráció",
        "short": "Offline Pihenés",
        "description": "Kötelező képernyőmentes idő az idegrendszeri regeneráció és az AuDHD túlterhelődés elkerülése érdekében.",
        "target_minutes": 0,
        "tasks": [
            "🌿 Séta a természetben és képernyőmentes offline pihenés",
            "☕ Családi és baráti kapcsolatok ápolása",
            "📖 Csendes olvasás, offline hobbik, idegrendszeri feltöltődés"
        ]
    },
    "Vasárnap": {
        "title": "🕊️ Vasárnap: Lelki Feltöltődés & Csendesség",
        "short": "Lelki Csendesség",
        "description": "Lelki megújulás, istentisztelet és felkészülés a következő heti 10 órás aszinkron alkotóciklusra.",
        "target_minutes": 0,
        "tasks": [
            "🕊️ Közösség, istentisztelet és hálaadás",
            "🧘 Csendes elmélkedés és lelki megnyugvás",
            "✨ Motivált, békés ráhangolódás a hétfői kutatási napra"
        ]
    }
}

AUDHD_DAY_PLANS_EN = {
    "Monday": {
        "title": "🔍 Monday: Pure Research & RAG Data Mining (NotebookLM & Gemini)",
        "short": "Research & Mining",
        "description": "2-hour deep focus: Amazon/Etsy keyword mining, 100% verified KJV scripture extraction, competitor 1-3 star review mining.",
        "target_minutes": 120,
        "tasks": [
            "🎯 1. [🌐 Amazon/Etsy] Keyword research (High Volume, Low Competition) (30 min)",
            "📖 2. [📓 NotebookLM] Upload KJV Bible & extract 30 scenes/scriptures (30 min)",
            "⭐ 3. [📓 NotebookLM] Competitor 1-3 star review mining & gap analysis (30 min)",
            "📁 4. [💾 Drive] Save market gaps and 5 unique value propositions (15 min)",
            "📋 5. [📓 NotebookLM] Finalize weekly product specifications in RAG tab (15 min)"
        ]
    },
    "Tuesday": {
        "title": "📑 Tuesday: Theological Matrix & Manuscript Generation (NotebookLM & Gemini)",
        "short": "Matrix & Manuscript",
        "description": "2-hour deep focus: Build 30-day grounded theological table, execute Gemini Advanced Master Prompts.",
        "target_minutes": 120,
        "tasks": [
            "🕊️ 1. [📓 NotebookLM] Upload theological source materials into notebook (20 min)",
            "📑 2. [📓 NotebookLM] Generate 30-day structured matrix table with prompt (40 min)",
            "💎 3. [💎 Gemini Advanced] Run Master Prompts for each matrix row (40 min)",
            "✍️ 4. [💎 Gemini Advanced] Polish 200-word reflections, prayers and 3 prompts (10 min)",
            "💾 5. [💾 Drive/Docs] Save complete manuscript into 05_GUMROAD folder (10 min)"
        ]
    },
    "Wednesday": {
        "title": "🎨 Wednesday: Visual Generation & Image Editing (Gemini Web)",
        "short": "4K Art & Clipart",
        "description": "2-hour deep focus: 8.5x11 4K black & white coloring pages, 4:5 wall arts, clipart bundles & multi-turn background removal.",
        "target_minutes": 120,
        "tasks": [
            "🎨 1. [💎 Gemini Web] Generate KDP coloring pages with Custom Gem (45 min)",
            "🖼️ 2. [💎 Gemini Web] Generate Etsy 4:5 Scandinavian eucalyptus wall arts (30 min)",
            "✂️ 3. [💎 Gemini Web] Generate clipart illustrations on pure white BG (25 min)",
            "✨ 4. [💎 Gemini Web] Multi-turn conversational background removal (Transparent PNG) (10 min)",
            "📁 5. [💾 Drive] Save and organize artwork in project folders (10 min)"
        ]
    },
    "Thursday": {
        "title": "📐 Thursday: Publication Layout & PDF Compilation (ReportLab / Canva)",
        "short": "Book Layout & PDF",
        "description": "2-hour deep focus: ReportLab print-ready KDP interior PDF assembly, wrap-around cover math, Etsy ZIP packaging.",
        "target_minutes": 120,
        "tasks": [
            "📖 1. [🖨️ ReportLab] Compile KDP interior PDF with bleed margins & test pages (40 min)",
            "🎨 2. [💎 Gemini / Canva] Generate 17.412:11.25 Wrap-Around KDP cover (35 min)",
            "🛍️ 3. [📐 Canva / ZIP] Prepare Etsy wall art size bundles (4:5, 3:4, 2:3) (25 min)",
            "📦 4. [📐 ZIP] Package clipart PNG sets and user instructions (10 min)",
            "💾 5. [💾 Drive] Archive print-ready files in Google Drive (10 min)"
        ]
    },
    "Friday": {
        "title": "🚀 Friday: Automated Publishing & Audio Upsell (KDP, Etsy, Gumroad)",
        "short": "Publish & Audio",
        "description": "2-hour deep focus: Upload products with 13 SEO tags, Pinterest passive pins, and generate NotebookLM Audio Devotional ($39 upsell).",
        "target_minutes": 120,
        "tasks": [
            "🛍️ 1. [🛍️ KDP / Etsy] Publish listings with 13 SEO tags and copy (40 min)",
            "📌 2. [📌 Pinterest] Schedule passive SEO pins with direct product links (20 min)",
            "🎙️ 3. [📓 NotebookLM] Generate Audio Overview (Deep Dive MP3 podcast) (35 min)",
            "💰 4. [🛍️ Gumroad] Publish product bundle + Audio Companion ($39) upsell (15 min)",
            "🏆 5. [⏱️ Time Log] Review weekly focus streak and prepare for weekend rest (10 min)"
        ]
    },
    "Saturday": {
        "title": "🌿 Saturday: Rest & Nervous System Recovery",
        "short": "Offline Rest",
        "description": "Mandatory screen-free time for nervous system regulation and AuDHD sensory decompression.",
        "target_minutes": 0,
        "tasks": [
            "🌿 Nature walks and screen-free offline relaxation",
            "☕ Nurture family and meaningful friendships",
            "📖 Quiet reading, offline hobbies, sensory recovery"
        ]
    },
    "Sunday": {
        "title": "🕊️ Sunday: Spiritual Renewal & Quiet Reflection",
        "short": "Spiritual Quietness",
        "description": "Spiritual renewal, worship and peaceful grounding for the upcoming weekly 10-hour asynchronous cycle.",
        "target_minutes": 0,
        "tasks": [
            "🕊️ Community, worship, gratitude and prayer",
            "🧘 Quiet contemplation and peace",
            "✨ Grounded and inspired outlook for Monday research"
        ]
    }
}

DAYS_HU = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]
DAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def get_today_index() -> int:
    """Returns today's weekday index (0=Monday, 6=Sunday)."""
    return datetime.datetime.now().weekday()


def load_time_logs() -> List[Dict[str, Any]]:
    """Loads historical focus sessions from time_log.json."""
    if os.path.exists(TIME_LOG_FILE):
        try:
            with open(TIME_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_time_log_entry(entry: Dict[str, Any]) -> bool:
    """Appends a new completed focus session entry into time_log.json."""
    try:
        logs = load_time_logs()
        logs.append(entry)
        with open(TIME_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def get_current_timer_seconds() -> float:
    """Calculates live elapsed seconds from session state."""
    if st.session_state.get("timer_running", False) and st.session_state.get("timer_start_time"):
        return st.session_state.get("timer_elapsed_seconds", 0) + (time.time() - st.session_state["timer_start_time"])
    return st.session_state.get("timer_elapsed_seconds", 0)


def format_seconds_to_hms(seconds: float) -> str:
    """Formats seconds into HH:MM:SS format."""
    secs = int(max(0, seconds))
    hours = secs // 3600
    minutes = (secs % 3600) // 60
    rem_secs = secs % 60
    return f"{hours:02d}:{minutes:02d}:{rem_secs:02d}"


def render_live_clock_html(cur_secs: float, is_running: bool, is_hu: bool = True):
    """Renders giant live client-side ticking digital clock in Emerald Green (or Fiery Red when overtime)."""
    running_js = "true" if is_running else "false"
    normal_status = "🟢 ÉLŐ SZÁMLÁLÁS FOLYAMATBAN..." if is_hu else "🟢 LIVE COUNTING IN PROGRESS..."
    paused_status = "⏸️ Szüneteltetve · 120 perces keret" if is_hu else "⏸️ Paused · 120-minute frame"
    overtime_status = "⚠️ 120 PERC TÚLLÉPVE (OVERTIME)!" if is_hu else "⚠️ 120 MINUTES EXCEEDED (OVERTIME)!"
    
    html_code = f"""
    <div id="clock_wrapper" style="text-align:center; padding: 10px 14px; background: #0b1120; border-radius: 12px; border: 1.5px solid #1e293b; box-shadow: inset 0 2px 8px rgba(0,0,0,0.5);">
        <div id="clock_display" style="font-size: 3.2rem; font-weight: 900; font-family: 'SF Mono', Consolas, monospace, sans-serif; color: #10b981; letter-spacing: 3px; line-height: 1.1; text-shadow: 0 0 20px rgba(16,185,129,0.4);">
            00:00:00
        </div>
        <div id="clock_status" style="font-size: 0.82rem; font-weight: 600; color: #94a3b8; margin-top: 4px; letter-spacing: 0.5px;">
            {'120 Perces Mélyfókusz Keret' if is_hu else '120-Minute Deep Focus Frame'}
        </div>
    </div>

    <script>
    (function() {{
        let isRunning = {running_js};
        let baseElapsed = {int(cur_secs)};
        let mountTime = Date.now();

        function formatHMS(totalSeconds) {{
            let h = Math.floor(totalSeconds / 3600);
            let m = Math.floor((totalSeconds % 3600) / 60);
            let s = totalSeconds % 60;
            return (h < 10 ? "0" + h : h) + ":" + (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
        }}

        function updateClock() {{
            let currentElapsed = baseElapsed;
            if (isRunning) {{
                currentElapsed += Math.floor((Date.now() - mountTime) / 1000);
            }}

            let displayEl = document.getElementById("clock_display");
            let statusEl = document.getElementById("clock_status");

            if (displayEl) {{
                displayEl.innerText = formatHMS(currentElapsed);

                if (currentElapsed >= 7200) {{
                    // Overtime: Fiery Red
                    displayEl.style.color = "#ef4444";
                    displayEl.style.textShadow = "0 0 25px rgba(239, 68, 68, 0.6)";
                    if (statusEl) {{
                        statusEl.innerHTML = "<strong style='color:#ef4444;'>{overtime_status}</strong>";
                    }}
                }} else {{
                    // Normal: Emerald Green
                    displayEl.style.color = "#10b981";
                    displayEl.style.textShadow = "0 0 20px rgba(16, 185, 129, 0.4)";
                    if (statusEl) {{
                        if (isRunning) {{
                            statusEl.innerHTML = "<strong style='color:#10b981;'>{normal_status}</strong>";
                        }} else {{
                            statusEl.innerHTML = "<span style='color:#94a3b8;'>{paused_status}</span>";
                        }}
                    }}
                }}
            }}
        }}

        updateClock();
        if (isRunning) {{
            setInterval(updateClock, 1000);
        }}
    }})();
    </script>
    """
    components.html(html_code, height=115)


def render_audhd_tracker():
    """Renders permanent top dashboard bar with live green/red clock and synchronous day switcher."""
    is_hu = st.session_state.get("app_global_lang", "HU") == "HU"

    if "timer_running" not in st.session_state:
        st.session_state["timer_running"] = False
    if "timer_elapsed_seconds" not in st.session_state:
        st.session_state["timer_elapsed_seconds"] = 0
    if "timer_start_time" not in st.session_state:
        st.session_state["timer_start_time"] = None
    if "audhd_day_index" not in st.session_state:
        st.session_state["audhd_day_index"] = get_today_index()

    day_idx = st.session_state.get("audhd_day_index", get_today_index())
    day_plans = AUDHD_DAY_PLANS_HU if is_hu else AUDHD_DAY_PLANS_EN
    day_names = DAYS_HU if is_hu else DAYS_EN
    current_day_name = day_names[day_idx]
    cur_plan = day_plans.get(current_day_name, day_plans[day_names[0]])

    cur_secs = get_current_timer_seconds()
    timer_hms = format_seconds_to_hms(cur_secs)
    target_secs = 120 * 60
    progress = min(1.0, max(0.0, cur_secs / target_secs))

    # ── PERMANENS FELSŐ FÓKUSZ KÁRTYA ──
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(30, 41, 59, 0.92)); border: 2px solid rgba(56, 189, 248, 0.4); border-radius: 16px; padding: 16px 20px; margin-bottom: 8px; box-shadow: 0 8px 30px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);'>
    """, unsafe_allow_html=True)

    col_clock, col_info = st.columns([1.1, 1.9])

    with col_clock:
        render_live_clock_html(cur_secs, st.session_state["timer_running"], is_hu)
        
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if not st.session_state["timer_running"]:
                if st.button("▶️ " + ("Indítás" if is_hu else "Start"), key="top_timer_start_btn", use_container_width=True, type="primary"):
                    st.session_state["timer_running"] = True
                    st.session_state["timer_start_time"] = time.time()
                    st.rerun()
            else:
                if st.button("⏸️ " + ("Szünet" if is_hu else "Pause"), key="top_timer_pause_btn", use_container_width=True):
                    st.session_state["timer_running"] = False
                    st.session_state["timer_elapsed_seconds"] = cur_secs
                    st.session_state["timer_start_time"] = None
                    st.rerun()

        with btn_c2:
            if st.button("🔄 Reset", key="top_timer_reset_btn", use_container_width=True):
                st.session_state["timer_running"] = False
                st.session_state["timer_elapsed_seconds"] = 0
                st.session_state["timer_start_time"] = None
                st.rerun()

        with btn_c3:
            if st.button("💾 " + ("Mentés" if is_hu else "Save"), key="top_timer_save_btn", use_container_width=True):
                if cur_secs >= 60:
                    save_time_log_entry({
                        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "day": current_day_name,
                        "duration_seconds": cur_secs,
                        "duration_formatted": timer_hms,
                        "completed": progress >= 0.90
                    })
                    st.session_state["timer_running"] = False
                    st.session_state["timer_elapsed_seconds"] = 0
                    st.session_state["timer_start_time"] = None
                    st.success("✅ " + ("Fókuszblokk elmentve az időnaplóba!" if is_hu else "Focus session saved to time log!"))
                    st.rerun()
                else:
                    st.warning("Legalább 1 perc szükséges a mentéshez." if is_hu else "At least 1 minute required to save.")

    with col_info:
        top_c1, top_c2 = st.columns([1.2, 1.0])
        with top_c1:
            st.markdown(f"<div style='font-size:1.1rem; font-weight:800; color:#38bdf8;'>⏱️ {'AuDHD 120-Perces Mélyfókusz' if is_hu else 'AuDHD 120-Minute Deep Focus'}</div>", unsafe_allow_html=True)
            st.markdown(f"**{'Aktuális Nap' if is_hu else 'Current Day'}:** `{cur_plan.get('title')}`")
        with top_c2:
            chosen_day_idx = st.selectbox(
                "📅 " + ("Válassz Napot:" if is_hu else "Select Day:"),
                options=list(range(7)),
                index=day_idx,
                format_func=lambda i: day_names[i],
                key="top_audhd_day_idx_select"
            )
            if chosen_day_idx != st.session_state["audhd_day_index"]:
                st.session_state["audhd_day_index"] = chosen_day_idx
                st.rerun()

        st.caption(f"{'Haladás' if is_hu else 'Progress'}: {int(progress * 100)}% ({timer_hms} / 02:00:00)")
        st.progress(progress)

        exp_title = f"📋 {current_day_name} {'2 Órás Timeboxing Ellenőrzőlista (Kattints a nyitáshoz/záráshoz)' if is_hu else '2-Hour Timeboxing Checklist (Click to expand)'}"
        with st.expander(exp_title, expanded=True):
            tasks = cur_plan.get("tasks", [])
            for t_idx, task_text in enumerate(tasks):
                st.checkbox(task_text, key=f"task_{current_day_name}_{t_idx}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── GLOWING ELVÁLASZTÓ SÁV AZ AUDHD SZÁMLÁLÓ ÉS AZ ALSÓ RÉSZ KÖZÉ ──
    sep_badge_text = "⚡ AKTÍV MUNKATERÜLET & PIPELINE ⚡" if is_hu else "⚡ ACTIVE WORKSPACE & PIPELINE ⚡"
    st.markdown(f"""
    <div style='margin: 22px 0 26px 0; position: relative; text-align: center;'>
        <div style='height: 2px; background: linear-gradient(90deg, transparent 0%, rgba(56, 189, 248, 0.25) 15%, rgba(56, 189, 248, 0.95) 50%, rgba(16, 185, 129, 0.85) 75%, transparent 100%); box-shadow: 0 0 14px rgba(56, 189, 248, 0.6);'></div>
        <div style='display: inline-block; position: relative; top: -13px; background: #0b1329; padding: 3px 20px; border-radius: 20px; border: 1.5px solid #38bdf8; font-size: 0.76rem; font-weight: 800; letter-spacing: 2px; color: #38bdf8; text-transform: uppercase; box-shadow: 0 4px 15px rgba(0,0,0,0.7), 0 0 10px rgba(56, 189, 248, 0.25);'>
            {sep_badge_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
