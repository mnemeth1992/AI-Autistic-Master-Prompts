"""
Etsy CSV & Listing Engine for Digital Products
==============================================
Provides strict Etsy compliant formatting and CSV export for digital products:
  - Title: Max 140 characters, front-loaded with primary keywords.
  - Tags: Exactly 13 tags, each strictly <= 20 characters, lowercase, no prohibited symbols.
  - Description: FFC (Features-Feelings-Consequences) copy + Instant Google Drive delivery notice + AI transparency notice.
  - Export: Official Etsy CSV listing template with auto-save to Google Drive.
"""

import io
import os
import csv
import re
import time
from typing import List, Dict, Any, Tuple, Optional


def sanitize_etsy_title(title: str, max_chars: int = 140) -> str:
    """
    Cleans and truncates title to strictly adhere to Etsy's 140 character limit.
    Preserves whole words when possible.
    """
    cleaned = re.sub(r'[\r\n\t]+', ' ', title).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    if len(cleaned) <= max_chars:
        return cleaned
    
    # Truncate to nearest word boundary before max_chars
    truncated = cleaned[:max_chars]
    last_space = truncated.rfind(' ')
    last_comma = truncated.rfind(',')
    last_dash = truncated.rfind('-')
    split_pos = max(last_space, last_comma, last_dash)
    
    if split_pos > 80:
        return truncated[:split_pos].rstrip(' ,-—|')
    return truncated.rstrip(' ,-—|')


def sanitize_etsy_tags(tags_input: Any, max_tags: int = 13, max_tag_len: int = 20) -> List[str]:
    """
    Cleans, deduplicates, and formats tags into exactly 13 Etsy-compliant tags.
    Each tag is strictly <= 20 characters, lowercased, and free of prohibited characters (%$@!?* etc).
    """
    raw_list = []
    if isinstance(tags_input, list):
        raw_list = [str(t) for t in tags_input]
    elif isinstance(tags_input, str):
        # Split by comma or newline
        raw_list = [t.strip() for t in re.split(r'[,;\n\r]+', tags_input) if t.strip()]

    cleaned_tags = []
    seen = set()

    for item in raw_list:
        # Strip numbers, bullets, hashtags, quotes, and invalid symbols
        clean_item = re.sub(r'^[\d\.\-\*\#\s]+', '', item)
        clean_item = re.sub(r'[\"\'\`\$\%\@\!\?\*\(\)\[\]\{\}\<\>\:\;]', '', clean_item)
        clean_item = re.sub(r'\s+', ' ', clean_item).strip().lower()

        if not clean_item:
            continue

        # If tag is longer than 20 chars, split into chunks <= 20 chars
        if len(clean_item) > max_tag_len:
            words = clean_item.split()
            sub_tag = ""
            for w in words:
                test_str = (sub_tag + " " + w).strip() if sub_tag else w.strip()
                if len(test_str) <= max_tag_len:
                    sub_tag = test_str
                else:
                    if sub_tag and sub_tag not in seen:
                        valid_tag = sub_tag[:max_tag_len].strip()
                        if valid_tag and valid_tag not in seen:
                            cleaned_tags.append(valid_tag)
                            seen.add(valid_tag)
                    sub_tag = w[:max_tag_len].strip()
            if sub_tag and sub_tag not in seen:
                valid_tag = sub_tag[:max_tag_len].strip()
                if valid_tag and valid_tag not in seen:
                    cleaned_tags.append(valid_tag)
                    seen.add(valid_tag)
        else:
            valid_tag = clean_item[:max_tag_len].strip()
            if valid_tag and valid_tag not in seen:
                cleaned_tags.append(valid_tag)
                seen.add(valid_tag)

    # Fallback high-conversion evergreen Christian / digital product tags if fewer than 13
    fallback_tags = [
        "christian wall art",
        "bible verse print",
        "scripture poster",
        "christian gift",
        "faith wall decor",
        "printable wall art",
        "digital download",
        "minimalist scripture",
        "kjv bible art",
        "spiritual wall decor",
        "christian home decor",
        "encouraging scripture",
        "christian printable"
    ]

    for fb in fallback_tags:
        if len(cleaned_tags) >= max_tags:
            break
        clean_fb = fb[:max_tag_len].strip().lower()
        if clean_fb not in seen and len(clean_fb) <= max_tag_len:
            cleaned_tags.append(clean_fb)
            seen.add(clean_fb)

    # Final guarantee that all tags are <= max_tag_len
    return [t[:max_tag_len].strip() for t in cleaned_tags[:max_tags]]


def build_etsy_ffc_description(
    product_title: str,
    features_bullets: str,
    emotional_hook: str = "",
    drive_delivery_note: str = "",
    ai_transparency: bool = True
) -> str:
    """
    Assembles a high-conversion FFC product description with Google Drive delivery
    instructions and official Etsy AI Transparency notice.
    """
    clean_bullets = features_bullets.strip() if features_bullets else ""
    if not clean_bullets:
        clean_bullets = (
            "• 5 High-Resolution 300 DPI File Ratios included (Print over 20+ frame sizes!)\n"
            "• Crystal-clear museum quality vector & watercolor detailing\n"
            "• Instant Access: Download, print at home or your local print shop immediately\n"
            "• Standard ratios: 2:3, 3:4, 4:5, 11:14 and International ISO A1-A4"
        )

    hook_section = f"{emotional_hook.strip()}\n\n" if emotional_hook.strip() else ""

    delivery_section = (
        "📥 INSTANT DIGITAL DOWNLOAD DELIVERY (GOOGLE DRIVE):\n"
        "Please note: This is a 100% DIGITAL item. No physical product will be shipped.\n"
        "After completing your purchase, you will instantly receive a download guide PDF containing "
        "your direct, secure Google Drive link to access and download all full-resolution 300 DPI artwork files, "
        "organized neatly in all standard printing ratios."
    )
    if drive_delivery_note.strip():
        delivery_section += f"\n\n📂 Access Note: {drive_delivery_note.strip()}"

    ai_notice = ""
    if ai_transparency:
        ai_notice = (
            "\n\n🤖 AI TRANSPARENCY & CRAFTSMANSHIP DISCLOSURE:\n"
            "In compliance with Etsy's Seller Guidelines, this digital artwork was created using advanced generative AI "
            "as a creative partner, then meticulously hand-curated, color-calibrated, and upscaled to ultra-high 300 DPI "
            "print standards to ensure pristine, flawless physical print results."
        )

    return f"""{product_title}

{hook_section}✨ WHAT IS INCLUDED IN YOUR DOWNLOAD:
{clean_bullets}

{delivery_section}

🖼️ HOW TO PRINT:
1. Print at home using high-quality matte photo paper or cardstock.
2. Order online through Shutterfly, Printify, Vistaprint, or Walgreens.
3. Bring files to your local print shop (FedEx, Staples, Office Depot).

📜 TERMS OF USE & COPYRIGHT:
For personal use only. You may print as many copies as you wish for your home, church, or as gifts. Commercial resale or redistribution of digital files is strictly prohibited.

{ai_notice}
"""


def generate_etsy_csv(
    listings: List[Dict[str, Any]],
    output_path: Optional[str] = None
) -> Tuple[bool, str, bytes]:
    """
    Compiles listings into Etsy's official CSV structure for bulk upload / draft import.
    Headers: Title, Description, Price, Quantity, Tags, Materials, Section, Renewal option, Type, SKU, Delivery Note
    
    Returns (success: bool, filepath_or_message: str, csv_bytes: bytes).
    """
    if not listings:
        return False, "Nincsenek feldolgozható termékek a CSV generáláshoz.", b""

    csv_headers = [
        "Title",
        "Description",
        "Price",
        "Quantity",
        "Tags",
        "Materials",
        "Section",
        "Renewal option",
        "Type",
        "SKU",
        "File URL / Delivery Note"
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=csv_headers, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    for item in listings:
        raw_title = item.get("title", "Christian Digital Wall Art Printable")
        san_title = sanitize_etsy_title(raw_title, 140)

        raw_tags = item.get("tags", [])
        san_tags = sanitize_etsy_tags(raw_tags, max_tags=13, max_tag_len=20)
        tags_str = ", ".join(san_tags)

        raw_desc = item.get("description", "")
        if not raw_desc:
            raw_desc = build_etsy_ffc_description(
                product_title=san_title,
                features_bullets=item.get("features", ""),
                emotional_hook=item.get("emotional_hook", ""),
                drive_delivery_note=item.get("drive_url", "")
            )

        row = {
            "Title": san_title,
            "Description": raw_desc,
            "Price": item.get("price", "6.99"),
            "Quantity": str(item.get("quantity", "999")),
            "Tags": tags_str,
            "Materials": item.get("materials", "Digital Download, 300 DPI PNG, JPG, PDF"),
            "Section": item.get("section", "Christian Wall Art"),
            "Renewal option": "auto",
            "Type": "download",
            "SKU": item.get("sku", f"DIG-{int(time.time())}"),
            "File URL / Delivery Note": item.get("drive_url", "Google Drive PDF Delivery Link")
        }
        writer.writerow(row)

    csv_text = output.getvalue()
    csv_bytes = csv_text.encode("utf-8-sig")  # UTF-8 with BOM for Excel/Etsy compatibility

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f_csv:
            f_csv.write(csv_bytes)

    return True, output_path or "CSV sikeresen generálva!", csv_bytes
