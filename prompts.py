"""
Master Prompt Generator Engine for Christian & Multi-Niche Digital Products
Based on the Autism-Friendly 100% Async Digital Business System Document
(Google AI Pro Ecosystem - Master Prompt Templates, 22 High-Demand Niches & FFC Copywriting Framework)
"""

# ─────────────────────────────────────────────────────────
# 22 HIGH-DEMAND NICHE CATEGORIES (5 SUPERGROUPS)
# ─────────────────────────────────────────────────────────

NICHE_CATEGORIES = {
    "✝️ Keresztény & Bibliai Rétegpiac (Alapértelmezett)": {
        "group": "Spirituality & Faith",
        "name_en": "Christian & Biblical Niche",
        "default_audience": "Keresztény hívők, édesanyák és családok, akik lelki csendességre és hitbeli megújulásra vágynak",
        "keywords": ["Scripture", "KJV Bible", "Faith", "Devotional", "Prayer", "Christian living", "Peace with God"],
        "tone": "Meleg, tiszteletteljes, biblikus, bátorító, mélyen emberi és békességet sugárzó",
        "visual_style": "Soft Scandinavian sage green, gold accents, clean minimalist typography, watercolor floral borders"
    },
    # 1. Make Money & Business
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
    "🏠 Ingatlanbefektetés & Ingatlanpiac (Real Estate)": {
        "group": "Make Money & Business",
        "name_en": "Real Estate & Property Investment",
        "default_audience": "Ingatlanbefektetők, bérbeadók és ingatlanvásárlás előtt álló tudatos vásárlók",
        "keywords": ["Real estate cashflow", "BRRRR", "Rental property", "Property evaluation", "Mortgage tips"],
        "tone": "Stratégiai, tapasztalt, tőkefókuszú, realista és üzleties",
        "visual_style": "Warm slate gray, brick terracotta accents, architectural line drawings, premium layout"
    },
    "💎 Magas Jövedelmű Skillek & Szabadúszás (High-Income Skills)": {
        "group": "Make Money & Business",
        "name_en": "High-Income Skills & Freelancing",
        "default_audience": "Karrierváltók, szabadúszók és szakemberek, akik piacképes tudással akarnak magas óradíjat elérni",
        "keywords": ["Copywriting", "Sales closing", "Consulting", "Remote client acquisition", "High ticket"],
        "tone": "Dinamikus, ambiciózus, közvetlen válaszmarketingre épülő, eredményorientált",
        "visual_style": "Luxury charcoal, champagne gold accents, bold modern typography"
    },
    # 2. Self-Improvement
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
    "🦁 Önbizalom & Kommunikáció (Confidence & Communication)": {
        "group": "Self-Improvement",
        "name_en": "Confidence & Social Skills",
        "default_audience": "Introvertek és szakemberek, akik magabiztosan akarnak megszólalni és határozottan kommunikálni",
        "keywords": ["Charisma", "Public speaking", "Assertiveness", "Body language", "Social ease"],
        "tone": "Empatikus, bátor, önbizalomépítő és barátságos",
        "visual_style": "Rich navy, warm amber accents, expressive typography, strong clean lines"
    },
    "📚 Memória & Gyors Tanulás (Memory & Accelerated Learning)": {
        "group": "Self-Improvement",
        "name_en": "Memory & Accelerated Learning",
        "default_audience": "Diákok, vizsgázók és élethosszig tanulók, akik gyorsabban akarnak memorizálni és tanulni",
        "keywords": ["Memory palace", "Active recall", "Spaced repetition", "Speed reading", "Feynman technique"],
        "tone": "Tudományos alapú, gyakorlatias, kíváncsiságot ébresztő és strukturált",
        "visual_style": "Clean parchment, deep indigo, vintage scholarly touches, neat outlines"
    },
    "🕊️ Spiritualitás & Tudatosság (Spirituality & Mindfulness)": {
        "group": "Self-Improvement",
        "name_en": "Spirituality & Mindfulness",
        "default_audience": "Belső békét, meditációt és lelki mélységet kereső tudatos emberek",
        "keywords": ["Inner peace", "Mindfulness", "Daily meditation", "Gratitude journaling", "Presence"],
        "tone": "Békés, leföldelő, gyengéd, meleg és reflektív",
        "visual_style": "Soft eucalyptus sage, warm sand, delicate botanical watercolor motifs"
    },
    # 3. Health & Fitness
    "🥗 Fogyás & Egészséges Táplálkozás (Weight Loss & Nutrition)": {
        "group": "Health & Fitness",
        "name_en": "Weight Loss & Healthy Nutrition",
        "default_audience": "Egészséges, fenntartható életmódváltásra és testsúlycsökkentésre vágyók",
        "keywords": ["Meal planning", "Clean eating", "Intermittent fasting", "Keto/Low-carb", "Healthy recipes"],
        "tone": "Támogató, ítélkezésmentes, energizáló és egészségközpontú",
        "visual_style": "Fresh lime green, crisp white background, vibrant fresh food aesthetic"
    },
    "🧬 Biohacking & Hosszú Élet (Biohacking & Longevity)": {
        "group": "Health & Fitness",
        "name_en": "Biohacking & Longevity",
        "default_audience": "Teljesítmény- és egészség-optimalizálók, akik a maximumot akarják kihozni a testükből",
        "keywords": ["Sleep optimization", "Circadian rhythm", "Cold plunge", "Nootropics", "Metabolic health"],
        "tone": "Adatvezérelt, élvonalbeli tudományra épülő, precíz és csúcsteljesítmény-fókuszú",
        "visual_style": "Dark titanium slate, neon cyan metrics, scientific minimalist layout"
    },
    "🧘 Mentális Egészség & Stresszoldás (Mental Health & Stress Relief)": {
        "group": "Health & Fitness",
        "name_en": "Mental Health & Stress Relief",
        "default_audience": "Szorongással, kiégéssel és stresszel küzdő egyének, akik belső békére vágynak",
        "keywords": ["Burnout recovery", "Anxiety relief", "Nervous system regulation", "Journaling prompts", "Somatic exercises"],
        "tone": "Mélyen együttérző, biztonságos, megnyugtató és támogató",
        "visual_style": "Muted lavender, soft sage, warm cream, calming minimalist aesthetic"
    },
    "🌿 Természetes Gyógymódok & Holisztikus Egészség (Holistic Health)": {
        "group": "Health & Fitness",
        "name_en": "Holistic Health & Natural Remedies",
        "default_audience": "Természetes életmódot és gyógynövényes/holisztikus egészségmegőrzést követők",
        "keywords": ["Herbal remedies", "Essential oils", "Gut health", "Detox", "Natural wellness guide"],
        "tone": "Organikus, gondoskodó, természethez igazodó és hiteles",
        "visual_style": "Earthy terracotta, olive green, botanical illustrations, kraft paper texture"
    },
    "🏋️ Otthoni Edzés & Testformálás (Home Workouts)": {
        "group": "Health & Fitness",
        "name_en": "Home Workouts & Body Transformation",
        "default_audience": "Edzőterem nélküli, otthoni hatékony testmozgást és erősödést keresők",
        "keywords": ["Bodyweight workout", "HIIT at home", "Dumbbell routine", "30-day fitness challenge", "Form guide"],
        "tone": "Motiváló, energikus, akcióorientált és egyértelmű",
        "visual_style": "Charcoal black, energetic electric orange, athletic typography, dynamic layouts"
    },
    # 4. Tech & Creativity
    "🎨 Grafikai Tervezés & Canva Sablonok (Graphic Design / Canva)": {
        "group": "Tech & Creativity",
        "name_en": "Graphic Design & Canva Templates",
        "default_audience": "Kisvállalkozók, tartalomkészítők és alkotók, akik gyorsan akarnak profi dizájnokat készíteni",
        "keywords": ["Canva templates", "Brand identity", "Typography rules", "Color palettes", "Social media kits"],
        "tone": "Kreatív, stílusos, esztétikus és lépésről-lépésre gyakorlatias",
        "visual_style": "Pastel aesthetic, modern grid cards, beautiful typography hierarchy"
    },
    "📱 Tartalomgyártás & Közösségi Média (Content Creation / Social Media)": {
        "group": "Tech & Creativity",
        "name_en": "Content Creation & Social Media Growth",
        "default_audience": "TikTok, Instagram, YouTube és Pinterest alkotók, akik követőbázist és eladásokat akarnak építeni",
        "keywords": ["Faceless marketing", "Viral hooks", "Reels/Shorts strategy", "Carousel templates", "Pinterest SEO"],
        "tone": "Trendi, dinamikus, algoritmustudatos és elköteleződés-fókuszú",
        "visual_style": "Dark gradient purple-cyan, bold headline typography, sleek mockups"
    },
    "🎵 Zenei Produkció & Hangtechnika (Music & Audio)": {
        "group": "Tech & Creativity",
        "name_en": "Music Production & Audio Engineering",
        "default_audience": "Zenészek, podcast készítők, beatmakerek és audio szakemberek",
        "keywords": ["DAW workflow", "Mixing & Mastering", "Sample packs", "Vocal chain", "Beat making guide"],
        "tone": "Művészi, technikai, szenvedélyes és hangzásfókuszú",
        "visual_style": "Dark studio aesthetic, neon violet waveforms, vintage analog gear touches"
    },
    "📷 Fotózás & Videózás (Photography & Video)": {
        "group": "Tech & Creativity",
        "name_en": "Photography & Video Creation",
        "default_audience": "Fotósok, videósok, Lightroom preset vásárlók és vizuális alkotók",
        "keywords": ["Lightroom presets", "Camera composition", "Smartphone photography", "Cinematic color grading"],
        "tone": "Vizuálisan gazdag, részletorientált, művészi és filmszerű",
        "visual_style": "Cinematic 16:9 frames, monochrome minimal with golden hour warm tones"
    },
    "📖 Könyvkiadás & Amazon KDP (Self-Publishing / KDP)": {
        "group": "Tech & Creativity",
        "name_en": "Self-Publishing & Amazon KDP Books",
        "default_audience": "Amazon KDP szerzők, színezőkönyv és alacsony tartalmú könyvkiadók",
        "keywords": ["KDP interiors", "Book cover design", "Amazon KDP keywords", "Coloring books", "Publishing blueprint"],
        "tone": "Kiadói színvonalú, strukturált, kereskedelmi és niche-célzott",
        "visual_style": "Clean book trim outlines, 8.5x11 mockups, elegant editorial covers"
    },
    # 5. Lifestyle & Hobbies
    "✈️ Utazási Trükkök & Digitális Nomád (Travel Hacks & Nomad)": {
        "group": "Lifestyle & Hobbies",
        "name_en": "Travel Hacks & Digital Nomad",
        "default_audience": "Utazók, távmunkások és kalandvágyók, akik olcsóbban és okosabban akarnak világot látni",
        "keywords": ["Flight hacks", "Credit card points", "Remote work nomad guide", "Packing checklist", "Hidden gems"],
        "tone": "Kalandvágyó, gyakorlatias, szabadságközpontú és leleményes",
        "visual_style": "Sky blue and sunny sand, passport stamp motifs, clean travel cards"
    },
    "👑 Prémium Életmód & Luxus (Luxury Lifestyle)": {
        "group": "Lifestyle & Hobbies",
        "name_en": "Luxury Lifestyle & High-End Living",
        "default_audience": "Elegáns, magas minőségű életstílust és esztétikát követő tudatos vásárlók",
        "keywords": ["Old money aesthetic", "Quiet luxury", "Fine dining etiquette", "High-end curation", "Elegance"],
        "tone": "Kifinomult, exkluzív, elegáns, diszkrét és csiszolt",
        "visual_style": "Deep emerald, brushed gold, classic serif typography, minimal luxury margins"
    }
}


# ─────────────────────────────────────────────────────────
# AI IMAGE MODEL-SPECIFIC PROMPT PROFILES
# Each image generation AI requires different prompt engineering.
# FLUX: Natural language, affirmative framing only, no negation.
# Imagen: Creative brief style, explicit negative constraints OK.
# ─────────────────────────────────────────────────────────

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
        ),
        "enhance_instruction": (
            "TARGET IMAGE AI: Pollinations FLUX\n"
            "CRITICAL FLUX PROMPT RULES:\n"
            "1. Use ONLY AFFIRMATIVE statements. NEVER use negation words: 'no', 'zero', 'without', 'never', 'not', 'don't'.\n"
            "2. Instead of 'no shading' → write 'clean flat ink lines'.\n"
            "3. Instead of 'no colors' → write 'black ink on solid white paper'.\n"
            "4. Instead of 'no grayscale' → write 'high-contrast pure black and white only'.\n"
            "5. Instead of 'no cartoon' → write 'realistic anatomical proportions with classical engraving style'.\n"
            "6. FRONT-LOAD the subject: start with 'A coloring book page of...' or 'An intricate adult coloring book page of...'.\n"
            "7. Use natural language PARAGRAPHS, not comma-separated keyword tags.\n"
            "8. Optimal prompt length: 40-60 words. Do not exceed 80 words.\n"
            "9. Describe the PHYSICAL PROPERTIES of lines: thickness, ink style, contrast level."
        ),
        "manifest_instruction": (
            "CRITICAL: The image generation AI is Pollinations FLUX which requires AFFIRMATIVE-ONLY natural language prompts.\n"
            "Write each visual_prompt as a NATURAL LANGUAGE PARAGRAPH of 40-60 words.\n"
            "Front-load the subject: start every prompt with 'A coloring book page of...' (children) or 'An intricate adult coloring book page of...' (adult).\n"
            "Use ONLY AFFIRMATIVE STATEMENTS describing what IS visible in the scene.\n"
            "ABSOLUTELY FORBIDDEN negation words in visual_prompt: 'no', 'zero', 'without', 'never', 'not', 'don\\'t', 'none'.\n"
            "Replacements: 'no shading' → 'clean flat ink lines'; 'no colors' → 'black ink on white paper'; 'no grayscale' → 'high-contrast black and white only'.\n"
            "Always include: 'solid pure white background' and 'bold black ink outlines' (children) or 'fine detailed black ink lines' (adult)."
        ),
        "dimensions": {"portrait": (1024, 1408), "square": (1024, 1024), "landscape": (1408, 1024)},
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
        ),
        "enhance_instruction": (
            "TARGET IMAGE AI: Google Imagen 3/4\n"
            "IMAGEN PROMPT RULES:\n"
            "1. Use DETAILED creative brief style with explicit constraints.\n"
            "2. Explicit negative constraints ARE allowed and encouraged: 'zero shading', 'no colors', 'NO cartoon elements'.\n"
            "3. Include technical parameters: '4K resolution', '8.5x11 portrait ratio', '300 DPI'.\n"
            "4. Comma-separated quality modifiers at the end are acceptable.\n"
            "5. Be specific about composition, focal points, and line weight.\n"
            "6. For adult pages include: 'NO cartoon elements, NO chibi style, NO simplified shapes'."
        ),
        "manifest_instruction": (
            "The image generation AI is Google Imagen which works best with detailed creative brief style prompts.\n"
            "Write each visual_prompt with explicit style constraints.\n"
            "Include 'zero shading, zero grayscale, no colors' and technical parameters like '4K resolution, 8.5x11 ratio'.\n"
            "For adult pages include: 'NO cartoon elements, NO chibi style'.\n"
            "Comma-separated modifiers at the end are acceptable and recommended."
        ),
        "dimensions": {"portrait": "3:4", "square": "1:1", "landscape": "16:9"},
    },
    "gemini-image": {
        "name": "Gemini Native Image",
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
        ),
        "enhance_instruction": (
            "TARGET IMAGE AI: Gemini Native Image Generation\n"
            "GEMINI IMAGE PROMPT RULES:\n"
            "1. Use detailed creative brief style (similar to Imagen prompts).\n"
            "2. Explicit negative constraints are OK: 'zero shading', 'no colors'.\n"
            "3. Include technical parameters: '4K resolution', '8.5x11 portrait ratio'.\n"
            "4. Supports text rendering natively — include exact quoted text if needed.\n"
            "5. Be specific about composition, focal points, and line weight."
        ),
        "manifest_instruction": (
            "The image generation AI is Gemini Native Image which uses Imagen-compatible detailed prompts.\n"
            "Write each visual_prompt with explicit style constraints.\n"
            "Include 'zero shading, zero grayscale, no colors' and technical parameters.\n"
            "Comma-separated modifiers at the end are acceptable."
        ),
        "dimensions": {"portrait": "3:4", "square": "1:1", "landscape": "16:9"},
    }
}


def get_model_profile(model_name: str) -> dict:
    """Returns the appropriate IMAGE_MODEL_PROFILES entry based on any model name string.
    
    Automatically maps model names like 'pollinations-flux', 'imagen-4.0-generate-001',
    'gemini-3-pro-image', etc. to their corresponding prompt profile.
    
    Args:
        model_name: Any image model name string from the app configuration.
        
    Returns:
        The matching IMAGE_MODEL_PROFILES dict entry. Defaults to 'imagen' profile.
    """
    if not model_name:
        return IMAGE_MODEL_PROFILES["imagen"]
    name_lower = model_name.lower()
    if any(k in name_lower for k in ["pollin", "flux"]):
        return IMAGE_MODEL_PROFILES["flux"]
    if any(k in name_lower for k in ["gemini"] ) and "image" in name_lower:
        return IMAGE_MODEL_PROFILES["gemini-image"]
    # Default: Imagen (covers imagen-3.0, imagen-4.0, nano-banana, etc.)
    return IMAGE_MODEL_PROFILES["imagen"]


def get_niche_prompt_context(niche_key: str) -> dict:
    """Returns niche details dictionary or falls back to Christian default."""
    if niche_key in NICHE_CATEGORIES:
        return NICHE_CATEGORIES[niche_key]
    return NICHE_CATEGORIES["✝️ Keresztény & Bibliai Rétegpiac (Alapértelmezett)"]


# ─────────────────────────────────────────────────────────
# KDP, ETSY & GUMROAD PRODUCT PROMPT TEMPLATES (1-7. Út)
# ─────────────────────────────────────────────────────────

def build_kdp_coloring_master_prompt(scene_description: str, niche_context: str = "", image_model: str = "", is_adult: bool = False) -> str:
    """
    KDP Coloring Book Master Prompt (1. út):
    Now generates model-specific prompts based on the target image generation AI.
    """
    profile = get_model_profile(image_model)
    niche_suffix = f" Theme: {niche_context}." if niche_context else ""
    scene_with_niche = f"{scene_description}.{niche_suffix}" if niche_suffix else scene_description
    
    if is_adult:
        template = profile.get("coloring_adult_template", profile.get("coloring_child_template", ""))
    else:
        template = profile.get("coloring_child_template", "")
    
    if template and "{scene}" in template:
        return template.format(scene=scene_with_niche)
    
    # Legacy fallback for unknown profiles
    return (
        f"Kérlek, hozz létre egy tiszta, fekete-fehér színező oldalt a következőről: {scene_description}"
        f"{' Niche fókusz: ' + niche_context + '.' if niche_context else ''} "
        f"a Nano Banana Pro modellel. Stíluskövetelmények: Egyszerű, vastag fekete vonalakkal dolgozz, "
        f"tiszta fehér háttérrel, árnyékolás, szürke tónusok és színek nélkül. Letisztult vektorgrafikus "
        f"stílus legyen, egységes vonalvastagsággal és tiszta formákkal. A lap méretaránya legyen 8.5:11 hüvelyk, 4K felbontásban."
    )

def build_kdp_cover_master_prompt(scene_description: str, title: str) -> str:
    """
    KDP Book Cover Master Prompt (1. út).
    """
    return (
        f"A high-quality colorful book cover depicting {scene_description}, "
        f"consistent pastel color palette, vector art style, with bold, clean typography at the top "
        f"that reads exactly: '{title}', high resolution, professional design, 17.412:11.25 aspect ratio."
    )

def build_etsy_wall_art_master_prompt(verse_quote: str, style_note: str = "soft green eucalyptus leaves framing a central text") -> str:
    """
    Etsy Wall Art Master Prompt (2. út).
    """
    return (
        f"An elegant minimalist watercolor design with {style_note}. "
        f"The text reads in beautiful, clean typography: '{verse_quote}', "
        f"high resolution, modern Scandinavian wall art style, 4:5 aspect ratio."
    )

def build_etsy_clipart_master_prompt(character_or_object: str) -> str:
    """
    Etsy Clipart Master Prompt (2. út).
    """
    return (
        f"Watercolor illustration of {character_or_object}, cute chibi style, "
        f"soft pastel color palette, isolated on pure white background, high detail, consistent clipart bundle style."
    )

def build_etsy_bg_removal_prompt() -> str:
    """
    Etsy Background Removal Master Prompt.
    """
    return "Kérlek, távolítsd el a fehér hátteret a fenti grafikák mögül, és tegyed őket teljesen átlátszóvá (transparent PNG format)."

def generate_gemini_gem_master_instruction(is_adult: bool = False, style_name: str = "") -> str:
    """
    Generates a master system instruction / custom Gem prompt for Gemini Web UI.
    This locks the model into producing consistent, clean black & white coloring book pages.
    """
    edition_type = "intricate adult coloring book pages (fine black line art, detailed zentangle and mandala patterns, zero shading, realistic proportions)" if is_adult else "children's coloring book pages (bold clean black outlines, cute friendly characters, simple compositions, pure white background)"
    style_clause = f"\n- Consistent Art Style: {style_name}" if style_name else ""
    
    return (
        f"GEMINI GEM MASTER INSTRUCTION — AMAZON KDP COLORING BOOK ARTIST\n"
        f"================================================================\n"
        f"You are a world-class illustration artist specializing in creating high-quality Amazon KDP black and white coloring book pages.\n\n"
        f"ROLE & MISSION:\n"
        f"Generate {edition_type}.\n\n"
        f"CRITICAL MANDATORY VISUAL RULES (ENFORCE FOR EVERY IMAGE):\n"
        f"1. PURE BLACK AND WHITE ONLY: Solid black line art outlines on a pure crisp clean white background (#FFFFFF).\n"
        f"2. ZERO SHADING / ZERO GRAYSCALE: No color, no gray gradients, no cross-hatching shadows, no colored pencil effects, zero fill.\n"
        f"3. ASPECT RATIO: Always generate in 3:4 vertical aspect ratio (ideal for 8.5x11 inch standard book pages).\n"
        f"4. FRAMING & COMPOSITION: Perfectly centered with comfortable margins, no cut-off subjects, ready for coloring.{style_clause}\n\n"
        f"When given a scene description, produce the illustration matching these exact rules."
    )

def build_gumroad_devotional_master_prompt(target_audience: str, theme_title: str, day_number: str = "1.") -> str:
    """
    Gumroad PLR Devotional / Guide Master Prompt (3. út).
    """
    return (
        f"Szeretnék egy mély, hiteles és lelkileg építő 30 napos keresztény áhítat naplót (devotional) írni {target_audience} részére "
        f"'{theme_title}' címmel. Kérlek, írd meg nekem a(z) {day_number} nap teljes tartalmát. "
        f"Tartalmazzon: egy releváns bibliai igét (KJV fordításból és magyar nyelven), egy 200 szavas bátorító magyarázó-elmélkedő szöveget, "
        f"egy napi imát, és 3 db mély, elgondolkodtató önreflektív kérdést, amit a naplóba le tudnak írni a hívők. "
        f"Stílusutasítás: Kerüld a tipikus, mesterkélt AI-fordulatokat és a túl száraz megfogalmazást. "
        f"Írj meleg, mélyen bátorító, spirituális, tiszteletteljes és emberi tónusban, mintha egy hívő barát beszélgetne a másikkal."
    )

def extract_visual_prompt_for_image_engine(raw_prompt: str, category: str, image_model: str = "") -> str:
    """
    Extracts a clean, direct English visual description and formats it using the
    appropriate model-specific template for the target image generation AI.
    
    Supports: Pollinations FLUX (affirmative natural language), Imagen (creative brief with negation), Gemini Image.
    """
    profile = get_model_profile(image_model)
    
    # Clean Hungarian framing text
    clean_text = raw_prompt
    for prefix in [
        "Kérlek, hozz létre egy tiszta, fekete-fehér gyermek színező oldalt a következőről:",
        "Kérlek, hozz létre egy tiszta, fekete-fehér színező oldalt a következőről:",
        "a Nano Banana Pro modellel.",
        "Stíluskövetelmények:",
        "Szeretnék egy mély,"
    ]:
        clean_text = clean_text.replace(prefix, "")
    clean_text = clean_text.strip()
    
    if category == "kdp":
        template = profile.get("coloring_child_template", "")
        if template and "{scene}" in template:
            return template.format(scene=clean_text)
        return (
            f"Black and white coloring book page depicting {clean_text}. "
            f"Simple bold black line art outlines, pure crisp white background, zero shading, "
            f"zero grayscale, no colors, clean vector line art style, 8.5x11 aspect ratio."
        )
    elif category == "etsy_wall":
        template = profile.get("wall_art_template", "")
        if template and "{scene}" in template:
            return template.format(scene=clean_text, text=clean_text)
        return (
            f"Modern printable wall art, {clean_text}, "
            f"soft pastel watercolor, elegant clean typography, Scandinavian style, 300 DPI, 4:5 aspect ratio."
        )
    elif category == "etsy_clipart":
        template = profile.get("clipart_template", "")
        if template and "{scene}" in template:
            return template.format(scene=clean_text)
        return (
            f"Watercolor illustration of {clean_text}, cute chibi style, "
            f"soft pastel color palette, isolated on pure white background, clipart bundle art."
        )
    elif category == "devotional_cover":
        template = profile.get("cover_template", "")
        if template and "{scene}" in template:
            return template.format(scene=clean_text, title="Devotional")
        return (
            f"Book cover illustration, {clean_text}, "
            f"pastel color palette, vector art style, elegant typography header, high resolution."
        )
    return clean_text


# ─────────────────────────────────────────────────────────
# FFC (FACELESS FUNNEL CHALLENGE) MAGIC COPYWRITING FRAMEWORK
# ─────────────────────────────────────────────────────────

def build_ffc_avatar_research_prompt(product_name: str, target_audience: str, main_transformation: str, additional_notes: str = "", niche_name: str = "") -> str:
    """
    FFC 8-Step Avatar Deep Psychological Research Master Prompt.
    Extracts deep emotional drivers: Fears, Secret Desires, Internal/External Obstacles, Objections, and the Big Domino.
    """
    niche_clause = f"\nPiaci Niche: {niche_name}" if niche_name else ""
    extra_clause = f"\nExtra megfontolások / háttér: {additional_notes}" if additional_notes.strip() else ""
    return (
        f"Te vagy a világ egyik legelismertebb közvetlen válaszmarketing (Direct Response Copywriting) és fogyasztói "
        f"pszichológiai szakértője, aki a Russell Brunson és Stefan Georgi módszertan mestere.{niche_clause}\n\n"
        f"Végezz egy mélyreható, kíméletlenül őszinte és pszichológiailag tűpontos AVATAR KUTATÁST az alábbi digitális termékhez:\n\n"
        f"📌 TERMÉK NEVE: {product_name}\n"
        f"🎯 CÉLKÖZÖNSÉG: {target_audience}\n"
        f"✨ FŐ TRANSZFORMÁCIÓ / ÍGÉRET: {main_transformation}{extra_clause}\n\n"
        f"KÉREM AZ ELEMZÉST AZ ALÁBBI STRUKTÚRÁBAN (Használj érzelmileg gazdag, empátiával teli, hiteles nyelvezetet):\n\n"
        f"1. 🔥 5 MÉLY BELSŐ FÉLELEM & CSALÓDOTTSÁG:\n"
        f"   - Mitől félnek éjszaka, ami miatt nem tudnak aludni? Milyen rejtett bűntudat, lelki kimerültség vagy kudarcérzés gyötri őket?\n\n"
        f"2. 🌟 5 TITKOS ÉS KIMONDOTT VÁGY (A Mennyország Állapot):\n"
        f"   - Milyen békességre, megerősödésre, anyagi/szellemi célokra, harmóniára vagy sikerre vágynak igazán?\n\n"
        f"3. 🚧 5 KÜLSŐ ÉS BELSŐ AKADÁLY (Mi tartotta vissza őket eddig?):\n"
        f"   - Időhiány, túlterheltség, ADHD/figyelemzavar, túl bonyolult rendszerek, korábbi sikertelen próbálkozások.\n\n"
        f"4. 🛑 5 LEGGYAKORIBB VÁSÁRLÁSI KIFOGÁS ÉS AZOK PSZICHOLÓGIAI ELLENSZERE:\n"
        f"   - Pl.: 'Nincs időm ezzel foglalkozni', 'Biztos drága/bonyolult', 'Nem vagyok elég jó ebben', 'Már próbáltam hasonlót'.\n\n"
        f"5. 🀄 A 'BIG DOMINO' GONDOLAT:\n"
        f"   - Az EGYETLEN kulcsmondat és felismerés, amit ha elhisznek, az összes kifogásuk összeomlik, és a vásárlás elkerülhetetlen magától értetődő lépéssé válik."
    )


def build_ffc_big_domino_hooks_prompt(product_name: str, target_audience: str, main_transformation: str, vehicle: str = "ezzel a kész digitális kiadvánnyal", language: str = "magyar", niche_name: str = "") -> str:
    """
    FFC Big Domino Hooks & Headlines Generator Prompt.
    Generates 10 high-converting headlines in the format:
    'Get [Desire] without [Pain], even if [Objection], using [Vehicle]'
    """
    lang_instruction = "magyar nyelven" if language.lower().startswith("magy") else "angol nyelven (English)"
    niche_clause = f"\nPiaci Niche: {niche_name}" if niche_name else ""
    return (
        f"Te egy mester szövegíró (Master Copywriter) vagy, aki a világ legmagasabb konverziójú horgait (Hooks & Headlines) készíti el.{niche_clause}\n\n"
        f"Készíts pontosan 10 db pszichológiailag ellenállhatatlan BIG DOMINO HORGOT ÉS FŐCÍMET {lang_instruction} az alábbi termékhez:\n\n"
        f"📌 TERMÉK: {product_name}\n"
        f"🎯 CÉLCSOPORT: {target_audience}\n"
        f"✨ FŐ VÁGY / TRANSZFORMÁCIÓ: {main_transformation}\n"
        f"🚀 MÓDSZER / ESZKÖZ (VEHICLE): {vehicle}\n\n"
        f"KÖVETELMÉNYEK ÉS FORMÁTUM:\n"
        f"Minden egyes horgot pontosan az FFC (Faceless Funnel) Big Domino aranyformulájára építs fel:\n"
        f"👉 'Hogyan érheted el a(z) [Áhított Vágyat] a(z) [Frusztráló Fájdalom/Erőfeszítés] NÉLKÜL, MÉG AKKOR IS, HA [Legfőbb Kifogás/Korlát], a(z) [Eszköz/Módszer] segítségével!'\n"
        f"(Angolul: 'How to Get [Desire] without [Pain], even if [Objection], using [Vehicle]')\n\n"
        f"Készíts 10 egyedi variációt:\n"
        f"- 1-3. Közvetlen Transzformációs Horgok (Erős, tiszta ígéret)\n"
        f"- 4-6. 'Még akkor is ha...' Kifogásromboló Horgok (Időhiány, fáradtság, kezdő szint)\n"
        f"- 7-8. Kíváncsiság- és Titok-alapú Horgok (A rejtett kulcs)\n"
        f"- 9-10. Rövid, ütős Social Media & E-mail Tárgymező Horgok (Max 10 szó)"
    )


def build_ffc_value_stack_prompt(product_name: str, target_audience: str, core_features: str, bonuses: str = "", regular_price: str = "19 990 Ft", language: str = "magyar") -> str:
    """
    FFC Value Stack & Feature-Benefit-Meaning Matrix Generator.
    Generates bullet points following: 'You get [feature] so that you can [benefit]... even if [objection]... which means [outcome]'
    """
    lang_inst = "magyar nyelven" if language.lower().startswith("magy") else "in English"
    bonus_part = f"\nBónuszok: {bonuses}" if bonuses.strip() else ""
    return (
        f"Készíts egy profi, Russell Brunson-stílusú ÉRTÉKHALMOZÁST (Value Stack) és termék-bulletpont rendszert {lang_inst} az alábbi termékhez:\n\n"
        f"📌 TERMÉK: {product_name}\n"
        f"🎯 CÉLCSOPORT: {target_audience}\n"
        f"📦 FŐ TULAJDONSÁGOK / CSOMAG ELEMEI: {core_features}{bonus_part}\n"
        f"💰 NÉVLEGES PIACI ÉRTÉK: {regular_price}\n\n"
        f"STRUKTÚRA KÖVETELMÉNYEK:\n\n"
        f"1. ✨ 5-7 DB MASTER BULLETPOINT AZ FFC NÉGYFÁZISÚ FORMULÁVAL:\n"
        f"   Minden pont így épüljön fel:\n"
        f"   'Megkapod a(z) [Funkció/Anyag], hogy [Közvetlen Haszon/Előny]... még akkor is, ha [Kifogás/Félelem]... ami azt jelenti, hogy [Mélyebb Lelki/Gyakorlati Eredmény].'\n\n"
        f"2. 📊 TELJES ÉRTÉKHALMOZÁSI TÁBLÁZAT (THE VALUE STACK TABLE):\n"
        f"   - Tétel 1 + Reális Piaci Érték\n"
        f"   - Tétel 2 + Reális Piaci Érték\n"
        f"   - Bónuszok + Reális Piaci Érték\n"
        f"   - ----------------------------------------\n"
        f"   - TELJES BECSÜLT ÉRTÉK (Total Real Value): [Összeg]\n"
        f"   - MAI AJÁNDÉK / KEDVEZMÉNYES ÁR (Today's Offer): [Végleges Kedvezményes Ár]\n\n"
        f"3. 💥 'WHY IT'S A NO-BRAINER' (1 bekezdéses indoklás, miért elképesztő üzlet ez most a vásárlónak)."
    )


def build_ffc_sales_letter_prompt(product_name: str, target_audience: str, main_transformation: str, pain_points: str = "", vehicle: str = "", bonuses: str = "", guarantee_type: str = "30 napos 100% elégedettségi garancia", language: str = "magyar", niche_name: str = "") -> str:
    """
    FFC 12-Step Master Sales Letter Generator Prompt (Russell Brunson High-Converting Model).
    Includes Hook, Shocking Statement, Pain/Desire, Method, Credibility, Proof, Product Overview, Pitch, Bonuses, Guarantee, CTA, and P.S.
    """
    lang_inst = "magyar nyelven" if language.lower().startswith("magy") else "in English (US)"
    niche_clause = f"\nPiaci Niche: {niche_name}" if niche_name else ""
    pains = f"\nFő fájdalompontok/frusztrációk: {pain_points}" if pain_points.strip() else ""
    veh = f"\nHasznált módszer/eszköz: {vehicle}" if vehicle.strip() else ""
    bon = f"\nAjándék bónuszok: {bonuses}" if bonuses.strip() else ""
    
    return (
        f"Te a világ egyik legelismertebb elit szövegírója vagy, aki Russell Brunson ('DotCom Secrets', 'Expert Secrets') és a modern "
        f"Faceless Funnel Challenge (FFC) közvetlen eladási stratégiájának legmagasabb szintű mestere.{niche_clause}\n\n"
        f"Írj egy teljes, magával ragadó, lebilincselő és rendkívül magas konverziójú ÉRTÉKESÍTÉSI LEVELET (Long-Form Sales Letter) {lang_inst} az alábbi adatok alapján:\n\n"
        f"📌 TERMÉK NEVE: {product_name}\n"
        f"🎯 CÉLKÖZÖNSÉG: {target_audience}\n"
        f"✨ FŐ TRANSZFORMÁCIÓ: {main_transformation}{pains}{veh}{bon}\n"
        f"🛡️ GARANCIA TÍPUSA: {guarantee_type}\n\n"
        f"A LEVÉLNEK PONTOSAN AZ ALÁBBI 12 LÉPÉSES PSZICHOLÓGIAI ÍVET KELL KÖVETNIE:\n\n"
        f"1. 🎣 THE BIG HOOK & PRE-HEADLINE: Figyelemfelkeltő felütés és főcím a Big Domino formátumban.\n"
        f"2. ⚡ SHOCKING STATEMENT / BOLD CLAIM: Egy bátor, meglepő állítás, ami megtöri az olvasó közönyét.\n"
        f"3. 💔 DEEP PAIN & BURNING DESIRE (Empathy Bridge): Mély együttérzés, a mindennapi nehézségek, elakadások és a vágyott cél ábrázolása.\n"
        f"4. 💡 THE EPIPHANY BRIDGE & THE NEW VEHICLE: A felismerés pillanata — miért a régi módszerek vallottak kudarcot, és miért ez az új út a valódi megoldás.\n"
        f"5. 🤝 CREATOR CREDIBILITY & ORIGIN STORY: Rövid, szimpatikus, hiteles alkotói bemutatkozás.\n"
        f"6. 🕊️ SOCIAL PROOF & VALIDATION: Visszajelzések, esettanulmányok és gyakorlati megerősítés.\n"
        f"7. 🎁 INTRODUCING THE SOLUTION: A(z) {product_name} hivatalos bemutatása, mi ez pontosan és hogyan működik.\n"
        f"8. 📋 THE VALUE STACK & BULLET POINTS: 5-7 db erőteljes bulletpont (Feature + Benefit + Even If + Meaning).\n"
        f"9. 🌟 IRRESISTIBLE BONUSES: Az ingyenes bónuszok bemutatása, amelyek önmagukban is értékesebbek a fő árnál.\n"
        f"10. 🛡️ IRON-CLAD 100% GUARANTEE: Teljesen kockázatmentes garancia leírása (pl. {guarantee_type}).\n"
        f"11. 🚀 URGENT CALL TO ACTION (CTA): Egyértelmű, meleg hangvételű, de sürgető vásárlási felszólítás link-gomb helyőrzőkkel.\n"
        f"12. ✍️ P.S. (POST SCRIPTUM) & CLOSING INSPIRATION: 2 db ütős P.S. (1. Emlékeztető a kockázatmentességre; 2. Mi történik, ha nem lépsz ma: a helyzet nem változik magától).\n\n"
        f"TÓNUS: Meleg, meggyőző, mélyen hiteles, tiszteletteljes, de határozott és cselekvésre ösztönző! Kerüld az olcsó 'teleshop' kliséket."
    )


GOOGLE_SITES_LANDING_PAGE_PROMPT = """
Te egy világszínvonalú Conversion Rate Optimization (CRO) és Landing Page szövegíró szakértő vagy, aki kifejezetten a 100%-ban ingyenes Google Sites (sites.google.com) keretrendszerhez készít magas konverziójú, elegáns, kész weboldal struktúrákat és szövegeket.

A feladatod: Készítsd el a teljes, blokkonként közvetlenül átmásolható tartalmat egy 0 Ft-os Google Sites értékesítési és feliratkozógyűjtő landing page-hez.

A generált anyagnak kötelezően tartalmaznia kell az alábbi 5 fő blokkot részletesen, igényes és meggyőző megfogalmazásban:

1. 🌟 HERO SECTION (Felső Fő Blokkat & Banner)
   - Felső Bejelentő Csík (Announcement Bar): '✨ Azonnali Digitális Letöltés · 100% Kockázatmentes Békesség'
   - Főcímsor (Main Headline): Figyelemfelkeltő, érzelmi hatású főcím (H1)
   - Alcím (Subheadline): A termék által nyújtott életérzés és transzformáció összefoglalása (H2)
   - Hívogató Bevezető Szöveg (Introduction): 2-3 bekezdésnyi meleg, megnyugtató, értékközpontú bevezető
   - Elsődleges CTA Gomb (Fő Gomb Szöveg & Link helyőrző)
   - Bizalmi Elemek (Trust Badges): 🔒 Biztonságos Fizetés | ⚡ Azonnali Hozzáférés | 🕊️ 100% Garancia

2. 🎁 LEAD MAGNET SECTION (0 Ft-os Ingyenes Csalitermék Blokkat)
   - Csalitermék Címe & Leírása: Ingyenes 3-oldalas minta / mini áhítat / kifestő letöltő felhívás
   - 'Mit tartalmaz az ingyenes minta?': 3 db konkrét, azonnali értéket adó pont
   - Gumroad 0 Ft-os Letöltési Gomb: Pontos gombszöveg és Gumroad hivatkozási struktúra (pl. '📥 Ingyenes Minta Letöltése Gumroadon (0 Ft)')

3. 🛍️ FEATURED PRODUCTS (Kiemelt Termékek Bemutató Kártyái)
   - 1. Kártya: 📚 Amazon KDP Kiadás (Fizikai nyomtatott színezőkönyv / napló leírása, előnyök és '📖 Megtekintés Amazonon' gomb)
   - 2. Kártya: 🖼️ Etsy Digitális Csomag (Azonnal nyomtatható 300 DPI faliképek / clipart csomag és '🛍️ Vásárlás Etsy-n' gomb)
   - 3. Kártya: 📖 Gumroad Teljes Digitális Életmód Csomag (Komplett vezetett áhítat, bónuszok, azonnali PDF és '⚡ Letöltés Gumroadon' gomb)

4. 🚀 CTA BUTTONS & ACTION LINKS (Összesített Gombtár & Hivatkozások)
   - Exact gombfeliratok és célpontok összefoglaló táblázata (Amazon KDP, Etsy, Gumroad)
   - Végleges sürgető záró CTA felhívás és 100% elégedettségi garancia nyilatkozat

5. 🎨 VISUAL THEME GUIDE (Google Sites Téma & Beállítási Útmutató)
   - Javasolt Színpaletta (Hex kódokkal):
     * Háttér / Alapszín: Pasztell meleg bézs (`#F9F6F0`)
     * Fő Márkaszín: Zsályazöld (`#8A9A86` vagy `#34D399`)
     * Kiemelő / Arany Akcentus: Puha meleg arany (`#D4AF37`)
     * Szövegszín: Mély pala / Antracit (`#1E293B`)
   - Javasolt Google Fonts Betűtípus-párok:
     * Címsorok: Merriweather vagy Playfair Display
     * Kenyérszöveg: Montserrat vagy Open Sans
   - Lépésről-lépésre Google Sites Építési Útmutató (Blokk típusok: Banner, 2-oszlopos tartalomblokk, 3-oszlopos kártyarács, Elválasztó vonalak, Gombok).
"""


def build_google_sites_landing_page_prompt(
    product_name: str,
    target_audience: str,
    headline: str = "",
    tagline: str = "",
    lead_magnet_desc: str = "",
    features: str = "",
    offer_price: str = "$17 - $27",
    amazon_url: str = "#",
    etsy_url: str = "#",
    gumroad_url: str = "#",
    style_theme: str = "Keresztény Pasztell Minimalista (Zsályazöld & Bézs)",
    language: str = "magyar",
    niche_name: str = ""
) -> str:
    """
    100% Free Google Sites (sites.google.com) Landing Page Master Prompt.
    Generates structured, high-converting copy and visual layout guidelines for building
    a free Google Sites landing page routing customers to Amazon, Etsy, and Gumroad.
    """
    niche_ctx = f"\nRELEVÁNS RÉTEGPIAC KONTEXTUS:\n{get_niche_prompt_context(niche_name)}\n" if niche_name else ""
    head = headline if headline.strip() else f"Találd meg a napi békességet és inspirációt: {product_name}"
    tag = tagline if tagline.strip() else f"Prémium keresztény digitális alkotások {target_audience} számára a mindennapi lelki feltöltődéshez."
    lm_desc = lead_magnet_desc if lead_magnet_desc.strip() else "3-oldalas ingyenes nyomtatható kifestő és mini áhítat mintacsomag azonnali letöltéssel."
    feat = features if features.strip() else "30 napos vezetett áhítat és napló, 4K felbontású nyomtatható színező lapok, 300 DPI faliképek, azonnali digitális hozzáférés."

    return (
        f"{GOOGLE_SITES_LANDING_PAGE_PROMPT}\n\n"
        f"TERMÉK ÉS PROJEKT ADATOK:\n"
        f"- Termék Neve: {product_name}\n"
        f"- Célközönség: {target_audience}\n"
        f"- Fő Címsor / Horog: \"{head}\"\n"
        f"- Alcím / Életérzés: \"{tag}\"\n"
        f"- Ingyenes Csalitermék (Lead Magnet) Leírása: {lm_desc}\n"
        f"- Főbb Tartalmi Elemek & Előnyök: {feat}\n"
        f"- Ajánlat Ára (Gumroad Teljes Csomag): {offer_price}\n"
        f"- Vizuális & Hangulati Téma: {style_theme}\n"
        f"- Hivatkozási Linkek:\n"
        f"  * Amazon KDP Nyomtatott Könyv Link: {amazon_url}\n"
        f"  * Etsy Digitális Letöltés Link: {etsy_url}\n"
        f"  * Gumroad Közvetlen Vásárlás Link: {gumroad_url}\n"
        f"{niche_ctx}\n"
        f"KÉRLEK KÉSZÍTSD EL A TELJES GOOGLE SITES TARTALMAT {language.upper()} NYELVEN! "
        f"Minden egyes szekció legyen teljesen készre írva, sablonos szövegek nélkül, közvetlenül a Google Sites oldalra beilleszthető formában!"
    )


def build_polsia_landing_page_prompt(*args, **kwargs) -> str:
    """Alias for backwards compatibility."""
    return build_google_sites_landing_page_prompt(*args, **kwargs)


def build_email_funnel_3day_prompt(lead_magnet_name: str, paid_product_name: str, target_audience: str, discount_offer: str = "20% exkluzív kedvezmény", main_story: str = "", language: str = "magyar", niche_name: str = "") -> str:
    """
    3-Day Automated Email Funnel Generator Prompt for Lead Magnets to Paid Digital Products.
    Day 1: Free Sample Delivery + Warm Welcome + Quick Win
    Day 2: Pure Value + Origin Story (Chaos to Clarity) + Relatable Connection
    Day 3: Paid Pitch + Special Limited Discount + Urgency/Closing
    """
    lang_inst = "magyar nyelven" if language.lower().startswith("magy") else "in English"
    niche_clause = f"\nPiaci Niche: {niche_name}" if niche_name else ""
    story_clause = f"\nHáttér történet / tanulság: {main_story}" if main_story.strip() else ""
    
    return (
        f"Te egy professzionális e-mail marketing és tölcsér-építő (Funnel Copywriting) specialista vagy.{niche_clause}\n\n"
        f"Írj egy teljes, nagy megnyitási és átkattintási arányú 3 NAPOS AUTOMATA E-MAIL SZEKVENCIÁT {lang_inst} az alábbi adatok alapján:\n\n"
        f"🎁 INGYENES CSALITERMÉK (LEAD MAGNET): {lead_magnet_name}\n"
        f"💎 FIZETŐS AJÁNLAT / TERMÉK: {paid_product_name}\n"
        f"🎯 CÉLKÖZÖNSÉG: {target_audience}\n"
        f"🏷️ EXKLUZÍV AJÁNLAT / KEDVEZMÉNY: {discount_offer}{story_clause}\n\n"
        f"MINDEN EGYES E-MAILNÉL ADJ MEG:\n"
        f"- 2 db A/B Tesztelhető Tárgymezőt (Subject Lines: 1 db Érzelmi/Kíváncsiság alapú + 1 db Közvetlen/Haszon alapú)\n"
        f"- Előnézeti Szöveget (Preview Text - max 90 karakter)\n"
        f"- A teljes, formázott Levéltörzset (megszólítás, bekezdések, CTA linkek és P.S.)\n\n"
        f"A 3 NAP PONTOS STRUKTÚRÁJA:\n\n"
        f"📧 1. NAP: AZ AJÁNDÉK MEGFÉRKEZETT + GYORS SIKERÉLMÉNY & KÖSZÖNET\n"
        f"   - Cél: Kézbesíteni a(z) '{lead_magnet_name}' ingyenes anyagot, azonnali örömet és hálát ébreszteni, és 1 egyszerű tippel segíteni az azonnali használatát.\n\n"
        f"📧 2. NAP: ÉRTÉKADÁS ÉS SZEMÉLYES TÖRTÉNET (A Káoszból a Megoldásig)\n"
        f"   - Cél: Kapcsolódás mély érzelmekkel — hogyan jutottunk el a nehézségekből a valódi megoldásig. 3 gyakorlati tipp. Nincs kemény eladás, csak finom utalás a holnapi meglepetésre!\n\n"
        f"📧 3. NAP: A TELJES MEGOLDÁS + EXKLUZÍV KEDVEZMÉNY ÉS SÜRGŐSSÉG\n"
        f"   - Cél: A(z) '{paid_product_name}' bemutatása mint a következő természetes lépés. A(z) {discount_offer} átadása korlátozott határidővel. Kockázatmentes garancia és közvetlen kattintási felhívás.\n\n"
        f"TÓNUS: Meleg, őszinte, támogató, emberi és felemelő."
    )


def build_email_funnel_30day_prompt(product_name: str, target_audience: str, core_offer: str, lead_magnet: str = "Ingyenes Letölthető Minta / Munkafüzet", discount_info: str = "25% kedvezmény az ÜDVÖZÖLLEK kuponnal", language: str = "magyar", niche_name: str = "") -> str:
    """
    30-Day Complete Automated Email Marketing Funnel Master Prompt (Based on '30 Email Marketing Bundle').
    Divides into 5 structured phases:
    Phase 1 (Days 1-5): Welcome, Lead Magnet Delivery & Indoctrination
    Phase 2 (Days 6-12): Pure Value, Epiphany Stories & Authority Building
    Phase 3 (Days 13-18): Core Offer Pitch, Feature-Benefit Stack & Bonuses
    Phase 4 (Days 19-24): Social Proof, Case Studies & Objection Crushing
    Phase 5 (Days 25-30): Urgency, Scarcity, Price Increase Warning & Last Call
    """
    lang_inst = "magyar nyelven" if language.lower().startswith("magy") else "in English"
    niche_clause = f"\nPiaci Niche: {niche_name}" if niche_name else ""
    return (
        f"Te egy világklasszis e-mail marketing és ügyfélgondozási (Lifecycle Email Marketing) szakértő vagy, aki a '30 Email Marketing Bundle' rendszer mestere.{niche_clause}\n\n"
        f"Tervezz meg és írj meg egy TELJES 30 NAPOS AUTOMATA E-MAIL TÖLCSÉR STRUKTÚRÁT ÉS SZEKVENCIÁT {lang_inst} az alábbi digitális termékhez:\n\n"
        f"📌 TERMÉK / FŐ AJÁNLAT: {product_name}\n"
        f"🎯 CÉLKÖZÖNSÉG: {target_audience}\n"
        f"🎁 INGYENES CSALITERMÉK: {lead_magnet}\n"
        f"💎 FŐ AJÁNLAT LEÍRÁSA: {core_offer}\n"
        f"🏷️ KEDVEZMÉNY / AJÁNLAT: {discount_info}\n\n"
        f"A 30 NAPOS SZEKVENCIÁNAK AZ ALÁBBI 5 FÁZIST KELL LEFEDNIE:\n\n"
        f"🔹 1. FÁZIS: ÜDVÖZLÉS & BEVEZETÉS (1-5. NAP)\n"
        f"   - 1. nap: Lead magnet kézbesítése + Üdvözlés + 'Miért vagy itt?'\n"
        f"   - 2. nap: Gyors győzelem (Quick Win) — 1 azonnal alkalmazható lépés\n"
        f"   - 3. nap: Az én történetem (Hogyan voltam én is ebben a helyzetben)\n"
        f"   - 4. nap: A leggyakoribb hiba, amit 90% elkövet\n"
        f"   - 5. nap: Kérdezz-felelek (Visszajelzés kérése, közvetlen kapcsolat)\n\n"
        f"🔹 2. FÁZIS: TISZTA ÉRTÉKADÁS & HITELESSÉG (6-12. NAP)\n"
        f"   - 6. nap: Stratégiai tipp #1 (Gyakorlati megvalósítás)\n"
        f"   - 7. nap: Esettanulmány / Bizonyság (Hogyan változott meg valakinek az élete)\n"
        f"   - 8. nap: 'A titok, amiről senki sem beszél'\n"
        f"   - 9. nap: Ellenőrzőlista & Napi rutin tipp\n"
        f"   - 10. nap: Mi a különbség a sikeres és sikertelen próbálkozók között?\n"
        f"   - 11. nap: Ingyenes forrásajánló / Bónusz gondolat\n"
        f"   - 12. nap: Felvezetés: 'Holnap valami különleges érkezik...'\n\n"
        f"🔹 3. FÁZIS: A FŐ AJÁNLAT & ÉRTÉKHALMOZÁS (13-18. NAP)\n"
        f"   - 13. nap: A(z) {product_name} hivatalos bemutatása (A New Vehicle)\n"
        f"   - 14. nap: Mi van a csomagban? (Részletes Value Stack bemutatás)\n"
        f"   - 15. nap: Az exkluzív bónuszok leleplezése\n"
        f"   - 16. nap: Kockázatmentes garancia (Miért nem veszíthetsz semmit?)\n"
        f"   - 17. nap: Hogyan működik a gyakorlatban? (Lépésről lépésre betekintés)\n"
        f"   - 18. nap: Gyakori kérdések (FAQ) és kifogásrombolás\n\n"
        f"🔹 4. FÁZIS: BIZONYÍTÉKOK & KIFOGÁSKEZELÉS (19-24. NAP)\n"
        f"   - 19. nap: 'Nincs időm' kifogás eloszlatása\n"
        f"   - 20. nap: Vásárlói visszajelzések és tapasztalatok\n"
        f"   - 21. nap: 'Mi van, ha nem vagyok elég tehetséges / tapasztalt?'\n"
        f"   - 22. nap: Összehasonlítás: Más alternatívák vs. Ez a megoldás\n"
        f"   - 23. nap: Egy személyes vallomás / Miért fontos ez nekem?\n"
        f"   - 24. nap: A döntés pillanata (2 út áll előtted)\n\n"
        f"🔹 5. FÁZIS: SÜRGŐSSÉG & UTOLSÓ HÍVÁS (25-30. NAP)\n"
        f"   - 25. nap: Figyelmeztetés: A kedvezmény / bónusz hamarosan lejár\n"
        f"   - 26. nap: Mit veszítesz, ha most nem lépsz?\n"
        f"   - 27. nap: 48 óra van hátra — Utolsó esély a kedvezményre\n"
        f"   - 28. nap: 24 órás visszaszámlálás\n"
        f"   - 29. nap: MA ÉJFÉLKOR ZÁRUL: Utolsó lehetőség a bónuszokkal\n"
        f"   - 30. nap: Zárás & Köszönet (Új fejezet kezdete + következő lépések)\n\n"
        f"KIMENETI FORMÁTUM:\n"
        f"Adjad meg a 30 nap teljes áttekintését sorszámozva, minden naphoz:\n"
        f"- Tárgymező javaslattal\n"
        f"- Cél / Fő üzenet 2-3 mondatban\n"
        f"- Mintaszöveg / Levélvázlat lényegi bekezdésekkel és Call-to-Actionnel."
    )


def build_social_seo_calendar_30day_prompt(product_name: str, target_audience: str, main_topics: str = "", platforms: str = "Pinterest, Instagram, Blog", language: str = "magyar", niche_name: str = "") -> str:
    """
    30-Day Multi-Platform Social Media & SEO Content Calendar Master Prompt.
    Generates structured daily posts with Pinterest SEO titles/descriptions/tags, Instagram hooks/carousels, and Blog keywords.
    """
    lang_inst = "magyar nyelven" if language.lower().startswith("magy") else "in English"
    niche_clause = f"\nPiaci Niche: {niche_name}" if niche_name else ""
    topics = f"\nFő témakörök / pillérek: {main_topics}" if main_topics.strip() else ""
    
    return (
        f"Te egy mester Social Media & Organikus Keresőoptimalizálási (SEO & Content Strategy) szakértő vagy.{niche_clause}\n\n"
        f"Készíts egy strukturált, azonnal végrehajtható 30 NAPOS TARTALOMNAPTÁRAT ÉS SOCIAL SEO STRATÉGIÁT {lang_inst} az alábbi termékhez:\n\n"
        f"📌 TERMÉK: {product_name}\n"
        f"🎯 CÉLKÖZÖNSÉG: {target_audience}\n"
        f"📱 CÉLPLATFORMOK: {platforms}{topics}\n\n"
        f"STRUKTÚRA KÖVETELMÉNYEK:\n\n"
        f"Oszd fel a 30 napot 4 heti tematikus blokkra (Hét 1: Tudatosság & Fájdalompontok; Hét 2: Gyakorlati Tippek & Oktatás; Hét 3: Esettanulmányok & Ajánlat; Hét 4: Sürgősség & Közösségépítés).\n\n"
        f"MINDEN NAPHOZ (1–30. NAP) ADJ MEG:\n"
        f"1. 📌 PINTEREST PIN SEO:\n"
        f"   - Kattintásmágnes Pin Cím\n"
        f"   - 2 mondatos SEO Leírás releváns kulcsszavakkal\n"
        f"   - 5 db pontos keresési címke / hashtag\n\n"
        f"2. 📸 INSTAGRAM / TIKTOK POSZT:\n"
        f"   - 3 másodperces Horog (Hook) Reelhez vagy Carousel 1. diához\n"
        f"   - Tartalom lényege (3 bulletpoint)\n"
        f"   - Call To Action (pl. 'Írd meg kommentben a BÉKE szót és elküldöm a linket')\n\n"
        f"3. 📝 BLOG / EMAIL MIKRO-TÉMA:\n"
        f"   - 1 mondatos keresőbarát blogcím vagy hírlevél téma."
    )


# Aliases for backwards compatibility with any legacy imports
build_kdp_master_prompt = lambda *args, **kwargs: build_kdp_coloring_master_prompt(args[2] if len(args)>2 else (args[0] if args else "Bible scene"))
build_etsy_master_prompt = lambda *args, **kwargs: build_etsy_wall_art_master_prompt(args[3] if len(args)>3 else (args[0] if args else "Bible verse"))
build_devotional_master_prompt = lambda *args, **kwargs: build_gumroad_devotional_master_prompt(args[0] if args else "nőknek", args[1] if len(args)>1 else "Áhítat")
build_devotional_cover_prompt = lambda *args, **kwargs: build_kdp_cover_master_prompt(args[0] if args else "Bible scene", "Devotional")


# ─────────────────────────────────────────────────────────
# ⚡ KDP AUTO-PILOT BOOK FACTORY MANIFEST BUILDER & PARSER
# ─────────────────────────────────────────────────────────

def build_kdp_autopilot_manifest_prompt(
    book_title: str,
    theme: str,
    page_count: int = 30,
    target_audience: str = "children",
    style_name: str = "",
    image_model: str = "",
    trim_size: str = "8.5x11",
    aspect_ratio: str = "3:4"
) -> str:
    """
    Builds the Master Prompt for Gemini 3.7 Flash to generate the full book JSON manifest.
    Strict JSON output containing all scene details, KJV scripture references/texts, color suggestions,
    and optimized Imagen 3 / Nano Banana Pro visual prompts with exact aspect ratio and framing rules.
    """
    is_adult = "adult" in target_audience.lower() or "felnőtt" in target_audience.lower()
    style_spec = f"\nVisual Style Modifier: {style_name}" if style_name else ""
    clean_ratio = aspect_ratio.strip() if aspect_ratio else ("1:1" if "8.5x8.5" in trim_size else "3:4")
    
    framing_rule = "centered composition, full body framing showing the complete subject from head to toe, generous safe margins around all outer borders, zero cut-off elements"
    
    if is_adult:
        prompt_style_guide = (
            f"Create an intricate adult coloring book page illustration of: [Scene Description]. "
            f"Style: Highly intricate black line art on a pure crisp white background, realistic adult anatomical proportions, "
            f"dignified classic engraving style, complex floral mandala and zentangle background patterns, "
            f"zero shading, zero grayscale, zero colors. Aspect ratio: {clean_ratio}, {framing_rule}, formatted for Amazon KDP {trim_size}."
        )
    else:
        prompt_style_guide = (
            f"Create a clean black and white children's coloring book page illustration of: [Scene Description]. "
            f"Style: Bold clean black outlines on a pure crisp white background, cute friendly characters with expressive joyful faces, "
            f"clear distinct colorable shapes, vector illustration, zero shading, zero grayscale, zero colors. "
            f"Aspect ratio: {clean_ratio}, {framing_rule}, formatted for Amazon KDP {trim_size}."
        )

    model_visual_instruction = (
        "GEMINI WEB UI COMPATIBILITY RULES:\n"
        f"- Every `visual_prompt` must start with: 'Create a black and white coloring book page illustration of: '\n"
        f"- Follow with rich, specific details of the characters, actions, and scenery.\n"
        f"- End with: 'Style: [Style specs as defined above]. Aspect ratio: {clean_ratio}.'\n"
        f"- Ensure 100% character and style consistency across all pages."
    )

    return f"""You are an elite Christian Book Designer and KDP Publishing Architect.
Generate a structured, cohesive, publication-ready {page_count}-page coloring book outline and visual prompt manifest for Amazon KDP.

BOOK DETAILS:
- Main Title: {book_title}
- Theme / Storyline: {theme}
- Target Audience: {"Adult Christian Coloring & Meditation Book" if is_adult else "Children's Christian Coloring Book (Ages 4-8)"}
- Number of Unique Scenes: {page_count}
- Target Print Format: Amazon KDP {trim_size} (Aspect Ratio: {clean_ratio}){style_spec}

{model_visual_instruction}

CRITICAL REQUIREMENTS:
1. Every scene must be chronologically ordered or thematically coherent covering the story/theme across all {page_count} pages.
2. For each scene, provide:
   - `page_number`: Integer from 1 to {page_count}.
   - `title`: Short, inspiring scene title in English (e.g. "Noah Building the Wooden Ark").
   - `title_hu`: Hungarian translation of the scene title (e.g. "Noé a fahajót építi").
   - `scripture_reference`: Exact KJV Bible reference (e.g. "Genesis 6:14").
   - `scripture_text`: Accurate King James Version (KJV) Bible verse text.
   - `color_suggestions`: Array of 4 to 5 harmonious color names (e.g. ["Sky Blue", "Olive Green", "Warm Wood Brown", "Golden Yellow"]).
   - `visual_prompt`: A complete, self-contained, high-detail English image prompt strictly following this style:
     "{prompt_style_guide}"
     Describe the specific scene, characters, postures, background, and elements clearly.
   - `reflection_thought`: A 1-2 sentence warm, encouraging Christian meditation or prayer thought for the facing companion page.

OUTPUT FORMAT:
Output ONLY a valid, parseable JSON array of objects (one object per scene), with NO markdown backticks, NO markdown formatting, and NO text before or after the JSON.
Example structure:
[
  {{
    "page_number": 1,
    "title": "Noah Building the Wooden Ark",
    "title_hu": "Noé a fahajót építi",
    "scripture_reference": "Genesis 6:14",
    "scripture_text": "Make thee an ark of gopher wood; rooms shalt thou make in the ark...",
    "color_suggestions": ["Sky Blue", "Olive Green", "Warm Wood Brown", "Golden Yellow"],
    "visual_prompt": "Clean black and white children coloring book page of Noah standing on a wooden scaffold constructing the giant ark with hammer and wood planks, sunny hill background, simple thick black outlines, pure white background, zero shading, aspect ratio {clean_ratio}, centered composition, ready for {trim_size} print",
    "reflection_thought": "God gave Noah the exact wisdom to build the ark. Remember that God will guide and equip you for every task He calls you to."
  }}
]
"""


def build_kdp_dynamic_cover_prompt(
    book_title: str,
    theme_desc: str,
    page_count: int = 76,
    trim_size: str = "8.5x11",
    paper_type: str = "white",
    art_style: str = "",
    subtitle: str = ""
) -> str:
    """
    Builds a full wrap-around KDP cover prompt with dynamic spine calculation.
    """
    from kdp_math import calculate_kdp_cover_dimensions
    dims = calculate_kdp_cover_dimensions(page_count=page_count, trim_size=trim_size, paper_type=paper_type)
    
    spine_w = dims["spine_width_in"]
    total_w = dims["total_cover_width_in"]
    total_h = dims["total_cover_height_in"]
    style_suffix = f"\nArtistic Style: {art_style}" if art_style else ""

    return f"""Create a breathtaking, commercial-grade Amazon KDP wrap-around book cover illustration (Front Cover, Spine, and Back Cover).

BOOK DETAILS:
- Title: "{book_title}"
{f'- Subtitle: "{subtitle}"' if subtitle else ''}
- Cover Visual Concept: {theme_desc}
- Trim Size: {trim_size} Paperback
- Page Count: {page_count} pages ({paper_type.capitalize()} Paper)
- Calculated Total Dimensions: {total_w}" width x {total_h}" height (Spine width: {spine_w}"){style_suffix}

COMPOSITION REQUIREMENTS:
1. FRONT COVER (Right 45%):
   - Hero focal illustration depicting {theme_desc} with vibrant, joyful lighting.
   - Large bold prominent title lettering at top: "{book_title}".
   - Centered subject, leaving safe bleed margins at the edges.

2. SPINE (Middle ~{spine_w}"):
   - Harmonious background matching front and back colors.
   - Title text aligned vertically along the spine: "{book_title}".

3. BACK COVER (Left 45%):
   - Complementary scenery, soft background pattern, and designated clean space for barcode and blurb.

4. OVERALL STYLE:
   - High resolution 300 DPI print ready, clean vector/painted storybook style, no watermarks, professional KDP publication standard.
"""


def build_illustrated_book_manifest_prompt(
    book_title: str,
    book_genre: str = "Illustrated Story",
    target_audience: str = "Children",
    theme_storyline: str = "",
    page_count: int = 6,
    art_style: str = "",
    trim_size: str = "8.5x8.5",
    aspect_ratio: str = "1:1"
) -> str:
    """
    Builds the prompt for generating an illustrated and written storybook manifest with story text and image prompts.
    """
    clean_ratio = aspect_ratio.strip() if aspect_ratio else ("1:1" if "8.5x8.5" in trim_size else "3:4")
    style_suffix = f" Art Style: {art_style}." if art_style else " Art Style: Disney Pixar 3D cute vibrant storybook illustration, rich lighting."

    return f"""You are a master children's author and professional picture book illustrator.
Write an engaging, heart-warming {page_count}-chapter illustrated storybook for Amazon KDP publication.

BOOK SPECIFICATIONS:
- Title: {book_title}
- Target Audience / Subtitle: {target_audience}
- Core Theme & Plot: {theme_storyline}
- Number of Chapters / Pages: {page_count}
- Print Trim Size: {trim_size} (Aspect Ratio: {clean_ratio})

REQUIREMENTS:
1. Write a complete, heartwarming story across exactly {page_count} sequential chapters.
2. For each chapter:
   - `page_number`: Integer 1 to {page_count}.
   - `chapter_title`: Engaging chapter heading (e.g. "1. Fejezet: Barnabás és a napsütötte völgy").
   - `story_text`: Rich, beautifully written narrative story text (about 60-120 words per chapter in Hungarian, teaching faith, courage, and love).
   - `illustration_prompt`: A detailed, self-contained English image generation prompt tailored for {clean_ratio} aspect ratio and Amazon KDP {trim_size} print.{style_suffix}
   - `scene_summary`: Brief 1-sentence summary of the chapter's key visual event.

OUTPUT FORMAT:
Output ONLY a valid, parseable JSON array of objects with NO markdown formatting, NO markdown code fences, and NO extra commentary.
[
  {{
    "page_number": 1,
    "chapter_title": "1. Fejezet: A békés völgy reggele",
    "story_text": "A hegyek lábánál, a zöldellő legelő szélén élt Barnabás, a kis bárány...",
    "illustration_prompt": "Vibrant storybook illustration of a cute fluffy lamb standing in a sunlit wildflower meadow, soft golden morning light, Disney Pixar 3D art style, centered framing, 1:1 aspect ratio, ready for 8.5x8.5 KDP print",
    "scene_summary": "Barnabás a napsütötte réten játszik a barátaival."
  }}
]
"""


def robust_json_repair_and_parse(raw_text: str, expected_type: str = "list", default_fallback: Any = None) -> Any:
    """
    Ultra-resilient multi-stage JSON parser and repair engine for LLM outputs.
    Handles:
    - Markdown code fences (```json ... ```)
    - Preamble/postamble commentary text
    - Unescaped newlines and unescaped double quotes inside strings
    - Trailing commas before } and ]
    - Truncated JSON arrays (auto-closes open quotes, braces, brackets)
    - Individual object regex harvesting if full array parse fails
    """
    import json, re

    if not raw_text or not raw_text.strip():
        return default_fallback if default_fallback is not None else ([] if expected_type == "list" else {})

    clean = raw_text.strip()

    # Step 1: Strip markdown backticks
    if clean.startswith("```json"):
        clean = clean[7:]
    elif clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    clean = clean.strip()

    # Step 2: Try direct parse
    try:
        data = json.loads(clean)
        if expected_type == "list" and isinstance(data, list):
            return data
        elif expected_type == "list" and isinstance(data, dict):
            for k in ["pages", "chapters", "scenes", "items", "manifest", "data", "book"]:
                if k in data and isinstance(data[k], list):
                    return data[k]
            return [data]
        elif expected_type == "dict" and isinstance(data, dict):
            return data
    except Exception:
        pass

    # Step 3: Locate outer [ ... ] or { ... } boundaries
    first_bracket = clean.find("[")
    last_bracket = clean.rfind("]")
    if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
        json_candidate = clean[first_bracket:last_bracket + 1]
    else:
        first_brace = clean.find("{")
        last_brace = clean.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            json_candidate = clean[first_brace:last_brace + 1]
        else:
            json_candidate = clean[first_bracket:] if first_bracket != -1 else clean

    # Step 4: Fix trailing commas
    fixed_commas = re.sub(r',\s*([\]}])', r'\1', json_candidate)
    try:
        data = json.loads(fixed_commas)
        if expected_type == "list" and isinstance(data, list):
            return data
        elif expected_type == "list" and isinstance(data, dict):
            for k in ["pages", "chapters", "scenes", "items", "manifest", "data", "book"]:
                if k in data and isinstance(data[k], list):
                    return data[k]
            return [data]
        elif expected_type == "dict" and isinstance(data, dict):
            return data
    except Exception:
        pass

    # Step 5: Truncated JSON array repair (auto-close open string, open braces, open bracket)
    if first_bracket != -1:
        repaired = json_candidate.strip()
        # If open string exists (odd number of unescaped quotes)
        quotes_count = len(re.findall(r'(?<!\\)"', repaired))
        if quotes_count % 2 != 0:
            repaired += '"'
        # Close open braces
        open_braces = repaired.count("{") - repaired.count("}")
        if open_braces > 0:
            repaired += "}" * open_braces
        # Close open bracket
        if repaired.count("[") > repaired.count("]"):
            repaired += "]"
        
        # Clean trailing commas again
        repaired = re.sub(r',\s*([\]}])', r'\1', repaired)
        try:
            data = json.loads(repaired)
            if isinstance(data, list) and len(data) > 0:
                return data
        except Exception:
            pass

    # Step 6: Regex harvesting of individual JSON objects { ... }
    # Extracts each chapter / scene dictionary independently even if the overall array is broken
    objects = []
    # Pattern to match balanced or near-balanced top-level JSON objects
    obj_matches = re.finditer(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', clean, re.DOTALL)
    for m in obj_matches:
        chunk = m.group(0).strip()
        chunk_clean = re.sub(r',\s*([\]}])', r'\1', chunk)
        try:
            parsed_obj = json.loads(chunk_clean)
            if isinstance(parsed_obj, dict) and any(k in parsed_obj for k in ["page_number", "chapter_title", "title", "story_text", "visual_prompt", "illustration_prompt"]):
                objects.append(parsed_obj)
        except Exception:
            # Try to fix unescaped double quotes inside values using key-value regex
            try:
                fixed_chunk = re.sub(r'(?<!\\)"(?=(?:[^"]*"[^"]*")*[^"]*$)', '\\"', chunk)
                fixed_chunk = re.sub(r'\\"(page_number|chapter_title|title|title_hu|story_text|visual_prompt|illustration_prompt|scripture_reference|scripture_text|color_suggestions|reflection_thought|scene_summary)\\"', r'"\1"', fixed_chunk)
                parsed_obj = json.loads(fixed_chunk)
                if isinstance(parsed_obj, dict):
                    objects.append(parsed_obj)
            except Exception:
                pass

    if objects:
        return objects

    return default_fallback if default_fallback is not None else ([] if expected_type == "list" else {})


def parse_kdp_autopilot_manifest_json(response_text: str) -> list:
    """
    Parses and sanitizes the JSON response returned by Gemini for the coloring book manifest.
    Guarantees a clean, complete list of scenes with all required fields.
    """
    parsed = robust_json_repair_and_parse(response_text, expected_type="list", default_fallback=[])
    
    if parsed and isinstance(parsed, list):
        cleaned_list = []
        for idx, sc in enumerate(parsed, start=1):
            if isinstance(sc, dict):
                p_num = sc.get("page_number", idx)
                title = sc.get("title", f"Bible Scene {idx}")
                title_hu = sc.get("title_hu", f"{idx}. Jelenet")
                s_ref = sc.get("scripture_reference", "Scripture Reference")
                s_text = sc.get("scripture_text", "Thy word is a lamp unto my feet, and a light unto my path.")
                s_colors = sc.get("color_suggestions", ["Sky Blue", "Olive Green", "Sun Gold", "Wood Brown", "Rose Pink"])
                if isinstance(s_colors, str):
                    s_colors = [c.strip() for c in s_colors.split(",") if c.strip()]
                v_prompt = sc.get("visual_prompt") or sc.get("illustration_prompt") or f"Clean black and white coloring book page of {title}, bold outlines, white background"
                ref_thought = sc.get("reflection_thought", "God is faithful and guides your path every day.")

                cleaned_list.append({
                    "page_number": p_num,
                    "title": title,
                    "title_hu": title_hu,
                    "scripture_reference": s_ref,
                    "scripture_text": s_text,
                    "color_suggestions": s_colors,
                    "visual_prompt": v_prompt,
                    "reflection_thought": ref_thought
                })
        if cleaned_list:
            return cleaned_list

    return []


def parse_illustrated_book_manifest_json(response_text: str) -> list:
    """
    Parses and sanitizes the JSON response returned by Gemini for an illustrated & written book manifest.
    Guarantees a clean list of chapters with complete story text, titles, and illustration prompts.
    """
    parsed = robust_json_repair_and_parse(response_text, expected_type="list", default_fallback=[])

    if parsed and isinstance(parsed, list):
        cleaned_chapters = []
        for idx, ch in enumerate(parsed, start=1):
            if isinstance(ch, dict):
                p_num = ch.get("page_number", idx)
                c_title = ch.get("chapter_title") or ch.get("title") or f"{idx}. Fejezet"
                s_text = ch.get("story_text") or ch.get("text") or ch.get("content") or ""
                ill_prompt = ch.get("illustration_prompt") or ch.get("visual_prompt") or ch.get("image_prompt") or f"Vibrant full color storybook illustration of {c_title}, high resolution, 8.5x8.5"
                s_summary = ch.get("scene_summary", "")

                cleaned_chapters.append({
                    "page_number": p_num,
                    "chapter_title": c_title,
                    "story_text": s_text,
                    "illustration_prompt": ill_prompt,
                    "scene_summary": s_summary
                })
        if cleaned_chapters:
            return cleaned_chapters

    return []


# ─────────────────────────────────────────────────────────
# STRICT ETSY SEO PROMPT & PARSER ENGINE
# ─────────────────────────────────────────────────────────

def build_strict_etsy_seo_prompt(
    product_title: str,
    product_type: str = "Wall Art",
    niche_name: str = "",
    extra_details: str = ""
) -> str:
    """
    Constructs an expert Etsy SEO prompt adhering strictly to 2026 Etsy algorithm rules:
    - Title: Max 140 characters, front-loaded with primary high-intent keywords
    - Tags: Exactly 13 tags, each max 20 characters, multi-word long-tail keywords
    - Description: High-converting FFC framework with Value Stack and clear instructions
    """
    return f"""You are a master Etsy SEO strategist and conversion copywriter.
Generate a complete, high-ranking Etsy listing package for the following digital product:

PRODUCT TITLE / THEME: {product_title}
PRODUCT TYPE: {product_type}
NICHE / TARGET AUDIENCE: {niche_name if niche_name else "Christian Faith, Home Decor & Digital Art"}
EXTRA KEYWORDS & DETAILS: {extra_details if extra_details else "High quality 300 DPI print-ready files, instant digital download"}

STRICT ETSY COMPLIANCE REQUIREMENTS:
1. TITLE:
   - MUST BE STRICTLY UNDER 140 CHARACTERS.
   - Front-load with the most searched 2-3 word keyword phrase.
   - Separate phrases with clean punctuation (e.g., " | " or " - ").
   - No repetitive keyword stuffing.

2. TAGS:
   - EXACTLY 13 TAGS.
   - EACH TAG MUST BE STRICTLY 20 CHARACTERS OR LESS (including spaces).
   - Use multi-word long-tail phrases (no single words).
   - Do NOT repeat the exact same word across too many tags.
   - All lowercase.

3. DESCRIPTION:
   - Professional, high-converting product description using the Feel-Felt-Found / FFC framework.
   - Include: Hook & Emotional benefit, What is Included (File formats, 300 DPI, sizes), How it Works / Instant Download Instructions, and Licensing / Terms of Use.

OUTPUT FORMAT:
Output ONLY a valid, parseable JSON object with NO markdown backticks, with the following exact keys:
{{
  "title": "Front-Loaded Etsy Title (max 140 chars)",
  "tags": [
    "tag 1 (max 20 c)",
    "tag 2 (max 20 c)",
    "tag 3 (max 20 c)",
    "tag 4 (max 20 c)",
    "tag 5 (max 20 c)",
    "tag 6 (max 20 c)",
    "tag 7 (max 20 c)",
    "tag 8 (max 20 c)",
    "tag 9 (max 20 c)",
    "tag 10 (max 20 c)",
    "tag 11 (max 20 c)",
    "tag 12 (max 20 c)",
    "tag 13 (max 20 c)"
  ],
  "description": "Full formatted product description text"
}}
"""


def parse_strict_etsy_seo_output(raw_text: str) -> dict:
    """
    Parses and enforces strict Etsy SEO limits on LLM output:
    - Truncates title to 140 characters
    - Sanitizes tags to exactly 13 items, each max 20 characters
    - Returns structured dictionary
    """
    import re
    parsed = robust_json_repair_and_parse(raw_text, expected_type="dict", default_fallback={})

    title = ""
    tags = []
    description = ""

    if isinstance(parsed, dict) and "title" in parsed:
        title = str(parsed.get("title", "")).strip()
        raw_tags = parsed.get("tags", [])
        if isinstance(raw_tags, list):
            tags = [str(t).strip().lower() for t in raw_tags if str(t).strip()]
        elif isinstance(raw_tags, str):
            tags = [t.strip().lower() for t in raw_tags.split(",") if t.strip()]
        description = str(parsed.get("description", "")).strip()

    # Fallback text parsing if JSON parse yielded empty results
    if not title:
        title_match = re.search(r'(?:TITLE|CÍM):\s*(.+)', raw_text, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            first_line = raw_text.strip().split("\n")[0]
            title = first_line[:140]

    if not tags:
        tags_match = re.search(r'(?:TAGS|CÍMKÉK):\s*(.+)', raw_text, re.IGNORECASE)
        if tags_match:
            tags_str = tags_match.group(1)
            tags = [t.strip().lower() for t in tags_str.split(",") if t.strip()]

    if not description:
        desc_match = re.search(r'(?:DESCRIPTION|LEÍRÁS):\s*(.+)', raw_text, re.IGNORECASE | re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()
        else:
            description = raw_text.strip()

    # Enforce strict Etsy rules
    # 1. Title max 140 chars
    if len(title) > 140:
        title = title[:137].rsplit(" ", 1)[0] + "..."

    # 2. Tags max 20 chars each, max 13 tags
    sanitized_tags = []
    for t in tags:
        clean_t = re.sub(r'[^a-zA-Z0-9\s-]', '', t).strip()
        if len(clean_t) > 20:
            clean_t = clean_t[:20].strip()
        if clean_t and clean_t not in sanitized_tags:
            sanitized_tags.append(clean_t)
        if len(sanitized_tags) >= 13:
            break

    # If fewer than 13 tags, fill with default high-demand tags
    default_fill_tags = [
        "digital download", "printable art", "instant download", "home wall decor",
        "bible scripture", "christian gift", "faith poster", "modern wall art",
        "aesthetic print", "minimalist art", "300 dpi printable", "wall decor print", "digital print"
    ]
    for dt in default_fill_tags:
        if len(sanitized_tags) >= 13:
            break
        if dt not in sanitized_tags:
            sanitized_tags.append(dt)

    return {
        "title": title,
        "tags": sanitized_tags[:13],
        "description": description
    }




