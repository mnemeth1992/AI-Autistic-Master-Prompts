"""
modules/ffc_engine.py - FFC Marketing & Gemini/Groq Copywriting Engine
Generates 10-part sales letters, Big Domino statements, 3-part bullet points,
VSL scripts, value stacks, and objection handling with multi-provider fallback.
"""

import os
import json
import re
import time
from typing import Dict, Any, Optional, Tuple

try:
    from key_manager import get_key_manager
except ImportError:
    try:
        from app.core.key_manager import get_key_manager
    except ImportError:
        get_key_manager = None


def load_ffc_templates() -> Dict[str, Any]:
    """Loads default conversion templates from data/ffc_templates.json."""
    tmpl_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "ffc_templates.json")
    if os.path.exists(tmpl_path):
        try:
            with open(tmpl_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def build_ffc_prompt(
    topic: str,
    target_audience: str,
    core_transformation: str,
    language: str = "Magyar",
    vehicle: str = "",
    extra_notes: str = "",
    product_type: str = "Keresztény Digitális Termék"
) -> str:
    """Builds a structured prompt for Russell Brunson & Alex Hormozi style direct response copy with strict language purity."""
    is_en = "angol" in language.lower() or "english" in language.lower()
    
    if is_en:
        vehicle_text = vehicle if vehicle.strip() else "Guided daily reflections, prayer anchors, and clean printable daily journal sheets"
        notes_text = f"\n- Additional preferences: {extra_notes}" if extra_notes.strip() else ""
        return f"""
You are a world-class Direct Response Copywriter and FFC (Faceless Funnel) marketing master in the style of Russell Brunson ('DotCom Secrets') and Alex Hormozi ('$100M Offers').
Your task is to craft a deeply moving, highly converting, 10-part Sales Pack in 100% FLUENT, NATURAL ENGLISH (US).

CRITICAL LANGUAGE REQUIREMENT:
- Every single word, headline, bullet point, VSL script, and sales letter MUST be written in 100% pure English.
- DO NOT mix any Hungarian or other foreign words into the output.

=== PRODUCT DETAILS ===
- Product Type: {product_type}
- Core Offer / Topic: {topic}
- Target Audience: {target_audience}
- Core Transformation (Ultimate Promise): {core_transformation}
- The Vehicle / Unique Mechanism: {vehicle_text}{notes_text}
- Language: English (US)

Generate the complete sales pack STRICTLY as a valid JSON object matching this schema:
{{
  "product_title": "{topic}",
  "big_domino": "The Big Domino statement (If I can convince them that [Vehicle] is the ONLY key to [Transformation], then all other objections become irrelevant...)",
  "headlines": [
    "1. How to Achieve [Desire] Without [Pain], Even If [Objection]...",
    "2. The Secret Method Helping [Audience] Finally...",
    "3. 3 Simple Steps to [Transformation]...",
    "4. Finally, a Proven Solution That...",
    "5. Why Traditional Methods Fail (And What to Do Instead)..."
  ],
  "vsl_script": "3-minute high-converting VSL script with [0:00-0:30 HOOK], [0:30-1:00 PROBLEM], [1:00-1:45 EPIPHANY BRIDGE & SOLUTION], [1:45-2:30 THE OFFER & BONUSES], [2:30-3:00 GUARANTEE & URGENT CTA]...",
  "three_part_bullets": [
    {{
      "mit_kap": "1. Core Component / Module Name",
      "meg_akkor_is_ha": "Even if you only have 10 minutes a day / have doubts...",
      "ami_azt_jelenti": "Which means you experience genuine daily peace and clarity without overwhelm..."
    }},
    {{
      "mit_kap": "2. High-Value Feature / Template Name",
      "meg_akkor_is_ha": "Even if you've never used a guided journal before...",
      "ami_azt_jelenti": "Which means you get an effortless step-by-step structure..."
    }},
    {{
      "mit_kap": "3. Special Bonus / Reflection Pack",
      "meg_akkor_is_ha": "Even if you wake up feeling stressed and scattered...",
      "ami_azt_jelenti": "Which means you instantly reset your focus in under 10 minutes..."
    }},
    {{
      "mit_kap": "4. Printable & Digital Worksheets",
      "meg_akkor_is_ha": "Even if your schedule is packed from morning to night...",
      "ami_azt_jelenti": "Which means you can practice daily mindfulness completely guilt-free..."
    }},
    {{
      "mit_kap": "5. Quick-Start Guide / Action Tracker",
      "meg_akkor_is_ha": "Even if you feel stuck or lack motivation...",
      "ami_azt_jelenti": "Which means you always know your exact next step with unwavering confidence..."
    }}
  ],
  "objection_handling": {{
    "vehicle_objection": "1. Vehicle Objection: Why this exact method works even when other journals/books failed.",
    "internal_objection": "2. Internal Objection: Why they have what it takes even if they lack discipline.",
    "external_objection": "3. External Objection: Why time constraints, busy schedules, or costs won't hold them back."
  }},
  "value_stack": {{
    "main_product_value": "Core Master Digital Product (Real Value: $47)",
    "bonus_1": "Bonus #1: 30-Day Daily Prayer & Focus Cards (Value: $27)",
    "bonus_2": "Bonus #2: Morning Mindfulness Audio & Routine Checklist (Value: $19)",
    "bonus_3": "Bonus #3: Digital Life & Habit Tracker Template (Value: $29)",
    "total_value": "$122",
    "offer_price": "$27",
    "guarantee_text": "100% Risk-Free 14-Day Money-Back Guarantee: Try it for 14 full days. If it doesn't bring peace and clarity to your life, send 1 quick email for an immediate 100% refund."
  }},
  "sales_letter_full": "Complete, beautifully formatted Russell Brunson style long-form sales letter in English with powerful headings, empathetic story, bullet points, value stack, and compelling CTA."
}}
"""
    else:
        vehicle_text = vehicle if vehicle.strip() else "Vezetett napi bibliai reflexiók, imádságok és letisztult printable naplólapok"
        notes_text = f"\n- További preferenciák: {extra_notes}" if extra_notes.strip() else ""
        return f"""
Te egy világklasszis Direct Response Copywriter és FFC (Faceless Funnel) értékesítési szakértő vagy Russell Brunson és Alex Hormozi stílusában.
A feladatod egy mélyen megrendítő, hiteles, magas konverziójú, 10-részes értékesítési csomag (Sales Pack) elkészítése 100%-BAN TISZTA MAGYAR NYELVEN.

SZIGORÚ NYELVI KÖVETELMÉNY:
- Minden egyes szó, cím, bulletpont és szöveg kizárólag hibátlan, természetes magyar nyelven készüljön!
- Tilos angol és magyar szavakat vegyesen használni a szövegtörzsben!

=== TERMÉK ADATOK ===
- Terméktípus: {product_type}
- Fő téma / Piac: {topic}
- Célközönség: {target_audience}
- Fő transzformáció (Végső Ígéret): {core_transformation}
- Eszköz / Módszer (The Vehicle): {vehicle_text}{notes_text}
- Nyelv: Magyar

Készítsd el a teljes értékesítési csomagot SZIGORÚAN az alábbi érvényes JSON formátumban:
{{
  "product_title": "{topic}",
  "big_domino": "A fő dominó állítás (Ha meg tudom győzni őket arról, hogy [Vehicle] az egyetlen út [Transzformációhoz], minden más kifogás elenyészik...)",
  "headlines": [
    "1. Főcím: Hogyan érj el X-et Y nélkül, még ha Z is...",
    "2. Főcím: A titkos módszer...",
    "3. Főcím: 3 lépés a békességhez...",
    "4. Főcím: Végre egy megoldás, ami...",
    "5. Főcím: Miért buknak el a hagyományos utak..."
  ],
  "vsl_script": "3 perces VSL forgatókönyv (0:00-0:30 Hook, 0:30-1:00 Fájdalompont, 1:00-1:45 Epiphany Bridge, 1:45-2:30 Ajánlat & Bónuszok, 2:30-3:00 Sürgetés & CTA)...",
  "three_part_bullets": [
    {{
      "mit_kap": "1. Rész / Sablon neve",
      "meg_akkor_is_ha": "Még akkor is ha nincs időd / kételkedsz...",
      "ami_azt_jelenti": "Ami azt jelenti, hogy valódi belső békességet tapasztalsz a hétköznapokban..."
    }},
    {{
      "mit_kap": "2. Rész / Bónusz neve",
      "meg_akkor_is_ha": "Még akkor is ha sosem vezettél még naplót...",
      "ami_azt_jelenti": "Ami azt jelenti, hogy azonnal tiszta struktúrát kapsz..."
    }},
    {{
      "mit_kap": "3. Rész / Bónusz neve",
      "meg_akkor_is_ha": "Még akkor is ha zaklatottan ébredsz...",
      "ami_azt_jelenti": "Ami azt jelenti, hogy 10 perc alatt visszanyered a fókuszt..."
    }},
    {{
      "mit_kap": "4. Rész / Munkafüzet neve",
      "meg_akkor_is_ha": "Még akkor is ha tele van a naptárad...",
      "ami_azt_jelenti": "Ami azt jelenti, hogy bűntudat nélkül építheted a lelki életed..."
    }},
    {{
      "mit_kap": "5. Rész / Útmutató neve",
      "meg_akkor_is_ha": "Még akkor is ha egyedül érzed magad az úton...",
      "ami_azt_jelenti": "Ami azt jelenti, hogy Isten ígéretei vezetik a napodat..."
    }}
  ],
  "objection_handling": {{
    "vehicle_objection": "1. Eszköz kifogás kezelése (Miért működik ez a módszer akkor is, ha más könyvek/naplók nem segítettek?)",
    "internal_objection": "2. Belső önbizalomhiány kezelése (Nekem van elég akaraterőm / kitartásom ehhez?)",
    "external_objection": "3. Külső akadályok / időhiány kezelése (Nincs időm, a családom lefoglal, drága-e?)"
  }},
  "value_stack": {{
    "main_product_value": "Fő Digitális Termék (Valós érték: 14.990 Ft / $47)",
    "bonus_1": "Bónusz #1: 30 Napos Imakártya Csomag (Érték: 6.990 Ft / $27)",
    "bonus_2": "Bónusz #2: Reggeli Csendesség Hanganyag & Playlista (Érték: 4.990 Ft / $19)",
    "bonus_3": "Bónusz #3: Éves Keresztény Céltervező Sablon (Érték: 7.990 Ft / $29)",
    "total_value": "34.960 Ft ($122)",
    "offer_price": "9.990 Ft ($27)",
    "guarantee_text": "100% Kockázatmentes 14 Napos Áldás-Garancia: Ha nem hoz békességet a mindennapjaidba, 1 e-mail és kérdés nélkül visszatérítjük az összeget."
  }},
  "sales_letter_full": "Teljes formázott Russell Brunson stílusú értékesítési szöveg magyarul címsorokkal, történettel, bullet pontokkal és lezárással."
}}
"""


def generate_offline_ffc_pack(topic: str, target_audience: str, core_transformation: str, language: str = "Magyar") -> Dict[str, Any]:
    """Generates an immediate, high-quality offline FFC sales pack if all APIs are unavailable, strictly matching the requested language."""
    is_en = "angol" in language.lower() or "english" in language.lower()
    
    if is_en:
        return {
            "product_title": topic,
            "big_domino": f"If I can convince {target_audience} that daily structured reflection is the single key to {core_transformation}, they will immediately invest in this complete bundle.",
            "headlines": [
                f"How to Achieve {core_transformation} in Just 10 Minutes a Day – Without Guilt or Overwhelm!",
                f"The Proven Biblical Method Helping {target_audience} Finally Experience Lasting Inner Peace",
                f"Finally, a Guided Faith Companion That Actually Fits Into Your Busy Daily Routine",
                f"3 Simple Steps to Release Anxiety and Walk Daily in Divine Focus and Clarity",
                f"Why Traditional Journals Fail – And Why This New Framework Changes Everything"
            ],
            "vsl_script": f"""[0:00 - 0:25 HOOK]
If you wake up feeling like daily stress and endless to-do lists are drowning out your spiritual peace, you are not alone. But what if there was an effortless 10-minute daily framework to {core_transformation}?

[0:25 - 1:00 THE PROBLEM]
Many {target_audience} attempt morning devotions, but thoughts wander, phone notifications chime, and by evening only guilt remains. The problem isn't your devotion—it's that old generic methods weren't designed for modern, high-distraction lives.

[1:00 - 1:45 THE EPIPHANY BRIDGE & THE SOLUTION]
When we engineered a micro-reflection system anchored in daily scripture and structured prompts, everything changed. You don't need hours of isolated silence: 10 focused minutes gets straight to the heart. That's why we created {topic}.

[1:45 - 2:30 THE VALUE STACK & BONUSES]
This bundle doesn't just include the core 30-day guided guide—you also get instant access to the 30-Day Daily Prayer Cards and the Annual Life & Focus Tracker. Valued at over $120, today you get complete instant access for just $27.

[2:30 - 3:00 THE GUARANTEE & CALL TO ACTION]
We back this with a 100% risk-free 14-day blessing guarantee. Click the button below, access your private Google Drive download immediately, and start your spiritual breakthrough today!""",
            "three_part_bullets": [
                {
                    "mit_kap": "30-Day Guided Daily Workbook (Printable PDF & Digital)",
                    "meg_akkor_is_ha": "Even if you only have 10 quiet minutes beside your morning coffee",
                    "ami_azt_jelenti": "Which means you begin every single day anchored in divine peace instead of rushing anxiety."
                },
                {
                    "mit_kap": "30 Handpicked KJV Scripture Passages with Practical Insights",
                    "meg_akkor_is_ha": "Even if you struggle to find the practical application in biblical texts",
                    "ami_azt_jelenti": "Which means you receive immediately actionable wisdom for every season of life."
                },
                {
                    "mit_kap": "Deep Reflection & Daily Gratitude Prompts",
                    "meg_akkor_is_ha": "Even if you've never known what to write on a blank journal page",
                    "ami_azt_jelenti": "Which means you never feel stuck—the guided prompts gently lead your thoughts."
                },
                {
                    "mit_kap": "Print-Ready US Letter & A4 Formats",
                    "meg_akkor_is_ha": "Even if you prefer digital iPad apps (GoodNotes/Notability) or physical paper",
                    "ami_azt_jelenti": "Which means maximum flexibility to use it wherever life takes you."
                },
                {
                    "mit_kap": "Exclusive Emergency Prayer Collection for Hard Days",
                    "meg_akkor_is_ha": "Even if you feel completely overwhelmed and have no words to pray",
                    "ami_azt_jelenti": "Which means you always have an anchor of comfort and strength when you need it most."
                }
            ],
            "objection_handling": {
                "vehicle_objection": "This isn't a dense theological textbook—it is an interactive, actionable daily tool designed to deliver quick wins in under 10 minutes.",
                "internal_objection": "You don't need superhuman willpower: the simple structured prompts remove all decision fatigue.",
                "external_objection": "Instant digital download with lifetime access—no shipping delays or worn-out pages."
            },
            "value_stack": {
                "main_product_value": f"{topic} (Real Value: $47)",
                "bonus_1": "Bonus #1: 30-Day Daily Prayer Cards Pack (Value: $27)",
                "bonus_2": "Bonus #2: Morning Mindfulness & Routine Checklist (Value: $19)",
                "bonus_3": "Bonus #3: Digital Christian Life & Habit Tracker (Value: $29)",
                "total_value": "$122",
                "offer_price": "$27",
                "guarantee_text": "100% Risk-Free 14-Day Money-Back Guarantee: Try it for 14 full days. If it doesn't bring peace and clarity to your life, send 1 quick email for an immediate 100% refund."
            },
            "sales_letter_full": f"""# {topic}

## How to Find Lasting Daily Peace in a Busy, Distracted World – In Just 10 Minutes a Day

Dear Friend,

Do you know that feeling when your alarm goes off, and before your feet even touch the floor, your mind is already flooded with deadlines, worries, and endless to-do lists?

You are not alone. As believers and seekers, we deeply crave quiet time, connection, and peace—but in today's fast-paced world, generic methods often fail.

### The Solution: {topic}

This guided digital workbook and reflection system was created to bridge that gap in just 10 focused minutes each morning.

### What's Inside the Bundle?
- **30-Day Guided Daily Workbook:** Effortless 10-minute daily format, even if your schedule is packed, which means genuine peace of mind.
- **30 Selected Scripture Passages & Commentary:** Practical wisdom you can apply to your workday immediately.
- **Exclusive Bonuses Included:** Daily prayer cards, focus sheets, and digital habit tracking templates!

### 100% Risk-Free Guarantee
Try it for 14 days. If you don't feel calmer, more centered, and more spiritually renewed, just send us an email for a prompt 100% refund.

**[ GET INSTANT ACCESS NOW – IMMEDIATE DIGITAL DOWNLOAD ]**"""
        }

    return {
        "product_title": topic,
        "big_domino": f"Ha meg tudom győzni {target_audience} tagjait arról, hogy a napi vezetett reflexió az egyetlen kulcs {core_transformation} eléréséhez, akkor azonnal meg fogják vásárolni ezt a csomagot.",
        "headlines": [
            f"Hogyan Érd El: {core_transformation} – Napi 10 Percben, Bűntudat és Időhiány Nélkül!",
            f"A Rejtett Módszer, Amivel {target_audience} Végre Megtalálja a Tartós Lelki Békességet",
            f"Végre Egy Útmutató, Ami Valóban Működik a Zsúfolt Hétköznapokban is",
            f"3 Egyszerű Lépés a Szorongás Elengedéséhez és a Belső Harmónia Megéléséhez",
            f"Miért Buknak El a Hagyományos Naplók – És Miért Változtat Meg Mindent Ez az Új Rendszer?"
        ],
        "vsl_script": f"""[0:00 - 0:25 HOOK]
Ha úgy érzed, hogy a mindennapi stressz és rohanás elnyomja a lelki békességedet, nem vagy egyedül. De mi van, ha létezik egy napi 10 perces egyszerű út, amivel {core_transformation}?

[0:25 - 1:00 A PROBLÉMA]
Sok {target_audience} próbálkozik reggeli csendességgel, de a gondolatok elkalandoznak, a teendők listája zakatol, és végül csak a bűntudat marad. A probléma nem veled van – a régi módszerek nem a mai modern, ingerrel teli életre lettek tervezve.

[1:00 - 1:45 A MEGVILÁGOSODÁS & MEGOLDÁS]
Amikor felfedeztük a mikro-reflexiók fókuszált rendszerét, minden megváltozott. Nem kell órákat ülnöd csendben: a vezetett kérdések azonnal a lényegre tapintanak. Ezért hoztuk létre a(z) {topic} csomagot.

[1:45 - 2:30 AZ AJÁNLAT & BÓNUSZOK]
A teljes csomag nemcsak a 30 napos fő útmutatót tartalmazza, hanem azonnali bónuszként megkapod a 30 Napos Imakártyákat és a Céltervező Sablont is. Az összköltség több tízezer forint lenne, de ma egy jelképes 9.990 Ft ($27) összegért a tiéd lehet.

[2:30 - 3:00 GARANCIA & CTA]
14 napos teljes elégedettségi garanciát vállalunk. Kattints az alábbi gombra, töltsd le azonnal a privát hozzáféréseddel, és kezdd el a megújulást még ma!""",
        "three_part_bullets": [
            {
                "mit_kap": "30 Napos Vezetett Lelki Munkafüzet (Printable PDF & Digital)",
                "meg_akkor_is_ha": "Még akkor is, ha reggelente csak 10 perced van a kávéd mellett",
                "ami_azt_jelenti": "Ami azt jelenti, hogy zaklatottság helyett békességben indíthatod a napodat."
            },
            {
                "mit_kap": "30 Válogatott Igehely & Inspiráció Magyarázattal",
                "meg_akkor_is_ha": "Még akkor is, ha nehezen találod meg az igék gyakorlati üzenetét",
                "ami_azt_jelenti": "Ami azt jelenti, hogy azonnal alkalmazható bölcsességet kapsz minden élethelyzetre."
            },
            {
                "mit_kap": "Mély Önismereti & Hálaadó Naplózó Kérdések",
                "meg_akkor_is_ha": "Még akkor is, ha eddig sosem tudtad, mit írj egy üres lapra",
                "ami_azt_jelenti": "Ami azt jelenti, hogy soha nem akadsz el, a kérdések vezetik a gondolataidat."
            },
            {
                "mit_kap": "Nyomtatható A4 & US Letter Formátumok",
                "meg_akkor_is_ha": "Még akkor is, ha tableten (GoodNotes/Notability) vagy papíron szeretsz dolgozni",
                "ami_azt_jelenti": "Ami azt jelenti, hogy maximális kényelemben, bárhol használhatod."
            },
            {
                "mit_kap": "Exkluzív Imádsággyűjtemény a Nehéz Pillanatokra",
                "meg_akkor_is_ha": "Még akkor is, ha úgy érzed, nincsenek szavaid az elcsendesedéshez",
                "ami_azt_jelenti": "Ami azt jelenti, hogy a legnehezebb napokon is támaszt és vigaszt kapsz."
            }
        ],
        "objection_handling": {
            "vehicle_objection": "Ez a csomag nem egy unalmas elméleti könyv, hanem egy azonnal kitölthető, interaktív gyakorlati eszköz napi 10 percben.",
            "internal_objection": "Nem kell szuper-fegyelmezettnek lenned: a struktúra leveszi a döntési fáradtság terhét a válladról.",
            "external_objection": "A digitális letöltés azonnali, örökös hozzáféréssel – nincs szállítási idő vagy elkopó lapok."
        },
        "value_stack": {
            "main_product_value": f"{topic} (Érték: 14.990 Ft)",
            "bonus_1": "30 Napos Keresztény Imakártya Csomag (Érték: 6.990 Ft)",
            "bonus_2": "Reggeli Csendesség Fókuszlapok (Érték: 4.990 Ft)",
            "bonus_3": "Digitális Szokáskövető Sablon (Érték: 7.990 Ft)",
            "total_value": "34.960 Ft ($122)",
            "offer_price": "9.990 Ft ($27)",
            "guarantee_text": "100% Kockázatmentes 14 Napos Áldás-Garancia: Próbáld ki 14 napig, és ha nem hozott valós békességet a napjaidba, kérdés nélkül visszakapod a teljes összeget."
        },
        "sales_letter_full": f"""# {topic}

## Hogyan Találj Tartós Lelki Békességet a Zsúfolt Hétköznapokban – Napi 10 Percben?

Kedves Barátom!

Ismerős az az érzés, amikor reggel még ki sem keltél az ágyból, de az elmédet máris elárasztják a teendők, a határidők és a mindennapi aggodalmak?

Nem vagy egyedül. Mindannyian vágyunk a csendességre és a belső harmóniára, de a mai rohanó világban a hagyományos módszerek sokszor kudarcot vallanak.

### A Megoldás: {topic}

Ez a digitális munkafüzet és lelki napló azért született, hogy kézzelfogható, napi 10 perces hidat adjon a kezedbe.

### Mit Kapsz a Csomagban?
- **30 Napos Vezetett Lelki Munkafüzet:** Napi 10 percben elvégezhető, még ha tele is van a napod, ami azt jelenti, hogy valódi belső békességet kapsz.
- **30 Kiválasztott Igehely & Reflexió:** Pontos gyakorlati tanácsok, hogy azonnal tudd, hogyan cselekedj.
- **Exkluzív Bónuszok:** Imakártyák, fókuszlapok és digitális szokáskövető sablonok!

### 100% Kockázatmentes Garancia
Próbáld ki 14 napig. Ha nem tapasztalsz mélyebb békességet és tisztább fókuszt, 1 e-mail és 100%-ban visszatérítjük az árat.

**[ RENDELD MEG MOST – AZONNALI LETÖLTÉSSEL ]**"""
    }


def parse_json_or_fallback(raw_text: str, topic: str, target_audience: str, core_transformation: str, language: str = "Magyar") -> Dict[str, Any]:
    """Parses JSON safely from AI output with markdown fence stripping and fallback."""
    cleaned = raw_text.strip()
    if "```json" in cleaned:
        cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in cleaned:
        cleaned = cleaned.split("```", 1)[1].split("```", 1)[0].strip()

    try:
        data = json.loads(cleaned)
        if isinstance(data, dict) and "big_domino" in data and "headlines" in data:
            return data
    except Exception:
        pass

    # Regex extraction fallback
    try:
        json_match = re.search(r'(\{[\s\S]*\})', cleaned)
        if json_match:
            data = json.loads(json_match.group(1))
            if isinstance(data, dict) and "big_domino" in data:
                return data
    except Exception:
        pass

    # Fallback to offline generator
    fallback = generate_offline_ffc_pack(topic, target_audience, core_transformation, language=language)
    if cleaned and len(cleaned) > 100:
        fallback["sales_letter_full"] = cleaned
    return fallback


def generate_ffc_sales_pack(
    topic: str,
    target_audience: str,
    core_transformation: str,
    language: str = "Magyar",
    vehicle: str = "",
    extra_notes: str = "",
    product_type: str = "Keresztény Digitális Termék"
) -> Dict[str, Any]:
    """
    Main entry point: Generates a complete FFC sales pack using KeyManager with 4-tier fallback.
    Returns a robust structured dictionary matching the exact language requested.
    """
    is_en = "angol" in language.lower() or "english" in language.lower()
    prompt = build_ffc_prompt(topic, target_audience, core_transformation, language, vehicle, extra_notes, product_type)

    if get_key_manager:
        km = get_key_manager()
        sys_inst = (
            "You are a world-class Direct Response Copywriter in the style of Russell Brunson and Alex Hormozi. Output strictly valid JSON in 100% pure, natural, fluent English (US) without mixing any other languages."
            if is_en else
            "Te egy világklasszis Russell Brunson és Alex Hormozi stílusú konverziós szövegíró vagy. Válaszolj szigorúan érvényes JSON formátumban 100%-ban tiszta, professzionális magyar nyelven."
        )
        ok, res = km.generate_text_with_fallback(
            prompt=prompt,
            system_instruction=sys_inst
        )
        if ok and res.strip():
            return parse_json_or_fallback(res, topic, target_audience, core_transformation, language=language)

    return generate_offline_ffc_pack(topic, target_audience, core_transformation, language=language)

