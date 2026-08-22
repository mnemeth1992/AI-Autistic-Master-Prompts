"""
KDP PDF Compilation Engine for Christian & Multi-Niche Coloring Books
====================================================================
Uses ReportLab to generate exact 8.5 x 11 inch (letter portrait) Amazon KDP
compliant interior PDF documents with:
  - Page 1: Title Page & Color/Marker Test Swatches
  - Companion Pages (Even: 2, 6, 10...): Scripture Verse (KJV) + Color Palette + Reflection
  - Main Coloring Pages (Odd: 3, 7, 11...): Scaled High-Res PNG Image with safe margins
  - Bleed Protection Pages (Even: 4, 8, 12...): Clean blank pages to prevent marker bleed
"""

import io
import os
import time
from typing import List, Dict, Any, Tuple, Optional
from PIL import Image

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, black, white, gray, Color
    from reportlab.pdfgen import canvas
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Line
    from reportlab.lib.utils import ImageReader
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# Standard KDP Dimensions helper
from kdp_math import parse_trim_size

def get_kdp_page_metrics(trim_size: str = "8.5x11", margin_in: float = 0.5) -> Tuple[float, float, float, float, float]:
    """
    Returns (page_width, page_height, margin, content_width, content_height) in points (72 pt / inch)
    for any Amazon KDP trim size (e.g. '8.5x8.5', '8.5x11', '8x10', '6x9') and custom margin.
    """
    trim_w_in, trim_h_in = parse_trim_size(trim_size)
    pw = trim_w_in * 72.0
    ph = trim_h_in * 72.0
    safe_margin_in = max(0.2, min(1.25, float(margin_in)))
    margin = safe_margin_in * 72.0
    cw = max(50.0, pw - (2 * margin))
    ch = max(50.0, ph - (2 * margin))
    return pw, ph, margin, cw, ch


# Predefined Color Swatch Hex Mapping for visual palette rendering
SWATCH_COLOR_MAP = {
    "blue": HexColor("#6BA4D9"),
    "sky blue": HexColor("#87CEEB"),
    "navy": HexColor("#1E3A8A"),
    "ocean": HexColor("#0284C7"),
    "green": HexColor("#4ADE80"),
    "emerald": HexColor("#10B981"),
    "olive": HexColor("#84CC16"),
    "forest": HexColor("#15803D"),
    "yellow": HexColor("#FACC15"),
    "gold": HexColor("#F59E0B"),
    "amber": HexColor("#D97706"),
    "sun": HexColor("#FDE047"),
    "red": HexColor("#EF4444"),
    "ruby": HexColor("#DC2626"),
    "crimson": HexColor("#B91C1C"),
    "pink": HexColor("#F472B6"),
    "rose": HexColor("#FB7185"),
    "blush": HexColor("#FDA4AF"),
    "purple": HexColor("#A855F7"),
    "violet": HexColor("#8B5CF6"),
    "lavender": HexColor("#C084FC"),
    "brown": HexColor("#A16207"),
    "earth": HexColor("#78350F"),
    "wood": HexColor("#92400E"),
    "sand": HexColor("#D97706"),
    "beige": HexColor("#E2D9C8"),
    "orange": HexColor("#FB923C"),
    "peach": HexColor("#FDBA74"),
    "gray": HexColor("#9CA3AF"),
    "charcoal": HexColor("#374151"),
    "white": HexColor("#F8FAFC"),
    "black": HexColor("#18181B")
}


def get_color_for_name(name: str) -> Color:
    """Matches a color name string to a ReportLab Color object, fallback to pleasant pastel."""
    name_lower = name.lower().strip()
    for k, col in SWATCH_COLOR_MAP.items():
        if k in name_lower:
            return col
    return HexColor("#94A3B8")


def draw_decorative_frame(c: canvas.Canvas, width: float, height: float, margin: float = 36.0):
    """Draws a clean, elegant double line vector border with corner accents."""
    c.saveState()
    c.setStrokeColor(HexColor("#1E293B"))
    c.setLineWidth(1.5)
    
    # Outer box
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin, fill=0, stroke=1)
    
    # Inner thin box
    inner_pad = 4.0
    c.setLineWidth(0.5)
    c.setStrokeColor(HexColor("#64748B"))
    c.rect(
        margin + inner_pad,
        margin + inner_pad,
        width - 2 * (margin + inner_pad),
        height - 2 * (margin + inner_pad),
        fill=0,
        stroke=1
    )
    
    # Small decorative corner diamonds
    c.setFillColor(HexColor("#1E293B"))
    corner_offset = margin + 2.0
    s = 3.0
    for cx, cy in [
        (corner_offset, corner_offset),
        (width - corner_offset, corner_offset),
        (corner_offset, height - corner_offset),
        (width - corner_offset, height - corner_offset)
    ]:
        p = c.beginPath()
        p.moveTo(cx, cy - s)
        p.lineTo(cx + s, cy)
        p.lineTo(cx, cy + s)
        p.lineTo(cx - s, cy)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        
    c.restoreState()


def draw_title_and_tester_page(
    c: canvas.Canvas,
    title: str,
    subtitle: str,
    trim_size: str = "8.5x11",
    show_decorative_frame: bool = True,
    show_swatches: bool = True,
    margin_in: float = 0.5
):
    """
    Renders Page 1: Title Page & Color Swatch Tester.
    Includes book title, subtitle, ownership frame, and optional coloring test shapes adapted to trim size.
    """
    pw, ph, margin, cw, ch = get_kdp_page_metrics(trim_size, margin_in=margin_in)
    if show_decorative_frame:
        draw_decorative_frame(c, pw, ph, margin)
    
    c.saveState()
    
    # Header Banner & Title
    c.setFont("Helvetica-Bold", 22 if pw < 500 else 24)
    c.setFillColor(HexColor("#0F172A"))
    c.drawCentredString(pw / 2.0, ph - margin - 50, title.upper()[:45])
    
    if len(title) > 45:
        c.setFont("Helvetica-Bold", 18 if pw < 500 else 20)
        c.drawCentredString(pw / 2.0, ph - margin - 75, title.upper()[45:90])
        sub_top = ph - margin - 100
    else:
        sub_top = ph - margin - 75
        
    # Subtitle
    if subtitle:
        c.setFont("Helvetica-Oblique", 11 if pw < 500 else 12)
        c.setFillColor(HexColor("#64748B"))
        c.drawCentredString(pw / 2.0, sub_top, subtitle[:60])
        div_y = sub_top - 18
    else:
        div_y = sub_top - 10

    # Decorative dividing line
    c.setLineWidth(1)
    c.setStrokeColor(HexColor("#CBD5E1"))
    c.line(pw / 2.0 - 120, div_y, pw / 2.0 + 120, div_y)

    # "This Book Belongs To" decorative name box
    box_w = min(360.0, cw - 40)
    box_h = 44.0
    box_x = (pw - box_w) / 2.0
    box_y = div_y - 60.0
    
    c.setStrokeColor(HexColor("#1E3A8A"))
    c.setLineWidth(1.2)
    c.setFillColor(HexColor("#F8FAFC"))
    c.roundRect(box_x, box_y, box_w, box_h, 6, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 10 if pw < 500 else 11)
    c.setFillColor(HexColor("#1E3A8A"))
    c.drawString(box_x + 14, box_y + 26, "✏️ THIS COLORING BOOK BELONGS TO:")
    
    c.setLineWidth(0.8)
    c.setStrokeColor(HexColor("#94A3B8"))
    c.line(box_x + 14, box_y + 12, box_x + box_w - 14, box_y + 12)

    # Bottom Color Test Section (Optional)
    if show_swatches:
        swatch_top = box_y - (20 if ph < 650 else 30)
        c.setFont("Helvetica-Bold", 11 if pw < 500 else 12)
        c.setFillColor(HexColor("#0F172A"))
        c.drawCentredString(pw / 2.0, swatch_top, "🎨 COLOR PALETTE & MARKER TEST")
        
        c.setFont("Helvetica", 8.5 if pw < 500 else 9)
        c.setFillColor(HexColor("#64748B"))
        c.drawCentredString(pw / 2.0, swatch_top - 14, "Test your colored pencils, markers, and gel pens in the shapes below before coloring:")

        # Draw clean vector test swatch shapes
        swatch_grid_y = swatch_top - (35 if ph < 650 else 45)
        num_cols = 5
        num_rows = 2 if ph < 650 else 3
        shape_w = 40.0 if pw < 500 else 48.0
        shape_h = 30.0 if ph < 650 else 38.0
        gap_x = 14.0 if pw < 500 else 20.0
        gap_y = 10.0 if ph < 650 else 14.0
        
        start_x = (pw - (num_cols * shape_w + (num_cols - 1) * gap_x)) / 2.0
        
        c.setStrokeColor(HexColor("#334155"))
        c.setLineWidth(1)
        c.setFillColor(HexColor("#FFFFFF"))

        for r in range(num_rows):
            for col in range(num_cols):
                sx = start_x + col * (shape_w + gap_x)
                sy = swatch_grid_y - r * (shape_h + gap_y) - shape_h
                
                # Alternate between rounded rectangles, circles, and shields
                shape_type = (r * num_cols + col) % 3
                if shape_type == 0:
                    c.roundRect(sx, sy, shape_w, shape_h, 4, fill=1, stroke=1)
                elif shape_type == 1:
                    c.circle(sx + shape_w / 2.0, sy + shape_h / 2.0, shape_h / 2.0 - 2, fill=1, stroke=1)
                else:
                    c.rect(sx, sy, shape_w, shape_h, fill=1, stroke=1)
                    
                # Small swatch label inside
                c.setFont("Helvetica", 6 if pw < 500 else 6.5)
                c.setFillColor(HexColor("#94A3B8"))
                c.drawCentredString(sx + shape_w / 2.0, sy + 4, f"#{r*num_cols + col + 1}")
                c.setFillColor(HexColor("#FFFFFF"))

    # Footer note
    c.setFont("Helvetica-Oblique", 7.5 if pw < 500 else 8)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawCentredString(pw / 2.0, margin + 12, f"Created with Faith & Inspiration · Amazon KDP {trim_size} Interior Edition")

    c.restoreState()
    c.showPage()


def draw_companion_page(
    c: canvas.Canvas,
    scene_number: int,
    total_scenes: int,
    scene_title: str,
    scripture_ref: str,
    scripture_text: str,
    color_suggestions: List[str],
    reflection_thought: str,
    trim_size: str = "8.5x11",
    show_decorative_frame: bool = True,
    show_footer: bool = True,
    margin_in: float = 0.5
):
    """
    Renders Companion Scripture & Color Guide Page (Even pages: 2, 6, 10...).
    Placed on the left-hand page directly facing the coloring illustration on the right.
    """
    pw, ph, margin, cw, ch = get_kdp_page_metrics(trim_size, margin_in=margin_in)
    if show_decorative_frame:
        draw_decorative_frame(c, pw, ph, margin)
    c.saveState()
    
    # 1. Page Header (Scene Number & Title)
    header_top = ph - margin - 35
    c.setFont("Helvetica-Bold", 10 if pw < 500 else 11)
    c.setFillColor(HexColor("#64748B"))
    c.drawCentredString(pw / 2.0, header_top, f"— SCENE {scene_number} OF {total_scenes} —")
    
    c.setFont("Helvetica-Bold", 15 if pw < 500 else 18)
    c.setFillColor(HexColor("#0F172A"))
    c.drawCentredString(pw / 2.0, header_top - 20, scene_title[:50])
    
    div_y = header_top - 34

    c.setLineWidth(0.8)
    c.setStrokeColor(HexColor("#CBD5E1"))
    c.line(margin + 40, div_y, pw - margin - 40, div_y)

    # 2. Scripture Reference & Text Box (Framed Card)
    card_top = div_y - 14
    card_w = cw - 20
    card_h = 120 if ph < 650 else 150
    card_x = (pw - card_w) / 2.0
    card_y = card_top - card_h

    c.setFillColor(HexColor("#F8FAFC"))
    c.setStrokeColor(HexColor("#3B82F6"))
    c.setLineWidth(1)
    c.roundRect(card_x, card_y, card_w, card_h, 6, fill=1, stroke=1)

    badge_w = min(220.0, card_w - 40)
    badge_h = 18
    badge_x = (pw - badge_w) / 2.0
    badge_y = card_top - (badge_h / 2.0)
    
    c.setFillColor(HexColor("#1E3A8A"))
    c.roundRect(badge_x, badge_y, badge_w, badge_h, 9, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(HexColor("#FFFFFF"))
    c.drawCentredString(pw / 2.0, badge_y + 5, f"📖 {scripture_ref[:40]}")

    c.setFont("Helvetica-Oblique", 9.5 if pw < 500 else 11)
    c.setFillColor(HexColor("#1E293B"))
    
    clean_verse = f'"{scripture_text.strip()}"' if scripture_text else '"Thy word is a lamp unto my feet, and a light unto my path. - Psalm 119:105"'
    
    words = clean_verse.split()
    lines = []
    curr_line = []
    max_w = card_w - 36
    for w in words:
        test_line = " ".join(curr_line + [w])
        if c.stringWidth(test_line, "Helvetica-Oblique", 10) < max_w:
            curr_line.append(w)
        else:
            lines.append(" ".join(curr_line))
            curr_line = [w]
    if curr_line:
        lines.append(" ".join(curr_line))

    text_y_start = card_top - 28
    line_spacing = 15 if ph >= 650 else 13
    for idx, l in enumerate(lines[:6]):
        c.drawCentredString(pw / 2.0, text_y_start - (idx * line_spacing), l)

    # 3. Recommended Color Palette Section
    palette_top = card_y - (20 if ph < 650 else 30)
    c.setFont("Helvetica-Bold", 10 if pw < 500 else 11)
    c.setFillColor(HexColor("#0F172A"))
    c.drawCentredString(pw / 2.0, palette_top, "🎨 RECOMMENDED COLOR PALETTE:")

    # Render Color Swatch Circles with Labels
    swatches = color_suggestions if color_suggestions else ["Sky Blue", "Olive Green", "Sun Gold", "Wood Brown", "Rose Pink"]
    swatches = swatches[:5]
    
    circle_r = 14.0 if pw < 500 else 17.0
    spacing = 52.0 if pw < 500 else 66.0
    chips_y = palette_top - (24 if ph < 650 else 32)
    chips_start_x = (pw - ((len(swatches) - 1) * spacing)) / 2.0

    for s_idx, col_name in enumerate(swatches):
        cx = chips_start_x + (s_idx * spacing)
        cy = chips_y
        
        # Color circle
        col_obj = get_color_for_name(col_name)
        c.setFillColor(col_obj)
        c.setStrokeColor(HexColor("#1E293B"))
        c.setLineWidth(1)
        c.circle(cx, cy, circle_r, fill=1, stroke=1)
        
        c.setStrokeColor(HexColor("#FFFFFF"))
        c.setLineWidth(0.8)
        c.circle(cx, cy, circle_r - 4, fill=0, stroke=1)

        c.setFont("Helvetica-Bold", 7 if pw < 500 else 8)
        c.setFillColor(HexColor("#1E293B"))
        c.drawCentredString(cx, cy - (circle_r + 10), col_name[:15])

    # 4. Devotional Reflection / Meditation Box
    ref_top = chips_y - (40 if ph < 650 else 55)
    ref_w = cw - 30
    ref_h = 65 if ph < 650 else 85
    ref_x = (pw - ref_w) / 2.0
    ref_y = ref_top - ref_h

    if ref_y > margin + 20:
        c.setFillColor(HexColor("#F1F5F9"))
        c.setStrokeColor(HexColor("#94A3B8"))
        c.setLineWidth(0.8)
        c.roundRect(ref_x, ref_y, ref_w, ref_h, 4, fill=1, stroke=1)

        c.setFont("Helvetica-Bold", 9 if pw < 500 else 10)
        c.setFillColor(HexColor("#334155"))
        c.drawString(ref_x + 12, ref_top - 15, "✨ REFLECTION & QUIET TIME PRAYER:")

        ref_text = reflection_thought.strip() if reflection_thought else "Take a deep breath as you color this page. Reflect on God's faithfulness and steady presence in your daily life."
        ref_words = ref_text.split()
        ref_lines = []
        curr_l = []
        for w in ref_words:
            test_str = " ".join(curr_l + [w])
            if c.stringWidth(test_str, "Helvetica", 8.5) < (ref_w - 24):
                curr_l.append(w)
            else:
                ref_lines.append(" ".join(curr_l))
                curr_l = [w]
        if curr_l:
            ref_lines.append(" ".join(curr_l))

        c.setFont("Helvetica", 8 if pw < 500 else 8.5)
        c.setFillColor(HexColor("#475569"))
        for i, rl in enumerate(ref_lines[:2 if ph < 650 else 3]):
            c.drawString(ref_x + 12, ref_top - 30 - (i * 12), rl)

    # Footer note
    if show_footer:
        c.setFont("Helvetica", 7.5 if pw < 500 else 8)
        c.setFillColor(HexColor("#94A3B8"))
        c.drawString(margin + 10, margin + 12, f"Scene {scene_number} Companion Guide")
        c.drawRightString(pw - margin - 10, margin + 12, "👉 Turn to right page to color")

    c.restoreState()
    c.showPage()


def draw_coloring_image_page(
    c: canvas.Canvas,
    image_data_or_path: Any,
    scene_title: str = "",
    scene_number: int = 1,
    trim_size: str = "8.5x11",
    show_decorative_frame: bool = True,
    show_image_border: bool = True,
    show_header_text: bool = True,
    show_footer_text: bool = True,
    margin_in: float = 0.5
):
    """
    Renders Main Coloring Page (Odd pages: 3, 7, 11...).
    Scales the high-resolution PNG image proportionally inside the KDP safe margins with optional framing and text.
    """
    pw, ph, margin, cw, ch = get_kdp_page_metrics(trim_size, margin_in=margin_in)
    if show_decorative_frame:
        draw_decorative_frame(c, pw, ph, margin)
    c.saveState()
    
    top_bar_height = 18 if show_header_text else 0
    bottom_bar_height = 18 if show_footer_text else 0
    avail_w = cw - (16 if show_decorative_frame else 0)
    avail_h = ch - top_bar_height - bottom_bar_height - (16 if show_decorative_frame else 0)
    
    # Load PIL image to compute aspect ratio and create ImageReader
    pil_img = None
    if isinstance(image_data_or_path, (bytes, bytearray)):
        pil_img = Image.open(io.BytesIO(image_data_or_path))
    elif isinstance(image_data_or_path, str) and os.path.exists(image_data_or_path):
        pil_img = Image.open(image_data_or_path)
    elif hasattr(image_data_or_path, "save"):
        pil_img = image_data_or_path

    if pil_img is not None:
        img_w, img_h = pil_img.size
        aspect = img_w / float(img_h)
        
        # Scale to fit inside avail_w x avail_h
        target_w = avail_w
        target_h = target_w / aspect
        if target_h > avail_h:
            target_h = avail_h
            target_w = target_h * aspect

        # Center inside printable area
        frame_offset_x = 8 if show_decorative_frame else 0
        frame_offset_y = 8 if show_decorative_frame else 0
        img_x = margin + frame_offset_x + ((avail_w - target_w) / 2.0)
        img_y = margin + bottom_bar_height + frame_offset_y + ((avail_h - target_h) / 2.0)

        # Outer fine framing border around illustration (Optional)
        if show_image_border:
            c.setStrokeColor(HexColor("#0F172A"))
            c.setLineWidth(1.2)
            c.rect(img_x - 2, img_y - 2, target_w + 4, target_h + 4, fill=0, stroke=1)

        # Draw the actual high-res image using ReportLab ImageReader
        img_reader = ImageReader(pil_img)
        c.drawImage(
            img_reader,
            img_x,
            img_y,
            width=target_w,
            height=target_h,
            preserveAspectRatio=True,
            mask="auto"
        )
    else:
        # Fallback placeholder if image failed
        c.setStrokeColor(HexColor("#DC2626"))
        c.setLineWidth(1)
        c.rect(margin + 20, margin + 30, cw - 40, ch - 60, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(HexColor("#DC2626"))
        c.drawCentredString(pw / 2.0, ph / 2.0, "⚠️ Image data could not be rendered.")

    # Top small scene title (Optional)
    if show_header_text and scene_title:
        c.setFont("Helvetica-Bold", 9 if pw < 500 else 10)
        c.setFillColor(HexColor("#1E293B"))
        c.drawCentredString(pw / 2.0, ph - margin - 16, f"SCENE {scene_number} · {scene_title.upper()[:55]}")

    # Bottom page footer (Optional)
    if show_footer_text:
        c.setFont("Helvetica", 7.5 if pw < 500 else 8)
        c.setFillColor(HexColor("#94A3B8"))
        c.drawCentredString(pw / 2.0, margin + 12, f"— COLORING PAGE · AMAZON KDP {trim_size} —")

    c.restoreState()
    c.showPage()


def draw_bleed_protection_page(
    c: canvas.Canvas,
    trim_size: str = "8.5x11",
    show_border: bool = True,
    show_text: bool = True,
    margin_in: float = 0.5
):
    """
    Renders Bleed Protection Page (Even pages: 4, 8, 12...).
    A clean blank page designed to absorb marker bleed-through, protecting the next scene.
    """
    pw, ph, margin, cw, ch = get_kdp_page_metrics(trim_size, margin_in=margin_in)
    c.saveState()
    
    if show_border:
        c.setStrokeColor(HexColor("#E2E8F0"))
        c.setLineWidth(0.5)
        c.rect(margin + 16, margin + 16, cw - 32, ch - 32, fill=0, stroke=1)

    if show_text:
        c.setFont("Helvetica-Oblique", 7.5 if pw < 500 else 8)
        c.setFillColor(HexColor("#CBD5E1"))
        c.drawCentredString(
            pw / 2.0,
            margin + 26,
            "🔒 BLEED PROTECTION PAGE · Intentionally left blank to protect your illustrations from marker bleed"
        )
    
    c.restoreState()
    c.showPage()


def build_kdp_book_pdf(
    title: str = "Christian Coloring Book",
    subtitle: str = "Bible Verse Coloring",
    pages_data: List[Dict[str, Any]] = None,
    output_path: Optional[str] = None,
    trim_size: str = "8.5x11",
    margin_in: float = 0.5,
    show_decorative_frame: bool = True,
    show_image_border: bool = True,
    show_header_text: bool = True,
    show_footer_text: bool = True,
    include_companion_pages: bool = True,
    include_bleed_protection: bool = True,
    include_swatches_tester: bool = True,
    book_title: str = None,
    scenes: List[Dict[str, Any]] = None,
    uploaded_images: List[Any] = None,
    trim_size_str: str = None,
    is_hu: bool = True,
    **kwargs
) -> Tuple[bool, bytes, str]:
    """
    Assembles a complete, publication-ready Amazon KDP coloring book PDF in the requested trim size
    (e.g., '8.5x11', '8.5x8.5', '8x10', '6x9') with fully customized layout and margin parameters.
    """
    if not REPORTLAB_AVAILABLE:
        return False, b"", "⚠️ A 'reportlab' csomag nincs telepítve a környezetben!"

    if book_title:
        title = book_title
    if trim_size_str:
        trim_size = trim_size_str
    if pages_data is None:
        pages_data = [dict(s) for s in (scenes or [])]
    else:
        pages_data = [dict(s) for s in pages_data]

    if uploaded_images:
        for idx, up_img in enumerate(uploaded_images):
            if idx < len(pages_data):
                try:
                    if hasattr(up_img, "read"):
                        up_img.seek(0)
                        pages_data[idx]["image_bytes"] = up_img.read()
                    elif isinstance(up_img, (bytes, bytearray)):
                        pages_data[idx]["image_bytes"] = up_img
                except Exception:
                    pass

    try:
        pw, ph, margin, cw, ch = get_kdp_page_metrics(trim_size, margin_in=margin_in)
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(pw, ph))
        c.setTitle(title)
        c.setAuthor("Christian Digital Products Studio")
        c.setSubject(f"Amazon KDP Coloring Book Interior ({trim_size})")

        # 1. Page 1: Title & Color Swatches Tester
        draw_title_and_tester_page(
            c,
            title,
            subtitle,
            trim_size=trim_size,
            show_decorative_frame=show_decorative_frame,
            show_swatches=include_swatches_tester,
            margin_in=margin_in
        )

        total_scenes = len(pages_data)

        # 2. Loop through all scenes
        for idx, scene in enumerate(pages_data, start=1):
            s_title = scene.get("title", f"Scene {idx}")
            s_ref = scene.get("scripture_reference", "Scripture Verse")
            s_text = scene.get("scripture_text", "")
            s_colors = scene.get("color_suggestions", ["Sky Blue", "Olive Green", "Sun Gold", "Earth Brown", "Blush Pink"])
            s_ref_thought = scene.get("reflection_thought", "")
            img_data = scene.get("image_bytes") or scene.get("filepath") or scene.get("pil_image")

            # Left Companion Page (Facing Page) - Optional
            if include_companion_pages:
                draw_companion_page(
                    c=c,
                    scene_number=idx,
                    total_scenes=total_scenes,
                    scene_title=s_title,
                    scripture_ref=s_ref,
                    scripture_text=s_text,
                    color_suggestions=s_colors,
                    reflection_thought=s_ref_thought,
                    trim_size=trim_size,
                    show_decorative_frame=show_decorative_frame,
                    show_footer=show_footer_text,
                    margin_in=margin_in
                )

            # Right Main Coloring Page
            draw_coloring_image_page(
                c=c,
                image_data_or_path=img_data,
                scene_title=s_title,
                scene_number=idx,
                trim_size=trim_size,
                show_decorative_frame=show_decorative_frame,
                show_image_border=show_image_border,
                show_header_text=show_header_text,
                show_footer_text=show_footer_text,
                margin_in=margin_in
            )

            # Bleed Protection Blank Page - Optional
            if include_bleed_protection:
                draw_bleed_protection_page(
                    c,
                    trim_size=trim_size,
                    show_border=show_decorative_frame,
                    show_text=True,
                    margin_in=margin_in
                )

        # Save ReportLab canvas
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()

        # If output path is specified, write to disk
        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            with open(output_path, "wb") as f_out:
                f_out.write(pdf_bytes)

        pages_per_scene = 1 + (1 if include_companion_pages else 0) + (1 if include_bleed_protection else 0)
        total_p_calc = 1 + (total_scenes * pages_per_scene)

        return True, pdf_bytes, f"PDF sikeresen összeállítva ({total_p_calc} oldal · {trim_size})!"

    except Exception as e:
        return False, b"", f"Hiba a PDF összefűzése során: {str(e)}"


# ─────────────────────────────────────────────────────────
# 📖 ILLUSTRATED & WRITTEN BOOK PDF COMPILER
# ─────────────────────────────────────────────────────────

def build_illustrated_book_pdf(
    title: str,
    subtitle: str = "",
    pages_data: List[Dict[str, Any]] = None,
    author: str = "Christian Digital Creator",
    output_path: Optional[str] = None,
    trim_size: str = "8.5x8.5",
    layout_mode: str = "half_page",
    margin_in: float = 0.5,
    show_decorative_frame: bool = True,
    show_image_border: bool = True,
    show_page_numbers: bool = True,
    show_chapter_header: bool = True
) -> Tuple[bool, bytes, str]:
    """
    Compiles an illustrated story/educational book with narrative text and color illustrations
    into an Amazon KDP print-ready PDF interior in any trim size ('8.5x8.5', '8.5x11', '8x10', '6x9')
    with customizable margin, borders, headers, and page numbers.
    """
    if not REPORTLAB_AVAILABLE:
        return False, b"", "A ReportLab könyvtár nincs telepítve."

    if not pages_data:
        return False, b"", "Nincsenek oldalak megadva a könyvhöz."

    try:
        pw, ph, margin, cw, ch = get_kdp_page_metrics(trim_size, margin_in=margin_in)
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(pw, ph))
        c.setTitle(title)
        c.setAuthor(author)
        c.setSubject(f"Amazon KDP Illustrated & Written Book Interior ({trim_size})")

        # ── 1. TITLE PAGE ──
        c.setFillColor(HexColor("#FFFFFF"))
        c.rect(0, 0, pw, ph, fill=True, stroke=False)

        if show_decorative_frame:
            # Decorative outer border
            c.setStrokeColor(HexColor("#CBD5E1"))
            c.setLineWidth(1)
            c.rect(margin - 6, margin - 6, cw + 12, ch + 12, stroke=True, fill=False)

            c.setStrokeColor(HexColor("#1E3A8A"))
            c.setLineWidth(1.5)
            c.rect(margin, margin, cw, ch, stroke=True, fill=False)

        # Title
        c.setFillColor(HexColor("#1E293B"))
        c.setFont("Helvetica-Bold", 22 if pw < 500 else 26)
        c.drawCentredString(pw / 2.0, ph - (1.8 * 72 if ph < 650 else 2.5 * 72), title.upper()[:45])

        # Subtitle
        if subtitle:
            c.setFillColor(HexColor("#64748B"))
            c.setFont("Helvetica-Oblique", 12 if pw < 500 else 14)
            c.drawCentredString(pw / 2.0, ph - (2.4 * 72 if ph < 650 else 3.2 * 72), subtitle[:60])

        # Decorative divider
        c.setStrokeColor(HexColor("#3B82F6"))
        c.setLineWidth(2)
        c.line(pw / 2.0 - 1.2 * 72, ph - (2.8 * 72 if ph < 650 else 3.8 * 72), pw / 2.0 + 1.2 * 72, ph - (2.8 * 72 if ph < 650 else 3.8 * 72))

        # Flourish symbol
        c.setFillColor(HexColor("#3B82F6"))
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(pw / 2.0, ph - (2.9 * 72 if ph < 650 else 3.9 * 72), "✦ ✦ ✦")

        # Author
        c.setFillColor(HexColor("#334155"))
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(pw / 2.0, margin + 1.4 * 72, f"Written & Illustrated by")
        c.setFont("Helvetica", 13)
        c.drawCentredString(pw / 2.0, margin + 1.1 * 72, author)

        c.showPage()

        # ── 2. COPYRIGHT / DEDICATION PAGE ──
        c.setFillColor(HexColor("#FFFFFF"))
        c.rect(0, 0, pw, ph, fill=True, stroke=False)

        c.setFillColor(HexColor("#64748B"))
        c.setFont("Helvetica-Oblique", 9.5)
        c.drawCentredString(pw / 2.0, ph / 2.0 + 0.4 * 72, f"'{title}'")
        c.drawCentredString(pw / 2.0, ph / 2.0 + 0.15 * 72, f"Copyright © {time.strftime('%Y')} {author}. All rights reserved.")
        c.drawCentredString(pw / 2.0, ph / 2.0 - 0.15 * 72, f"Published independently via Amazon KDP ({trim_size}).")
        c.drawCentredString(pw / 2.0, ph / 2.0 - 0.4 * 72, "May this book bring peace, wisdom, and joy to every reader.")

        c.showPage()

        # ── 3. STORY PAGES ──
        total_p = len(pages_data)
        is_square = "8.5x8.5" in trim_size or abs(pw - ph) < 20

        for idx, page in enumerate(pages_data, start=1):
            c.setFillColor(HexColor("#FFFFFF"))
            c.rect(0, 0, pw, ph, fill=True, stroke=False)

            c_title = page.get("chapter_title", f"Chapter {idx}")
            s_text = page.get("story_text", "")
            img_data = page.get("image_bytes") or page.get("filepath") or page.get("pil_image")

            # Header (Optional)
            if show_chapter_header:
                c.setFillColor(HexColor("#1E3A8A"))
                c.setFont("Helvetica-Bold", 13 if pw < 500 else 15)
                c.drawString(margin, ph - margin - 12, c_title)

                c.setStrokeColor(HexColor("#E2E8F0"))
                c.setLineWidth(1)
                c.line(margin, ph - margin - 18, pw - margin, ph - margin - 18)
                ill_top = ph - margin - 24
            else:
                ill_top = ph - margin

            # Illustration Area
            if is_square:
                ill_height = ch * (0.60 if show_chapter_header else 0.65)
            else:
                ill_height = ch * (0.52 if show_chapter_header else 0.58)
            ill_width = cw

            if img_data:
                try:
                    pil_img = None
                    if isinstance(img_data, bytes):
                        pil_img = Image.open(io.BytesIO(img_data))
                    elif isinstance(img_data, str) and os.path.exists(img_data):
                        pil_img = Image.open(img_data)
                    elif hasattr(img_data, "convert"):
                        pil_img = img_data

                    if pil_img:
                        img_w, img_h = pil_img.size
                        ratio = min(ill_width / float(img_w), ill_height / float(img_h))
                        draw_w = img_w * ratio
                        draw_h = img_h * ratio
                        draw_x = margin + (ill_width - draw_w) / 2.0
                        draw_y = ill_top - draw_h

                        # Optional framing border around image
                        if show_image_border:
                            c.setStrokeColor(HexColor("#CBD5E1"))
                            c.setLineWidth(1)
                            c.rect(draw_x - 2, draw_y - 2, draw_w + 4, draw_h + 4, stroke=True, fill=False)

                        img_bio = io.BytesIO()
                        pil_img.save(img_bio, format="PNG")
                        img_bio.seek(0)
                        rl_img = ImageReader(img_bio)
                        c.drawImage(rl_img, draw_x, draw_y, width=draw_w, height=draw_h)
                except Exception:
                    pass

            # Story Text Area (Bottom Section)
            text_top = ill_top - ill_height - 18
            c.setFillColor(HexColor("#1E293B"))
            c.setFont("Helvetica", 10 if pw < 500 else 11)

            # Split story text into wrapped paragraphs
            words = s_text.split()
            lines = []
            curr_line = []
            max_char_width = 65 if pw < 500 else 80

            for w in words:
                curr_line.append(w)
                if len(" ".join(curr_line)) > max_char_width:
                    lines.append(" ".join(curr_line[:-1]))
                    curr_line = [w]
            if curr_line:
                lines.append(" ".join(curr_line))

            y_pos = text_top
            line_height = 15
            for l in lines:
                if y_pos > margin + (22 if show_page_numbers else 8):
                    c.drawString(margin, y_pos, l)
                    y_pos -= line_height

            # Footer with page number (Optional)
            if show_page_numbers:
                c.setFillColor(HexColor("#94A3B8"))
                c.setFont("Helvetica", 8.5)
                c.drawCentredString(pw / 2.0, margin + 8, f"— {idx + 2} —")

            c.showPage()

        # Finalize and write
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()

        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            with open(output_path, "wb") as f_out:
                f_out.write(pdf_bytes)

        return True, pdf_bytes, f"Illusztrált könyv PDF sikeresen elkészült ({2 + total_p} oldal · {trim_size})!"

    except Exception as e:
        return False, b"", f"Hiba az illusztrált könyv PDF összefűzésekor: {str(e)}"
