"""
AuDHD 120-Minute Focus Timer, Phase Tracker & Streak Calendar Engine
===================================================================
Designed specifically for neurodivergent (AuDHD) asynchronous workflows:
  - Permanent, non-collapsing top dashboard with giant real-time ticking LED clock.
  - Emerald Green (< 120m) -> Fiery Red when overtime (> 120m).
  - Synchronous 7-day selector with instant day switching and persistent tasks.
  - Persistence of focus streaks in `time_log.json`.
"""

import os
import json
import time
import datetime
from typing import Dict, Any, List
import streamlit as st
import streamlit.components.v1 as components

TIME_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "time_log.json")

AUDHD_DAY_PLANS = {
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
        "title": "🎨 Szerda: Vizuális Generálás & Képszerkesztés (FLUX / Gemini)",
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
        "description": "Kötelező képernyőmentes idő az idegrendszeri regeneráció és az AudHD túlterhelődés elkerülése érdekében.",
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

HUNGARIAN_DAYS = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]


def get_today_hungarian_day() -> str:
    """Returns today's day name in Hungarian."""
    weekday_idx = datetime.datetime.now().weekday()
    return HUNGARIAN_DAYS[weekday_idx]


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


def render_live_clock_html(cur_secs: float, is_running: bool):
    """Renders giant live client-side ticking digital clock in Emerald Green (or Fiery Red when overtime)."""
    running_js = "true" if is_running else "false"
    
    html_code = f"""
    <div id="clock_wrapper" style="text-align:center; padding: 10px 14px; background: #0b1120; border-radius: 12px; border: 1.5px solid #1e293b; box-shadow: inset 0 2px 8px rgba(0,0,0,0.5);">
        <div id="clock_display" style="font-size: 3.2rem; font-weight: 900; font-family: 'SF Mono', Consolas, monospace, sans-serif; color: #10b981; letter-spacing: 3px; line-height: 1.1; text-shadow: 0 0 20px rgba(16,185,129,0.4);">
            00:00:00
        </div>
        <div id="clock_status" style="font-size: 0.82rem; font-weight: 600; color: #94a3b8; margin-top: 4px; letter-spacing: 0.5px;">
            120 Perces Mélyfókusz Keret
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
                        statusEl.innerHTML = "⚠️ <strong style='color:#ef4444;'>120 PERC TÚLLÉPVE (OVERTIME)!</strong>";
                    }}
                }} else {{
                    // Normal: Emerald Green
                    displayEl.style.color = "#10b981";
                    displayEl.style.textShadow = "0 0 20px rgba(16, 185, 129, 0.4)";
                    if (statusEl) {{
                        if (isRunning) {{
                            statusEl.innerHTML = "🟢 <strong style='color:#10b981;'>ÉLŐ SZÁMLÁLÁS FOLYAMATBAN...</strong>";
                        }} else {{
                            statusEl.innerHTML = "⏸️ <span style='color:#94a3b8;'>Szüneteltetve · 120 perces keret</span>";
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


def on_day_select_change():
    """Instant callback when user clicks a different day."""
    sel = st.session_state.get("top_audhd_day_select")
    if sel:
        st.session_state["audhd_selected_day"] = sel


def render_audhd_tracker():
    """Renders permanent top dashboard bar with live green/red clock and synchronous day switcher."""
    if "timer_running" not in st.session_state:
        st.session_state["timer_running"] = False
    if "timer_elapsed_seconds" not in st.session_state:
        st.session_state["timer_elapsed_seconds"] = 0
    if "timer_start_time" not in st.session_state:
        st.session_state["timer_start_time"] = None
    if "audhd_selected_day" not in st.session_state:
        st.session_state["audhd_selected_day"] = get_today_hungarian_day()

    # Synchronize day state immediately
    current_selected_day = st.session_state.get("audhd_selected_day", get_today_hungarian_day())
    cur_plan = AUDHD_DAY_PLANS.get(current_selected_day, AUDHD_DAY_PLANS["Hétfő"])

    cur_secs = get_current_timer_seconds()
    timer_hms = format_seconds_to_hms(cur_secs)
    target_secs = 120 * 60
    progress = min(1.0, max(0.0, cur_secs / target_secs))

    # ── PERMANENS FELSŐ FÓKUSZ KÁRTYA (MINDIG NYITVA, AZONNALI SZINKRON) ──
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85)); border: 1.5px solid #1e293b; border-radius: 14px; padding: 14px 18px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
    """, unsafe_allow_html=True)

    col_clock, col_info = st.columns([1.1, 1.9])

    with col_clock:
        # Giant real-time ticking clock display
        render_live_clock_html(cur_secs, st.session_state["timer_running"])
        
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if not st.session_state["timer_running"]:
                if st.button("▶️ Indítás", key="top_timer_start_btn", use_container_width=True, type="primary"):
                    st.session_state["timer_running"] = True
                    st.session_state["timer_start_time"] = time.time()
                    st.rerun()
            else:
                if st.button("⏸️ Szünet", key="top_timer_pause_btn", use_container_width=True):
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
            if st.button("💾 Mentés", key="top_timer_save_btn", use_container_width=True):
                if cur_secs >= 60:
                    save_time_log_entry({
                        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "day": st.session_state["audhd_selected_day"],
                        "duration_seconds": cur_secs,
                        "duration_formatted": timer_hms,
                        "completed": progress >= 0.90
                    })
                    st.session_state["timer_running"] = False
                    st.session_state["timer_elapsed_seconds"] = 0
                    st.session_state["timer_start_time"] = None
                    st.success("✅ Fókuszblokk elmentve az időnaplóba!")
                    st.rerun()
                else:
                    st.warning("Legalább 1 perc szükséges a mentéshez.")

    with col_info:
        top_c1, top_c2 = st.columns([1.2, 1.0])
        with top_c1:
            st.markdown(f"<div style='font-size:1.1rem; font-weight:800; color:#38bdf8;'>⏱️ AuDHD 120-Perces Mélyfókusz</div>", unsafe_allow_html=True)
            st.markdown(f"**Aktuális Nap:** `{cur_plan.get('title')}`")
        with top_c2:
            sel_day = st.selectbox(
                "📅 Válassz Napot:",
                options=HUNGARIAN_DAYS,
                index=HUNGARIAN_DAYS.index(current_selected_day),
                key="top_audhd_day_select",
                on_change=on_day_select_change
            )

        st.caption(f"Haladás: {int(progress * 100)}% ({timer_hms} / 02:00:00)")
        st.progress(progress)

        # Permanensen látható feladatlista (sosem csukódik be magától!)
        with st.expander(f"📋 {current_selected_day}i 2 Órás Timeboxing Ellenőrzőlista (Kattints a nyitáshoz/záráshoz)", expanded=True):
            tasks = cur_plan.get("tasks", [])
            for t_idx, task_text in enumerate(tasks):
                task_key = f"task_{current_selected_day}_{t_idx}"
                st.checkbox(task_text, key=task_key)

    st.markdown("</div>", unsafe_allow_html=True)
