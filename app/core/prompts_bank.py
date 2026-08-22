"""
Master Prompt Generator & Niche Bank for Christian & Multi-Niche Digital Products
================================================================================
Contains:
- 22 high-demand niche categories (5 supergroups)
- Model-specific prompt profiles (Pollinations FLUX, Google Imagen, Gemini Native)
- Builders for KDP interiors, storybooks, covers, Etsy listings, Gumroad devotionals, and FFC copy
"""

import re
import json
from typing import Dict, Any, List, Optional


NICHE_CATEGORIES = {
    "✝️ Keresztény & Bibliai Rétegpiac (Alapértelmezett)": {
        "group": "Spirituality & Faith",
        "name_en": "Christian & Biblical Niche",
        "default_audience": "Keresztény hívők, édesanyák és családok, akik lelki csendességre és hitbeli megújulásra vágynak",
        "keywords": ["Scripture", "KJV Bible", "Faith", "Devotional", "Prayer", "Christian living", "Peace with God"],
        "tone": "Meleg, tiszteletteljes, biblikus, bátorító, mélyen emberi és békességet sugárzó",
        "visual_style": "Soft Scandinavian sage green, gold accents, clean minimalist typography, watercolor floral borders"
    },
    "💼 Online Üzlet & Digitális Termékek (Online Business & PLR)": {
        "group": "Make Money & Business",
        "name_en": "Online Business & Digital Products",
        "default_audience": "Kezdő és haladó digitális vállalkozók, akik passzív jövedelmet és digitális termékeket akarnak eladni",
        "keywords": ["Passive income", "Digital products", "PLR", "Sales funnels", "Email marketing", "Gumroad", "Etsy"],
        "tone": "Közvetlen, gyakorlatias, konverziófókuszú, energikus és cselekvésre ösztönző",
        "visual_style": "Modern dark slate, vibrant emerald & gold accents, sleek dashboard elements, crisp modern typography"
    },
    "📈 Befektetés & Személyes Pénzügyek (Investing & Personal Finance)": {
        "group": "Make Money & Business",
        "name_en": "Investing & Personal Finance",
        "default_audience": "Pénzügyi tudatosságra, adósságmentességre és vagyonépítésre törekvő magánszemélyek és családok",
        "keywords": ["Financial freedom", "Index funds", "Budgeting", "Compound interest", "Wealth building", "Emergency fund"],
        "tone": "Hiteles, megbízható, elemző, letisztult, felelősségteljes és strukturált",
        "visual_style": "Deep navy blue, emerald green growth accents, minimalist charts, clean corporate serif layout"
    },
    "🤖 AI & Üzleti Automatizáció (AI & Business Automation)": {
        "group": "Make Money & Business",
        "name_en": "AI & Business Automation",
        "default_audience": "Szabadúszók, tartalomkészítők és cégvezetők, akik AI eszközökkel akarják 10x-ezni a hatékonyságukat",
        "keywords": ["AI prompts", "ChatGPT", "Gemini", "Workflow automation", "Make.com", "No-code", "Productivity 10x"],
        "tone": "Élvonalbeli, innovatív, lényegretörő, modern és technológiailag magabiztos",
        "visual_style": "Cyber slate, neon cyan and violet highlights, glowing modern interface cards"
    },
    "⚡ Produktivitás & Notion Rendszerek (Productivity/Notion)": {
        "group": "Self-Improvement",
        "name_en": "Productivity & Notion Systems",
        "default_audience": "Túlterhelt szakemberek, ADHD-s alkotók és diákok, akik rendszerezni akarják a mindennapjaikat",
        "keywords": ["Second Brain", "Notion templates", "Time blocking", "Deep work", "Habit tracker", "Task management"],
        "tone": "Rendszerezett, megnyugtató, strukturált és súrlódásmentes",
        "visual_style": "Minimalist monochrome, soft slate gray, clean grid structure, aesthetic Notion style"
    },
    "🧠 Gondolkodásmód & Szokások (Mindset & Habits)": {
        "group": "Self-Improvement",
        "name_en": "Mindset & Habit Mastery",
        "default_audience": "Önfejlesztésre nyitott emberek, akik le akarják győzni a halogatást és tartós szokásokat építenek",
        "keywords": ["Atomic habits", "Growth mindset", "Dopamine detox", "Overcoming procrastination", "Discipline"],
        "tone": "Inspiráló, pszichológiailag megalapozott, bátorító és együttérző",
        "visual_style": "Warm beige, terracotta and forest green, organic shapes, thoughtful editorial typography"
    },
    "🧘 Mentális Egészség & Stresszoldás (Mental Health & Stress Relief)": {
        "group": "Health & Fitness",
        "name_en": "Mental Health & Stress Relief",
        "default_audience": "Szorongással, kiégéssel és stresszel küzdő egyének, akik belső békére vágynak",
        "keywords": ["Burnout recovery", "Anxiety relief", "Nervous system regulation", "Journaling prompts", "Somatic exercises"],
        "tone": "Mélyen együttérző, biztonságos, megnyugtató és támogató",
        "visual_style": "Muted lavender, soft sage, warm cream, calming minimalist aesthetic"
    },
    "🎨 Grafikai Tervezés & Canva Sablonok (Graphic Design / Canva)": {
        "group": "Tech & Creativity",
        "name_en": "Graphic Design & Canva Templates",
        "default_audience": "Kisvállalkozók, tartalomkészítők és alkotók, akik gyorsan akarnak profi dizájnokat készíteni",
        "keywords": ["Canva templates", "Brand identity", "Typography rules", "Color palettes", "Social media kits"],
        "tone": "Kreatív, stílusos, esztétikus és lépésről-lépésre gyakorlatias",
        "visual_style": "Pastel aesthetic, modern grid cards, beautiful typography hierarchy"
    },
    "📖 Könyvkiadás & Amazon KDP (Self-Publishing / KDP)": {
        "group": "Tech & Creativity",
        "name_en": "Self-Publishing & Amazon KDP Books",
        "default_audience": "Amazon KDP szerzők, színezőkönyv és alacsony tartalmú könyvkiadók",
        "keywords": ["KDP interiors", "Book cover design", "Amazon KDP keywords", "Coloring books", "Publishing blueprint"],
        "tone": "Kiadói színvonalú, strukturált, kereskedelmi és niche-célzott",
        "visual_style": "Clean book trim outlines, 8.5x11 mockups, elegant editorial covers"
    }
}


IMAGE_MODEL_PROFILES = {
    "flux": {
        "name": "Pollinations FLUX",
        "prompt_style": "natural_language",
        "use_affirmative_framing": True,
        "coloring_child_template": (
            "A coloring book page for children of {scene}. "
            "Simple, bold, thick black ink outlines on a solid pure white background. "
            "Cute, friendly characters with expressive faces and large open areas for coloring. "
            "Flat vector line art style with uniform stroke weight throughout. "
            "Clean, high-contrast black ink drawing only, portrait orientation, "
            "professional printable coloring book illustration."
        ),
        "coloring_adult_template": (
            "An intricate adult coloring book page of {scene}. "
            "Fine detailed black ink line work on solid pure white paper. "
            "Classical engraving style combined with ornate zentangle "
            "and botanical mandala patterns filling the background. "
            "All human figures have realistic anatomical proportions with dignified, "
            "elegant facial features and flowing draped fabric folds. "
            "All animals are anatomically accurate and majestic. "
            "Dense decorative patterns extending to page edges. "
            "Flat black ink drawing with uniform line weight, "
            "portrait 8.5 by 11 inches format, ultra high detail, "
            "designed for adult stress relief coloring and meditation."
        ),
        "cover_template": (
            "A vibrant, colorful illustrated book cover depicting {scene}. "
            "Professional publishing quality with harmonious pastel color palette. "
            "The title '{title}' appears in bold, clean, highly legible typography at the top. "
            "Vector art illustration style with rich warm colors, high resolution, "
            "landscape orientation matching a wrap-around book cover format."
        ),
        "wall_art_template": (
            "An elegant minimalist watercolor art print of {scene}. "
            "Soft pastel watercolor palette with delicate brush strokes. "
            "Beautiful, clean typography reads: '{text}'. "
            "Modern Scandinavian wall art style, portrait orientation, "
            "museum-quality digital print, high resolution."
        ),
        "clipart_template": (
            "A watercolor illustration of {scene}, cute chibi kawaii style, "
            "soft pastel color palette, completely isolated on a solid pure white background, "
            "high detail, consistent clipart bundle art style."
        )
    },
    "imagen": {
        "name": "Google Imagen",
        "prompt_style": "creative_brief",
        "use_affirmative_framing": False,
        "coloring_child_template": (
            "Clean, friendly black and white children's coloring page of {scene}. "
            "Simple, bold thick black outlines on pure crisp white background. "
            "No shading, no gray tones, no color anywhere. "
            "Cute, expressive and joyful characters, clear distinct colorable shapes, "
            "vector illustration style. 8.5x11 portrait ratio, 4K resolution."
        ),
        "coloring_adult_template": (
            "Highly intricate adult coloring book page of {scene}. "
            "Fine black line art on pure crisp white background, zero shading, zero grayscale, zero colors. "
            "Realistic anatomical proportions, dignified classic engraving lines, "
            "flowing drapery, complex zentangle, botanical floral mandala background patterns. "
            "NO cartoon elements, NO chibi style, NO simplified toy-like shapes. "
            "8.5x11 portrait ratio, 4K resolution."
        ),
        "cover_template": (
            "A high-quality colorful book cover depicting {scene}, "
            "consistent pastel color palette, vector art style, with bold, clean typography at the top "
            "that reads exactly: '{title}', high resolution, professional design, 17.412:11.25 aspect ratio."
        ),
        "wall_art_template": (
            "An elegant minimalist watercolor design with {scene}. "
            "The text reads in beautiful, clean typography: '{text}', "
            "high resolution, modern Scandinavian wall art style, 4:5 aspect ratio."
        ),
        "clipart_template": (
            "Watercolor illustration of {scene}, cute chibi style, "
            "soft pastel color palette, isolated on pure white background, "
            "high detail, consistent clipart bundle style."
        )
    }
}


def get_model_profile(model_name: str = "") -> dict:
    if not model_name:
        return IMAGE_MODEL_PROFILES["flux"]
    name_lower = model_name.lower()
    if any(k in name_lower for k in ["pollin", "flux"]):
        return IMAGE_MODEL_PROFILES["flux"]
    return IMAGE_MODEL_PROFILES.get("imagen", IMAGE_MODEL_PROFILES["flux"])


def get_niche_prompt_context(niche_key: str) -> dict:
    if niche_key in NICHE_CATEGORIES:
        return NICHE_CATEGORIES[niche_key]
    return NICHE_CATEGORIES["✝️ Keresztény & Bibliai Rétegpiac (Alapértelmezett)"]


# ─────────────────────────────────────────────────────────
# KDP COLORING PROMPT BUILDERS
# ─────────────────────────────────────────────────────────

def build_kdp_gem_master_instruction(book_title: str, is_adult: bool = False, character_rules: str = "") -> str:
    """Generates Gemini Gem Master System Instruction for character & style consistency."""
    style_desc = (
        "Intricate adult coloring book pages with fine black ink engraving lines, detailed mandala/zentangle floral backgrounds, realistic dignified anatomy, zero shading, pure white background."
        if is_adult else
        "Cute, friendly children's coloring book pages with bold thick outlines, simple open shapes for coloring, adorable expressive characters, zero shading, pure white background."
    )
    
    char_section = f"\n3. CHARACTER CONSISTENCY RULES:\n{character_rules.strip()}" if character_rules.strip() else ""

    return f"""# GEMINI GEM MASTER INSTRUCTION: KDP COLORING BOOK CREATOR
You are the dedicated Master Art Director and Illustrator for the Amazon KDP coloring book titled: "{book_title}".

CORE DIRECTIVES:
1. ART STYLE: {style_desc}
2. RATIO & OUTPUT: 8.5x11 inch portrait ratio, high contrast black line art on pure solid white paper. No gray tones, no shading, no gradient fills.{char_section}
4. CONSISTENCY: Every image generated in this project MUST maintain the exact same stroke weight, artistic style, and character design features throughout all scenes.
5. PROMPT FORMAT: Generate high-detail English image prompts ready for Pollinations FLUX / Google Imagen.
"""


def build_kdp_autopilot_manifest_prompt(
    book_title: str,
    target_audience: str,
    page_count: int = 10,
    niche_context: str = "",
    is_adult: bool = False
) -> str:
    """Builds prompt requesting strict JSON manifest with numbered scenes."""
    style_mode = "ADULT intricate zentangle line art with fine details" if is_adult else "CHILDREN clean bold line art with cute shapes"
    
    return f"""Create a publication-ready {page_count}-page Amazon KDP coloring book outline and manifest for:
Book Title: "{book_title}"
Target Audience: {target_audience} ({style_mode})
Theme / Niche: {niche_context or 'Christian & Faith'}

Return a strictly valid JSON array of exactly {page_count} objects with NO markdown fences, matching this structure:
[
  {{
    "page_number": 1,
    "title": "Short Scene Title in English",
    "title_hu": "Jelenet címe magyarul",
    "scripture_reference": "Book Chapter:Verse (e.g. Genesis 1:3)",
    "scripture_text": "Full verse text in English (KJV)",
    "color_suggestions": ["Color 1", "Color 2", "Color 3", "Color 4", "Color 5"],
    "visual_prompt": "Clean natural language English image prompt for coloring page, pure white background, thick black ink lines, no shading, 8.5x11 ratio",
    "reflection_thought": "Short 1-2 sentence devotional reflection"
  }}
]
"""


def parse_kdp_autopilot_manifest_json(raw_text: str) -> List[Dict[str, Any]]:
    """Safely extracts JSON array of scenes from AI response."""
    clean = raw_text.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^```(?:json)?", "", clean)
        clean = re.sub(r"```$", "", clean).strip()

    start = clean.find("[")
    end = clean.rfind("]")
    if start != -1 and end != -1 and end > start:
        clean = clean[start:end + 1]

    try:
        data = json.loads(clean)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


# ─────────────────────────────────────────────────────────
# KDP STORYBOOK PROMPT BUILDERS
# ─────────────────────────────────────────────────────────

def build_illustrated_book_manifest_prompt(
    book_title: str,
    chapter_count: int = 6,
    theme: str = "Christian faith & courage",
    target_age: str = "Ages 4-8",
    art_style: str = "Disney Pixar 3D cute cartoon"
) -> str:
    """Builds prompt for illustrated children storybook with chapters and 1:1 image prompts."""
    return f"""Write a complete {chapter_count}-chapter illustrated children's storybook.
Title: "{book_title}"
Theme: {theme}
Target Age: {target_age}
Illustration Art Style: {art_style}

Return a strictly valid JSON array of {chapter_count} objects:
[
  {{
    "page_number": 1,
    "chapter_title": "1. Fejezet: [Magyar Cím]",
    "story_text": "Magyar nyelvű meserészlet (40-60 szó, szívhez szóló, bátorító történet).",
    "illustration_prompt": "Vibrant full color illustration of [scene], {art_style}, 1:1 square aspect ratio, soft warm lighting, 8.5x8.5 KDP print ready",
    "scene_summary": "Rövid összefoglaló a jelenetről"
  }}
]
"""


def parse_illustrated_book_manifest_json(raw_text: str) -> List[Dict[str, Any]]:
    return parse_kdp_autopilot_manifest_json(raw_text)


# ─────────────────────────────────────────────────────────
# KDP COVER PROMPT BUILDERS
# ─────────────────────────────────────────────────────────

def build_kdp_dynamic_cover_prompt(
    book_title: str,
    subtitle: str,
    author_name: str,
    scene_description: str,
    dimensions_summary: str,
    aspect_ratio_str: str = "1.55:1"
) -> str:
    """Builds wrap-around KDP book cover prompt."""
    return (
        f"A panoramic wrap-around book cover artwork for Amazon KDP ({dimensions_summary}, aspect ratio {aspect_ratio_str}). "
        f"Right 45% (Front Cover): Majestic scene depicting {scene_description}. "
        f"Prominently featuring the title '{book_title.upper()}' in bold elegant gold typography at the top, "
        f"subtitle '{subtitle}' in refined font, and author '{author_name}' at the bottom. "
        f"Center spine: Vertical title '{book_title}' with matching theme background. "
        f"Left 45% (Back Cover): Atmospheric matching background with soft lighting and empty area reserved for barcode. "
        f"Ultra high resolution, 300 DPI print quality, vivid harmonious colors, professional graphic design."
    )


# ─────────────────────────────────────────────────────────
# ETSY WALL ART & CLIPART PROMPT BUILDERS
# ─────────────────────────────────────────────────────────

def build_etsy_wall_art_prompt(scripture_ref: str, scripture_text: str, art_style: str = "Scandinavian Watercolor") -> str:
    """Generates prompt for Etsy Scripture Wall Art."""
    return (
        f"An elegant minimalist {art_style} art print featuring the Bible verse: '{scripture_text}' ({scripture_ref}). "
        f"Soft harmonious color palette, delicate botanical accents, clean modern typography, "
        f"museum-quality printable wall art, 4:5 portrait ratio, 300 DPI print ready."
    )


def build_etsy_clipart_prompt(subject: str, count: int = 6) -> str:
    """Generates prompt for transparent/white background sticker clipart bundle."""
    return (
        f"A set of {count} cute watercolor clipart illustrations of {subject}. "
        f"Chibi sticker style with clean edges, soft pastel colors, completely isolated on a pure white background, "
        f"high detail, PNG sticker bundle format."
    )


def build_strict_etsy_seo_prompt(product_title: str, niche: str = "Christian Wall Art") -> str:
    """Generates prompt for strict 2026 Etsy SEO (Title max 140, 13 tags max 20 chars each)."""
    return f"""You are an expert Etsy 2026 SEO copywriter.
Product: "{product_title}"
Niche: {niche}

Generate the optimized Etsy listing metadata:
1. TITLE: Exactly under 140 characters, frontloaded with high-search keywords.
2. 13 TAGS: Exactly 13 tags, each STRICTLY maximum 20 characters, lowercase, no prohibited symbols (%$#@!?).
3. FFC DESCRIPTION: High-conversion description with Features, Feelings, and Instant Google Drive Delivery Notice.

Return valid JSON:
{{
  "title": "Optimized Etsy Title (max 140 chars)",
  "tags": ["tag 1", "tag 2", "tag 3", "tag 4", "tag 5", "tag 6", "tag 7", "tag 8", "tag 9", "tag 10", "tag 11", "tag 12", "tag 13"],
  "features": "• Bullet point features",
  "emotional_hook": "Emotional hook paragraph",
  "price": "6.99"
}}
"""


def parse_strict_etsy_seo_output(raw_text: str) -> Dict[str, Any]:
    clean = raw_text.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^```(?:json)?", "", clean)
        clean = re.sub(r"```$", "", clean).strip()
    try:
        data = json.loads(clean)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


# ─────────────────────────────────────────────────────────
# GUMROAD & FFC MARKETING PROMPT BUILDERS
# ─────────────────────────────────────────────────────────

def build_ffc_avatar_research_prompt(product_name: str, niche: str) -> str:
    """Builds 8-step psychological avatar research prompt."""
    return f"""Perform an in-depth 8-step psychological avatar research for:
Product: "{product_name}"
Niche: {niche}

Analyze:
1. Demographics & Core Identity
2. Surface-level Frustrations vs. Deep Hidden Fears
3. Daily Friction Points & Sensory Overload
4. The Big Domino (The single belief shift required to make buying inevitable)
5. False Beliefs about The Vehicle (this type of solution)
6. False Beliefs about Internal Abilities
7. False Beliefs about External Obstacles
8. Emotional Payoff & Identity Transformation
"""


def build_ffc_big_domino_hooks_prompt(product_name: str, niche: str) -> str:
    """Builds prompt for 10 Russell Brunson style golden headline hooks."""
    return f"""Generate 10 Russell Brunson style golden formula headlines for "{product_name}" ({niche}):
Include:
- How To [Desire] Without [Pain]
- The Secret To [Desire] Even If [Obstacle]
- Warning: Stop [Mistake] Before It Costs You [Loss]
- The #1 Habit That [Achieves Goal] In [Timeframe]
"""


def build_ffc_value_stack_prompt(product_name: str, niche: str) -> str:
    """Builds Value Stack and pricing tier matrix prompt."""
    return f"""Create a high-converting Russell Brunson Value Stack for "{product_name}" ({niche}):
Include:
- Core Product + Perceived Value
- Bonus 1 (Fast Action) + Perceived Value
- Bonus 2 (Tool/Template) + Perceived Value
- Bonus 3 (Checklist/Tracker) + Perceived Value
- Total Perceived Value
- Irresistible Launch Price (e.g. 80% discount)
- 30-day Risk-Free Guarantee
"""


def build_ffc_sales_letter_prompt(product_name: str, niche: str) -> str:
    """Builds 12-step high-converting sales letter prompt."""
    return f"""Write a compelling 12-step direct response sales letter for:
Product: "{product_name}"
Niche: {niche}

Follow Russell Brunson's DotCom Secrets framework:
1. Headline & Hook
2. The Story & Struggle
3. The Epiphany (Aha! Moment)
4. The Big Domino
5. Introducing the Solution
6. What's Inside (Features & Benefits)
7. The Value Stack
8. Risk-Reversal Guarantee
9. Urgency & Scarcity
10. Call to Action
"""


def build_google_sites_landing_page_prompt(product_name: str, niche: str) -> str:
    """Builds 0 Ft Google Sites landing page wireframe prompt."""
    return f"""Create a clean, 0-Ft Google Sites sales page copy and wireframe layout for:
Product: "{product_name}"
Niche: {niche}

Provide section-by-section copy: Hero banner, Problem/Agitate, Solution, 3 Feature Cards, Testimonial placeholders, Value Stack box, and CTA button copy.
"""


def build_email_funnel_3day_prompt(product_name: str, niche: str) -> str:
    """Builds 3-day welcome sequence email prompt."""
    return f"""Write a 3-Day Welcome Email Sequence for "{product_name}" ({niche}):
Day 1: Instant Download & Welcome (Set expectations, deliver immediate win)
Day 2: The Origin Story & Overcoming the Struggle (Build deep empathy and trust)
Day 3: The Big Epiphany & Next Step Invitation (Soft pitch with value stack)
"""


def build_email_funnel_30day_prompt(product_name: str, niche: str) -> str:
    """Builds 30-day 5-phase email funnel outline."""
    return f"""Outline a 30-Day 5-Phase Email Marketing Funnel for "{product_name}" ({niche}):
Phase 1 (Days 1-5): Induction & Immediate Value
Phase 2 (Days 6-12): Overcoming Vehicle False Beliefs
Phase 3 (Days 13-19): Overcoming Internal False Beliefs
Phase 4 (Days 20-25): Case Studies & Social Proof
Phase 5 (Days 26-30): Urgency, Deadline & Final Stack
"""


def build_social_seo_calendar_30day_prompt(product_name: str, niche: str) -> str:
    """Builds 30-day multi-platform social media calendar."""
    return f"""Create a 30-Day Multi-Platform Social Media & SEO Calendar for "{product_name}" ({niche}):
Include for each week:
- 3x Pinterest Pin concepts (Keywords, visual prompt, hook)
- 3x Instagram Reels / TikTok scripts (3-second hook, core message, CTA)
- 1x Email newsletter snippet
"""


# ─────────────────────────────────────────────────────────
# PINTEREST PASSZÍV VIZUÁLIS SEO & SECTION 5 MASTER PROMPTOK
# ─────────────────────────────────────────────────────────

def build_pinterest_pin_seo_prompt(product_name: str, niche: str, product_type: str = "Etsy Digital Wall Art") -> str:
    """Builds prompt for generating 5 high-intent Pinterest Pin SEO sets."""
    return f"""Generate 5 high-converting, evergreen Pinterest Visual SEO Pin concepts for:
Product: "{product_name}"
Niche: {niche}
Product Type: {product_type}

Pinterest is a visual search engine where users search with strong purchase intent. 
Provide 5 distinct Pin concepts matching high-search volume keywords (e.g. 'Christian coloring book for toddlers', 'Psalm 23 minimalist wall art', '30 day devotional journal for women').

For each Pin provide:
1. Pin Concept & Target Search Keyword
2. Catchy Pin Title (max 100 chars, highly searchable)
3. SEO-Optimized Pin Description (200-400 chars, natural tone, clear benefit, call-to-action to visit store, 5 targeted hashtags)
4. Canva Visual Template Advice (Aspect ratio 2:3 or 1000x1500px, color palette, text overlay hook, mockup style)
5. Call To Action & Link Placement Strategy
"""


def build_kdp_coloring_interior_master_prompt(scene_description: str) -> str:
    """Section 5.1: Master Prompt for KDP Coloring Book Interior (Gemini / FLUX)."""
    return (
        f"Kérlek, hozz létre egy tiszta, fekete-fehér gyermek színező oldalt a következőről: "
        f"[{scene_description}] a Nano Banana Pro modellel. "
        f"Stíluskövetelmények: Egyszerű, vastag fekete vonalakkal dolgozz, tiszta fehér háttérrel, "
        f"árnyékolás, szürke tónusok és színátmenetek nélkül. Kedves, konzisztens vektorgrafikus gyerekkönyv stílus legyen, "
        f"egységes vonalvastagsággal és letisztult formákkal. A lap méretaránya legyen 8.5:11 hüvelyk, 4K felbontásban."
    )


def build_kdp_cover_master_prompt(main_theme: str, book_title: str) -> str:
    """Section 5.1: Master Prompt for KDP Book Cover."""
    return (
        f"A high-quality colorful children's book cover depicting [{main_theme}], "
        f"consistent pastel color palette, vector art style, with bold, clean typography at the top "
        f"that reads exactly: '[{book_title}]', high resolution, professional design, 17.412:11.25 aspect ratio."
    )


def build_etsy_wallart_master_prompt(exact_kjv_quote: str) -> str:
    """Section 5.2: Master Prompt for Etsy Christian Wall Art."""
    return (
        f"An elegant minimalist watercolor design with soft green eucalyptus leaves framing a central text. "
        f"The text reads in beautiful, clean typography: '[{exact_kjv_quote}]', "
        f"high resolution, modern Scandinavian Christian wall art style, 4:5 aspect ratio."
    )


def build_etsy_clipart_master_prompt(character_subject: str) -> str:
    """Section 5.2: Master Prompt for Etsy Clipart Bundles."""
    return (
        f"Watercolor illustration of [{character_subject}], cute chibi style, "
        f"soft pastel color palette, isolated on pure white background, high detail, consistent clipart bundle style."
    )


def build_etsy_bg_removal_prompt() -> str:
    """Section 5.2: Master Prompt for Multi-Turn Conversational Background Removal."""
    return "Kérlek, távolítsd el a fehér hátteret a fenti grafikák mögül, és tegyed őket teljesen átlátszóvá (transparent PNG format)."


def build_gumroad_devotional_master_prompt(devotional_title: str, day_number: int, matrix_row: str) -> str:
    """Section 5.3: Master Prompt for 30-Day Devotional Journal Text."""
    return f"""Szeretnék egy mély, hiteles és lelkileg építő 30 napos keresztény áhítat naplót (devotional) írni nőknek '[{devotional_title}]' címmel. Az alábbiakban megadom a NotebookLM által teológiailag ellenőrzött vázlatot a(z) [{day_number}.] naphoz: [{matrix_row}]. Kérlek, írd meg a nap teljes tartalmát. Tartalmazzon: a megadott KJV bibliai igét, egy 200 szavas bátorító magyarázó-elmélkedő szöveget, egy napi imát, és 3 db mély, elgondolkodtató önreflektív kérdést. Stílusutasítás: Kerüld a tipikus, mesterkélt AI-fordulatokat és a túl száraz megfogalmazást. Írj meleg, mélyen bátorító, spirituális, tiszteletteljes és emberi tónusban."""

