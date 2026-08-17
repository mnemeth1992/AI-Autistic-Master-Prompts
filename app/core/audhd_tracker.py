"""
AuDHD 120-Minute Focus Timer, Phase Tracker & Streak Calendar Engine
===================================================================
Designed specifically for neurodivergent (AuDHD) asynchronous workflows:
  - 120-minute visual deep-work timer with Pomodoro timeboxing.
  - 5-Step Phase Checklist: [Research] -> [Outline] -> [Images] -> [PDF] -> [Upload].
  - Daily thematic sprint schedule & persistence of focus streaks in `time_log.json`.
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
        "title": "📖 Amazon KDP Színezőkönyv & Nyomdakész PDF Műhely",
        "description": "2 órás mélyfókusz: 10-30 oldalas könyvvázlat, képgenerálás, Drive szinkron és nyomdakész KDP belső PDF.",
        "target_minutes": 120,
        "tasks": [
            "🎯 1. Téma, célközönség (Gyerek/Felnőtt) és KDP könyvcím meghatározása (15 perc)",
            "✨ 2. Könyvvázlat, KJV igék, színpaletta és promptok generálása (25 perc)",
            "🤖 3. Gem Mester Utasítás beállítása és képek legenerálása (40 perc)",
            "📁 4. Képek mentése a Google Drive projektmappába és ellenőrzése (20 perc)",
            "🚀 5. Nyomdakész KDP belső PDF összeállítása ReportLab-bal (20 perc)"
        ]
    },
    "Kedd": {
        "title": "🎨 Etsy Faliképek, Clipart Csomagok & CSV Export",
        "description": "2 órás mélyfókusz: 4:5 Skandináv faliképek, átlátszó clipart illusztrációk és Etsy Listing CSV.",
        "target_minutes": 120,
        "tasks": [
            "🖼️ 1. 5 db 4:5 arányú művészi Skandináv falikép prompt megtervezése (20 perc)",
            "✂️ 2. Chibi / Akvarell clipart illusztrációk legenerálása (35 perc)",
            "✨ 3. Képek mentése a Drive 04_🖼️_ETSY_DIGITAL mappába (25 perc)",
            "🛍️ 4. Etsy termékleírás, 13 SEO tag és címkészlet összeállítása (20 perc)",
            "📊 5. Etsy Listing CSV exportálása és ZIP digitális csomag összeállítása (20 perc)"
        ]
    },
    "Szerda": {
        "title": "✍️ Gumroad Áhítat & Vezetett Lelki Napló Műhely",
        "description": "2 órás mélyfókusz: 30 napos áhítat vezérfonal, napi reflexiók, imádságok és Gumroad kiadás.",
        "target_minutes": 120,
        "tasks": [
            "🕊️ 1. 30 napos áhítat / napló vezérfonal és KJV igék kiválasztása (20 perc)",
            "✍️ 2. Részletes áhítat szövegek és napi imádságok megírása AI-val (40 perc)",
            "📑 3. Önreflexiós kérdések és naplózó feladatok kidolgozása (25 perc)",
            "🏷️ 4. Gumroad termékleírás, vásárlói előnyök és árképzés (20 perc)",
            "💾 5. Kézirat és anyagok mentése a Drive 05_📖_GUMROAD_PLR mappába (15 perc)"
        ]
    },
    "Csütörtök": {
        "title": "🚀 FFC Marketing, Copywriting & Google Sites Stúdió",
        "description": "2 órás mélyfókusz: Avatar kutatás, 12-lépéses Sales Letter, 0 Ft-os Google Sites oldal & E-mailek.",
        "target_minutes": 120,
        "tasks": [
            "🎯 1. FFC Avatar kutatás & 10 db pszichológiai Big Domino horog generálása (25 perc)",
            "📜 2. 12-lépéses Russell Brunson Sales Letter megírása (35 perc)",
            "🌐 3. Google Sites 0 Ft-os Landing Page szövegek és CTA blokkok összeállítása (25 perc)",
            "📧 4. 3 napos / 30 napos automata e-mail tölcsér és hírlevél szekvencia generálása (20 perc)",
            "💾 5. Marketing anyagok mentése Word (.docx) és .txt formátumban a Drive-ra (15 perc)"
        ]
    },
    "Péntek": {
        "title": "🖼️ KDP Borító, Gemini Képbegyűjtő Központ & Heti Zárás",
        "description": "2 órás mélyfókusz: Wrap-around könyvborító méretezés, Drive képbegyűjtés, PDF-ek és heti audit.",
        "target_minutes": 120,
        "tasks": [
            "🎨 1. KDP Wrap-Around Borító méretezése és borítókép legenerálása (30 perc)",
            "📁 2. Heti Google Drive mappák áttekintése és rendszerezése (25 perc)",
            "🖼️ 3. Gemini Képbegyűjtő & PDF Központban az elmaradt PDF kötetek összefűzése (30 perc)",
            "🔑 4. API kulcsok és kvóták ellenőrzése a Rendszerbeállítások fülön (15 perc)",
            "🏆 5. Heti fókuszblokkok értékelése és az időnapló lezárása (20 perc)"
        ]
    }
}


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
    """Renders AuDHD 2-Hour Focus Timer, Phase Tracker & Streak Dashboard."""
    if "timer_running" not in st.session_state:
        st.session_state["timer_running"] = False
    if "timer_elapsed_seconds" not in st.session_state:
        st.session_state["timer_elapsed_seconds"] = 0
    if "timer_start_time" not in st.session_state:
        st.session_state["timer_start_time"] = None
    if "current_phase_idx" not in st.session_state:
        st.session_state["current_phase_idx"] = 0

    cur_secs = get_current_timer_seconds()
    timer_hms = format_seconds_to_hms(cur_secs)
    target_secs = 120 * 60
    progress = min(1.0, max(0.0, cur_secs / target_secs))

    status_tag = "🟢 FUT" if st.session_state["timer_running"] else "⏸️ SZÜNET"

    with st.expander(f"⏱️ AuDHD 2-Órás Fókusz Időzítő & Ciklus Követő ({status_tag} · {timer_hms} / 02:00:00)", expanded=False):
        c_timer, c_phases = st.columns([1.2, 1.8])

        with c_timer:
            st.markdown(f"<div class='timer-display'>{timer_hms}</div>", unsafe_allow_html=True)
            st.progress(progress)
            st.caption(f"Haladás: {int(progress * 100)}% a 120 perces mélyfókusz blokkból")

            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                if not st.session_state["timer_running"]:
                    if st.button("▶️ Indítás", key="audhd_start_btn", use_container_width=True):
                        st.session_state["timer_running"] = True
                        st.session_state["timer_start_time"] = time.time()
                        st.rerun()
                else:
                    if st.button("⏸️ Szünet", key="audhd_pause_btn", use_container_width=True):
                        st.session_state["timer_running"] = False
                        st.session_state["timer_elapsed_seconds"] = cur_secs
                        st.session_state["timer_start_time"] = None
                        st.rerun()

            with btn_col2:
                if st.button("🔄 Reset", key="audhd_reset_btn", use_container_width=True):
                    st.session_state["timer_running"] = False
                    st.session_state["timer_elapsed_seconds"] = 0
                    st.session_state["timer_start_time"] = None
                    st.rerun()

            with btn_col3:
                if st.button("💾 Zárás", key="audhd_save_btn", use_container_width=True):
                    if cur_secs >= 60:
                        save_time_log_entry({
                            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "duration_seconds": cur_secs,
                            "duration_formatted": timer_hms,
                            "completed": progress >= 0.95
                        })
                        st.session_state["timer_running"] = False
                        st.session_state["timer_elapsed_seconds"] = 0
                        st.session_state["timer_start_time"] = None
                        st.success("✅ Fókuszblokk mentve az időnaplóba!")
                        st.rerun()
                    else:
                        st.warning("Legalább 1 perc szükséges a mentéshez.")

        with c_phases:
            st.markdown("##### 📍 5-Lépéses Fázis-Ellenőrzőlista")
            phases = [
                ("1. Kutatás & Niche", "Téma és célközönség kiválasztása"),
                ("2. Vázlat & Szöveg", "Könyvvázlat, KJV igék és promptok generálása"),
                ("3. Képgenerálás", "FLUX/Imagen képek előállítása"),
                ("4. PDF & Csomagolás", "ReportLab nyomdai PDF és borító összeállítása"),
                ("5. Feltöltés & Eladás", "KDP, Etsy vagy Gumroad publikálás")
            ]

            phase_cols = st.columns(5)
            for p_idx, (p_name, p_desc) in enumerate(phases):
                with phase_cols[p_idx]:
                    is_active = (p_idx == st.session_state["current_phase_idx"])
                    is_done = (p_idx < st.session_state["current_phase_idx"])
                    
                    lbl = f"✅ {p_name}" if is_done else (f"👉 {p_name}" if is_active else p_name)
                    if st.button(lbl, key=f"phase_btn_{p_idx}", use_container_width=True):
                        st.session_state["current_phase_idx"] = p_idx
                        st.rerun()

            active_p_name, active_p_desc = phases[st.session_state["current_phase_idx"]]
            st.info(f"**Aktuális Fázis:** {active_p_name} — *{active_p_desc}*")
