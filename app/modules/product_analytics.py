"""
Termék Piac & Értékesítési Analytics Modul
=========================================
Termékszintű értékesítési kimutatások, bestseller rangsor, eladott darabszámok,
bevételmegoszlás és AuDHD skálázási javaslatok (Amazon KDP, Etsy, Gumroad).
"""

import os
import io
import json
import uuid
import datetime
from typing import List, Dict, Any, Tuple
import streamlit as st

# Storage paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(CURRENT_DIR)
ROOT_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data", "ev_data")
os.makedirs(DATA_DIR, exist_ok=True)

PRODUCT_SALES_FILE = os.path.join(DATA_DIR, "product_sales.json")


def fmt_huf(val: float) -> str:
    """Formats float/int into standard Hungarian currency string."""
    return f"{int(round(val)):,} Ft".replace(",", " ")


def load_product_catalog() -> List[Dict[str, Any]]:
    """Loads the persistent product sales and performance catalog."""
    if os.path.exists(PRODUCT_SALES_FILE):
        try:
            with open(PRODUCT_SALES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except Exception:
            pass

    # Default Christian Product Portfolio Benchmarks
    default_catalog = [
        {
            "id": "prod-kdp-01",
            "name": "Noé Bárkája Bibliai Kalandok Színezőkönyv",
            "name_en": "Noah's Ark Bible Adventures Coloring Book",
            "category": "📘 Amazon KDP Könyv",
            "platform": "Amazon KDP",
            "price_usd": 9.99,
            "price_huf": 3850.0,
            "units_sold": 420,
            "total_revenue_huf": 1617000.0,
            "rating": 4.9,
            "reviews_count": 58,
            "launch_date": "2026-01-15",
            "is_bestseller": True,
            "notes": "8.5x11 KDP Paperback, 4-8 éves gyermekeknek, 30 illusztrált oldal"
        },
        {
            "id": "prod-etsy-01",
            "name": "Zsoltárok 23 Skandináv Igés Falikép (4:5 Wall Art)",
            "name_en": "Psalm 23 Scandinavian Minimalist Scripture Print",
            "category": "🖼️ Etsy Wall Art",
            "platform": "Etsy Payments",
            "price_usd": 6.99,
            "price_huf": 2690.0,
            "units_sold": 315,
            "total_revenue_huf": 847350.0,
            "rating": 5.0,
            "reviews_count": 46,
            "launch_date": "2026-02-01",
            "is_bestseller": False,
            "notes": "300 DPI nyomtatható digitális letöltés, 5 méretarány, eukaliptusz stílus"
        },
        {
            "id": "prod-gum-01",
            "name": "30 Napos Békesség a Viharban Áhítat + Audio Podcast ($39)",
            "name_en": "30-Day Devotional + Audio Podcast Bundle",
            "category": "🎙️ Gumroad Áhítat & Podcast",
            "platform": "Gumroad",
            "price_usd": 39.00,
            "price_huf": 15000.0,
            "units_sold": 185,
            "total_revenue_huf": 2775000.0,
            "rating": 4.95,
            "reviews_count": 32,
            "launch_date": "2026-02-20",
            "is_bestseller": True,
            "notes": "Prémium csomag: 30 napos vezetett napló PDF + NotebookLM Deep Dive 15 perces MP3 podcast"
        },
        {
            "id": "prod-etsy-02",
            "name": "Bibliai Hősök Chibi Akvarell Clipart Csomag (50 db PNG)",
            "name_en": "Bible Heroes Chibi Watercolor Clipart Bundle (50 PNGs)",
            "category": "✂️ Etsy Clipart Csomag",
            "platform": "Etsy Payments",
            "price_usd": 8.99,
            "price_huf": 3450.0,
            "units_sold": 210,
            "total_revenue_huf": 724500.0,
            "rating": 4.85,
            "reviews_count": 27,
            "launch_date": "2026-03-05",
            "is_bestseller": False,
            "notes": "Átlátszó hátterű 4K PNG grafikák, kereskedelmi licenccel"
        },
        {
            "id": "prod-kdp-02",
            "name": "Dávid és Góliát – Bátor Szív Kifestőkönyv",
            "name_en": "David and Goliath – Brave Heart Coloring Book",
            "category": "📘 Amazon KDP Könyv",
            "platform": "Amazon KDP",
            "price_usd": 8.99,
            "price_huf": 3450.0,
            "units_sold": 160,
            "total_revenue_huf": 552000.0,
            "rating": 4.8,
            "reviews_count": 19,
            "launch_date": "2026-03-15",
            "is_bestseller": False,
            "notes": "Fekete-fehér vonalrajz, 20 jelenet, bátorító igékkel"
        }
    ]
    save_product_catalog(default_catalog)
    return default_catalog


def save_product_catalog(catalog: List[Dict[str, Any]]):
    """Saves the product catalog to local disk."""
    with open(PRODUCT_SALES_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)


def render_product_analytics_module():
    """Renders the comprehensive Product Sales, Leaderboard & Market Analytics dashboard."""
    catalog = load_product_catalog()

    # Recalculate totals
    total_units_sold = sum(p.get("units_sold", 0) for p in catalog)
    total_revenue_huf = sum(p.get("total_revenue_huf", p.get("units_sold", 0) * p.get("price_huf", 0.0)) for p in catalog)
    bestseller_count = sum(1 for p in catalog if p.get("is_bestseller"))

    # Sort products by total revenue descending
    sorted_by_rev = sorted(catalog, key=lambda x: x.get("total_revenue_huf", 0.0), reverse=True)
    top_product = sorted_by_rev[0] if sorted_by_rev else {}

    # Group by category
    cat_totals = {}
    cat_units = {}
    for p in catalog:
        cat = p.get("category", "Egyéb")
        cat_totals[cat] = cat_totals.get(cat, 0.0) + p.get("total_revenue_huf", 0.0)
        cat_units[cat] = cat_units.get(cat, 0) + p.get("units_sold", 0)

    top_cat = max(cat_totals.items(), key=lambda x: x[1])[0] if cat_totals else "N/A"

    # Header Banner
    header_html = f"""<div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(15, 23, 42, 0.95)); border: 1.5px solid #10b981; border-radius: 14px; padding: 14px 20px; margin-bottom: 18px; box-shadow: 0 4px 16px rgba(0,0,0,0.25);'>
<div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;'>
<div>
<h3 style='margin:0; color:#34d399; font-size:1.3rem;'>📈 Termék Piac & Értékesítési Analytics Hub</h3>
<p style='margin:3px 0 0 0; color:#94a3b8; font-size:0.86rem;'>Valós idejű termékkimutatások, eladási darabszámok, bestseller rangsor és profitmegoszlás.</p>
</div>
<div>
<span class='param-badge'>📦 {len(catalog)} Aktív Termék</span>
<span class='param-badge'>🏆 {bestseller_count} Bestseller</span>
</div>
</div>
</div>"""
    st.markdown(header_html, unsafe_allow_html=True)

    # ── 4 FŐ KPI METRIKA KÁRTYA ──
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Összes Eladott Darabszám", f"{total_units_sold:,} db".replace(",", " "), delta=f"{len(catalog)} termékből")
    with k2:
        st.metric("Összesített Termékbevétel", fmt_huf(total_revenue_huf), delta="Bruttó forgalom")
    with k3:
        st.metric("🥇 #1 Bestseller Termék", top_product.get("name", "N/A")[:22] + "...", delta=f"{top_product.get('units_sold', 0)} db ({fmt_huf(top_product.get('total_revenue_huf', 0))})")
    with k4:
        st.metric("💎 Legjobb Termékvonal", top_cat.split(" ")[1] if " " in top_cat else top_cat, delta=fmt_huf(cat_totals.get(top_cat, 0)))

    st.markdown("---")

    t_rank, t_cat, t_add, t_strat = st.tabs([
        "🏆 1. Bestseller Rangsor & Terméklista",
        "📊 2. Kategória & Platform Megoszlás",
        "➕ 3. Új Termék / Eladás Rögzítése",
        "🧠 4. AuDHD Skálázási Stratégia"
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1: BESTSELLER RANGSOR & TERMÉKLISTA
    # ─────────────────────────────────────────────────────────
    with t_rank:
        st.markdown("#### 🏆 Termékek Értékesítési Ranglistája (Bevétel Alapján)")
        st.caption("A termékek rangsora az összesített forintbevétel és az eladott darabszámok szerint:")

        for idx, prod in enumerate(sorted_by_rev):
            rank_icon = "🥇" if idx == 0 else ("🥈" if idx == 1 else ("🥉" if idx == 2 else f"#{idx+1}"))
            is_best = prod.get("is_bestseller", False)
            p_rev = prod.get("total_revenue_huf", 0.0)
            share_pct = (p_rev / total_revenue_huf * 100.0) if total_revenue_huf > 0 else 0.0
            border_col = '#f59e0b' if idx == 0 else ('#38bdf8' if idx == 1 else ('#10b981' if idx == 2 else '#334155'))
            badge_html = "<span style='background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid #f59e0b; border-radius:12px; padding:2px 8px; font-size:0.75rem; font-weight:800; margin-left:8px;'>👑 BESTSELLER</span>" if is_best else ""

            card_html = f"""<div class='zen-card' style='border-left: 4px solid {border_col}; margin-bottom: 12px;'>
<div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;'>
<div style='display:flex; align-items:center; gap: 12px;'>
<span style='font-size: 1.8rem;'>{rank_icon}</span>
<div>
<strong style='font-size: 1.05rem; color: #f1f5f9;'>{prod.get('name')}</strong> {badge_html}
<div style='font-size:0.83rem; color:#94a3b8; margin-top:2px;'>
Kategória: <span style='color:#38bdf8;'>{prod.get('category')}</span> · Platform: <strong>{prod.get('platform')}</strong> · Értékelés: ⭐ <strong>{prod.get('rating', 5.0):.1f}</strong> ({prod.get('reviews_count', 0)} vélemény)
</div>
</div>
</div>
<div style='text-align: right;'>
<div style='font-size: 1.25rem; font-weight: 900; color: #10b981;'>{fmt_huf(p_rev)}</div>
<div style='font-size: 0.82rem; color: #cbd5e1;'>
<strong>{prod.get('units_sold', 0)} db eladva</strong> · {share_pct:.1f}% részesedés
</div>
</div>
</div>
</div>"""
            st.markdown(card_html, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────
    # TAB 2: KATEGÓRIA & PLATFORM MEGOSZLÁS
    # ─────────────────────────────────────────────────────────
    with t_cat:
        st.markdown("#### 📊 Értékesítési Megoszlás Termékvonalak Szerint")
        st.caption("Összehasonlító kimutatás a 3 fő digitális ökoszisztéma pillér között:")

        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.markdown("##### 💰 Bevétel Megoszlás (HUF):")
            for cat_name, cat_amt in cat_totals.items():
                cat_pct = (cat_amt / total_revenue_huf * 100.0) if total_revenue_huf > 0 else 0.0
                bar_color = "#38bdf8" if "KDP" in cat_name else ("#10b981" if "Etsy" in cat_name else "#a855f7")

                cat_bar_html = f"""<div style='margin-bottom: 14px;'>
<div style='display:flex; justify-content:space-between; font-size:0.88rem; margin-bottom:4px;'>
<strong>{cat_name}</strong>
<span style='color:#f1f5f9; font-weight:700;'>{fmt_huf(cat_amt)} ({cat_pct:.1f}%)</span>
</div>
<div style='background:#0f172a; border-radius:10px; height:14px; width:100%; overflow:hidden; border:1px solid #334155;'>
<div style='background:{bar_color}; width:{cat_pct:.1f}%; height:100%;'></div>
</div>
</div>"""
                st.markdown(cat_bar_html, unsafe_allow_html=True)

        with c_p2:
            st.markdown("##### 📦 Eladott Darabszám Megoszlás (Units):")
            for cat_name, u_count in cat_units.items():
                u_pct = (u_count / total_units_sold * 100.0) if total_units_sold > 0 else 0.0
                unit_bar_html = f"""<div style='margin-bottom: 14px;'>
<div style='display:flex; justify-content:space-between; font-size:0.88rem; margin-bottom:4px;'>
<strong>{cat_name}</strong>
<span style='color:#38bdf8; font-weight:700;'>{u_count} db ({u_pct:.1f}%)</span>
</div>
<div style='background:#0f172a; border-radius:10px; height:14px; width:100%; overflow:hidden; border:1px solid #334155;'>
<div style='background:#f59e0b; width:{u_pct:.1f}%; height:100%;'></div>
</div>
</div>"""
                st.markdown(unit_bar_html, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────
    # TAB 3: ÚJ TERMÉK / ELADÁS RÖGZÍTÉSE
    # ─────────────────────────────────────────────────────────
    with t_add:
        st.markdown("#### ➕ Új Termék Rögzítése vagy Eladások Frissítése")
        st.caption("Adj hozzá új kiadványt a portfóliódhoz, vagy frissítsd a meglévő termékek értékesítési számait.")

        with st.form("add_product_form"):
            ca1, ca2 = st.columns(2)
            with ca1:
                p_name_in = st.text_input("Termék Pontos Neve:", placeholder="Pl. Dániel az oroszlánok vermében KDP Színező")
                p_cat_in = st.selectbox("Termékkategória:", [
                    "📘 Amazon KDP Könyv",
                    "🖼️ Etsy Wall Art",
                    "✂️ Etsy Clipart Csomag",
                    "🎙️ Gumroad Áhítat & Podcast",
                    "📦 PLR & Egyéb Digitális Termék"
                ])
                p_plat_in = st.selectbox("Értékesítési Platform:", ["Amazon KDP", "Etsy Payments", "Gumroad", "Stripe / Direct", "Saját Weboldal"])

            with ca2:
                p_price_usd_in = st.number_input("Eladási Ár ($ USD):", min_value=0.0, value=9.99, step=0.5)
                p_price_huf_in = st.number_input("Eladási Ár (HUF):", min_value=0.0, value=3850.0, step=100.0)
                p_units_in = st.number_input("Eddig Eladott Mennyiség (db):", min_value=0, value=10, step=1)
                p_best_in = st.checkbox("👑 Bestsellerként megjelölve", value=False)
                p_notes_in = st.text_input("Megjegyzés / Részletek:", placeholder="Pl. 24 oldalas, 8.5x11 formátum")

            submitted_prod = st.form_submit_button("💾 Termék Mentése a Portfólióba", type="primary", use_container_width=True)
            if submitted_prod and p_name_in:
                new_p = {
                    "id": f"prod-{str(uuid.uuid4())[:8]}",
                    "name": p_name_in,
                    "name_en": p_name_in,
                    "category": p_cat_in,
                    "platform": p_plat_in,
                    "price_usd": p_price_usd_in,
                    "price_huf": p_price_huf_in,
                    "units_sold": p_units_in,
                    "total_revenue_huf": p_units_in * p_price_huf_in,
                    "rating": 5.0,
                    "reviews_count": 0,
                    "launch_date": datetime.date.today().strftime("%Y-%m-%d"),
                    "is_bestseller": p_best_in,
                    "notes": p_notes_in
                }
                catalog.append(new_p)
                save_product_catalog(catalog)
                st.success(f"✅ '{p_name_in}' sikeresen hozzáadva a termékkatalógushoz!")
                st.rerun()

        st.markdown("---")
        st.markdown("##### ⚡ Meglévő Termékek Eladási Darabszámának Gyors Frissítése:")
        for p in catalog:
            cp_col1, cp_col2, cp_col3 = st.columns([2.5, 1.5, 1.2])
            with cp_col1:
                st.markdown(f"**{p.get('name')}** (`{p.get('category')}`)")
            with cp_col2:
                st.markdown(f"Jelenlegi: **{p.get('units_sold')} db** ({fmt_huf(p.get('total_revenue_huf', 0))})")
            with cp_col3:
                if st.button(f"➕ +5 eladás", key=f"quick_add_{p.get('id')}"):
                    p["units_sold"] = p.get("units_sold", 0) + 5
                    p["total_revenue_huf"] = p["units_sold"] * p.get("price_huf", 3850.0)
                    save_product_catalog(catalog)
                    st.rerun()

    # ─────────────────────────────────────────────────────────
    # TAB 4: AUDHD SKÁLÁZÁSI STRATÉGIA
    # ─────────────────────────────────────────────────────────
    with t_strat:
        st.markdown("#### 🧠 AuDHD Portfólió Elemzés & Skálázási Iránytű")
        st.caption("Döntési bénulás (choice paralysis) helyett 3 fókuszált, magas hatékonyságú lépés a meglévő eladásaid alapján:")

        top_share = (top_product.get('total_revenue_huf', 0) / total_revenue_huf * 100) if total_revenue_huf > 0 else 0
        aam_share = (total_revenue_huf / 18000000 * 100) if total_revenue_huf > 0 else 0

        strat_html = f"""<div class='zen-card' style='border-left: 4px solid #38bdf8; margin-bottom: 14px;'>
<h5 style='color:#38bdf8; margin:0 0 6px 0;'>🎯 1. Skálázási Fókusz: '{top_product.get('name', 'Bestseller')}' Multipack Keresztértékesítés</h5>
<p style='margin:0; color:#cbd5e1; font-size:0.9rem;'>
Ez a termék generálja a teljes bevételed <strong>{top_share:.1f}%</strong>-át! 
<strong>Teendő:</strong> Ne indíts 10 teljesen új témát. Hozz létre ebből a témából egy kapcsolódó <em>Etsy Clipart csomagot</em> és egy <em>Gumroad Áhítatot</em>, mert a már meglévő vevőid azonnal megvásárolják a kapcsolódó terméket is.
</p>
</div>

<div class='zen-card' style='border-left: 4px solid #a855f7; margin-bottom: 14px;'>
<h5 style='color:#a855f7; margin:0 0 6px 0;'>🎙️ 2. Profit Multiplikátor: A $39-os Gumroad Audio Upsell Erőssége</h5>
<p style='margin:0; color:#cbd5e1; font-size:0.9rem;'>
A <strong>30 Napos Áhítat + Deep Dive Audio Podcast</strong> terméked adja a legmagasabb egységárat ($39 = 15 000 Ft/vásárlás). 
<strong>Teendő:</strong> Már mindössze heti 3 db Gumroad eladás havi <strong>180 000 Ft</strong> tiszta plusz profitot termel minimális extra energiával.
</p>
</div>

<div class='zen-card' style='border-left: 4px solid #10b981;'>
<h5 style='color:#10b981; margin:0 0 6px 0;'>🛡️ 3. AAM Keretbiztonság (18 000 000 Ft)</h5>
<p style='margin:0; color:#cbd5e1; font-size:0.9rem;'>
A jelenlegi termékportfóliód <strong>{fmt_huf(total_revenue_huf)}</strong> éves forgalmat realizált, ami 
<strong>{aam_share:.1f}%</strong>-os AAM keretkihasználtságot jelent. A vállalkozásod teljesen biztonságos, adómentes zónában működik!
</p>
</div>"""
        st.markdown(strat_html, unsafe_allow_html=True)
