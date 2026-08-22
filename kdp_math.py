"""
KDP Dynamic Spine Thickness & Cover Dimensions Calculator Engine
================================================================
Implements precise Amazon KDP mathematical formulas for paperback and hardcover
wrap-around book covers based on page count, trim size, paper type, and binding.

Formula Specs:
- Spine Width (in) = Page Count * Paper Multiplier
- Paperback Total Width (in) = (2 * Trim Width) + Spine Width + 0.25 (0.125" bleed per side)
- Paperback Total Height (in) = Trim Height + 0.25 (0.125" bleed top & bottom)
- Hardcover Total Width (in) = (2 * Trim Width) + Spine Width + 1.25 (Case laminate wrap & hinge)
- Hardcover Total Height (in) = Trim Height + 0.50
- 300 DPI Pixel Size = Inches * 300
- Spine Text Allowed: True if Page Count >= 79
"""

import math
from typing import Dict, Any, Tuple


# Standard KDP Paper Thickness Multipliers (Inches per Page)
PAPER_MULTIPLIERS = {
    "white": 0.002252,          # Black & White on White paper
    "cream": 0.0025,            # Black & White on Cream paper
    "standard_color": 0.0032,   # Standard Color on White paper
    "premium_color": 0.002252   # Premium Color on White paper
}

# Standard KDP Trim Sizes (Width x Height in Inches)
TRIM_SIZES = {
    "8.5x11": (8.5, 11.0),      # Coloring books, workbooks, large format
    "6x9": (6.0, 9.0),          # Standard trade paperbacks, novels, devotionals
    "5.5x8.5": (5.5, 8.5),      # Journals, prayer books, digests
    "8.5x8.5": (8.5, 8.5),      # Square children's storybooks
    "7x10": (7.0, 10.0),        # Educational, reference, guidebooks
    "5x8": (5.0, 8.0)           # Pocket books, poetry
}


def parse_trim_size(trim_size_str: str) -> Tuple[float, float]:
    """Parses a trim size string like '8.5x11' or '6x9' into (width, height) in inches."""
    clean = trim_size_str.lower().strip()
    if clean in TRIM_SIZES:
        return TRIM_SIZES[clean]
    
    # Try custom parsing if formatted as WxH or W x H
    clean = clean.replace(" ", "").replace("inch", "").replace("in", "").replace('"', "")
    if "x" in clean:
        parts = clean.split("x")
        try:
            w = float(parts[0])
            h = float(parts[1])
            return (w, h)
        except ValueError:
            pass
            
    return (8.5, 11.0)


def calculate_kdp_cover_dimensions(
    page_count: int,
    trim_size: str = "8.5x11",
    paper_type: str = "white",
    binding_type: str = "paperback",
    trim_size_str: str = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Calculates exact Amazon KDP cover specifications:
    
    Args:
        page_count: Number of book pages (int, minimum 4)
        trim_size: Trim size string (e.g. '8.5x11', '6x9', '8.5x8.5')
        paper_type: 'white', 'cream', 'standard_color', 'premium_color'
        binding_type: 'paperback' or 'hardcover'
        
    Returns:
        Dictionary containing spine thickness (in, mm), total cover dimensions (in, px @ 300 DPI),
        aspect ratios, and spine text permission flag.
    """
    # Sanitize inputs
    p_count = max(4, int(page_count))
    p_type_clean = paper_type.lower().strip().replace(" ", "_")
    if p_type_clean not in PAPER_MULTIPLIERS:
        p_type_clean = "white"
        
    is_hardcover = "hardcover" in binding_type.lower() or "kemény" in binding_type.lower()
    binding_key = "hardcover" if is_hardcover else "paperback"
    if trim_size_str:
        trim_size = trim_size_str
    trim_w, trim_h = parse_trim_size(trim_size)
    multiplier = PAPER_MULTIPLIERS.get(p_type_clean, 0.002252)
    
    # Calculate spine thickness
    spine_width_in = p_count * multiplier
    spine_width_mm = spine_width_in * 25.4
    
    # Calculate total cover dimensions including bleed and wrap
    if is_hardcover:
        # KDP Case Laminate wrap margin + hinge allowance
        total_width_in = (2 * trim_w) + spine_width_in + 1.25
        total_height_in = trim_h + 0.50
    else:
        # Standard Paperback 0.125" bleed on all 4 sides
        total_width_in = (2 * trim_w) + spine_width_in + 0.25
        total_height_in = trim_h + 0.25
        
    # 300 DPI Pixel Dimensions for print-ready graphics
    width_px_300dpi = int(round(total_width_in * 300))
    height_px_300dpi = int(round(total_height_in * 300))
    spine_px_300dpi = int(round(spine_width_in * 300))
    
    # Aspect ratios
    aspect_ratio_float = total_width_in / total_height_in
    aspect_ratio_str = f"{total_width_in:.3f}:{total_height_in:.3f}"
    aspect_ratio_simplified = f"{round(total_width_in, 2)}:{round(total_height_in, 2)}"
    
    # Spine text validation
    spine_text_allowed = p_count >= 79
    if spine_text_allowed:
        warning_msg = "✅ A gerinc vastagsága elegendő a cím és szerző nevének nyomtatásához az Amazon KDP-n (>= 79 oldal)."
    else:
        warning_msg = f"⚠️ 79 oldal alatt (jelenleg: {p_count} oldal) az Amazon KDP nem nyomtat szöveget a gerincre (túl vékony a gerincfelület)."
        
    dimensions_summary = f"{total_width_in:.3f}\" × {total_height_in:.3f}\" ({width_px_300dpi} × {height_px_300dpi} px @ 300 DPI)"
    
    return {
        "page_count": p_count,
        "trim_size": trim_size,
        "trim_width_in": trim_w,
        "trim_height_in": trim_h,
        "paper_type": p_type_clean,
        "paper_multiplier": multiplier,
        "binding_type": binding_key,
        "spine_width_in": round(spine_width_in, 4),
        "spine_width_inch": round(spine_width_in, 4),
        "spine_width_mm": round(spine_width_mm, 2),
        "total_cover_width_in": round(total_width_in, 3),
        "total_width_in": round(total_width_in, 3),
        "total_cover_height_in": round(total_height_in, 3),
        "total_height_in": round(total_height_in, 3),
        "full_width_inch": round(total_width_in, 3),
        "full_height_inch": round(total_height_in, 3),
        "width_px_300dpi": width_px_300dpi,
        "height_px_300dpi": height_px_300dpi,
        "pixel_width_300dpi": width_px_300dpi,
        "pixel_height_300dpi": height_px_300dpi,
        "full_width_px_300dpi": width_px_300dpi,
        "full_height_px_300dpi": height_px_300dpi,
        "spine_px_300dpi": spine_px_300dpi,
        "spine_width_px_300dpi": spine_px_300dpi,
        "aspect_ratio": round(aspect_ratio_float, 4),
        "aspect_ratio_str": aspect_ratio_str,
        "aspect_ratio_simplified": aspect_ratio_simplified,
        "spine_text_allowed": spine_text_allowed,
        "warning_msg": warning_msg,
        "dimensions_summary": dimensions_summary
    }
