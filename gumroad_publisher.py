"""
Gumroad API v2 Direct Publisher Engine
=====================================
Enables 1-click product creation and publishing to Gumroad accounts using the
official Gumroad API (POST https://api.gumroad.com/v2/products).
"""

import os
import json
import logging
import requests
from typing import Tuple, Dict, Any, Optional

logger = logging.getLogger("GumroadPublisher")

GUMROAD_API_URL = "https://api.gumroad.com/v2/products"
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def get_stored_gumroad_token() -> str:
    """Retrieves Gumroad API Access Token from config.json or environment variables."""
    env_token = os.getenv("GUMROAD_ACCESS_TOKEN", "").strip()
    if env_token:
        return env_token

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                return cfg.get("gumroad_access_token", "").strip()
        except Exception as e:
            logger.warning(f"Could not read config.json for Gumroad token: {e}")

    return ""


def publish_to_gumroad(
    product_name: str,
    price_usd: float,
    description: str,
    drive_delivery_url: str = "",
    access_token: Optional[str] = None,
    custom_permalink: Optional[str] = None,
    require_shipping: bool = False
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Publishes a new digital product directly to Gumroad via the Gumroad API v2.
    
    Parameters:
      - product_name: Title of the product
      - price_usd: Price in USD (e.g. 9.99 or 0 for free lead magnet)
      - description: Full product description / sales letter (supports Markdown / HTML)
      - drive_delivery_url: Google Drive delivery download link for custom receipt
      - access_token: Personal Gumroad Access Token (if None, loaded from config.json)
      - custom_permalink: Optional URL slug
      - require_shipping: False for digital products
      
    Returns:
      - (success: bool, product_url_or_error: str, raw_response: dict)
    """
    token = (access_token or "").strip() or get_stored_gumroad_token()

    if not token:
        return False, "⚠️ Nincs megadva Gumroad API Access Token! Kérlek add meg a 7. Tab Beállításokban.", {}

    if not product_name.strip():
        return False, "⚠️ A termék neve nem lehet üres.", {}

    # Gumroad API expects price in cents (e.g. $9.99 = 999 cents)
    price_in_cents = int(round(max(0.0, float(price_usd)) * 100))

    # Format custom delivery receipt
    receipt_message = "Thank you for your purchase!"
    if drive_delivery_url.strip():
        receipt_message = (
            f"Thank you for your purchase!\n\n"
            f"📥 Access your high-resolution files on Google Drive:\n{drive_delivery_url.strip()}\n\n"
            f"If you have any questions, feel free to reach out."
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    payload = {
        "name": product_name.strip(),
        "price": price_in_cents,
        "description": description.strip(),
        "custom_receipt": receipt_message,
        "require_shipping": "false" if not require_shipping else "true",
        "published": "true"
    }

    if custom_permalink and custom_permalink.strip():
        payload["custom_permalink"] = custom_permalink.strip().lower()

    try:
        logger.info(f"Publishing '{product_name}' to Gumroad API (Price: ${price_usd:.2f})...")
        response = requests.post(
            GUMROAD_API_URL,
            headers=headers,
            data=payload,
            timeout=20
        )

        try:
            resp_data = response.json()
        except Exception:
            resp_data = {"raw_text": response.text}

        if response.status_code in [200, 201] and resp_data.get("success"):
            product_obj = resp_data.get("product", {})
            prod_url = product_obj.get("short_url") or product_obj.get("url") or f"https://gumroad.com/l/{product_obj.get('id', '')}"
            logger.info(f"✅ Product published successfully on Gumroad: {prod_url}")
            return True, prod_url, resp_data
        else:
            # Handle Gumroad API specific errors
            err_msg = resp_data.get("message") or resp_data.get("error") or response.text
            if response.status_code == 401:
                return False, "⚠️ Érvénytelen Gumroad Access Token (401 Unauthorized). Ellenőrizd a beállított tokent a 7. Tab-on!", resp_data
            return False, f"Gumroad API Hiba ({response.status_code}): {err_msg}", resp_data

    except requests.exceptions.Timeout:
        return False, "⚠️ Időtúllépés (Timeout) a Gumroad API szerverhez kapcsolódáskor. Kérlek próbáld újra!", {}
    except requests.exceptions.RequestException as req_err:
        return False, f"Hálózati hiba a Gumroad hívásakor: {str(req_err)}", {}
    except Exception as ex:
        return False, f"Váratlan hiba történt a Gumroad publikálásakor: {str(ex)}", {}
