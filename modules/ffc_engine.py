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
    """Builds a structured prompt for Russell Brunson & Alex Hormozi style direct response copy."""
    vehicle_text = vehicle if vehicle.strip() else "Vezetett napi bibliai reflexiók, imádságok és letisztult printable naplólapok"
    notes_text = f"\n- További preferenciák: {extra_notes}" if extra_notes.strip() else ""

    return f"""
Te egy világklasszis Direct Response Copywriter és FFC (Faceless Funnel) értékesítési szakértő vagy Russell Brunson és Alex Hormozi stílusában.
A feladatod egy mélyen megrendítő, hiteles, magas konverziójú, 10-részes értékesítési csomag (Sales Pack) elkészítése az alábbi termékhez.

=== TERMÉK ADATOK ===
- Terméktípus: {product_type}
- Fő téma / Piac: {topic}
- Célközönség: {target_audience}
- Fő transzformáció (Végső Ígéret): {core_transformation}
- Eszköz / Módszer (The Vehicle): {vehicle_text}{notes_text}
- Nyelv: {language}

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
  "sales_letter_full": "Teljes formázott Russell Brunson stílusú értékesítési szöveg címsorokkal, történettel, bullet pontokkal és lezárással."
}}
"""


def generate_offline_ffc_pack(topic: str, target_audience: str, core_transformation: str) -> Dict[str, Any]:
    """Generates an immediate, high-quality offline FFC sales pack if all APIs are unavailable."""
    return {
        "product_title": topic,
        "big_domino": f"Ha meg tudom győzni {target_audience} tagjait arról, hogy a napi vezetett keresztény reflexió az egyetlen kulcs {core_transformation} eléréséhez, akkor azonnal meg fogják vásárolni ezt a csomagot.",
        "headlines": [
            f"Hogyan Érd El: {core_transformation} – Napi 10 Percben, Bűntudat és Időhiány Nélkül!",
            f"A Rejtett Bibliai Módszer, Amivel {target_audience} Végre Megtalálja a Tartós Lelki Békességet",
            f"Végre Egy Keresztény Útmutató, Ami Valóban Működik a Zsúfolt Hétköznapokban is",
            f"3 Egyszerű Lépés a Szorongás Elengedéséhez és a Belső Harmónia Megéléséhez",
            f"Miért Buknak El a Hagyományos Naplók – És Miért Változtat Meg Mindent Ez az Új Rendszer?"
        ],
        "vsl_script": f"""[0:00 - 0:25 HOOK]
Ha úgy érzed, hogy a mindennapi stressz és rohanás elnyomja a lelki békességedet, nem vagy egyedül. De mi van, ha létezik egy napi 10 perces egyszerű út, amivel {core_transformation}?

[0:25 - 1:00 A PROBLÉMA]
Sok {target_audience} próbálkozik reggeli csendességgel, de a gondolatok elkalandoznak, a teendők listája zakatol, és végül csak a bűntudat marad. A probléma nem veled van – a régi módszerek nem a mai modern, ingerrel teli életre lettek tervezve.

[1:00 - 1:45 A MEGVILÁGOSODÁS & MEGOLDÁS]
Amikor felfedeztük a mikro-reflexiók és a bibliai igék fókuszált rendszerét, minden megváltozott. Nem kell órákat ülnöd csendben: a vezetett kérdések azonnal a lényegre tapintanak. Ezért hoztuk létre a(z) {topic} csomagot.

[1:45 - 2:30 AZ AJÁNLAT & BÓNUSZOK]
A teljes csomag nemcsak a 30 napos fő útmutatót tartalmazza, hanem azonnali bónuszként megkapod a 30 Napos Imakártyákat és a Keresztény Céltervező Sablont is. Az összköltség több tízezer forint lenne, de ma egy jelképes 9.990 Ft ($27) összegért a tiéd lehet.

[2:30 - 3:00 GARANCIA & CTA]
14 napos teljes elégedettségi garanciát vállalunk. Kattints az alábbi gombra, töltsd le azonnal a privát Google Drive hozzáféréseddel, és kezdd el a megújulást még ma!""",
        "three_part_bullets": [
            {
                "mit_kap": "30 Napos Vezetett Lelki Munkafüzet (Printable PDF & Digital)",
                "meg_akkor_is_ha": "Még akkor is, ha reggelente csak 10 perced van a kávéd mellett",
                "ami_azt_jelenti": "Ami azt jelenti, hogy zaklatottság helyett Isten jelenlétében és békességben indíthatod a napodat."
            },
            {
                "mit_kap": "30 Válogatott KJV & Magyar Igehely Magyarázattal",
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
                "meg_akkor_is_ha": "Még akkor is, ha úgy érzed, nincsenek szavaid az imádsághoz",
                "ami_azt_jelenti": "Ami azt jelenti, hogy a legnehezebb napokon is támaszt és vigaszt kapsz."
            }
        ],
        "objection_handling": {
            "vehicle_objection": "Ez a csomag nem egy unalmas teológiai könyv, hanem egy azonnal kitölthető, interaktív gyakorlati eszköz napi 10 percben.",
            "internal_objection": "Nem kell szuper-fegyelmezettnek lenned: a struktúra leveszi a döntési fáradtság terhét a válladról.",
            "external_objection": "A digitális letöltés azonnali, örökös hozzáféréssel – nincs szállítási idő vagy elkopó lapok."
        },
        "value_stack": {
            "main_product_value": f"{topic} (Érték: 14.990 Ft)",
            "bonus_1": "30 Napos Keresztény Imakártya Csomag (Érték: 6.990 Ft)",
            "bonus_2": "Reggeli Csendesség Fókuszlapok (Érték: 4.990 Ft)",
            "bonus_3": "Digitális Keresztény Szokáskövető Sablon (Érték: 7.990 Ft)",
            "total_value": "34.960 Ft ($122)",
            "offer_price": "9.990 Ft ($27)",
            "guarantee_text": "100% Kockázatmentes 14 Napos Áldás-Garancia: Próbáld ki 14 napig, és ha nem hozott valós békességet a napjaidba, kérdés nélkül visszakapod a teljes összeget."
        },
        "sales_letter_full": f"""# {topic}

## Hogyan Találj Tartós Lelki Békességet a Zsúfolt Hétköznapokban – Napi 10 Percben?

Kedves Barátom!

Ismerős az az érzés, amikor reggel még ki sem keltél az ágyból, de az elmédet máris elárasztják a teendők, a határidők és a mindennapi aggodalmak?

Nem vagy egyedül. Keresztényként mindannyian vágyunk a csendességre és Isten jelenlétére, de a mai rohanó világban a hagyományos módszerek sokszor kudarcot vallanak.

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


def parse_json_or_fallback(raw_text: str, topic: str, target_audience: str, core_transformation: str) -> Dict[str, Any]:
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
    fallback = generate_offline_ffc_pack(topic, target_audience, core_transformation)
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
    Returns a robust structured dictionary.
    """
    prompt = build_ffc_prompt(topic, target_audience, core_transformation, language, vehicle, extra_notes, product_type)

    if get_key_manager:
        km = get_key_manager()
        ok, res = km.generate_text_with_fallback(
            prompt=prompt,
            system_instruction="Te egy világklasszis Russell Brunson és Alex Hormozi stílusú konverziós szövegíró vagy. Válaszolj szigorúan érvényes JSON formátumban."
        )
        if ok and res.strip():
            return parse_json_or_fallback(res, topic, target_audience, core_transformation)

    return generate_offline_ffc_pack(topic, target_audience, core_transformation)
