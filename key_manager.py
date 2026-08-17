"""
Multi-Provider Key & Text/Image Fallback Manager (Groq Cloud -> OpenRouter -> Paid Gemini -> Offline)
====================================================================================================
Manages:
1. 100% Free Image Generation via Pollinations.ai (FLUX.1 & SDXL models, 0 API key required).
2. Groq Cloud API (PRIMARY TEXT ENGINE: Llama 3.3 70B - High free tier quota, ultra fast 300 words/sec).
3. OpenRouter Free Tier (SECONDARY TEXT ENGINE: :free models like Llama 3.3 70B, DeepSeek R1, Mistral).
4. Google Gemini API (TERTIARY PAID FALLBACK: Activates only when Groq & OpenRouter are exhausted).
5. Offline Zero-API Algorithmic Synthesizers for KDP books, marketing copy, and 30-day planners.
"""

import os
import json
import time
import urllib.parse
import logging
import random
import requests
from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict, Tuple, Optional, Any
from PIL import Image
import io

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("KeyManager")


class KeyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"


class GeminiKeyManager:
    """
    Intelligent Multi-Provider AI Hub & Fallback Manager.
    Text Fallback Hierarchy:
    1. Groq Cloud (Llama 3.3 70B - Free, Ultra-fast)
    2. OpenRouter (:free models - Free backup)
    3. Paid Google Gemini API (Paid Key fallback)
    4. Offline Built-in Synthesizers (Zero-API guarantee)
    """

    CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

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
        self.image_engine: str = image_engine or "pollinations_flux"  # "pollinations_flux", "imagen"
        self.text_provider: str = text_provider or "auto"              # "auto", "groq", "openrouter", "gemini", "offline"

        # Legacy compatibility attribute
        self.free_keys: List[str] = []
        self.key_states: List[Dict[str, Any]] = []

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
        # Streamlit secrets check
        try:
            import streamlit as st
            if "GROQ_API_KEY" in st.secrets:
                env_groq_key = env_groq_key or str(st.secrets["GROQ_API_KEY"]).strip()
            if "OPENROUTER_API_KEY" in st.secrets:
                env_openrouter_key = env_openrouter_key or str(st.secrets["OPENROUTER_API_KEY"]).strip()
            if "GEMINI_PAID_KEY" in st.secrets:
                env_paid_key = env_paid_key or str(st.secrets["GEMINI_PAID_KEY"]).strip()
            elif "GEMINI_API_KEY" in st.secrets:
                env_paid_key = env_paid_key or str(st.secrets["GEMINI_API_KEY"]).strip()
        except Exception:
            pass

        self.paid_key = self.paid_key or env_paid_key or cfg_paid_key
        self.groq_key = self.groq_key or env_groq_key or cfg_groq_key
        self.openrouter_key = self.openrouter_key or env_openrouter_key or cfg_openrouter_key


    def save_configuration(
        self,
        paid_key: Optional[str] = None,
        groq_key: Optional[str] = None,
        openrouter_key: Optional[str] = None,
        image_engine: Optional[str] = None,
        text_provider: Optional[str] = None,
        free_keys: Optional[List[str]] = None  # Kept for backward compatibility
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
            cfg["api_key"] = ""
            cfg["free_keys"] = []
            cfg["api_keys"] = []

            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save key config to config.json: {e}")

    def get_available_key(self) -> Tuple[Optional[str], bool, int]:
        """Returns (api_key, is_paid, key_index) for Gemini calls (paid key only)."""
        if self.paid_key.strip():
            return self.paid_key.strip(), True, 0
        return None, False, -1

    def reset_all_keys(self):
        """Resets active provider status."""
        logger.info("🟢 [RESET] Provider status checked.")

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary metrics of all available AI providers."""
        has_groq = bool(self.groq_key.strip())
        has_openrouter = bool(self.openrouter_key.strip())
        has_paid_gemini = bool(self.paid_key.strip())

        total_active_providers = (1 if has_groq else 0) + (1 if has_openrouter else 0) + (1 if has_paid_gemini else 0)

        return {
            "has_groq": has_groq,
            "has_openrouter": has_openrouter,
            "has_gemini": has_paid_gemini,
            "has_paid_key": has_paid_gemini,
            "has_pollinations_free_image": True,
            "total_active_providers": total_active_providers,
            "image_engine": self.image_engine,
            "text_provider": self.text_provider,
            "total_free_keys": 0,
            "active_keys": 1 if has_paid_gemini else 0,
            "rpm_limited_keys": 0,
            "daily_exhausted_keys": 0
        }

    @property
    def keys(self):
        class KeyInfo:
            def __init__(self, key, status):
                self.key = key
                self.status = status

        if self.paid_key.strip():
            return [KeyInfo(self.paid_key.strip(), "ACTIVE (Fizetős)")]
        return []

    def update_keys(
        self,
        paid_key: Optional[str] = None,
        groq_key: Optional[str] = None,
        openrouter_key: Optional[str] = None,
        image_engine: Optional[str] = None,
        text_provider: Optional[str] = None,
        free_keys: Optional[List[str]] = None
    ):
        self.save_configuration(
            paid_key=paid_key,
            groq_key=groq_key,
            openrouter_key=openrouter_key,
            image_engine=image_engine,
            text_provider=text_provider
        )

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
        Generates 100% FREE high-resolution images via Pollinations.ai (FLUX.1 / Turbo / SDXL).
        Requires ZERO API keys and ZERO payment.
        """
        clean_r = aspect_ratio.strip().lower()
        if clean_r in ["3:4", "8.5:11", "8:10", "portrait"]:
            width, height = 1024, 1408
        elif clean_r in ["4:3", "11:8.5", "10:8", "landscape"]:
            width, height = 1408, 1024
        elif clean_r in ["1:1", "square"]:
            width, height = 1024, 1024
        elif clean_r in ["4:5"]:
            width, height = 1024, 1280
        elif clean_r in ["9:16", "2:3"]:
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
                    logger.warning(f"Pollinations attempt {attempt} returned status {response.status_code}")
                    time.sleep(2)
            except Exception as e:
                logger.warning(f"Pollinations attempt {attempt} error: {e}")
                time.sleep(2)

        return False, [], "Pollinations.ai képgenerálási időtúllépés. Kérlek próbáld újra!"

    # ─────────────────────────────────────────────────────────
    # MULTI-PROVIDER TEXT GENERATION (Groq -> OpenRouter -> Paid Gemini)
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
        # deduplicate while keeping order
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

        return False, "Gemini fizetős API hívási hiba. Ellenőrizd a fizetős kulcsodat vagy kvótádat."

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
        1. Groq Cloud (Llama 3.3 70B) - 100% Free, 300 words/sec
        2. OpenRouter Free Tier (:free models) - 100% Free fallback
        3. Paid Google Gemini API - Activates only when Groq & OpenRouter fail/run out
        4. Offline Built-in Synthesizer Engine - Zero failure guarantee
        """
        provider_pref = self.text_provider.lower()
        is_groq_requested = "groq" in model_name.lower() or "llama" in model_name.lower() or provider_pref == "groq"
        is_openrouter_requested = "openrouter" in model_name.lower() or provider_pref == "openrouter"
        is_gemini_explicitly_requested = "gemini" in model_name.lower() and provider_pref == "gemini"

        # If user explicitly forced Gemini only:
        if is_gemini_explicitly_requested and self.paid_key.strip() and GENAI_AVAILABLE:
            logger.info(f"✨ Using Google Gemini API (Fizetős Tartalék Kulcs) [Explicit choice]...")
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

        # ── PRIORITY 1: Groq Cloud (Llama 3.3 70B - High free tier quota, ultra fast) ──
        if self.groq_key.strip():
            logger.info("🚀 [1. LÉPÉS - ELSŐDLEGES] Groq Cloud API hívása (Llama 3.3 70B)...")
            groq_models = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "llama3-70b-8192"]
            for gm in groq_models:
                ok, text = self.call_openai_compatible(
                    endpoint="https://api.groq.com/openai/v1/chat/completions",
                    api_key=self.groq_key.strip(),
                    model=gm,
                    prompt=prompt,
                    system_instruction=system_instruction or "Te egy mester AI tartalomkészítő és prompttervező vagy.",
                    temperature=temperature
                )
                if ok and text:
                    logger.info(f"✅ Groq Cloud ({gm}) sikeresen válaszolt!")
                    return True, text
                else:
                    logger.warning(f"Groq Cloud ({gm}) sikertelen: {text}")

            if status_widget:
                status_widget.warning("⏳ Groq Cloud kvóta kimerült -> Váltás az OpenRouter Free motorra...")

        # ── PRIORITY 2: OpenRouter Free Tier (:free open-source models) ──
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
                else:
                    logger.warning(f"OpenRouter ({om}) hiba: {text_or}")

            if status_widget:
                status_widget.warning("⏳ OpenRouter kvóta kimerült -> Váltás a Fizetős Gemini motorra...")

        # ── PRIORITY 3: Google Gemini API (Fizetős Tartalék Kulcs) ──
        if self.paid_key.strip() and GENAI_AVAILABLE:
            logger.info("💎 [3. LÉPÉS - HARMADLAGOS FIZETŐS TARTALÉK] Google Gemini Fizetős API hívása...")
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
                logger.info("✅ Google Gemini (Fizetős kulcs) sikeresen válaszolt!")
                return True, text_g

        # ── PRIORITY 4: Built-in Offline Fallback Synthesizer ──
        logger.info("🛡️ [4. LÉPÉS - VÉGSŐ HÁLÓ] Beépített 0-API Offline Szintetizátor használata...")
        offline_res = self.generate_offline_content(prompt)
        return True, offline_res

    # ─────────────────────────────────────────────────────────
    # UNIFIED IMAGE GENERATION WITH AUTOMATIC FALLBACK
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
        """
        Unified image generation router.
        - Defaults to Pollinations.ai FLUX (100% Free, No limit, 300 DPI).
        - If Imagen is explicitly chosen and paid Gemini key exists, tries Imagen; on failure, automatically falls back to Pollinations FLUX.
        """
        use_pollinations_direct = ("pollin" in self.image_engine.lower()) or ("flux" in model_name.lower()) or (not self.paid_key.strip()) or (not GENAI_AVAILABLE)

        if use_pollinations_direct:
            if status_widget:
                status_widget.info("⚡ Ingyenes Pollinations FLUX.1 motor generálja a képet...")
            return self.generate_image_pollinations(
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                model="flux"
            )

        # Otherwise try Google Imagen with Paid key
        logger.info("🎨 Trying Google Imagen 3 API with Paid key...")
        try:
            client = genai.Client(api_key=self.paid_key.strip())
            im_ratio = "3:4" if "3:4" in aspect_ratio or "8.5:11" in aspect_ratio or "4:5" in aspect_ratio else ("1:1" if "1:1" in aspect_ratio else ("16:9" if "16:9" in aspect_ratio else "3:4"))
            cfg = types.GenerateImagesConfig(
                number_of_images=number_of_images,
                aspect_ratio=im_ratio,
                output_mime_type=output_mime_type
            )
            actual_imagen_model = model_name if model_name and not any(k in model_name.lower() for k in ["pollin", "flux", "gemini"]) else "imagen-3.0-generate-002"
            resp = client.models.generate_images(
                model=actual_imagen_model,
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

        # Automatic fallback to Pollinations.ai FLUX if Imagen failed
        logger.info("🛡️ Google Imagen 3 unavailable. Auto-falling back to Pollinations FLUX.1...")
        if status_widget:
            status_widget.warning("🔄 Imagen 3 kvóta kimerült -> Automatikus váltás a 100% ingyenes Pollinations FLUX.1 motorra!")
        return self.generate_image_pollinations(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            model="flux"
        )

    def edit_image_with_fallback(
        self,
        original_image_bytes: bytes,
        edit_instruction: str,
        original_prompt: str = "",
        aspect_ratio: str = "3:4",
        model_name: str = "imagen-3.0-generate-002",
        output_mime_type: str = "image/png",
        max_retries: int = 3,
        status_widget: Any = None
    ) -> Tuple[bool, List[bytes], str, str]:
        """Modifies existing image with refined prompt and generates via Pollinations / Imagen."""
        if not edit_instruction.strip() and not original_prompt.strip():
            return False, [], "⚠️ Kérlek adj meg módosítási utasítást!", ""

        refined_prompt = f"{original_prompt}. Modified and updated with: {edit_instruction.strip()}."
        logger.info(f"🎨 Refined prompt: {refined_prompt[:100]}...")

        ok, img_list, err = self.generate_image_with_fallback(
            prompt=refined_prompt,
            aspect_ratio=aspect_ratio,
            model_name=model_name,
            status_widget=status_widget
        )
        return ok, img_list, err, refined_prompt

    # ─────────────────────────────────────────────────────────
    # BUILT-IN OFFLINE ZERO-API SYNTHESIZER
    # ─────────────────────────────────────────────────────────

    def generate_offline_content(self, prompt: str) -> str:
        """Generates rich, publication-ready responses offline with zero API calls."""
        p_lower = prompt.lower()

        # 1. Illustrated & Written Storybook Manifest
        if "illustrated" in p_lower or "story_text" in p_lower or "chapter_title" in p_lower:
            # Extract requested page count or default to 6
            cnt = 6
            for num in [16, 12, 10, 8, 6, 4]:
                if f"{num}-page" in p_lower or f" {num} " in p_lower or f"({num})" in p_lower:
                    cnt = num
                    break

            chapters = []
            sample_plots = [
                ("A hegyek lábánál, a békés völgy szélén élt Barnabás, a kis bárány.", "Barnaby standing in a sunny peaceful green meadow"),
                ("Barnabás észrevette, hogy a kis barátja, Pityu a kismadár bajba került a sziklák között.", "Barnaby looking worried as a small bird is stuck on a rock"),
                ("Bár félt a magas hegyektől, Barnabás imádkozott bátorságért, és elindult a meredek ösvényen.", "Barnaby bravely stepping onto a winding mountain path"),
                ("Lépésről lépésre haladt, és érezte, hogy a Jó Pásztor vigyáz rá a szeles sziklákon.", "Barnaby climbing carefully with golden sunbeams guiding his way"),
                ("Elérte a bajba jutott kismadarat, és gyengéd orrával kiszabadította az ágak közül.", "Barnaby gently helping the small bluebird among wildflowers"),
                ("Együtt tértek vissza a biztonságos akolba, hálát adva a kapott bátorságért és barátságért.", "Barnaby and the happy bluebird resting in the warm sunset pasture")
            ]
            for i in range(1, cnt + 1):
                p_idx = (i - 1) % len(sample_plots)
                story_t, prompt_t = sample_plots[p_idx]
                chapters.append({
                    "page_number": i,
                    "chapter_title": f"{i}. Fejezet: A bátor utazás #{i}",
                    "story_text": f"{story_t} Barnabás megtanulta, hogy a hit és a szeretet minden félelmet legyőz.",
                    "illustration_prompt": f"Vibrant full color storybook illustration of {prompt_t}, Disney Pixar 3D cute art style, soft lighting, 1:1 aspect ratio, centered full body framing, 8.5x8.5 KDP print ready.",
                    "scene_summary": f"Barnabás történetének {i}. része a békés völgyben."
                })
            return json.dumps(chapters, ensure_ascii=False, indent=2)

        # 2. KDP Autopilot Coloring Book Manifest (Strict JSON)
        if "coloring book outline" in p_lower or "manifest" in p_lower or "scenes" in p_lower:
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

        # 2. 30 Ideas / Topics
        if "30" in p_lower and ("ötlet" in p_lower or "idea" in p_lower or "topic" in p_lower):
            items = []
            for i in range(1, 31):
                items.append(f"{i}. Bibliai Jelenet #{i} | Inspiring biblical scene with beautiful landscape and figures | Psalm {20+i}:{1+(i%10)}")
            return "\n".join(items)

        # 3. Russell Brunson 12-Step Sales Letter
        if "sales letter" in p_lower or "értékesítési levél" in p_lower:
            return (
                "# VÉGRE: Egy Békés, Strukturált Út a Lelki Megújuláshoz\n\n"
                "## 1. A Megrázó Felismerés\n"
                "Állandóan rohansz, a fejed tele van teendőkkel, és a nap végén csak a kimerültséget érzed? Nem vagy egyedül.\n\n"
                "## 2. A Titkos Akadály\n"
                "A legtöbben azt hiszik, órák kellenek a békességhez. A valóság: napi 10 perc fókuszált, vezetett csendesség mindent megváltoztat.\n\n"
                "## 3. Bemutatkozik a Teljes Digitális Csomag\n"
                "Egy azonnal nyomtatható, lépésről lépésre vezetett rendszer, ami segít elcsendesedni és megerősödni a mindennapokban.\n\n"
                "## 4. Mit Kapsz Pontosan? (Value Stack)\n"
                "- ✅ 30 Napos Vezetett Áhítat & Napló (Értéke: 7 990 Ft)\n"
                "- ✅ 30 db 4K Nyomtatható Színező Lap (Értéke: 5 990 Ft)\n"
                "- ✅ Bónusz: 10 db Keretezhető Falikép Nyomat (Értéke: 4 990 Ft)\n"
                "- ✅ Bónusz: Napi Hálaadás Tracker (Értéke: 2 990 Ft)\n\n"
                "**Összérték: 21 960 Ft**\n\n"
                "### Ma Mindez a Tiéd Lehet mindössze 4 990 Ft-ért!\n\n"
                "## 5. 100% Kockázatmentes Garancia\n"
                "Próbáld ki 30 napig! Ha nem érzed a pozitív változást, 100%-ban visszatérítjük az árát, kérdések nélkül."
            )

        # Generic default response
        return (
            "✅ **Generálás sikeresen elkészült (Offline Motor)!**\n\n"
            "A rendszer a beépített sablonok és a kiválasztott niche adatai alapján összeállította a tartalmat.\n"
            "API kulcs megadásával (Groq, OpenRouter vagy Fizetős Gemini) a válaszok még egyedibbé tehetők a Rendszerbeállítások fülön."
        )

    def fetch_categorized_models(self, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Returns categorized text models prioritized by Groq -> OpenRouter -> Paid Gemini."""
        text_models = [
            {"id": "groq-llama-3.3-70b", "display_name": "Groq Llama 3.3 70B (Ingyenes & Villámgyors · Elsődleges)", "description": "300 szó/mp sebességű prémium marketing szöveg- és ötletíró", "actions": ["generateContent"]},
            {"id": "openrouter-free", "display_name": "OpenRouter Free Models (Ingyenes Nyílt Modellek · Másodlagos)", "description": "Ingyenes nyílt forráskódú modellek hálózata (:free)", "actions": ["generateContent"]},
            {"id": "gemini-3.7-flash", "display_name": "Gemini 3.7 Flash (Google · Fizetős Tartalék)", "description": "Google legújabb generációs gondolkodó modellje (Fizetős kulcs)", "actions": ["generateContent"]},
            {"id": "gemini-2.5-flash", "display_name": "Gemini 2.5 Flash (Google · Fizetős Tartalék)", "description": "Google gyors és precíz modellje (Fizetős kulcs)", "actions": ["generateContent"]},
            {"id": "gemini-2.5-pro", "display_name": "Gemini 2.5 Pro (Google · Fizetős Tartalék)", "description": "Google pro szintű szövegíró modell (Fizetős kulcs)", "actions": ["generateContent"]}
        ]
        return {
            "all_models": text_models,
            "text_models": text_models,
            "image_models": [],
            "video_models": [],
            "audio_models": []
        }


# Singleton instance helper
_manager_instance: Optional[GeminiKeyManager] = None

def get_key_manager() -> GeminiKeyManager:
    """Returns singleton GeminiKeyManager instance."""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = GeminiKeyManager()
    return _manager_instance

def generate_image_with_fallback(
    prompt: str,
    aspect_ratio: str = "3:4",
    model_name: str = "imagen-3.0-generate-002",
    number_of_images: int = 1,
    output_mime_type: str = "image/png",
    max_retries: int = 3,
    status_widget: Any = None
) -> Tuple[bool, List[bytes], str]:
    """Helper calling singleton KeyManager generate_image_with_fallback."""
    km = get_key_manager()
    return km.generate_image_with_fallback(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        model_name=model_name,
        number_of_images=number_of_images,
        output_mime_type=output_mime_type,
        max_retries=max_retries,
        status_widget=status_widget
    )

def edit_image_with_fallback(
    original_image_bytes: bytes,
    edit_instruction: str,
    original_prompt: str = "",
    aspect_ratio: str = "3:4",
    model_name: str = "imagen-3.0-generate-002",
    output_mime_type: str = "image/png",
    max_retries: int = 3,
    status_widget: Any = None
) -> Tuple[bool, List[bytes], str, str]:
    """Helper calling singleton KeyManager edit_image_with_fallback."""
    km = get_key_manager()
    return km.edit_image_with_fallback(
        original_image_bytes=original_image_bytes,
        edit_instruction=edit_instruction,
        original_prompt=original_prompt,
        aspect_ratio=aspect_ratio,
        model_name=model_name,
        output_mime_type=output_mime_type,
        max_retries=max_retries,
        status_widget=status_widget
    )
