"""
Master Prompt Generator Engine for Christian & Multi-Niche Digital Products
Based on the Autism-Friendly 100% Async Digital Business System Document
(Google AI Pro Ecosystem - Master Prompt Templates, 22 High-Demand Niches & FFC Copywriting Framework)
"""

# ─────────────────────────────────────────────────────────
# KERESZTÉNY CÉLCSOPORTOK & FELADAT-SPECIFIKUS STÍLUSOK
# ─────────────────────────────────────────────────────────

CHRISTIAN_SUB_NICHES = {
    "👶 Gyermekek & Családok (Bible Stories & Coloring)": {
        "audience": "Keresztény családok, vasárnapi iskolások és kisgyermekes édesanyák",
        "keywords": ["bible stories for kids", "christian coloring book", "noah ark", "toddler scripture"],
        "tone": "Kedves, vidám, tiszta és bátorító",
        "default_kdp_title_en": "Noah's Ark Bible Adventures",
        "default_kdp_title_hu": "Noé Bárkája Bibliai Kalandok",
        "default_kdp_sub_en": "Inspiring Bible Verse Coloring Book for Children",
        "default_kdp_sub_hu": "Inspiráló Bibliai Igés Színezőkönyv Gyermekeknek"
    },
    "🌸 Édesanyák & Keresztény Nők (Devotionals & Peace)": {
        "audience": "Túlterhelt keresztény édesanyák és nők, akik lelki megújulásra vágynak",
        "keywords": ["devotional for women", "christian mom journal", "peace in the storm", "prayer journal"],
        "tone": "Meleg, mélyen lelkigondozói, megértő és vigasztaló",
        "default_kdp_title_en": "Peace in the Storm: Daily Devotional for Mothers",
        "default_kdp_title_hu": "Békesség a Viharban: Napi Áhítat Édesanyáknak",
        "default_kdp_sub_en": "30 Days of Guided Scripture & Prayer Journal",
        "default_kdp_sub_hu": "30 Napos Vezetett Igés Imádságos Napló"
    },
    "🛡️ Férfiak & Családfők (Faith & Leadership)": {
        "audience": "Keresztény férfiak, apák és vezetők",
        "keywords": ["christian men devotional", "biblical leadership", "strength in faith", "men prayer"],
        "tone": "Erőt adó, bátor, gyakorlatias és hitvalló",
        "default_kdp_title_en": "Armor of God: Daily Devotional for Men",
        "default_kdp_title_hu": "Isten Fegyverzete: Napi Áhítat Férfiaknak",
        "default_kdp_sub_en": "Strength, Courage and Biblical Wisdom for Daily Battles",
        "default_kdp_sub_hu": "Erő, Bátorság és Bibliai Bölcsesség a Mindennapi Harcokhoz"
    },
    "🕊️ Lelki Béke & Csendesség (Mindfulness & Prayer)": {
        "audience": "Belső békét, imádságos elcsendesedést és Isten jelenlétét keresők",
        "keywords": ["christian mindfulness", "prayer journal", "psalms of peace", "silent prayer"],
        "tone": "Leföldelő, békés, kontemplatív és hálaadó",
        "default_kdp_title_en": "Be Still and Know: Guided Prayer Journal",
        "default_kdp_title_hu": "Csendesedjetek El: Vezetett Imádságos Napló",
        "default_kdp_sub_en": "Quiet Meditations and Scripture Reflections",
        "default_kdp_sub_hu": "Csendes Elmélkedések és Bibliai Reflexiók"
    },
    "📖 Zsoltárok & Dicsőítés (Wall Art & Devotional)": {
        "audience": "Igei otthondekorációt és dicsőítő reflexiókat keresők",
        "keywords": ["psalms wall art", "scripture prints", "worship journal", "eucalyptus bible art"],
        "tone": "Ünnepélyes, felemelő, biblikus és dicsőítő",
        "default_kdp_title_en": "Psalms of Grace: Scripture Coloring & Reflection",
        "default_kdp_title_hu": "A Kegyelem Zsoltárai: Igés Színező és Elmélkedés",
        "default_kdp_sub_en": "Beautiful Bible Verse Art and Meditations",
        "default_kdp_sub_hu": "Gyönyörű Bibliai Igés Grafikák és Elmélkedések"
    }
}

KDP_TASK_STYLES = {
    "👶 Gyermek Vonalrajz (Section 5.1 - Vastag kontúrok, cuki formák, tiszta fehér háttér, árnyékmentes)": {
        "prompt_mod": "clean bold black line art, cute simple vector style for children coloring book, pure white background, no shading, no grayscale, no gradients, 8.5:11 inch, 4K resolution",
        "is_adult": False
    },
    "🧘 Felnőtt Meditációs Színező (Intrikát botanikai minták, mandala, zentangle, finom vonalháló)": {
        "prompt_mod": "intricate black and white line art, botanical zentangle patterns, detailed coloring page for adult relaxation, pure white background, crisp outlines, 8.5:11 inch, 4K",
        "is_adult": True
    },
    "📖 Akvarell Mesekönyv Illusztráció (Lágy pasztell akvarell, következetes karakterek, meleg fények)": {
        "prompt_mod": "soft watercolor storybook illustration, gentle pastel colors, warm glowing light, consistent children's book art style, high detail, 8.5:8.5 inch",
        "is_adult": False
    },
    "🎨 Élénk Vektoros Borító (17.412:11.25 Wrap-Around, pasztell harmónia, tiszta tipográfia)": {
        "prompt_mod": "professional children's book wrap-around cover, pastel color palette, clean modern vector art, bold typography header, 17.412:11.25 aspect ratio",
        "is_adult": False
    }
}

ETSY_TASK_STYLES = {
    "🌿 Skandináv Eukaliptusz Minimalista (Section 5.2 - Lágy zöld akvarell levelek, letisztult KJV tipográfia, 4:5)": {
        "prompt_mod": "elegant minimalist watercolor design with soft green eucalyptus leaves framing central text, Scandinavian Christian wall art style, 4:5 aspect ratio",
        "tags_addon": ["scandinavian art", "eucalyptus print", "minimalist poster", "modern wall art"]
    },
    "✨ Modern Arany & Márvány Prémium (Arany fólia elemek, finom márvány textúra, luxus serif betűk)": {
        "prompt_mod": "luxury Christian wall art, gold foil geometric accents, subtle white marble background, elegant serif scripture typography, 4:5 ratio",
        "tags_addon": ["gold scripture art", "marble wall art", "luxury faith decor", "elegant poster"]
    },
    "🎨 Vintage Botanikai & Vadvirágos (Klasszikus herbárium stílus, antik papír árnyalat, finom virágkoszorú)": {
        "prompt_mod": "vintage botanical watercolor illustration, pressed wildflowers wreath framing scripture text, antique warm paper tone, 4:5 ratio",
        "tags_addon": ["vintage scripture", "botanical wall art", "wildflower print", "cottagecore faith"]
    },
    "✂️ Cuki Chibi Clipart (Izolált tiszta fehér háttér, matrica kontúr, pasztell akvarell karakter)": {
        "prompt_mod": "cute chibi watercolor clipart character, soft pastel palette, isolated on pure white background, sticker outline, high resolution, 1:1 ratio",
        "tags_addon": ["chibi clipart", "watercolor sticker", "christian clipart", "digital png"]
    },
    "🕊️ Rusztikus Farmhouse & Fa Textúra (Meleg barna tónusok, fehérre meszelt deszka háttér, vintage kalligráfia)": {
        "prompt_mod": "rustic farmhouse Christian wall art, whitewashed wood background, dark charcoal modern calligraphy scripture, 4:5 ratio",
        "tags_addon": ["farmhouse decor", "rustic scripture", "wooden wall art", "country faith"]
    }
}

GUMROAD_TASK_STYLES = {
    "🕊️ Meleg, Bátorító Lelkigondozói (Section 5.3 - Mélyen emberi, vigasztaló, békességet sugárzó)": {
        "instruction": "Írj meleg, mélyen bátorító, lelki békességet sugárzó, tiszteletteljes és emberi tónusban. Kerüld a mesterkélt AI fordulatokat és a száraz teológiai fejtegetéseket."
    },
    "🧘 Csendes Meditatív & Imádságos (Lassú reflexió, mély belső elcsendesedés, kontemplatív kérdések)": {
        "instruction": "Írj csendes, meditatív, imádságos hangvételben, amely segít lelassulni, elengedni a szorongást és Isten jelenlétében megnyugodni."
    },
    "⚔️ Hitvalló, Bátor & Gyakorlatias (Erőt adó, bibliai igazságok gyakorlati alkalmazása a mindennapi harcokban)": {
        "instruction": "Írj dinamikus, erőt adó, bátor és gyakorlatias stílusban, amely konkrét cselekvésre és hitbeli kitartásra ösztönöz a mindennapokban."
    },
    "🌸 Édesanyáknak & Nőknek Szóló Gyengéd Tónus (Család, anyaság, hálaadás, lelki feltöltődés a rohanásban)": {
        "instruction": "Írj gyengéd, megértő, édesanyák szívéhez szóló hangvételben, amely elismeri a mindennapi fáradtságot és Isten megújító kegyelmére mutat."
    }
}


def build_gemini_custom_gem_instructions(
    gem_type: str,
    project_title: str,
    style_name: str = "",
    target_audience: str = "",
    characters_desc: str = ""
) -> str:
    """
    Generates a turnkey Gemini Custom Gem (or Custom GPT) System Instruction prompt
    to ensure 100% style consistency, consistent character faces/clothing, and strict formatting.
    """
    if "kdp" in gem_type.lower() or "coloring" in gem_type.lower() or "könyv" in gem_type.lower():
        char_clause = f"\n- **Főszereplők leírása:** {characters_desc}" if characters_desc else "\n- **Főszereplők:** Ha egy bibliai alak (pl. Noé, Mózes, Dávid, kisfiú, oroszlán) többször megjelenik, minden oldalon tartsd meg ugyanazt a ruhát, arcszerkezetet, hajat és arckifejezést!"
        return f"""# 💎 GEMINI CUSTOM GEM: KDP KÖNYV- ÉS SZÍNEZŐ SPECIALISTA
Te egy professzionális Amazon KDP illusztrátor és színezőkönyv-készítő AI vagy a(z) '{project_title}' kötethez.

## 🎨 KÖTELEZŐ VIZUÁLIS SZABÁLYOK (100% STÍLUS- ÉS KARAKTERKONZISZTENCIA):
1. **Művészeti Stílus:** {style_name or 'Tiszta, vastag fekete vonalrajz (Bold Black Line Art), pure white background'}
2. **Háttér & Tónusok:** Kizárólag hófehér háttér (#ffffff). SOHA ne használj szürkeárnyalatot (grayscale), árnyékolást (shading), sem színátmeneteket!
3. **Formátum & Margók:** 8.5x11 hüvelyk arány (3:4 portrait). A figurák mindig a kép közepére kerüljenek, kényelmes margót hagyva a széleken (nincs levágott fej/kéz/láb).
4. **Vonalvezetés:** Zárt, határozott, kifesthető fekete kontúrok minden egyes oldalon.{char_clause}

## 🚀 MŰKÖDÉSI UTASÍTÁS:
Amikor megadok egy jelenetet vagy oldalszámot, AZONNAL generáld le a fenti szabályoknak megfelelő 4K képet a Gemini Imagen motorral!"""

    elif "etsy" in gem_type.lower() or "wall" in gem_type.lower() or "clipart" in gem_type.lower():
        return f"""# 💎 GEMINI CUSTOM GEM: ETSY WALL ART & CLIPART MŰVÉSZETI SPECIALISTA
Te egy prémium minőségű Etsy digitális művész és grafikus AI vagy a(z) '{project_title}' kollekcióhoz.

## 🎨 KÖTELEZŐ MŰVÉSZETI ÉS FORMÁTUM SZABÁLYOK:
1. **Művészeti Stílus:** {style_name or 'Skandináv minimalista akvarell eukaliptusz levelekkel keretezett tiszta tipográfia'}
2. **Képarány:** Faliképeknél pontos 4:5 arány (300 DPI 4K minőség), Clipart csomagoknál 1:1 arány.
3. **Színharmónia:** Lágy, elegáns pasztell árnyalatok, prémium hangulat, finom részletek.
4. **Háttér:** Faliképeknél tiszta vagy lágy textúra; Clipartoknál izolált 100% tiszta fehér háttér (könnyű többkörös háttéreltávolításhoz).

## 🚀 MŰKÖDÉSI UTASÍTÁS:
Bibliai igehely vagy téma megadásakor azonnal készítsd el a 4K művészi kompozíciót a Gemini Imagen motorral!"""

    else:
        return f"""# 💎 GEMINI CUSTOM GEM: KERESZTÉNY LELKIGONDOZÓI & ÁHÍTAT ÍRÓ
Te egy mélyen hiteles, melegszívű lelkigondozó író AI vagy a(z) '{project_title}' kötethez.
Hangnem és stílus: {style_name or 'Meleg, bátorító, mélyen spirituális, tiszteletteljes és emberi tónus'}. Kerüld az elcsépelt AI kliséket és a száraz fejtegetéseket."""


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
    FFC Big Domino Hooks & Headlines Generator Prompt with strict language separation.
    Generates 10 high-converting headlines in the format:
    'Get [Desire] without [Pain], even if [Objection], using [Vehicle]'
    """
    is_en = "angol" in language.lower() or "english" in language.lower()
    niche_clause = f"\nNiche: {niche_name}" if niche_name else ""

    if is_en:
        return (
            f"You are an elite Direct Response Copywriter specialized in crafting world-class Big Domino hooks and headlines.{niche_clause}\n\n"
            f"Craft exactly 10 high-converting BIG DOMINO HOOKS AND HEADLINES in 100% PURE, NATURAL ENGLISH (US) for the following product:\n\n"
            f"📌 PRODUCT: {product_name}\n"
            f"🎯 TARGET AUDIENCE: {target_audience}\n"
            f"✨ DESIRE / TRANSFORMATION: {main_transformation}\n"
            f"🚀 VEHICLE / MECHANISM: {vehicle}\n\n"
            f"CRITICAL LANGUAGE RULE: Output ONLY 100% fluent English. Do NOT mix any Hungarian words or characters.\n\n"
            f"HEADLINE CATEGORIES TO GENERATE:\n"
            f"- 1-3. Direct Transformation & Big Promise Headlines\n"
            f"- 4-6. 'Even If' Objection-Crushing Headlines (Time constraints, doubts, beginners)\n"
            f"- 7-8. Curiosity & Secret-Based Discovery Headlines\n"
            f"- 9-10. Short, Punchy Social Media & Email Subject Line Hooks (Max 10 words)"
        )
    else:
        return (
            f"Te egy mester szövegíró (Master Copywriter) vagy, aki a világ legmagasabb konverziójú horgait (Hooks & Headlines) készíti el.{niche_clause}\n\n"
            f"Készíts pontosan 10 db pszichológiailag ellenállhatatlan BIG DOMINO HORGOT ÉS FŐCÍMET 100%-BAN TISZTA MAGYAR NYELVEN az alábbi termékhez:\n\n"
            f"📌 TERMÉK: {product_name}\n"
            f"🎯 CÉLCSOPORT: {target_audience}\n"
            f"✨ FŐ VÁGY / TRANSZFORMÁCIÓ: {main_transformation}\n"
            f"🚀 MÓDSZER / ESZKÖZ (VEHICLE): {vehicle}\n\n"
            f"SZIGORÚ NYELVI KÖVETELMÉNY: Kizárólag hibátlan, természetes magyar nyelven írj! Tilos idegen szavakat keverni.\n\n"
            f"KÉSZÍTS 10 EGYEDI VARIÁCIÓT:\n"
            f"- 1-3. Közvetlen Transzformációs Horgok (Erős, tiszta ígéret)\n"
            f"- 4-6. 'Még akkor is ha...' Kifogásromboló Horgok (Időhiány, fáradtság, kezdő szint)\n"
            f"- 7-8. Kíváncsiság- és Titok-alapú Horgok (A rejtett kulcs)\n"
            f"- 9-10. Rövid, ütős Social Media & E-mail Tárgymező Horgok (Max 10 szó)"
        )


def build_ffc_value_stack_prompt(product_name: str, target_audience: str, core_features: str, bonuses: str = "", regular_price: str = "19 990 Ft", language: str = "magyar") -> str:
    """
    FFC Value Stack & Feature-Benefit-Meaning Matrix Generator with strict language purity.
    """
    is_en = "angol" in language.lower() or "english" in language.lower()
    bonus_part = f"\nBonuses: {bonuses}" if bonuses.strip() else ""

    if is_en:
        return (
            f"Create a high-converting Russell Brunson style VALUE STACK and feature-benefit matrix in 100% PURE ENGLISH (US) for the following product:\n\n"
            f"📌 PRODUCT: {product_name}\n"
            f"🎯 TARGET AUDIENCE: {target_audience}\n"
            f"📦 CORE FEATURES & DELIVERABLES: {core_features}{bonus_part}\n"
            f"💰 TOTAL ESTIMATED VALUE: {regular_price}\n\n"
            f"CRITICAL LANGUAGE RULE: Output ONLY 100% fluent English. Do NOT mix any foreign words.\n\n"
            f"STRUCTURE REQUIREMENTS:\n"
            f"1. 5-7 MASTER BULLET POINTS (Feature + Benefit + Even If + Meaning)\n"
            f"2. THE COMPLETE VALUE STACK TABLE (Items + Real Market Values + Total Real Value + Today's Discount Price)\n"
            f"3. 'WHY IT'S A NO-BRAINER' (1 compelling paragraph justifying why this offer is irresistible)."
        )
    else:
        return (
            f"Készíts egy profi, Russell Brunson-stílusú ÉRTÉKHALMOZÁST (Value Stack) és termék-bulletpont rendszert 100%-BAN TISZTA MAGYAR NYELVEN az alábbi termékhez:\n\n"
            f"📌 TERMÉK: {product_name}\n"
            f"🎯 CÉLCSOPORT: {target_audience}\n"
            f"📦 FŐ TULAJDONSÁGOK / CSOMAG ELEMEI: {core_features}{bonus_part}\n"
            f"💰 NÉVLEGES PIACI ÉRTÉK: {regular_price}\n\n"
            f"SZIGORÚ NYELVI KÖVETELMÉNY: Kizárólag hibátlan, természetes magyar nyelven írj! Tilos idegen kifejezéseket keverni.\n\n"
            f"STRUKTÚRA KÖVETELMÉNYEK:\n"
            f"1. ✨ 5-7 DB MASTER BULLETPOINT AZ FFC NÉGYFÁZISÚ FORMULÁVAL (Funkció + Haszon + Még akkor is ha + Ami azt jelenti)\n"
            f"2. 📊 TELJES ÉRTÉKHALMOZÁSI TÁBLÁZAT (Tételek + Piaci Értékek + Teljes Érték + Kedvezményes Ár)\n"
            f"3. 💥 'MIÉRT VISSZAUTASÍTHATATLAN AJÁNLAT EZ' (1 meggyőző bekezdés)."
        )


def build_ffc_sales_letter_prompt(product_name: str, target_audience: str, main_transformation: str, pain_points: str = "", vehicle: str = "", bonuses: str = "", guarantee_type: str = "30 napos 100% elégedettségi garancia", language: str = "magyar", niche_name: str = "") -> str:
    """
    FFC 12-Step Master Sales Letter Generator Prompt with strict language purity.
    """
    is_en = "angol" in language.lower() or "english" in language.lower()
    niche_clause = f"\nNiche: {niche_name}" if niche_name else ""
    pains = f"\nFrustrations/Pains: {pain_points}" if pain_points.strip() else ""
    veh = f"\nMechanism/Vehicle: {vehicle}" if vehicle.strip() else ""
    bon = f"\nBonuses: {bonuses}" if bonuses.strip() else ""

    if is_en:
        return (
            f"You are a world-class Direct Response Copywriter in the style of Russell Brunson and Alex Hormozi.{niche_clause}\n\n"
            f"Write a complete, deeply engaging, highly converting Long-Form Sales Letter in 100% PURE, NATURAL ENGLISH (US) for this product:\n\n"
            f"📌 PRODUCT NAME: {product_name}\n"
            f"🎯 TARGET AUDIENCE: {target_audience}\n"
            f"✨ CORE TRANSFORMATION: {main_transformation}{pains}{veh}{bon}\n"
            f"🛡️ GUARANTEE TYPE: {guarantee_type}\n\n"
            f"CRITICAL LANGUAGE RULE: Output strictly 100% natural, polished English. Do NOT mix in any Hungarian or other foreign words.\n\n"
            f"STRUCTURE TO FOLLOW (12-STEP PSYCHOLOGICAL ARC):\n"
            f"1. THE BIG HOOK & PRE-HEADLINE\n"
            f"2. SHOCKING STATEMENT / BOLD CLAIM\n"
            f"3. DEEP PAIN & BURNING DESIRE (Empathy Bridge)\n"
            f"4. THE EPIPHANY BRIDGE & THE NEW VEHICLE\n"
            f"5. CREATOR CREDIBILITY & ORIGIN STORY\n"
            f"6. SOCIAL PROOF & TESTIMONIALS\n"
            f"7. INTRODUCING THE SOLUTION ({product_name})\n"
            f"8. THE VALUE STACK & 5-7 HIGH-IMPACT BULLET POINTS\n"
            f"9. IRRESISTIBLE BONUSES\n"
            f"10. IRON-CLAD 100% MONEY-BACK GUARANTEE\n"
            f"11. URGENT CALL TO ACTION (CTA Buttons)\n"
            f"12. P.S. (POST SCRIPTUM) & CLOSING REMINDERS\n\n"
            f"TONE: Warm, authentic, empathetic, persuasive, and completely free of cheesy gimmicks."
        )
    else:
        return (
            f"Te a világ egyik legelismertebb elit szövegírója vagy, aki Russell Brunson és a Faceless Funnel Challenge közvetlen eladási stratégiájának mestere.{niche_clause}\n\n"
            f"Írj egy teljes, magával ragadó, rendkívül magas konverziójú ÉRTÉKESÍTÉSI LEVELET 100%-BAN TISZTA MAGYAR NYELVEN az alábbi adatok alapján:\n\n"
            f"📌 TERMÉK NEVE: {product_name}\n"
            f"🎯 CÉLKÖZÖNSÉG: {target_audience}\n"
            f"✨ FŐ TRANSZFORMÁCIÓ: {main_transformation}{pains}{veh}{bon}\n"
            f"🛡️ GARANCIA TÍPUSA: {guarantee_type}\n\n"
            f"SZIGORÚ NYELVI KÖVETELMÉNY: Kizárólag hibátlan, természetes magyar nyelven írj! Tilos idegen szavakat keverni.\n\n"
            f"A LEVÉLNEK PONTOSAN AZ ALÁBBI 12 LÉPÉSES PSZICHOLÓGIAI ÍVET KELL KÖVETNIE:\n"
            f"1. 🎣 THE BIG HOOK & PRE-HEADLINE (Figyelemfelkeltő felütés)\n"
            f"2. ⚡ SHOCKING STATEMENT (Bátor, meglepő állítás)\n"
            f"3. 💔 DEEP PAIN & DESIRE (Mély együttérzés és a vágyott cél)\n"
            f"4. 💡 THE EPIPHANY BRIDGE & NEW VEHICLE (A felismerés és az új módszer)\n"
            f"5. 🤝 ALKOTÓI BEMUTATKOZÁS (Hitelesség)\n"
            f"6. 🕊️ TÁRSADALMI BIZONYÍTÉK (Vélemények, tapasztalatok)\n"
            f"7. 🎁 A MEGOLDÁS HIVATALOS BEMUTATÁSA ({product_name})\n"
            f"8. 📋 VALUE STACK & BULLET PONTOK (5-7 db négyfázisú bullet)\n"
            f"9. 🌟 INGYENES AJÁNDÉK BÓNUSZOK\n"
            f"10. 🛡️ 100% KOCKÁZATMENTES GARANCIA\n"
            f"11. 🚀 SÜRGŐS CALL TO ACTION (CTA gombok)\n"
            f"12. ✍️ P.S. (POST SCRIPTUM) & ZÁRÓ GONDOLATOK\n\n"
            f"TÓNUS: Meleg, meggyőző, mélyen hiteles, tiszteletteljes és határozott!"
        )


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
    100% Free Google Sites (sites.google.com) Landing Page Master Prompt with strict language separation.
    """
    is_en = "angol" in language.lower() or "english" in language.lower()
    niche_ctx = f"\nNICHE CONTEXT:\n{get_niche_prompt_context(niche_name)}\n" if niche_name else ""

    if is_en:
        head = headline if headline.strip() else f"Find Daily Peace and Purpose with {product_name}"
        tag = tagline if tagline.strip() else f"A premium digital mindfulness framework crafted for {target_audience}."
        lm_desc = lead_magnet_desc if lead_magnet_desc.strip() else "Free 3-page printable sample workbook with instant download."
        feat = features if features.strip() else "30-day guided workbook, 4K printable coloring templates, and instant digital access."

        return (
            f"You are a world-class Conversion Rate Optimization (CRO) and Landing Page copywriter specialized in creating free Google Sites (sites.google.com) high-converting page structures.\n\n"
            f"Your task is to generate complete, ready-to-paste landing page copy in 100% PURE ENGLISH (US) covering these 5 sections:\n\n"
            f"1. 🌟 HERO SECTION (Announcement bar, Headline H1, Subheadline H2, Introduction, Primary CTA, Trust Badges)\n"
            f"2. 🎁 LEAD MAGNET SECTION (Free Sample Offer, 'What's Inside', Gumroad Free Download CTA Button)\n"
            f"3. 🛍️ FEATURED PRODUCTS (3-card showcase: Amazon KDP Physical, Etsy Wall Art, Gumroad Complete Master Bundle)\n"
            f"4. 🚀 CTA BUTTONS & ACTION LINKS TABLE (Amazon, Etsy, Gumroad URLs & 100% Guarantee Statement)\n"
            f"5. 🎨 VISUAL THEME GUIDE (Hex color palette, Google Fonts pairings, block layout guide)\n\n"
            f"CRITICAL LANGUAGE RULE: Output ONLY 100% fluent, natural English without any foreign words.\n\n"
            f"=== PROJECT DATA ===\n"
            f"- Product Name: {product_name}\n"
            f"- Target Audience: {target_audience}\n"
            f"- Main Headline: \"{head}\"\n"
            f"- Subheadline: \"{tag}\"\n"
            f"- Free Lead Magnet: {lm_desc}\n"
            f"- Key Deliverables: {feat}\n"
            f"- Offer Price: {offer_price}\n"
            f"- Visual Theme: {style_theme}\n"
            f"- Links: Amazon ({amazon_url}), Etsy ({etsy_url}), Gumroad ({gumroad_url})\n"
            f"{niche_ctx}"
        )
    else:
        head = headline if headline.strip() else f"Találd meg a napi békességet és inspirációt: {product_name}"
        tag = tagline if tagline.strip() else f"Prémium keresztény digitális alkotások {target_audience} számára."
        lm_desc = lead_magnet_desc if lead_magnet_desc.strip() else "3-oldalas ingyenes nyomtatható kifestő és mini áhítat mintacsomag azonnali letöltéssel."
        feat = features if features.strip() else "30 napos vezetett áhítat és napló, 4K felbontású nyomtatható lapok, azonnali digitális hozzáférés."

        return (
            f"Te egy világszínvonalú CRO és Landing Page szövegíró szakértő vagy a Google Sites (sites.google.com) keretrendszerhez.\n\n"
            f"Készítsd el a teljes, blokkonként közvetlenül átmásolható tartalmat 100%-BAN TISZTA MAGYAR NYELVEN az alábbi 5 fő blokkhoz:\n\n"
            f"1. 🌟 HERO SECTION (Bejelentő csík, Főcímsor, Alcím, Bevezető szöveg, Elsődleges CTA, Bizalmi elemek)\n"
            f"2. 🎁 LEAD MAGNET SECTION (Ingyenes csalitermék címe, 'Mit tartalmaz', Gumroad 0 Ft-os letöltés gomb)\n"
            f"3. 🛍️ FEATURED PRODUCTS (3 kiemelt kártya: Amazon KDP, Etsy Csomag, Gumroad Mestercsomag)\n"
            f"4. 🚀 CTA BUTTONS & ACTION LINKS (Gombtár és 100% garancia nyilatkozat)\n"
            f"5. 🎨 VISUAL THEME GUIDE (Hex színpaletta, Google Fonts betűtípusok, építési útmutató)\n\n"
            f"SZIGORÚ NYELVI KÖVETELMÉNY: Kizárólag hibátlan, természetes magyar nyelven írj! Tilos idegen kifejezéseket keverni.\n\n"
            f"=== TERMÉK ADATOK ===\n"
            f"- Termék Neve: {product_name}\n"
            f"- Célközönség: {target_audience}\n"
            f"- Fő Címsor: \"{head}\"\n"
            f"- Alcím: \"{tag}\"\n"
            f"- Ingyenes Csalitermék: {lm_desc}\n"
            f"- Főbb Tartalom: {feat}\n"
            f"- Ajánlat Ára: {offer_price}\n"
            f"- Vizuális Téma: {style_theme}\n"
            f"- Linkek: Amazon ({amazon_url}), Etsy ({etsy_url}), Gumroad ({gumroad_url})\n"
            f"{niche_ctx}"
        )


def build_polsia_landing_page_prompt(*args, **kwargs) -> str:
    """Alias for backwards compatibility."""
    return build_google_sites_landing_page_prompt(*args, **kwargs)


def build_email_funnel_3day_prompt(lead_magnet_name: str, paid_product_name: str, target_audience: str, discount_offer: str = "20% exkluzív kedvezmény", main_story: str = "", language: str = "magyar", niche_name: str = "") -> str:
    """
    3-Day Automated Email Funnel Generator Prompt with strict language separation.
    """
    is_en = "angol" in language.lower() or "english" in language.lower()
    niche_clause = f"\nNiche: {niche_name}" if niche_name else ""
    story_clause = f"\nOrigin story / Lesson: {main_story}" if main_story.strip() else ""

    if is_en:
        return (
            f"You are a world-class Email Marketing & Funnel Copywriting expert.{niche_clause}\n\n"
            f"Write a high-converting 3-DAY AUTOMATED EMAIL SEQUENCE in 100% PURE, NATURAL ENGLISH (US) for the following product:\n\n"
            f"🎁 FREE LEAD MAGNET: {lead_magnet_name}\n"
            f"💎 PAID CORE PRODUCT: {paid_product_name}\n"
            f"🎯 TARGET AUDIENCE: {target_audience}\n"
            f"🏷️ SPECIAL DISCOUNT OFFER: {discount_offer}{story_clause}\n\n"
            f"CRITICAL LANGUAGE RULE: Output strictly 100% natural English. Do NOT include any foreign words.\n\n"
            f"FOR EACH EMAIL (DAYS 1-3), PROVIDE:\n"
            f"- 2 A/B Subject Lines (1 Curiosity/Emotional + 1 Direct/Benefit)\n"
            f"- Preview Text (Max 90 chars)\n"
            f"- Complete Formatted Body Text (Salutation, paragraphs, bullet points, CTA links, P.S.)\n\n"
            f"THE 3-DAY STRUCTURE:\n"
            f"📧 DAY 1: GIFT DELIVERY + WARM WELCOME + QUICK WIN\n"
            f"📧 DAY 2: PURE VALUE & ORIGIN STORY (From Chaos to Clarity)\n"
            f"📧 DAY 3: THE COMPLETE SOLUTION + EXCLUSIVE DISCOUNT & URGENT CTA"
        )
    else:
        return (
            f"Te egy professzionális e-mail marketing és tölcsér-építő specialista vagy.{niche_clause}\n\n"
            f"Írj egy teljes 3 NAPOS AUTOMATA E-MAIL SZEKVENCIÁT 100%-BAN TISZTA MAGYAR NYELVEN az alábbi adatok alapján:\n\n"
            f"🎁 INGYENES CSALITERMÉK (LEAD MAGNET): {lead_magnet_name}\n"
            f"💎 FIZETŐS AJÁNLAT / TERMÉK: {paid_product_name}\n"
            f"🎯 CÉLKÖZÖNSÉG: {target_audience}\n"
            f"🏷️ EXKLUZÍV KEDVEZMÉNY: {discount_offer}{story_clause}\n\n"
            f"SZIGORÚ NYELVI KÖVETELMÉNY: Kizárólag hibátlan, természetes magyar nyelven írj! Tilos idegen szavakat keverni.\n\n"
            f"MINDEN EGYES E-MAILNÉL ADJ MEG:\n"
            f"- 2 db A/B Tesztelhető Tárgymezőt\n"
            f"- Előnézeti Szöveget (Preview Text)\n"
            f"- A teljes, formázott Levéltörzset (megszólítás, bekezdések, CTA linkek és P.S.)\n\n"
            f"A 3 NAP PONTOS STRUKTÚRÁJA:\n"
            f"📧 1. NAP: AZ AJÁNDÉK MEGFÉRKEZETT + GYORS SIKERÉLMÉNY & KÖSZÖNET\n"
            f"📧 2. NAP: ÉRTÉKADÁS ÉS SZEMÉLYES TÖRTÉNET\n"
            f"📧 3. NAP: A TELJES MEGOLDÁS + EXKLUZÍV KEDVEZMÉNY ÉS SÜRGŐSSÉG"
        )


def build_email_funnel_30day_prompt(product_name: str, target_audience: str, core_offer: str, lead_magnet: str = "Ingyenes Letölthető Minta / Munkafüzet", discount_info: str = "25% kedvezmény az ÜDVÖZÖLLEK kuponnal", language: str = "magyar", niche_name: str = "") -> str:
    """
    30-Day Complete Automated Email Marketing Funnel Master Prompt with strict language separation.
    """
    is_en = "angol" in language.lower() or "english" in language.lower()
    niche_clause = f"\nNiche: {niche_name}" if niche_name else ""

    if is_en:
        return (
            f"You are an elite Lifecycle Email Marketing strategist specialized in crafting 30-day automated customer journey sequences.{niche_clause}\n\n"
            f"Design and write a COMPLETE 30-DAY AUTOMATED EMAIL FUNNEL in 100% PURE, NATURAL ENGLISH (US) for this product:\n\n"
            f"📌 PRODUCT / CORE OFFER: {product_name}\n"
            f"🎯 TARGET AUDIENCE: {target_audience}\n"
            f"🎁 FREE LEAD MAGNET: {lead_magnet}\n"
            f"💎 CORE VALUE OFFER: {core_offer}\n"
            f"🏷️ SPECIAL DISCOUNT: {discount_info}\n\n"
            f"CRITICAL LANGUAGE RULE: Output strictly 100% natural English. Do NOT mix in any foreign words.\n\n"
            f"COVER ALL 5 PHASES (DAYS 1-30):\n"
            f"🔹 PHASE 1: WELCOME & INDOCTRINATION (Days 1-5)\n"
            f"🔹 PHASE 2: PURE VALUE & AUTHORITY (Days 6-12)\n"
            f"🔹 PHASE 3: CORE OFFER & VALUE STACK (Days 13-18)\n"
            f"🔹 PHASE 4: SOCIAL PROOF & OBJECTION CRUSHING (Days 19-24)\n"
            f"🔹 PHASE 5: URGENCY & FINAL CALL (Days 25-30)\n\n"
            f"FOR EACH DAY, PROVIDE:\n"
            f"- Subject Line\n"
            f"- Core Goal / Objective\n"
            f"- Full Email Body with Hook, Content, and CTA."
        )
    else:
        return (
            f"Te egy világklasszis e-mail marketing szakértő vagy, aki a 30 napos életút e-mail rendszerek mestere.{niche_clause}\n\n"
            f"Tervezz meg és írj meg egy TELJES 30 NAPOS AUTOMATA E-MAIL TÖLCSÉR STRUKTÚRÁT ÉS SZEKVENCIÁT 100%-BAN TISZTA MAGYAR NYELVEN az alábbi termékhez:\n\n"
            f"📌 TERMÉK / FŐ AJÁNLAT: {product_name}\n"
            f"🎯 CÉLKÖZÖNSÉG: {target_audience}\n"
            f"🎁 INGYENES CSALITERMÉK: {lead_magnet}\n"
            f"💎 FŐ AJÁNLAT LEÍRÁSA: {core_offer}\n"
            f"🏷️ KEDVEZMÉNY / AJÁNLAT: {discount_info}\n\n"
            f"SZIGORÚ NYELVI KÖVETELMÉNY: Kizárólag hibátlan, természetes magyar nyelven írj! Tilos idegen szavakat keverni.\n\n"
            f"A 30 NAPOS SZEKVENCIÁNAK AZ ALÁBBI 5 FÁZIST KELL LEFEDNIE:\n"
            f"🔹 1. FÁZIS: ÜDVÖZLÉS & BEVEZETÉS (1-5. NAP)\n"
            f"🔹 2. FÁZIS: TISZTA ÉRTÉKADÁS & HITELESSÉG (6-12. NAP)\n"
            f"🔹 3. FÁZIS: A FŐ AJÁNLAT & ÉRTÉKHALMOZÁS (13-18. NAP)\n"
            f"🔹 4. FÁZIS: BIZONYÍTÉKOK & KIFOGÁSKEZELÉS (19-24. NAP)\n"
            f"🔹 5. FÁZIS: SÜRGŐSSÉG & UTOLSÓ HÍVÁS (25-30. NAP)\n\n"
            f"MINDEN NAPHOZ ADJ MEG:\n"
            f"- Tárgymező javaslatot\n"
            f"- Cél / Fő üzenetet 2-3 mondatban\n"
            f"- Levélvázlatot lényegi bekezdésekkel és Call-to-Actionnel."
        )


def build_social_seo_calendar_30day_prompt(product_name: str, target_audience: str, main_topics: str = "", platforms: str = "Pinterest, Instagram, Blog", language: str = "magyar", niche_name: str = "") -> str:
    """
    30-Day Multi-Platform Social Media & SEO Content Calendar Master Prompt with strict language separation.
    """
    is_en = "angol" in language.lower() or "english" in language.lower()
    niche_clause = f"\nNiche: {niche_name}" if niche_name else ""
    topics = f"\nCore Topics / Pillars: {main_topics}" if main_topics.strip() else ""

    if is_en:
        return (
            f"You are a master Social Media & Organic Search Engine Optimization (SEO) Content Strategist.{niche_clause}\n\n"
            f"Create a structured, actionable 30-DAY SOCIAL MEDIA & SEO CONTENT CALENDAR in 100% PURE, NATURAL ENGLISH (US) for this product:\n\n"
            f"📌 PRODUCT: {product_name}\n"
            f"🎯 TARGET AUDIENCE: {target_audience}\n"
            f"📱 TARGET PLATFORMS: {platforms}{topics}\n\n"
            f"CRITICAL LANGUAGE RULE: Output strictly 100% natural English. Do NOT mix in any foreign words.\n\n"
            f"FOR EACH DAY (DAYS 1-30), PROVIDE:\n"
            f"1. 📌 PINTEREST PIN SEO (Click-magnet Title + 2-sentence SEO Description + 5 search tags)\n"
            f"2. 📸 INSTAGRAM / TIKTOK REELS POST (3-second Hook + 3 bullet takeaways + Clear CTA)\n"
            f"3. 📝 BLOG / NEWSLETTER MICRO-TOPIC (1-sentence SEO-optimized headline)."
        )
    else:
        return (
            f"Te egy mester Social Media & Organikus Keresőoptimalizálási (SEO & Content Strategy) szakértő vagy.{niche_clause}\n\n"
            f"Készíts egy strukturált, azonnal végrehajtható 30 NAPOS TARTALOMNAPTÁRAT ÉS SOCIAL SEO STRATÉGIÁT 100%-BAN TISZTA MAGYAR NYELVEN az alábbi termékhez:\n\n"
            f"📌 TERMÉK: {product_name}\n"
            f"🎯 CÉLKÖZÖNSÉG: {target_audience}\n"
            f"📱 CÉLPLATFORMOK: {platforms}{topics}\n\n"
            f"SZIGORÚ NYELVI KÖVETELMÉNY: Kizárólag hibátlan, természetes magyar nyelven írj! Tilos idegen szavakat keverni.\n\n"
            f"MINDEN NAPHOZ (1–30. NAP) ADJ MEG:\n"
            f"1. 📌 PINTEREST PIN SEO (Kattintásmágnes Cím + 2 mondatos SEO Leírás + 5 db címke)\n"
            f"2. 📸 INSTAGRAM / TIKTOK POSZT (3 mp-es Horog + Tartalom lényege + Call To Action)\n"
            f"3. 📝 BLOG / EMAIL MIKRO-TÉMA (1 mondatos keresőbarát cím)."
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
    book_title: str = "Coloring Book",
    theme: str = "",
    page_count: int = 30,
    target_audience: str = "children",
    style_name: str = "",
    image_model: str = "",
    trim_size: str = "8.5x11",
    aspect_ratio: str = "3:4",
    is_adult: bool = False,
    *args,
    **kwargs
) -> str:
    """
    Builds the Master Prompt for Gemini 3.7 Flash to generate the full book JSON manifest.
    Strict JSON output containing all scene details, KJV scripture references/texts, color suggestions,
    and optimized Imagen 3 / Nano Banana Pro visual prompts with exact aspect ratio and framing rules.
    """
    if is_adult or "adult" in target_audience.lower() or "felnőtt" in target_audience.lower():
        is_adult_mode = True
    else:
        is_adult_mode = False
    is_adult = is_adult_mode
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





