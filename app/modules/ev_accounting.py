"""
EV Pénzügyi, Bizonylattár & Könyvelői Vezérlőközpont (2026)
===========================================================
Magyar Egyéni Vállalkozói (EV) Pénzügyi, Bizonylatkezelő és Könyvelői Rendszer:
- 🏢 1. Vállalkozói Törzsadatok & Élő Keretfigyelő (AAM 18M Ft & Átalányadó sáv)
- 💸 2. Számla- & Bevételkezelő (Amazon KDP, Etsy, Gumroad deviza támogatással)
- 🏷️ 3. Költségszámlák & Kiadáskezelő (Google Cloud, AI Pro, Domain, Irodaszer)
- 📁 4. Beépített PDF Bizonylattár (Document Vault)
- 🏛️ 5. Adófizetési Napló & NAV Határidő Menedzser (1-Kattintásos Közlemény Másoló)
- 📦 6. 1-Kattintásos Könyvelői Záró Csomag Export (Zero-Friction ZIP + CSV + E-mail)
"""

import os
import io
import json
import uuid
import datetime
import zipfile
import csv
import re
from typing import List, Dict, Any, Tuple
import streamlit as st

# Storage base directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(CURRENT_DIR)
ROOT_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data", "ev_data")
DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

PROFILE_FILE = os.path.join(DATA_DIR, "profile.json")
INVOICES_FILE = os.path.join(DATA_DIR, "invoices.json")
EXPENSES_FILE = os.path.join(DATA_DIR, "expenses.json")
TAX_PAYMENTS_FILE = os.path.join(DATA_DIR, "tax_payments.json")

# Standard 2026 Hungarian Tax Constants
import urllib.request
import xml.etree.ElementTree as ET

AAM_LIMIT_2026 = 18000000.0  # 18 Million HUF
MIN_WAGE_MONTHLY_2026 = 322800.0
ANNUAL_MIN_WAGE_2026 = MIN_WAGE_MONTHLY_2026 * 12
TAX_FREE_INCOME_LIMIT_2026 = ANNUAL_MIN_WAGE_2026 / 2.0  # 1 936 800 HUF
CHAMBER_FEE_FIXED = 5000.0

DEFAULT_FX_RATES = {
    "USD": 315.50,
    "EUR": 365.00,
    "GBP": 426.50,
    "CHF": 395.00,
    "HUF": 1.0
}


# ─────────────────────────────────────────────────────────────
# 0. HIVATALOS MNB WEBSERVICE API MOTOR (AUTOMATIKUS ÁRFOLYAM)
# ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_mnb_exchange_rates(target_date_str: str = None) -> Tuple[str, Dict[str, float]]:
    """
    Fetches official exchange rates directly from Magyar Nemzeti Bank (MNB) SOAP Web Service.
    Legally compliant with NAV and Hungarian Accounting Law for foreign currency translation.
    Returns: (rate_date_str, {'USD': float, 'EUR': float, ...})
    """
    rates = DEFAULT_FX_RATES.copy()
    rate_date = target_date_str or datetime.date.today().strftime("%Y-%m-%d")

    try:
        if target_date_str:
            dt = datetime.datetime.strptime(target_date_str, "%Y-%m-%d")
            start_dt = dt - datetime.timedelta(days=7)
            start_str = start_dt.strftime("%Y-%m-%d")
            end_str = dt.strftime("%Y-%m-%d")

            soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetExchangeRates xmlns="http://www.mnb.hu/webservices/">
      <startDate>{start_str}</startDate>
      <endDate>{end_str}</endDate>
      <currencyNames>USD,EUR,GBP,CHF,CAD,AUD</currencyNames>
    </GetExchangeRates>
  </soap:Body>
</soap:Envelope>"""
            action = "http://www.mnb.hu/webservices/GetExchangeRates"
        else:
            soap_body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetCurrentExchangeRates xmlns="http://www.mnb.hu/webservices/" />
  </soap:Body>
</soap:Envelope>"""
            action = "http://www.mnb.hu/webservices/GetCurrentExchangeRates"

        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": action
        }

        req = urllib.request.Request("http://www.mnb.hu/arfolyamok.asmx", data=soap_body.encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=4) as response:
            resp_text = response.read().decode("utf-8")
            root = ET.fromstring(resp_text)
            body = root.find("{http://schemas.xmlsoap.org/soap/envelope/}Body")
            for elem in body.iter():
                if elem.tag.endswith("Result") and elem.text:
                    inner_xml = elem.text
                    inner_root = ET.fromstring(inner_xml)
                    days = inner_root.findall("Day")
                    if days:
                        latest_day = days[-1]
                        rate_date = latest_day.attrib.get("date", rate_date)
                        for r_tag in latest_day.findall("Rate"):
                            curr = r_tag.attrib.get("curr")
                            if r_tag.text:
                                rates[curr] = float(r_tag.text.replace(",", "."))
                    break
    except Exception:
        pass

    rates["HUF"] = 1.0
    return rate_date, rates


# ─────────────────────────────────────────────────────────────
# 1. HELYI ADATBÁZIS & FÁJLKEZELŐ SEGÉDFÜGGVÉNYEK (F5-BIZTOS)
# ─────────────────────────────────────────────────────────────

def load_ev_profile() -> Dict[str, Any]:
    """Loads the EV Master Profile from local storage."""
    default_profile = {
        "entrepreneur_name": "Németh Mihály EV",
        "tax_id": "12345678-1-42",
        "reg_number": "56789012",
        "ksh_number": "12345678-7410-231-01",
        "registered_address": "1111 Budapest, Példa utca 1.",
        "bank_name": "Revolut Bank / OTP Bank",
        "iban_account": "HU42 1177 3016 1234 5678 0000 0000",
        "ovtj_codes": ["741001 – Formatervezés, grafikai dizájn", "581901 – Egyéb kiadói tevékenység"],
        "cost_ratio": 45,  # 45% költséghányad digitális termékekre
        "employment_type": "36h",  # '36h' (mellékállás) vagy 'full_time' (főállás)
        "accountant_name": "Kiss Andrea Könyvelőiroda",
        "accountant_email": "konyvelo@pelda.hu",
        "default_currency": "HUF"
    }
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                default_profile.update(data)
        except Exception:
            pass
    return default_profile


def save_ev_profile(profile: Dict[str, Any]):
    """Saves the EV Master Profile to disk."""
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def load_invoices() -> List[Dict[str, Any]]:
    """Loads outgoing invoice / platform revenue records."""
    if os.path.exists(INVOICES_FILE):
        try:
            with open(INVOICES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_invoices(invoices: List[Dict[str, Any]]):
    """Saves outgoing invoice records."""
    with open(INVOICES_FILE, "w", encoding="utf-8") as f:
        json.dump(invoices, f, ensure_ascii=False, indent=2)


def load_expenses() -> List[Dict[str, Any]]:
    """Loads incoming expense records."""
    if os.path.exists(EXPENSES_FILE):
        try:
            with open(EXPENSES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_expenses(expenses: List[Dict[str, Any]]):
    """Saves incoming expense records."""
    with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)


def load_tax_payments() -> List[Dict[str, Any]]:
    """Loads tax settlements and payment records."""
    if os.path.exists(TAX_PAYMENTS_FILE):
        try:
            with open(TAX_PAYMENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_tax_payments(payments: List[Dict[str, Any]]):
    """Saves tax payment records."""
    with open(TAX_PAYMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(payments, f, ensure_ascii=False, indent=2)


def save_uploaded_document(uploaded_file, doc_type: str, date_str: str, record_id: str) -> str:
    """Saves an uploaded PDF to the structured vault folder and returns relative path."""
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        year_str = str(dt.year)
        month_str = f"{dt.month:02d}"
    except Exception:
        now = datetime.datetime.now()
        year_str = str(now.year)
        month_str = f"{now.month:02d}"

    folder = os.path.join(DOCUMENTS_DIR, year_str, month_str, doc_type)
    os.makedirs(folder, exist_ok=True)

    clean_name = re.sub(r'[^a-zA-Z0-9_\.-]', '_', uploaded_file.name)
    filename = f"{date_str}_{record_id[:8]}_{clean_name}"
    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return os.path.relpath(filepath, ROOT_DIR)


def fmt_huf(val: float) -> str:
    """Formats float/int into standard Hungarian currency string."""
    return f"{int(round(val)):,} Ft".replace(",", " ")


# ─────────────────────────────────────────────────────────────
# 2. ADÓKALKULÁCIÓS MOTOR (2026 TÖRVÉNYI ÁTALÁNYADÓ)
# ─────────────────────────────────────────────────────────────

def calculate_ev_tax_summary(yearly_gross: float, cost_ratio: int = 45) -> Dict[str, Any]:
    """Calculates all 2026 Hungarian flat-tax liabilities based on actual gross revenue."""
    ratio_mult = cost_ratio / 100.0
    recognized_expense = yearly_gross * ratio_mult
    calculated_income = yearly_gross * (1.0 - ratio_mult)
    tax_free_income_limit = TAX_FREE_INCOME_LIMIT_2026
    tax_free_gross_limit = tax_free_income_limit / (1.0 - ratio_mult)

    taxable_base = max(0.0, calculated_income - tax_free_income_limit)

    szja = taxable_base * 0.15
    tb = taxable_base * 0.185
    szocho = taxable_base * 0.13

    # Tiered simplified HIPA in Hungary
    if yearly_gross <= 12000000:
        hipa = 50000.0 if yearly_gross > 0 else 0.0
    elif yearly_gross <= 18000000:
        hipa = 120000.0
    elif yearly_gross <= 25000000:
        hipa = 170000.0
    else:
        hipa = calculated_income * 0.02

    chamber_fee = CHAMBER_FEE_FIXED if yearly_gross > 0 else 0.0
    total_tax = szja + tb + szocho + hipa + chamber_fee
    net_yearly = yearly_gross - total_tax
    net_monthly = net_yearly / 12.0
    effective_rate = (total_tax / yearly_gross * 100.0) if yearly_gross > 0 else 0.0

    return {
        "gross_yearly": yearly_gross,
        "cost_ratio": cost_ratio,
        "recognized_expense": recognized_expense,
        "calculated_income": calculated_income,
        "tax_free_income_limit": tax_free_income_limit,
        "tax_free_gross_limit": tax_free_gross_limit,
        "taxable_base": taxable_base,
        "szja": szja,
        "tb": tb,
        "szocho": szocho,
        "hipa": hipa,
        "chamber_fee": chamber_fee,
        "total_tax": total_tax,
        "net_yearly": net_yearly,
        "net_monthly": net_monthly,
        "effective_rate": effective_rate
    }


# ─────────────────────────────────────────────────────────────
# 3. KÖNYVELŐI EXPORT MOTOR (ZIP + CSV + KÍSÉRŐLEVÉL)
# ─────────────────────────────────────────────────────────────

def generate_accountant_pack_zip(year: int, month: int, profile: Dict[str, Any]) -> Tuple[bytes, str, Dict[str, Any]]:
    """
    Generates a zero-friction accountant ZIP bundle containing:
    1. Outgoing invoices CSV
    2. Incoming expenses CSV
    3. Combined ledger CSV
    4. All PDF documents in organized subfolders
    5. Formatted cover letter text
    """
    all_invoices = load_invoices()
    all_expenses = load_expenses()

    month_str = f"{month:02d}"
    prefix = f"{year}-{month_str}"

    month_invoices = [inv for inv in all_invoices if inv.get("date", "").startswith(prefix)]
    month_expenses = [exp for exp in all_expenses if exp.get("date", "").startswith(prefix)]

    total_gross_huf = sum(inv.get("amount_huf", 0.0) for inv in month_invoices)
    total_exp_huf = sum(exp.get("amount_huf", 0.0) for exp in month_expenses)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # 1. Generate Combined CSV Ledger
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Tipus", "Datum", "Bizonylatszam", "Partner / Szolgaltato", "Deviza", "Devizaosszeg", "Arfolyam", "Forintosszeg (HUF)", "Kategoria / Megjegyzes"])

        for inv in month_invoices:
            writer.writerow([
                "KIMENŐ SZÁMLA (Bevétel)",
                inv.get("date", ""),
                inv.get("invoice_number", ""),
                inv.get("platform", ""),
                inv.get("currency", "HUF"),
                f"{inv.get('amount_fx', 0):.2f}",
                f"{inv.get('exchange_rate', 1):.2f}",
                f"{inv.get('amount_huf', 0):.0f}",
                inv.get("description", "")
            ])

        for exp in month_expenses:
            writer.writerow([
                "BEJÖVŐ SZÁMLA (Kiadás)",
                exp.get("date", ""),
                exp.get("invoice_number", ""),
                exp.get("vendor", ""),
                exp.get("currency", "HUF"),
                f"{exp.get('amount_fx', 0):.2f}",
                f"{exp.get('exchange_rate', 1):.2f}",
                f"{exp.get('amount_huf', 0):.0f}",
                f"{exp.get('category', '')} - {exp.get('description', '')}"
            ])

        csv_bytes = csv_buffer.getvalue().encode("utf-8-sig")
        zip_file.writestr(f"{year}_{month_str}_Szamla_Osszesito_{profile.get('entrepreneur_name', 'EV').replace(' ', '_')}.csv", csv_bytes)

        # 2. Attach Invoices PDFs
        for inv in month_invoices:
            pdf_rel = inv.get("pdf_path")
            if pdf_rel:
                pdf_abs = os.path.join(ROOT_DIR, pdf_rel)
                if os.path.exists(pdf_abs):
                    arcname = os.path.join("Kimeno_Szamlak", os.path.basename(pdf_abs))
                    zip_file.write(pdf_abs, arcname=arcname)

        # 3. Attach Expense PDFs
        for exp in month_expenses:
            pdf_rel = exp.get("pdf_path")
            if pdf_rel:
                pdf_abs = os.path.join(ROOT_DIR, pdf_rel)
                if os.path.exists(pdf_abs):
                    arcname = os.path.join("Koltsegszamlak", os.path.basename(pdf_abs))
                    zip_file.write(pdf_abs, arcname=arcname)

        # 4. Generate Cover Letter Text
        cover_letter = f"""Kedves {profile.get('accountant_name', 'Könyvelőm')}!

Csatoltan küldöm a(z) {profile.get('entrepreneur_name', 'Egyéni Vállalkozásom')} (Adószám: {profile.get('tax_id', '')}, Nyilvántartási szám: {profile.get('reg_number', '')}) {year}. {month_str}. havi könyvelési záró anyagát.

Havi Összegzés ({year}. {month_str}. hó):
- Kimenő számlák (Összesített bruttó bevétel): {fmt_huf(total_gross_huf)} ({len(month_invoices)} db bizonylat)
- Költségszámlák (Tényleges igazolt kiadás): {fmt_huf(total_exp_huf)} ({len(month_expenses)} db bizonylat)
- Alkalmazott adózási forma: 2026-os Átalányadó ({profile.get('cost_ratio', 45)}% költséghányad, {profile.get('employment_type', '36h')})

A csatolt ZIP archívum tartalmazza a részletes CSV összesítőt és az összesített PDF számlákat.

Kérlek jelezz vissza, amennyiben bármilyen további adatra vagy bizonylatra szükség van a havi bevalláshoz!

Üdvözlettel,
{profile.get('entrepreneur_name', '')}
Tel / E-mail: {profile.get('iban_account', '')}
"""
        zip_file.writestr(f"Kiserolevel_Konyvelonek_{year}_{month_str}.txt", cover_letter.encode("utf-8-sig"))

    filename = f"{year}_{month_str}_Konyveloi_Csomag_{profile.get('entrepreneur_name', 'EV').replace(' ', '_')}.zip"
    summary_data = {
        "invoice_count": len(month_invoices),
        "expense_count": len(month_expenses),
        "gross_huf": total_gross_huf,
        "exp_huf": total_exp_huf,
        "cover_letter": cover_letter
    }
    return zip_buffer.getvalue(), filename, summary_data


# ─────────────────────────────────────────────────────────────
# 4. STREAMLIT FŐVEZÉRLŐ FELÜLET
# ─────────────────────────────────────────────────────────────

def render_ev_accounting_module():
    """Renders the comprehensive EV Financial, Vault & Accounting Control Center."""
    profile = load_ev_profile()
    invoices = load_invoices()
    expenses = load_expenses()
    tax_payments = load_tax_payments()

    current_year = datetime.datetime.now().year
    
    # Calculate YTD Gross Revenue
    ytd_invoices = [inv for inv in invoices if inv.get("date", "").startswith(str(current_year))]
    ytd_gross_huf = sum(inv.get("amount_huf", 0.0) for inv in ytd_invoices)

    # Calculate YTD Expenses
    ytd_expenses = [exp for exp in expenses if exp.get("date", "").startswith(str(current_year))]
    ytd_exp_huf = sum(exp.get("amount_huf", 0.0) for exp in ytd_expenses)

    tax_summary = calculate_ev_tax_summary(ytd_gross_huf, cost_ratio=profile.get("cost_ratio", 45))

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.98)); border: 1.5px solid #38bdf8; border-radius: 14px; padding: 16px 22px; margin-bottom: 20px; box-shadow: 0 4px 18px rgba(0,0,0,0.3);'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;'>
            <div>
                <h3 style='margin:0; color:#38bdf8; font-size:1.35rem;'>🏢 EV Pénzügyi, Bizonylattár & Könyvelői Vezérlőközpont</h3>
                <p style='margin:4px 0 0 0; color:#94a3b8; font-size:0.88rem;'>
                    Vállalkozó: <strong>{profile.get('entrepreneur_name')}</strong> · Adószám: <code>{profile.get('tax_id')}</code> · Forma: <strong>Átalányadó ({profile.get('cost_ratio')}% költséghányad, {profile.get('employment_type')})</strong>
                </p>
            </div>
            <div>
                <span class='param-badge'>📅 {current_year}. Év</span>
                <span class='param-badge'>📑 {len(ytd_invoices)} db Számla</span>
                <span class='param-badge'>📦 {len(ytd_expenses)} db Költség</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_dash, tab_inv, tab_exp, tab_tax, tab_export, tab_profile = st.tabs([
        "📊 1. Áttekintés & Keretek",
        "💸 2. Bevételek & Számlák",
        "🏷️ 3. Kiadások & Költségek",
        "🏛️ 4. Adók & NAV Határidők",
        "📦 5. Könyvelői Export (1-Kattintás)",
        "⚙️ 6. EV Törzsadatok & Profil"
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1: ÁTTEKINTÉS & ÉLŐ KERETFIGYELŐ
    # ─────────────────────────────────────────────────────────
    with tab_dash:
        st.markdown(f"#### 📊 {current_year}. Éves Pénzügyi Mérleg & Élő Keretfigyelő")
        
        # 4 Fő KPI Metrika Kártya
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("Éves Összesített Bruttó Bevétel", fmt_huf(ytd_gross_huf), delta=f"{len(ytd_invoices)} db számla")
        with k2:
            st.metric("Tiszta Éves Nettó (Zsebben)", fmt_huf(tax_summary["net_yearly"]), delta="Adózás utáni haszon")
        with k3:
            st.metric("Összes Éves Adóteher (Becsült)", fmt_huf(tax_summary["total_tax"]), delta=f"{tax_summary['effective_rate']:.1f}% effektív adó", delta_color="inverse")
        with k4:
            st.metric("Tényleges Igazolt Kiadások", fmt_huf(ytd_exp_huf), delta=f"{len(ytd_expenses)} db tétel", delta_color="off")

        st.markdown("---")
        st.markdown("##### 🛡️ Törvényi Adó- és ÁFA Keret Telítettsége (2026):")

        c_aam, c_taxfree = st.columns(2)
        with c_aam:
            aam_pct = min(100.0, (ytd_gross_huf / AAM_LIMIT_2026) * 100.0)
            aam_rem = max(0.0, AAM_LIMIT_2026 - ytd_gross_huf)
            
            status_color = "#10b981" if aam_pct < 75 else ("#f59e0b" if aam_pct < 90 else "#ef4444")
            status_text = "🟢 Biztonságos zóna" if aam_pct < 75 else ("🟡 Figyelmeztetés (75%+)" if aam_pct < 90 else "🔴 Limitközeli veszély!")

            st.markdown(f"""
            <div class='zen-card'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <strong style='color:#38bdf8;'>🏛️ AAM (Alanyi ÁFA-mentesség) Keret:</strong>
                    <span style='color:{status_color}; font-weight:800;'>{status_text}</span>
                </div>
                <div style='margin:10px 0;'>
                    <div style='background:#0f172a; border-radius:10px; height:18px; width:100%; overflow:hidden; border:1px solid #334155;'>
                        <div style='background:{status_color}; width:{aam_pct:.1f}%; height:100%; transition: width 0.3s ease;'></div>
                    </div>
                </div>
                <div style='display:flex; justify-content:space-between; font-size:0.85rem; color:#cbd5e1;'>
                    <span>Aktuális: <strong>{fmt_huf(ytd_gross_huf)}</strong> ({aam_pct:.1f}%)</span>
                    <span>Keret: <strong>{fmt_huf(AAM_LIMIT_2026)}</strong></span>
                </div>
                <div style='margin-top:6px; font-size:0.82rem; color:#94a3b8;'>
                    Még hátralévő AAM keret: <strong style='color:#38bdf8;'>{fmt_huf(aam_rem)}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c_taxfree:
            tf_gross_limit = tax_summary["tax_free_gross_limit"]
            tf_pct = min(100.0, (ytd_gross_huf / tf_gross_limit) * 100.0) if tf_gross_limit > 0 else 100.0
            tf_rem = max(0.0, tf_gross_limit - ytd_gross_huf)

            tf_color = "#10b981" if tf_pct < 100 else "#64748b"
            tf_msg = f"🟢 0 Ft SZJA & TB fizetés érvényben" if tf_pct < 100 else "🔵 Adóköteles sávba lépett (SZJA/TB aktív)"

            st.markdown(f"""
            <div class='zen-card'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <strong style='color:#10b981;'>🛡️ Átalányadó Adómentes Sáv (0 Ft Adó):</strong>
                    <span style='color:{tf_color}; font-weight:800;'>{tf_msg}</span>
                </div>
                <div style='margin:10px 0;'>
                    <div style='background:#0f172a; border-radius:10px; height:18px; width:100%; overflow:hidden; border:1px solid #334155;'>
                        <div style='background:#10b981; width:{tf_pct:.1f}%; height:100%;'></div>
                    </div>
                </div>
                <div style='display:flex; justify-content:space-between; font-size:0.85rem; color:#cbd5e1;'>
                    <span>Felhasznált: <strong>{fmt_huf(min(ytd_gross_huf, tf_gross_limit))}</strong> ({tf_pct:.1f}%)</span>
                    <span>0 Ft határ: <strong>{fmt_huf(tf_gross_limit)}</strong></span>
                </div>
                <div style='margin-top:6px; font-size:0.82rem; color:#94a3b8;'>
                    Hátralévő adómentes bruttó: <strong style='color:#10b981;'>{fmt_huf(tf_rem)}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("##### 📈 Platform Szerinti Bevétel Megoszlás:")
        platform_totals = {}
        for inv in ytd_invoices:
            p = inv.get("platform", "Egyéb")
            platform_totals[p] = platform_totals.get(p, 0.0) + inv.get("amount_huf", 0.0)

        if platform_totals:
            cols = st.columns(len(platform_totals))
            for i, (plat, amt) in enumerate(platform_totals.items()):
                with cols[i]:
                    st.metric(plat, fmt_huf(amt), delta=f"{(amt/ytd_gross_huf*100):.1f}%" if ytd_gross_huf > 0 else "")
        else:
            st.info("Még nincs rögzített számla a(z) " + str(current_year) + ". évben. Rögzíts számlákat a 'Bevételek & Számlák' fülön!")

    # ─────────────────────────────────────────────────────────
    # TAB 2: BEVÉTELEK & SZÁMLÁK (DEVIZA TÁMOGATÁSSAL)
    # ─────────────────────────────────────────────────────────
    with tab_inv:
        st.markdown("#### 💸 Kimenő Számlák & Platform Bevételek Rögzítése")
        st.caption("Rögzítsd az Amazon KDP, Etsy, Gumroad kifizetéseket és közvetlen számlákat eredeti devizában, automatikus forintosítással és PDF bizonylat mentéssel.")

        with st.expander("➕ Új Kimenő Számla / Kifizetés Rögzítése", expanded=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                inv_date = st.date_input("Kifizetés / Számla Dátuma:", value=datetime.date.today(), key="ev_new_inv_date")
                platform_opts = ["Amazon KDP (Royalty)", "Etsy Payments (Wall Art / Clipart)", "Gumroad (Devotionals / Audio)", "Stripe / Direct Client", "Egyéb Belföldi Vevő"]
                inv_platform = st.selectbox("Partner / Platform:", platform_opts, key="ev_new_inv_platform")
                inv_num = st.text_input("Bizonylat / Számlaszám:", value=f"KDP-{inv_date.strftime('%Y%m')}-01", key="ev_new_inv_num")

            with c2:
                inv_cur = st.selectbox("Eredeti Devizanem:", ["USD", "EUR", "GBP", "CHF", "HUF"], index=0 if "Amazon" in inv_platform or "Gumroad" in inv_platform else 4, key="ev_new_inv_cur")
                
                if inv_cur != "HUF":
                    mnb_date, mnb_rates = fetch_mnb_exchange_rates(inv_date.strftime("%Y-%m-%d"))
                    cur_mnb_val = float(mnb_rates.get(inv_cur, DEFAULT_FX_RATES.get(inv_cur, 1.0)))
                    st.markdown(f"<div style='background:rgba(56, 189, 248, 0.12); border:1px solid #38bdf8; border-radius:8px; padding:5px 10px; margin-bottom:6px; font-size:0.82rem; color:#38bdf8;'>🏛️ <strong>Hivatalos MNB ({mnb_date}):</strong> {cur_mnb_val:.2f} HUF</div>", unsafe_allow_html=True)
                else:
                    cur_mnb_val = 1.0

                inv_fx = st.number_input(f"Alkalmazott Árfolyam ({inv_cur} -> HUF):", min_value=1.0, value=cur_mnb_val, step=0.1, key="ev_new_inv_fx")
                inv_amount_fx = st.number_input(f"Deviza Összeg ({inv_cur}):", min_value=0.0, value=1250.0 if inv_cur != "HUF" else 480000.0, step=50.0, key="ev_new_inv_amt_fx")
                
            with c3:
                inv_amount_huf = inv_amount_fx * inv_fx
                st.markdown(f"""
                <div class='zen-card' style='margin-top:24px;'>
                    <strong style='color:#38bdf8;'>Számított Forintérték:</strong><br>
                    <span style='font-size:1.4rem; font-weight:800; color:#10b981;'>{fmt_huf(inv_amount_huf)}</span>
                </div>
                """, unsafe_allow_html=True)
                inv_desc = st.text_input("Megjegyzés / Termékleírás:", value=f"{inv_platform} havi jogdíj kifizetés", key="ev_new_inv_desc")

            uploaded_pdf = st.file_uploader("📄 PDF Bizonylat / Kifizetési Értesítő Csatolása (Opcionális):", type=["pdf", "png", "jpg"], key="ev_new_inv_pdf")

            if st.button("💾 Kimenő Számla Mentése az Adatbázisba", type="primary", use_container_width=True):
                new_id = str(uuid.uuid4())
                pdf_rel_path = None
                if uploaded_pdf:
                    pdf_rel_path = save_uploaded_document(uploaded_pdf, "invoices", inv_date.strftime("%Y-%m-%d"), new_id)

                new_inv = {
                    "id": new_id,
                    "date": inv_date.strftime("%Y-%m-%d"),
                    "platform": inv_platform,
                    "invoice_number": inv_num,
                    "currency": inv_cur,
                    "amount_fx": inv_amount_fx,
                    "exchange_rate": inv_fx,
                    "amount_huf": inv_amount_huf,
                    "description": inv_desc,
                    "pdf_path": pdf_rel_path,
                    "created_at": datetime.datetime.now().isoformat()
                }
                invoices.insert(0, new_inv)
                save_invoices(invoices)
                st.success(f"✅ Számla sikeresen rögzítve ({fmt_huf(inv_amount_huf)})!")
                st.rerun()

        st.markdown("---")
        st.markdown(f"##### 📑 Rögzített Kimenő Számlák ({len(invoices)} db összesen):")
        
        if invoices:
            for idx, inv in enumerate(invoices):
                c_d1, c_d2, c_d3, c_d4 = st.columns([1.2, 2.0, 1.4, 1.2])
                with c_d1:
                    st.markdown(f"**{inv.get('date')}**<br><code>{inv.get('invoice_number')}</code>", unsafe_allow_html=True)
                with c_d2:
                    st.markdown(f"<strong>{inv.get('platform')}</strong><br><small style='color:#94a3b8;'>{inv.get('description', '')}</small>", unsafe_allow_html=True)
                with c_d3:
                    st.markdown(f"<strong>{fmt_huf(inv.get('amount_huf', 0))}</strong><br><small style='color:#94a3b8;'>{inv.get('amount_fx', 0):.2f} {inv.get('currency')} (x{inv.get('exchange_rate', 1)})</small>", unsafe_allow_html=True)
                with c_d4:
                    pdf_path = inv.get("pdf_path")
                    if pdf_path and os.path.exists(os.path.join(ROOT_DIR, pdf_path)):
                        with open(os.path.join(ROOT_DIR, pdf_path), "rb") as f:
                            st.download_button("⬇️ PDF", data=f.read(), file_name=os.path.basename(pdf_path), mime="application/pdf", key=f"dl_inv_{inv.get('id')}")
                    else:
                        st.caption("Nincs PDF")
                st.markdown("<hr style='margin:4px 0; border-color:#334155;'>", unsafe_allow_html=True)
        else:
            st.info("Még nem rögzítettél kimenő számlát. Nyisd le a fenti 'Új Kimenő Számla' dobozt a rögzítéshez!")

    # ─────────────────────────────────────────────────────────
    # TAB 3: KIADÁSOK & KÖLTSÉGEK
    # ─────────────────────────────────────────────────────────
    with tab_exp:
        st.markdown("#### 🏷️ Bejövő Költségszámlák & Kiadások Rögzítése")
        st.caption("Bár az átalányadóban 45% a fix törvényi költséghányad, a tényleges költségszámlák gyűjtése a NAV ellenőrzés és a valós profit tisztánlátása miatt kötelező és hasznos.")

        with st.expander("➕ Új Költségszámla Rögzítése", expanded=False):
            ce1, ce2, ce3 = st.columns(3)
            with ce1:
                exp_date = st.date_input("Költség Dátuma:", value=datetime.date.today(), key="ev_new_exp_date")
                exp_vendor_opts = ["Google Cloud / Google AI Pro ($20/hó)", "Vercel / Hosting ($20/hó)", "Cloudflare / Domain", "Könyvelői havidíj (15 000 Ft)", "Adobe / Canva Pro", "Irodaszer / Posta", "Hardver / Eszköz", "Egyéb Szolgáltatás"]
                exp_vendor = st.selectbox("Szolgáltató / Kiadás Típusa:", exp_vendor_opts, key="ev_new_exp_vendor")
                exp_num = st.text_input("Költségszámla Száma:", value=f"EXP-{exp_date.strftime('%Y%m')}-01", key="ev_new_exp_num")

            with ce2:
                exp_cat = st.selectbox("Költségkategória:", ["Szoftver & AI Előfizetés", "Tárhely & Domain", "Könyvelési Díj", "Marketing & Hirdetés", "Irodaszer & Eszköz", "Egyéb Működés"], key="ev_new_exp_cat")
                exp_cur = st.selectbox("Pénznem:", ["USD", "EUR", "GBP", "CHF", "HUF"], index=0 if "Google" in exp_vendor or "Vercel" in exp_vendor else 4, key="ev_new_exp_cur")
                
                if exp_cur != "HUF":
                    exp_mnb_date, exp_mnb_rates = fetch_mnb_exchange_rates(exp_date.strftime("%Y-%m-%d"))
                    cur_exp_mnb_val = float(exp_mnb_rates.get(exp_cur, DEFAULT_FX_RATES.get(exp_cur, 1.0)))
                    st.markdown(f"<div style='background:rgba(245, 158, 11, 0.12); border:1px solid #f59e0b; border-radius:8px; padding:5px 10px; margin-bottom:6px; font-size:0.82rem; color:#f59e0b;'>🏛️ <strong>Hivatalos MNB ({exp_mnb_date}):</strong> {cur_exp_mnb_val:.2f} HUF</div>", unsafe_allow_html=True)
                else:
                    cur_exp_mnb_val = 1.0

                exp_fx = st.number_input("Árfolyam:", min_value=1.0, value=cur_exp_mnb_val, step=0.1, key="ev_new_exp_fx")
                exp_amt_fx = st.number_input("Összeg:", min_value=0.0, value=20.0 if exp_cur != "HUF" else 15000.0, step=5.0, key="ev_new_exp_amt_fx")

            with ce3:
                exp_amount_huf = exp_amt_fx * exp_fx
                st.markdown(f"""
                <div class='zen-card' style='margin-top:24px;'>
                    <strong style='color:#f59e0b;'>Költség Forintértéke:</strong><br>
                    <span style='font-size:1.4rem; font-weight:800; color:#f59e0b;'>{fmt_huf(exp_amount_huf)}</span>
                </div>
                """, unsafe_allow_html=True)
                exp_pay_method = st.selectbox("Fizetési Mód:", ["Vállalkozói Bankkártya", "Banki Átutalás", "Készpénz", "PayPal / Stripe"], key="ev_new_exp_pay")
                exp_desc = st.text_input("Megjegyzés:", value=f"{exp_vendor} havi díj", key="ev_new_exp_desc")

            uploaded_exp_pdf = st.file_uploader("📄 Költségszámla PDF Csatolása:", type=["pdf", "png", "jpg"], key="ev_new_exp_pdf")

            if st.button("💾 Költségszámla Mentése", type="primary", use_container_width=True):
                new_id = str(uuid.uuid4())
                pdf_rel_path = None
                if uploaded_exp_pdf:
                    pdf_rel_path = save_uploaded_document(uploaded_exp_pdf, "expenses", exp_date.strftime("%Y-%m-%d"), new_id)

                new_exp = {
                    "id": new_id,
                    "date": exp_date.strftime("%Y-%m-%d"),
                    "vendor": exp_vendor,
                    "invoice_number": exp_num,
                    "category": exp_cat,
                    "currency": exp_cur,
                    "amount_fx": exp_amt_fx,
                    "exchange_rate": exp_fx,
                    "amount_huf": exp_amount_huf,
                    "payment_method": exp_pay_method,
                    "description": exp_desc,
                    "pdf_path": pdf_rel_path,
                    "created_at": datetime.datetime.now().isoformat()
                }
                expenses.insert(0, new_exp)
                save_expenses(expenses)
                st.success(f"✅ Költség elmentve ({fmt_huf(exp_amount_huf)})!")
                st.rerun()

        st.markdown("---")
        st.markdown(f"##### 🏷️ Rögzített Költségek ({len(expenses)} db):")
        if expenses:
            for exp in expenses:
                c_e1, c_e2, c_e3, c_e4 = st.columns([1.2, 2.0, 1.4, 1.2])
                with c_e1:
                    st.markdown(f"**{exp.get('date')}**<br><code>{exp.get('invoice_number')}</code>", unsafe_allow_html=True)
                with c_e2:
                    st.markdown(f"<strong>{exp.get('vendor')}</strong><br><small style='color:#38bdf8;'>[{exp.get('category')}]</small> <small style='color:#94a3b8;'>{exp.get('description', '')}</small>", unsafe_allow_html=True)
                with c_e3:
                    st.markdown(f"<strong>{fmt_huf(exp.get('amount_huf', 0))}</strong><br><small style='color:#94a3b8;'>{exp.get('amount_fx', 0):.2f} {exp.get('currency')}</small>", unsafe_allow_html=True)
                with c_e4:
                    pdf_path = exp.get("pdf_path")
                    if pdf_path and os.path.exists(os.path.join(ROOT_DIR, pdf_path)):
                        with open(os.path.join(ROOT_DIR, pdf_path), "rb") as f:
                            st.download_button("⬇️ PDF", data=f.read(), file_name=os.path.basename(pdf_path), mime="application/pdf", key=f"dl_exp_{exp.get('id')}")
                    else:
                        st.caption("Nincs PDF")
                st.markdown("<hr style='margin:4px 0; border-color:#334155;'>", unsafe_allow_html=True)
        else:
            st.info("Még nincsenek rögzített költségszámlák.")

    # ─────────────────────────────────────────────────────────
    # TAB 4: ADÓK & NAV HATÁRIDŐK
    # ─────────────────────────────────────────────────────────
    with tab_tax:
        st.markdown(f"#### 🏛️ 2026-os Adófizetési Naptár & NAV Határidő Menedzser")
        st.caption("Negyedéves átalányadó kötelezettségek (SZJA, TB, SZOCHO, HIPA, Kamara) és 1-kattintásos banki utalási segéd.")

        q_deadlines = [
            {"period": "2026. I. Negyedév", "deadline": "2026-04-12", "desc": "Január, Február, Március havi kötelezettség"},
            {"period": "2026. II. Negyedév", "deadline": "2026-07-12", "desc": "Április, Május, Június havi kötelezettség"},
            {"period": "2026. III. Negyedév", "deadline": "2026-10-12", "desc": "Július, Augusztus, Szeptember havi kötelezettség"},
            {"period": "2026. IV. Negyedév", "deadline": "2027-01-12", "desc": "Október, November, December havi kötelezettség"}
        ]

        for q in q_deadlines:
            with st.expander(f"📅 {q['period']} — Határidő: {q['deadline']}", expanded=False):
                st.write(f"**Leírás:** {q['desc']}")
                c_tax1, c_tax2 = st.columns(2)
                with c_tax1:
                    st.markdown(f"""
                    **NAV Adószámlák & Bankszámlaszámok:**
                    - 🔹 **SZJA (15%):** `10032000-06056353` (NAV Személyi jövedelemadó)
                    - 🔹 **TB Járulék (18.5%):** `10032000-06056229` (NAV Társadalombiztosítás)
                    - 🔹 **SZOCHO (13%):** `10032000-06055912` (NAV Szociális hozzájárulás)
                    """)
                with c_tax2:
                    notice_example = f"{profile.get('tax_id')} - {profile.get('entrepreneur_name')} - {q['period']}"
                    st.markdown(f"""
                    **Másolható Utalási Közlemény:**
                    ```text
                    {notice_example}
                    ```
                    """)

        st.markdown("---")
        st.markdown("##### 💳 1-Kattintásos Éves Kamarai Hozzájárulás (MKIK - Fix 5 000 Ft):")
        st.markdown("""
        - **Kedvezményezett:** Magyar Kereskedelmi és Iparkamara
        - **Számlaszám:** `12100011-10639683`
        - **Összeg:** `5 000 Ft` (Minden év március 31-ig)
        """)

    # ─────────────────────────────────────────────────────────
    # TAB 5: KÖNYVELŐI EXPORT (1-KATTINTÁS)
    # ─────────────────────────────────────────────────────────
    with tab_export:
        st.markdown("#### 📦 1-Kattintásos Könyvelői Záró Csomag Export")
        st.caption("A hónap végén egyetlen kattintással letöltheted a könyvelőd számára szükséges összes számlát, Excel/CSV táblázatot és a kész kísérőlevelet.")

        c_ex1, c_ex2 = st.columns(2)
        with c_ex1:
            sel_year = st.selectbox("Zárási Év:", [2026, 2025], index=0, key="ev_exp_sel_year")
            sel_month = st.selectbox("Zárási Hónap:", list(range(1, 13)), index=datetime.datetime.now().month - 1, format_func=lambda m: f"{m:02d}. Hónap", key="ev_exp_sel_month")

        zip_bytes, zip_filename, pack_summary = generate_accountant_pack_zip(sel_year, sel_month, profile)

        with c_ex2:
            st.markdown(f"""
            <div class='zen-card'>
                <strong style='color:#10b981;'>📦 Csomag Tartalma ({sel_year}. {sel_month:02d}. hó):</strong><br>
                • <strong>Kimenő számlák:</strong> {pack_summary['invoice_count']} db ({fmt_huf(pack_summary['gross_huf'])})<br>
                • <strong>Költségszámlák:</strong> {pack_summary['expense_count']} db ({fmt_huf(pack_summary['exp_huf'])})<br>
                • <strong>Összesítő CSV:</strong> Excel-kompatibilis magyar táblázat<br>
                • <strong>Kísérőlevél:</strong> Automatikus szöveg
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.download_button(
            f"📥 {zip_filename} Letöltése (ZIP)",
            data=zip_bytes,
            file_name=zip_filename,
            mime="application/zip",
            type="primary",
            use_container_width=True
        )

        st.markdown("---")
        st.markdown("##### ✉️ Másolható Kísérő E-mail Sablon a Könyvelőnek:")
        st.code(pack_summary["cover_letter"], language="text")

    # ─────────────────────────────────────────────────────────
    # TAB 6: EV TÖRZSDATOK & BEÁLLÍTÁSOK
    # ─────────────────────────────────────────────────────────
    with tab_profile:
        st.markdown("#### ⚙️ Egyéni Vállalkozás Törzsadatlap & Konfiguráció")
        st.caption("Az itt megadott adatok automatikusan bekerülnek a könyvelői exportokba, kísérőlevelekbe és adószámításokba.")

        with st.form("ev_profile_form"):
            cp1, cp2 = st.columns(2)
            with cp1:
                p_name = st.text_input("Vállalkozó Neve:", value=profile.get("entrepreneur_name", ""))
                p_tax = st.text_input("Adószám (NAV):", value=profile.get("tax_id", ""))
                p_reg = st.text_input("Nyilvántartási Szám:", value=profile.get("reg_number", ""))
                p_ksh = st.text_input("KSH Statisztikai Szám:", value=profile.get("ksh_number", ""))
                p_addr = st.text_input("Székhely Címe:", value=profile.get("registered_address", ""))

            with cp2:
                p_bank = st.text_input("Bank Neve:", value=profile.get("bank_name", ""))
                p_iban = st.text_input("IBAN Számlaszám:", value=profile.get("iban_account", ""))
                p_cost = st.selectbox("Átalányadó Költséghányad:", [45, 40, 80], index=0 if profile.get("cost_ratio") == 45 else 1)
                p_emp = st.selectbox("Foglalkoztatás Jellege:", ["36h (Heti 36 órás munkaviszony melletti)", "full_time (Főállású egyéni vállalkozó)"], index=0 if profile.get("employment_type") == "36h" else 1)
                p_acc_name = st.text_input("Könyvelő Neve:", value=profile.get("accountant_name", ""))
                p_acc_email = st.text_input("Könyvelő E-mail Címe:", value=profile.get("accountant_email", ""))

            submitted = st.form_submit_button("💾 Vállalkozói Törzsadatok Mentése", type="primary", use_container_width=True)
            if submitted:
                updated_profile = {
                    "entrepreneur_name": p_name,
                    "tax_id": p_tax,
                    "reg_number": p_reg,
                    "ksh_number": p_ksh,
                    "registered_address": p_addr,
                    "bank_name": p_bank,
                    "iban_account": p_iban,
                    "cost_ratio": p_cost,
                    "employment_type": "36h" if "36h" in p_emp else "full_time",
                    "accountant_name": p_acc_name,
                    "accountant_email": p_acc_email,
                    "ovtj_codes": profile.get("ovtj_codes", [])
                }
                save_ev_profile(updated_profile)
                st.success("✅ EV Törzsadatok sikeresen elmentve!")
                st.rerun()


# Alias for seamless backwards compatibility
render_tax_calculator_2026_module = render_ev_accounting_module
