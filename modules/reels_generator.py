"""
modules/reels_generator.py - Faceless Reels Batch Generator & FLUX.1 B-Roll Creator
Generates 10 viral 5-7s Reels scripts, ManyChat CTAs, Instagram captions,
and automated 9:16 vertical FLUX.1 B-roll image assets for CapCut.
"""

import os
import io
import json
import re
import time
import requests
from typing import List, Dict, Any, Tuple, Optional

try:
    from key_manager import get_key_manager, generate_image_with_fallback
except ImportError:
    try:
        from app.core.key_manager import get_key_manager, generate_image_with_fallback
    except ImportError:
        get_key_manager = None
        generate_image_with_fallback = None


def load_reels_hooks_data() -> Dict[str, Any]:
    """Loads default hooks and CTA keywords from data/reels_hooks.json."""
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "reels_hooks.json")
    if os.path.exists(data_path):
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def generate_offline_reels_batch(topic: str, cta_keyword: str, count: int = 10) -> List[Dict[str, Any]]:
    """Generates 10 pre-engineered, high-converting Christian Reels scripts when offline."""
    hooks_data = load_reels_hooks_data()
    sample_hooks = hooks_data.get("christian_viral_hooks", [
        "Ha ma reggel aggódva ébredtél, ezt az 1 bibliai mondatot hallanod kell...",
        "A legnagyobb hiba, amit keresztényként a stresszes napokon elkövetünk...",
        "3 rejtett bibliai ígéret, ami azonnal elcsendesíti a zakatoló elmédet...",
        "Miért nem működtek az eddigi reggeli csendességeid? (És mi a valódi megoldás)",
        "Hogyan találd meg a belső békességet napi 10 percben, még ha tele is van a fejed tennivalókkal...",
        "Ezt az 1 igehelyet olvasd el, amikor úgy érzed, minden összeomlik körülötted...",
        "Ne kezdd el a napodat anélkül, hogy ezt az egyszerű hálaadó imát elmondanád...",
        "A titok, amitől a napi bibliaolvasás teher helyett a napod legbékésebb perceivé válik...",
        "Ha úgy érzed, Isten most csendben van: nézd meg ezt a 3 jelet...",
        "3 dolog, amit azonnal engedj el ma este a békés alvásért..."
    ])
    
    broll_templates = hooks_data.get("broll_image_prompt_templates", [
        "Aesthetic 9:16 vertical cinematography, peaceful morning sunlight streaming through a window onto an open rustic Bible on a wooden table, warm gentle coffee steam, delicate white flowers, soft bokeh, cozy and serene atmosphere, hyper-realistic 8k --ar 9:16",
        "Cinematic vertical 9:16 composition, an aesthetic cozy desk with an open prayer journal, minimalist gold pen, glowing beeswax candle, soft warm golden hour light, peaceful Christian aesthetic, highly detailed, photorealistic 8k --ar 9:16",
        "Aesthetic vertical 9:16 photo, serene hands holding an open vintage Bible with soft sun flare, gentle mountain landscape in soft focus background, tranquil, hopeful, divine peace, Kodak Portra aesthetic, 8k --ar 9:16",
        "Minimalist Scandinavian Christian wall art aesthetic, 9:16 vertical framing, warm neutral tones, beige linen background, subtle olive branch and golden cross motif, elegant typography space --ar 9:16",
        "Cinematic 9:16 vertical view of a quiet forest path at dawn with golden sunbeams breaking through the trees, symbolizing guidance and spiritual journey, serene, peaceful, photorealistic --ar 9:16"
    ])

    results = []
    for i in range(count):
        hook = sample_hooks[i % len(sample_hooks)]
        broll = broll_templates[i % len(broll_templates)]
        results.append({
            "id": i + 1,
            "title": f"Reels #{i+1} · {topic[:25]}",
            "hook_text": hook,
            "body_text": f"Nem a körülményeiden kell változtatnod, hanem az első 10 perced fókuszán. A(z) {topic} pontosan ebben ad napi vezetett struktúrát.",
            "cta_text": f"Kommenteld a(z) '{cta_keyword}' szót ide alulra, és azonnal elküldöm a privát letöltési linket DM-ben!",
            "caption_text": f"""🌿 {hook}

Sokan azt hiszik, hogy a belső békességhez órákig tartó meditáció vagy tökéletes élethelyzet kell. A valóság az, hogy napi 10 fókuszált, hálával teli perc mindent megváltoztat.

✨ Készítettünk egy 30 napos vezetett digitális útmutatót ({topic}), amivel könnyedén elengedheted a szorongást.

👉 Kommenteld a(z) "{cta_keyword}" szót kommentben, és privát üzenetben küldöm az azonnali hozzáférést!

#kereszteny #bekesseg #hit #ima #napiige #csendesseg #lelkielet #audhd #fokusz #digitalistermek""",
            "image_prompt": broll
        })
    return results


def build_reels_prompt(topic: str, cta_keyword: str, target_audience: str = "", count: int = 10, language: str = "Magyar") -> str:
    """Creates an AI prompt for generating 10 viral 5-7s Reels scripts with FLUX.1 prompts."""
    aud_text = f"Célközönség: {target_audience}\n" if target_audience else ""
    return f"""
Te egy virális közösségi média és Faceless Reels marketing szakértő vagy (ManyChat automatizációval).
Készíts {count} darab virális, arc nélküli (faceless), 5-7 másodperces Instagram/TikTok Reels forgatókönyvet a következő digitális keresztény termékhez:

- Termék / Téma: {topic}
{aud_text}- ManyChat CTA Kulcsszó: "{cta_keyword}"
- Nyelv: {language}

Minden egyes forgatókönyvnek a következő elemeket kell tartalmaznia SZIGORÚAN érvényes JSON listaként:
[
  {{
    "id": 1,
    "title": "Rövid téma cím",
    "hook_text": "A videó első 3 másodpercének sokkoló / kíváncsiságkeltő felirata",
    "body_text": "1 mondatos mély felismerés / bibliai megoldás",
    "cta_text": "Kommenteld a(z) '{cta_keyword}' szót...",
    "caption_text": "Teljes Instagram posztszöveg releváns keresztény hashtagekkel és CTA-val",
    "image_prompt": "Cinematic 9:16 vertical photorealistic prompt for peaceful aesthetic Christian B-roll background on FLUX.1 --ar 9:16"
  }},
  ...
]
Csak a tiszta JSON listát add vissza!
"""


def generate_faceless_reels_batch(
    topic: str,
    cta_keyword: str,
    target_audience: str = "",
    count: int = 10,
    language: str = "Magyar"
) -> List[Dict[str, Any]]:
    """
    Main entry point for Reels batch generation.
    Uses multi-provider AI fallback (Groq -> OpenRouter -> Gemini -> Offline).
    """
    prompt = build_reels_prompt(topic, cta_keyword, target_audience, count, language)

    if get_key_manager:
        km = get_key_manager()
        ok, res = km.generate_text_with_fallback(
            prompt=prompt,
            system_instruction="Te egy professzionális Instagram Reels és ManyChat marketing stratéga vagy. Válaszolj szigorúan érvényes JSON listaként."
        )
        if ok and res.strip():
            cleaned = res.strip()
            if "```json" in cleaned:
                cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```", 1)[1].split("```", 1)[0].strip()

            try:
                data = json.loads(cleaned)
                if isinstance(data, list) and len(data) > 0 and "hook_text" in data[0]:
                    return data
            except Exception:
                pass

            try:
                m = re.search(r'(\[[\s\S]*\])', cleaned)
                if m:
                    data = json.loads(m.group(1))
                    if isinstance(data, list) and len(data) > 0:
                        return data
            except Exception:
                pass

    return generate_offline_reels_batch(topic, cta_keyword, count)


def generate_reels_broll_image(prompt: str, seed: Optional[int] = None) -> Tuple[bool, Optional[bytes], str]:
    """
    Generates a single 9:16 vertical B-roll image using FLUX.1 or fallback engine.
    """
    # Force 9:16 vertical aspect ratio in prompt
    clean_p = prompt.strip()
    if "--ar 9:16" not in clean_p and "9:16" not in clean_p:
        clean_p += " --ar 9:16 vertical composition"

    if generate_image_with_fallback:
        ok, img, msg = generate_image_with_fallback(
            prompt=clean_p,
            width=720,
            height=1280,
            seed=seed or int(time.time()) % 100000
        )
        if ok and img:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return True, buf.getvalue(), "Kép sikeresen legenerálva!"
        return False, None, msg

    # Direct Pollinations FLUX.1 fallback
    try:
        encoded_prompt = requests.utils.quote(clean_p)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1280&nologo=true&model=flux"
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            return True, resp.content, "Pollinations FLUX.1 kép sikeresen letöltve!"
        return False, None, f"HTTP Hiba: {resp.status_code}"
    except Exception as e:
        return False, None, str(e)
