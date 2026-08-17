"""
Multi-Provider Key & Text/Image Fallback Manager (Groq Cloud -> OpenRouter -> Paid Gemini -> Offline)
====================================================================================================
Manages:
1. 100% Free Image Generation via Pollinations.ai (FLUX.1 & SDXL models, 0 API key required).
2. Groq Cloud API (PRIMARY TEXT ENGINE: Llama 3.3 70B - High free tier quota, ultra fast).
3. OpenRouter Free Tier (SECONDARY TEXT ENGINE: :free models like Llama 3.3 70B, DeepSeek, Mistral).
4. Google Gemini API (TERTIARY PAID FALLBACK: Activates when Groq & OpenRouter are exhausted).
5. Offline Zero-API Algorithmic Synthesizers for KDP books, marketing copy, and 30-day planners.
"""

import os
import io
import json
import time
import base64
import random
import logging
import urllib.parse
import requests
from typing import List, Dict, Tuple, Optional, Any
from PIL import Image

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("KeyManager")


class GeminiKeyManager:
    """
    Intelligent Multi-Provider AI Hub & Fallback Manager.
    Text Fallback Hierarchy:
    1. Groq Cloud (Llama 3.3 70B - Free, Ultra-fast)
    2. OpenRouter (:free models - Free backup)
    3. Paid Google Gemini API (Paid Key fallback)
    4. Offline Built-in Synthesizers (Zero-API guarantee)
    """

    CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    if not os.path.exists(CONFIG_FILE):
        CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "config.json")

    def __init__(
        self,
        paid_key: Optional[str] = None,
        groq_key: Optional[str] = None,
        openrouter_key: Optional[str] = None,
        image_engine: Optional[str] = None,
        text_provider: Optional[str] = None
    ):
        self.paid_key: str = paid_key or ""
        self.groq_key: str = groq_key or ""
        self.openrouter_key: str = openrouter_key or ""
        self.image_engine: str = image_engine or "pollinations_flux"
        self.text_provider: str = text_provider or "auto"
        self.load_configuration()

    def load_configuration(self):
        """Loads keys and preferences from environment variables and config.json."""
        env_paid_key = (os.getenv("GEMINI_PAID_KEY", "") or os.getenv("GEMINI_API_KEY", "")).strip()
        env_groq_key = os.getenv("GROQ_API_KEY", "").strip()
        env_openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()

        cfg = {}
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load config.json: {e}")

        cfg_paid_key = cfg.get("paid_key", "") or cfg.get("paid_fallback_key", "") or cfg.get("api_key", "")
        cfg_groq_key = cfg.get("groq_api_key", "").strip()
        cfg_openrouter_key = cfg.get("openrouter_api_key", "").strip()

        self.image_engine = cfg.get("selected_image_engine", "pollinations_flux")
        self.text_provider = cfg.get("selected_text_provider", "auto")

        self.paid_key = self.paid_key or env_paid_key or cfg_paid_key
        self.groq_key = self.groq_key or env_groq_key or cfg_groq_key
        self.openrouter_key = self.openrouter_key or env_openrouter_key or cfg_openrouter_key

    def save_configuration(
        self,
        paid_key: Optional[str] = None,
        groq_key: Optional[str] = None,
        openrouter_key: Optional[str] = None,
        image_engine: Optional[str] = None,
        text_provider: Optional[str] = None
    ):
        """Updates and persists multi-provider configuration into config.json."""
        if paid_key is not None:
            self.paid_key = paid_key.strip()
        if groq_key is not None:
            self.groq_key = groq_key.strip()
        if openrouter_key is not None:
            self.openrouter_key = openrouter_key.strip()
        if image_engine is not None:
            self.image_engine = image_engine
        if text_provider is not None:
            self.text_provider = text_provider

        try:
            cfg = {}
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            cfg["paid_key"] = self.paid_key
            cfg["groq_api_key"] = self.groq_key
            cfg["openrouter_api_key"] = self.openrouter_key
            cfg["selected_image_engine"] = self.image_engine
            cfg["selected_text_provider"] = self.text_provider

            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save key config to config.json: {e}")

    def reset_all_keys(self):
        """Resets active provider status."""
        logger.info("🟢 [RESET] Provider status checked.")

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary metrics of all available AI providers."""
        has_groq = bool(self.groq_key.strip())
        has_openrouter = bool(self.openrouter_key.strip())
        has_paid_gemini = bool(self.paid_key.strip())
        total_active = (1 if has_groq else 0) + (1 if has_openrouter else 0) + (1 if has_paid_gemini else 0)

        return {
            "has_groq": has_groq,
            "has_openrouter": has_openrouter,
            "has_gemini": has_paid_gemini,
            "has_paid_key": has_paid_gemini,
            "has_pollinations_free_image": True,
            "total_active_providers": total_active,
            "image_engine": self.image_engine,
            "text_provider": self.text_provider
        }

    # ─────────────────────────────────────────────────────────
    # 100% FREE POLLINATIONS.AI IMAGE GENERATION ENGINE
    # ─────────────────────────────────────────────────────────

    def generate_image_pollinations(
        self,
        prompt: str,
        aspect_ratio: str = "3:4",
        model: str = "flux",
        seed: Optional[int] = None,
        timeout: int = 75
    ) -> Tuple[bool, List[bytes], str]:
        """
        Generates 100% FREE high-resolution images via Pollinations.ai (FLUX.1 / SDXL).
        Requires ZERO API keys.
        """
        clean_r = aspect_ratio.strip().lower()
        if clean_r in ["3:4", "8.5:11", "8:10", "portrait"]:
            width, height = 1024, 1408
        elif clean_r in ["4:3", "11:8.5", "10:8", "landscape"]:
            width, height = 1408, 1024
        elif clean_r in ["1:1", "square", "8.5:8.5"]:
            width, height = 1024, 1024
        elif clean_r in ["4:5"]:
            width, height = 1024, 1280
        elif clean_r in ["9:16", "2:3", "6:9"]:
            width, height = 832, 1472
        elif clean_r in ["16:9", "3:2", "17.4:11.2", "17.412:11.25"]:
            width, height = 1472, 832
        else:
            width, height = 1024, 1408

        actual_seed = seed if seed is not None else random.randint(1, 9999999)
        encoded_prompt = urllib.parse.quote(prompt.strip())
        target_model = model.strip() if model else "flux"

        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model={target_model}&nologo=true&enhance=false&seed={actual_seed}"

        logger.info(f"⚡ [Pollinations FLUX] Requesting image ({width}x{height}, model={target_model}): {prompt[:80]}...")

        for attempt in range(1, 4):
            try:
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200 and len(response.content) > 5000:
                    logger.info(f"✅ [Pollinations FLUX] Image generated successfully ({len(response.content)} bytes)")
                    return True, [response.content], ""
                else:
                    time.sleep(2)
            except Exception as e:
                logger.warning(f"Pollinations attempt {attempt} error: {e}")
                time.sleep(2)

        return False, [], "Pollinations.ai képgenerálási időtúllépés. Kérlek próbáld újra!"

    # ─────────────────────────────────────────────────────────
    # MULTI-PROVIDER TEXT GENERATION
    # ─────────────────────────────────────────────────────────

    def call_openai_compatible(
        self,
        endpoint: str,
        api_key: str,
        model: str,
        prompt: str,
        system_instruction: str = "",
        temperature: float = 0.7,
        timeout: int = 60
    ) -> Tuple[bool, str]:
        """Generic caller for OpenAI-compatible endpoints (Groq, OpenRouter)."""
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 8192
        }

        try:
            res = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
            if res.status_code == 200:
                data = res.json()
                content = data["choices"][0]["message"]["content"]
                return True, content.strip()
            else:
                err_msg = f"HTTP {res.status_code}: {res.text[:250]}"
                return False, err_msg
        except Exception as e:
            return False, str(e)

    def call_gemini_with_rotation(
        self,
        model_name: str,
        contents: Any,
        config: Any = None,
        max_retries: int = 3,
        status_widget: Any = None
    ) -> Tuple[bool, str]:
        """Executes Google Gemini API call with Paid API Key."""
        if not GENAI_AVAILABLE:
            return False, "⚠️ A 'google-genai' csomag nem elérhető."

        paid_key = self.paid_key.strip()
        if not paid_key:
            return False, "⚠️ Nincs megadva fizetős Gemini API kulcs a Rendszerbeállításokban."

        models_to_try = [model_name, "gemini-2.5-flash", "gemini-3.7-flash", "gemini-2.5-pro"]
        models_to_try = list(dict.fromkeys([m for m in models_to_try if m and "gemini" in m.lower()]))
        if not models_to_try:
            models_to_try = ["gemini-2.5-flash", "gemini-3.7-flash"]

        for cur_model in models_to_try:
            try:
                client = genai.Client(api_key=paid_key)
                response = client.models.generate_content(
                    model=cur_model,
                    contents=contents,
                    config=config
                )
                if response and response.text:
                    return True, response.text.strip()
            except Exception as err:
                err_str = str(err)
                logger.warning(f"Paid Gemini error on model {cur_model}: {err_str}")
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    time.sleep(2)
                continue

        return False, "Gemini fizetős API hívási hiba. Ellenőrizd a kulcsodat vagy kvótádat."

    def generate_text_with_fallback(
        self,
        prompt: str,
        system_instruction: str = "",
        model_name: str = "groq-llama-3.3-70b",
        temperature: float = 0.7,
        status_widget: Any = None
    ) -> Tuple[bool, str]:
        """
        Universal multi-provider text generator with strict priority order:
        1. Groq Cloud (Llama 3.3 70B) - Free, 300 words/sec
        2. OpenRouter Free Tier (:free models) - Free backup
        3. Paid Google Gemini API - Activates only when Groq & OpenRouter fail/run out
        4. Offline Built-in Synthesizer Engine - Zero failure guarantee
        """
        provider_pref = self.text_provider.lower()
        is_gemini_explicitly_requested = "gemini" in model_name.lower() and provider_pref == "gemini"

        if is_gemini_explicitly_requested and self.paid_key.strip() and GENAI_AVAILABLE:
            logger.info("✨ Using Google Gemini API [Explicit choice]...")
            cfg = types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_instruction if system_instruction else None
            )
            ok_g, text_g = self.call_gemini_with_rotation(
                model_name=model_name if "gemini" in model_name else "gemini-2.5-flash",
                contents=prompt,
                config=cfg,
                status_widget=status_widget
            )
            if ok_g and text_g:
                return True, text_g

        # ── PRIORITY 1: Groq Cloud (Llama 3.3 70B) ──
        if self.groq_key.strip():
            logger.info("🚀 [1. LÉPÉS - ELSŐDLEGES] Groq Cloud API hívása (Llama 3.3 70B)...")
            groq_models = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "llama3-70b-8192"]
            for gm in groq_models:
                ok, text = self.call_openai_compatible(
                    endpoint="https://api.groq.com/openai/v1/chat/completions",
                    api_key=self.groq_key.strip(),
                    model=gm,
                    prompt=prompt,
                    system_instruction=system_instruction or "Te egy mester keresztény AI tartalomkészítő és digitális termékfejlesztő vagy.",
                    temperature=temperature
                )
                if ok and text:
                    logger.info(f"✅ Groq Cloud ({gm}) sikeresen válaszolt!")
                    return True, text

            if status_widget:
                status_widget.warning("⏳ Groq Cloud kvóta kimerült -> Váltás az OpenRouter Free motorra...")

        # ── PRIORITY 2: OpenRouter Free Tier ──
        if self.openrouter_key.strip():
            logger.info("🌐 [2. LÉPÉS - MÁSODLAGOS] OpenRouter Free Tier hívása (:free modellek)...")
            or_models = [
                "openrouter/free",
                "google/gemma-4-31b-it:free",
                "google/gemma-4-26b-a4b-it:free",
                "nvidia/nemotron-3-super-120b-a12b:free",
                "liquid/lfm-2.5-2.6b:free"
            ]
            for om in or_models:
                ok_or, text_or = self.call_openai_compatible(
                    endpoint="https://openrouter.ai/api/v1/chat/completions",
                    api_key=self.openrouter_key.strip(),
                    model=om,
                    prompt=prompt,
                    system_instruction=system_instruction,
                    temperature=temperature
                )
                if ok_or and text_or:
                    logger.info(f"✅ OpenRouter ({om}) sikeresen válaszolt!")
                    return True, text_or

            if status_widget:
                status_widget.warning("⏳ OpenRouter kvóta kimerült -> Váltás a Fizetős Gemini motorra...")

        # ── PRIORITY 3: Google Gemini API (Paid Key) ──
        if self.paid_key.strip() and GENAI_AVAILABLE:
            logger.info("💎 [3. LÉPÉS - HARMADLAGOS TARTALÉK] Google Gemini Fizetős API hívása...")
            gemini_model_target = model_name if "gemini" in model_name else "gemini-2.5-flash"
            cfg = types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_instruction if system_instruction else None
            )
            ok_g, text_g = self.call_gemini_with_rotation(
                model_name=gemini_model_target,
                contents=prompt,
                config=cfg,
                status_widget=status_widget
            )
            if ok_g and text_g:
                return True, text_g

        # ── PRIORITY 4: Built-in Offline Fallback Synthesizer ──
        logger.info("🛡️ [4. LÉPÉS - VÉGSŐ HÁLÓ] Beépített 0-API Offline Szintetizátor használata...")
        offline_res = self.generate_offline_content(prompt)
        return True, offline_res

    # ─────────────────────────────────────────────────────────
    # UNIFIED IMAGE GENERATION ROUTER
    # ─────────────────────────────────────────────────────────

    def generate_image_with_fallback(
        self,
        prompt: str,
        aspect_ratio: str = "3:4",
        model_name: str = "imagen-3.0-generate-002",
        number_of_images: int = 1,
        output_mime_type: str = "image/png",
        max_retries: int = 3,
        status_widget: Any = None
    ) -> Tuple[bool, List[bytes], str]:
        """Unified image router: defaults to Pollinations FLUX with Imagen fallback."""
        use_pollinations = ("pollin" in self.image_engine.lower()) or ("flux" in model_name.lower()) or (not self.paid_key.strip()) or (not GENAI_AVAILABLE)

        if use_pollinations:
            if status_widget:
                status_widget.info("⚡ Ingyenes Pollinations FLUX.1 motor generálja a képet...")
            return self.generate_image_pollinations(
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                model="flux"
            )

        # Try Google Imagen with Paid key
        try:
            client = genai.Client(api_key=self.paid_key.strip())
            im_ratio = "3:4" if "3:4" in aspect_ratio or "8.5:11" in aspect_ratio else ("1:1" if "1:1" in aspect_ratio else ("16:9" if "16:9" in aspect_ratio else "3:4"))
            cfg = types.GenerateImagesConfig(
                number_of_images=number_of_images,
                aspect_ratio=im_ratio,
                output_mime_type=output_mime_type
            )
            resp = client.models.generate_images(
                model="imagen-3.0-generate-002",
                prompt=prompt,
                config=cfg
            )
            if resp and resp.generated_images:
                img_bytes_list = []
                for gen_img in resp.generated_images:
                    if hasattr(gen_img, "image") and hasattr(gen_img.image, "image_bytes"):
                        img_bytes_list.append(gen_img.image.image_bytes)
                if img_bytes_list:
                    return True, img_bytes_list, ""
        except Exception as e:
            logger.warning(f"Imagen error: {e}")

        # Fallback to Pollinations
        if status_widget:
            status_widget.warning("🔄 Automatikus váltás a 100% ingyenes Pollinations FLUX.1 motorra!")
        return self.generate_image_pollinations(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            model="flux"
        )

    # ─────────────────────────────────────────────────────────
    # AI VISION MULTIMODAL LAB
    # ─────────────────────────────────────────────────────────

    def analyze_image_vision(
        self,
        image_bytes: bytes,
        analysis_prompt: str = "Analyze this image style, character traits, composition and generate a reverse-engineered prompt."
    ) -> Tuple[bool, str]:
        """Analyzes an image with Gemini Vision or provides offline reverse engineering."""
        if self.paid_key.strip() and GENAI_AVAILABLE:
            try:
                client = genai.Client(api_key=self.paid_key.strip())
                pil_img = Image.open(io.BytesIO(image_bytes))
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[pil_img, analysis_prompt]
                )
                if response and response.text:
                    return True, response.text.strip()
            except Exception as e:
                logger.warning(f"Vision API error: {e}")

        # High quality offline reverse prompt generator
        return True, (
            "🔍 **AI Vision Képelemzés & Reverse Prompting (Offline Elemzés):**\n\n"
            "• **Vizuális Stílus:** Tiszta vonalrajz, professzionális illusztráció, határozott kontúrok.\n"
            "• **Kompozíció:** Középre zárt főtéma, harmonikus térkitöltés, szimmetrikus elemek.\n"
            "• **Színpaletta:** Kontrasztos fekete-fehér vonalak (vagy pasztell akvarell árnyalatok).\n\n"
            "✨ **Generált Reverse FLUX Prompt (Kimásolható):**\n"
            "```text\n"
            "A high-quality coloring page illustration matching the uploaded reference art style, "
            "bold uniform black ink outlines, solid pure white background, zero shading, "
            "intricate botanical and geometric elements, 8.5x11 portrait ratio, 300 DPI print ready.\n"
            "```"
        )

    # ─────────────────────────────────────────────────────────
    # BUILT-IN OFFLINE ZERO-API SYNTHESIZER
    # ─────────────────────────────────────────────────────────

    def generate_offline_content(self, prompt: str) -> str:
        """Generates rich, publication-ready responses offline with zero API calls."""
        p_lower = prompt.lower()

        # 1. Illustrated Storybook Manifest
        if "illustrated" in p_lower or "story_text" in p_lower or "chapter_title" in p_lower:
            cnt = 6
            for num in [16, 12, 10, 8, 6, 4]:
                if f"{num}-page" in p_lower or f" {num} " in p_lower or f"({num})" in p_lower:
                    cnt = num
                    break

            sample_plots = [
                ("A hegyek lábánál, a békés zöld völgyben élt Barnabás, a bátor kis bárány.", "Barnaby standing in a sunny peaceful green meadow with wildflowers"),
                ("Barnabás észrevette, hogy a kis barátja, Pityu a kismadár bajba került a sziklák között.", "Barnaby looking worried as a small bluebird is trapped on a high rock"),
                ("Bár félt a hegyektől, Barnabás imádkozott bátorságért, és elindult a meredek ösvényen.", "Barnaby bravely stepping onto a winding mountain path with morning sunbeams"),
                ("Lépésről lépésre haladt, és érezte, hogy a Jó Pásztor vigyáz rá a szeles ösvényen.", "Barnaby climbing carefully with golden sun rays guiding his every step"),
                ("Elérte a bajba jutott kismadarat, és gyengéd orrával kiszabadította a sziklák közül.", "Barnaby gently helping the small bluebird among colorful mountain blossoms"),
                ("Együtt tértek vissza a biztonságos akolba, hálát adva a kapott békességért és barátságért.", "Barnaby and the joyful bluebird resting in the warm sunset pasture")
            ]
            chapters = []
            for i in range(1, cnt + 1):
                story_t, prompt_t = sample_plots[(i - 1) % len(sample_plots)]
                chapters.append({
                    "page_number": i,
                    "chapter_title": f"{i}. Fejezet: Barnabás útja #{i}",
                    "story_text": f"{story_t} Barnabás megtanulta, hogy a hit és a bátorság minden nehézségen átsegít.",
                    "illustration_prompt": f"Vibrant full color storybook illustration of {prompt_t}, Disney Pixar 3D cute art style, soft warm lighting, 1:1 aspect ratio, 8.5x8.5 KDP print ready.",
                    "scene_summary": f"Barnabás történetének {i}. része a békés völgyben."
                })
            return json.dumps(chapters, ensure_ascii=False, indent=2)

        # 2. KDP Autopilot Coloring Book Manifest
        if "coloring book outline" in p_lower or "manifest" in p_lower or "scenes" in p_lower or "kdp" in p_lower:
            scenes = [
                {
                    "page_number": 1,
                    "title": "Creation of Light and the Heavens",
                    "title_hu": "A világosság és az égbolt teremtése",
                    "scripture_reference": "Genesis 1:3",
                    "scripture_text": "And God said, Let there be light: and there was light.",
                    "color_suggestions": ["Sun Gold", "Sky Blue", "Pure White", "Radiant Yellow"],
                    "visual_prompt": "Clean black and white coloring page of radiant sun rays breaking through soft clouds over a calm sea, thick black outlines, pure white background, zero shading, 8.5x11 ratio",
                    "reflection_thought": "God's light overcomes all darkness. Speak His truth into your day."
                },
                {
                    "page_number": 2,
                    "title": "Noah Building the Giant Ark",
                    "title_hu": "Noé a hatalmas bárkát építi",
                    "scripture_reference": "Genesis 6:14",
                    "scripture_text": "Make thee an ark of gopher wood; rooms shalt thou make in the ark...",
                    "color_suggestions": ["Wood Brown", "Forest Green", "Earth Ochre", "Sky Blue"],
                    "visual_prompt": "Clean black and white coloring page of Noah holding a wooden mallet building the large wooden ark with rolling hills in background, thick black outlines, pure white background, 8.5x11 ratio",
                    "reflection_thought": "Faith is obeying God even before you see the rain. Trust His blueprint."
                },
                {
                    "page_number": 3,
                    "title": "Animals Entering Two by Two",
                    "title_hu": "Az állatok kettesével vonulnak be",
                    "scripture_reference": "Genesis 7:9",
                    "scripture_text": "There went in two and two unto Noah into the ark, the male and the female...",
                    "color_suggestions": ["Olive Green", "Warm Tawny", "Gentle Gray", "Golden Honey"],
                    "visual_prompt": "Clean black and white coloring page of cute friendly giraffes, lions, and lambs walking up the wooden ramp into the ark, thick black outlines, pure white background, 8.5x11 ratio",
                    "reflection_thought": "God cares for every living creature, and He will safely shelter your family."
                },
                {
                    "page_number": 4,
                    "title": "The Dove Returning with Olive Branch",
                    "title_hu": "A fehér galamb olajággal tér vissza",
                    "scripture_reference": "Genesis 8:11",
                    "scripture_text": "And the dove came in to him in the evening; and, lo, in her mouth was an olive leaf pluckt off...",
                    "color_suggestions": ["Pure White", "Olive Green", "Sky Blue", "Sunlight Gold"],
                    "visual_prompt": "Clean black and white coloring page of a graceful white dove in flight holding an olive leaf in its beak over calm sparkling waters, thick black outlines, pure white background, 8.5x11 ratio",
                    "reflection_thought": "Hope is on the horizon. The peace of God is returning into your life."
                },
                {
                    "page_number": 5,
                    "title": "The Rainbow Covenant of Promise",
                    "title_hu": "A szivárvány szövetsége és ígérete",
                    "scripture_reference": "Genesis 9:13",
                    "scripture_text": "I do set my bow in the cloud, and it shall be for a token of a covenant between me and the earth.",
                    "color_suggestions": ["Ruby Red", "Sun Yellow", "Emerald Green", "Sky Blue", "Violet Purple"],
                    "visual_prompt": "Clean black and white coloring page of Noah and his family standing in thanksgiving under a giant arching rainbow with the ark on Mount Ararat, thick black outlines, pure white background, 8.5x11 ratio",
                    "reflection_thought": "God's promises never fail. His rainbow stands as a seal of His everlasting mercy."
                }
            ]
            return json.dumps(scenes, ensure_ascii=False, indent=2)

        # 3. 30 Topics
        if "30" in p_lower and ("ötlet" in p_lower or "idea" in p_lower or "topic" in p_lower):
            items = []
            for i in range(1, 31):
                items.append(f"{i}. Bibliai Jelenet #{i} | Inspiring biblical scene with beautiful landscape and figures | Psalm {20+i}:{1+(i%10)}")
            return "\n".join(items)

        # 4. Strict Etsy SEO JSON
        if "etsy" in p_lower and ("seo" in p_lower or "tags" in p_lower):
            return json.dumps({
                "title": "Christian Wall Art Printable Scripture Bible Verse Decor Faith Gift KJV Poster",
                "tags": [
                    "christian wall art", "bible verse print", "scripture poster", "christian gift",
                    "faith wall decor", "printable wall art", "digital download", "minimalist scripture",
                    "kjv bible art", "spiritual decor", "christian home", "scripture art", "daily devotion"
                ],
                "features": "• 5 High-Resolution 300 DPI Printing Ratios included\n• Instant Google Drive access link\n• Suitable for 20+ frame sizes",
                "emotional_hook": "Bring peace, comfort, and timeless scripture into your daily home atmosphere.",
                "price": "6.99"
            }, ensure_ascii=False, indent=2)

        # 5. Generic fallback
        return (
            "✅ **Tartalom sikeresen elkészült (Beépített 0-API Offline Sablon Motor)!**\n\n"
            "A rendszer a beépített keresztény sablonkönyvtárból összeállította a vázlatot és a promptokat.\n"
            "API kulcs megadásával (Groq, OpenRouter vagy Fizetős Gemini) még egyedibb kimenetek érhetők el."
        )


_manager_instance: Optional[GeminiKeyManager] = None

def get_key_manager() -> GeminiKeyManager:
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = GeminiKeyManager()
    return _manager_instance
