"""
AuDHD 120-Minute Focus Timer, Phase Tracker & Streak Calendar Engine
===================================================================
Designed specifically for neurodivergent (AuDHD) asynchronous workflows:
  - 120-minute visual deep-work timer with Pomodoro timeboxing.
  - Section 8 NotebookLM-integrated 5-day daily task checklist.
  - Persistence of focus streaks in `time_log.json`.
"""

import os
import json
import time
import datetime
from typing import Dict, Any, List
import streamlit as st

TIME_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "time_log.json")

AUDHD_DAY_PLANS = {
    "Hétfő": {
        "title": "🔍 Hétfő: Tiszta Kutatás & RAG Data Mining (NotebookLM & Gemini)",
        "short": "Kutatás & Mining",
        "description": "2 órás mélyfókusz: Amazon/Etsy kulcsszókutatás, 100% pontos KJV igehely- és jelenetkutatás, versenytársi Review Mining.",
        "target_minutes": 120,
        "tasks": [
            "🎯 1. Amazon KDP és Etsy kulcsszókutatás (High Volume, Low Competition) (30 perc)",
            "📖 2. KJV Biblia feltöltése és 30 jelenet/ige kinyerése NotebookLM-ben (30 perc)",
            "⭐ 3. Top versenytársak 1-3 csillagos értékeléseinek Review Mining elemzése (30 perc)",
            "📁 4. Piaci hibák és 5 kiemelkedő termékelőny mentése a projektbe (15 perc)",
            "📋 5. Heti termékspecifikációk véglegesítése a NotebookLM RAG fülön (15 perc)"
        ]
    },
    "Kedd": {
        "title": "📑 Kedd: Teológiai Mátrix & Szöveggenerálás (NotebookLM & Gemini)",
        "short": "Mátrix & Szöveg",
        "description": "2 órás mélyfókusz: 30 napos teológiai mátrix felépítése forrásokból, Gemini Advanced Master Prompt futtatás.",
        "target_minutes": 120,
        "tasks": [
            "🕊️ 1. Teológiai jegyzetek és könyvek feltöltése NotebookLM jegyzetfüzetbe (20 perc)",
            "📑 2. 30 napos táblázatos mátrix legenerálása operatív prompttal (40 perc)",
            "💎 3. Gemini Advanced Master Prompt futtatása a mátrix soraihoz (40 perc)",
            "✍️ 4. 200 szavas reflexiók, imádságok és 3 önreflexiós kérdés finomhangolása (10 perc)",
            "💾 5. Kész kézirat mentése Google Docs-ba és a Drive 05_GUMROAD mappába (10 perc)"
        ]
    },
    "Szerda": {
        "title": "🎨 Szerda: Vizuális Generálás & Képszerkesztés (FLUX / Gemini)",
        "short": "4K Képek & Clipart",
        "description": "2 órás mélyfókusz: 8.5x11 4K fekete-fehér színezők, 4:5 faliképek, clipart csomagok és többkörös háttéreltávolítás.",
        "target_minutes": 120,
        "tasks": [
            "🎨 1. KDP Színező belső oldalak generálása 4K Master Prompttal (45 perc)",
            "🖼️ 2. Etsy 4:5 Skandináv eukaliptusz igés faliképek generálása (30 perc)",
            "✂️ 3. Clipart illusztrációk generálása tiszta fehér háttérrel (25 perc)",
            "✨ 4. Többkörös beszélgetős háttéreltávolítás (Transparent PNG) (10 perc)",
            "📁 5. Képek mentése és rendszerezése a Google Drive projektmappákba (10 perc)"
        ]
    },
    "Csütörtök": {
        "title": "📐 Csütörtök: Kiadványszerkesztés & PDF Szerkesztés (ReportLab / Canva)",
        "short": "Kiadvány & PDF",
        "description": "2 órás mélyfókusz: ReportLab nyomdakész KDP belső PDF összeállítása, borító méretezés és Etsy ZIP csomagolás.",
        "target_minutes": 120,
        "tasks": [
            "📖 1. KDP belső PDF összeállítása filcátütés-gátló lapokkal és margókkal (40 perc)",
            "🎨 2. KDP 17.412:11.25 arányú Wrap-Around borító generálása és méretezése (35 perc)",
            "🛍️ 3. Etsy digitális falikép méretcsomagok (4:5, 3:4, 2:3, 1:1) és mockupok készítése (25 perc)",
            "📦 4. Clipart PNG ZIP csomagok és vásárlói útmutatók összeállítása (10 perc)",
            "💾 5. Nyomdakész és letöltendő fájlok mentése a Drive mappákba (10 perc)"
        ]
    },
    "Péntek": {
        "title": "🚀 Péntek: Automata Publikálás & Audio Upsell (KDP, Etsy, Gumroad)",
        "short": "Publikálás & Audio",
        "description": "2 órás mélyfókusz: Termékfeltöltések, Pinterest passzív SEO leírások és NotebookLM Audio Devotional ($29->$39) generálás.",
        "target_minutes": 120,
        "tasks": [
            "🛍️ 1. Amazon KDP és Etsy termékek feltöltése 13 SEO taggel és leírással (40 perc)",
            "📌 2. Pinterest passzív SEO címek, leírások és közvetlen linkes pinek készítése (20 perc)",
            "🎙️ 3. NotebookLM Audio Overview (Deep Dive podcast MP3) generálása a kéziratból (35 perc)",
            "💰 4. Gumroad termék publikálás + Audio Companion prémium upsell ($39) beállítása (15 perc)",
            "🏆 5. Heti fókuszblokkok értékelése és felkészülés a képernyőmentes hétvégére (10 perc)"
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


def render_audhd_tracker():
    """Renders AuDHD 120-Minute Focus Timer in an expandable top bar with counter visible when collapsed."""
    if "timer_running" not in st.session_state:
        st.session_state["timer_running"] = False
    if "timer_elapsed_seconds" not in st.session_state:
        st.session_state["timer_elapsed_seconds"] = 0
    if "timer_start_time" not in st.session_state:
        st.session_state["timer_start_time"] = None
    if "audhd_selected_day" not in st.session_state:
        st.session_state["audhd_selected_day"] = get_today_hungarian_day()

    cur_secs = get_current_timer_seconds()
    timer_hms = format_seconds_to_hms(cur_secs)
    target_secs = 120 * 60
    progress = min(1.0, max(0.0, cur_secs / target_secs))

    today_day = get_today_hungarian_day()
    day_plan = AUDHD_DAY_PLANS.get(st.session_state["audhd_selected_day"], AUDHD_DAY_PLANS["Hétfő"])
    status_tag = "🟢 FUT" if st.session_state["timer_running"] else "⏸️ SZÜNETEL"

    expander_title = f"⏱️ AuDHD 120-Perces Mélyfókusz Időzítő | {status_tag}: {timer_hms} / 02:00:00 | Mai Fókusz: {today_day} ({day_plan.get('short', '')})"

    with st.expander(expander_title, expanded=False):
        c_timer, c_tasks = st.columns([1.1, 1.9])

        with c_timer:
            st.markdown(f"<div style='font-size:2rem; font-weight:800; color:#38bdf8; text-align:center; padding:6px 0;'>{timer_hms}</div>", unsafe_allow_html=True)
            st.progress(progress)
            st.caption(f"Fókusz haladás: {int(progress * 100)}% (120 perces napi keret)")

            btn_c1, btn_c2, btn_c3 = st.columns(3)
            with btn_c1:
                if not st.session_state["timer_running"]:
                    if st.button("▶️ Indítás", key="top_timer_start_btn", use_container_width=True):
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
                if st.button("💾 Zárás", key="top_timer_save_btn", use_container_width=True):
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

        with c_tasks:
            sel_day = st.selectbox(
                "Napi Timeboxing Terv Kiválasztása:",
                options=HUNGARIAN_DAYS,
                index=HUNGARIAN_DAYS.index(st.session_state["audhd_selected_day"]),
                key="top_audhd_day_select"
            )
            st.session_state["audhd_selected_day"] = sel_day
            cur_plan = AUDHD_DAY_PLANS[sel_day]

            st.markdown(f"**{cur_plan['title']}**")
            st.caption(cur_plan['description'])

            tasks = cur_plan.get("tasks", [])
            for t_idx, task_text in enumerate(tasks):
                task_key = f"task_{sel_day}_{t_idx}"
                st.checkbox(task_text, key=task_key)
