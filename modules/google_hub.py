"""
modules/google_hub.py - Google Ecosystem Hub & Stripe/Sheets Webhook Automation
Generates ready-to-paste Google Apps Script webhook code for automatic Stripe/Gumroad
order logging in Google Sheets and automated Gmail delivery with Google Drive links.
"""

from typing import Dict, Any


def get_apps_script_webhook_template(
    drive_folder_url: str,
    sheet_name: str = "Rendelések",
    product_name: str = "Keresztény Digitális Csomag"
) -> str:
    """
    Generates a production-ready, zero-cost Google Apps Script webhook
    that listens for Stripe & Gumroad checkout events, logs the order into Google Sheets,
    and sends an automated delivery email via Gmail with the Google Drive link.
    """
    clean_drive_url = drive_folder_url.strip() if drive_folder_url.strip() else "https://drive.google.com/drive/folders/TE_MAPPA_AZONOSITOD"

    return f"""// =========================================================================
// 🚀 0 FT-OS AUTOMATIZÁCIÓ: STRIPE / GUMROAD -> GOOGLE SHEETS -> GMAIL
// =========================================================================
// Használat:
// 1. Nyiss egy új Google Sheets táblázatot (pl. 'Keresztény Termék Eladások').
// 2. Menj a 'Bővítmények' (Extensions) -> 'Apps Script' menüpontba.
// 3. Törölj ki mindent, másold be ezt a teljes kódot, és kattints a Mentés ikonra.
// 4. Kattints a 'Telepítés' (Deploy) -> 'Új telepítés' (New deployment) gombra:
//    - Típus: Webes alkalmazás (Web App)
//    - Végrehajtás: Saját magam (Me)
//    - Ki férhet hozzá: Bárki (Anyone)  <-- FONTOS!
// 5. Másold ki a kapott Web App URL-t, és illeszd be a Stripe Webhookokhoz!
// =========================================================================

function doPost(e) {{
  try {{
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Táblázat fejlécek automatikus létrehozása, ha még üres
    if (sheet.getLastRow() === 0) {{
      sheet.appendRow(["Dátum", "Vásárló Neve", "E-mail Cím", "Összeg", "Fizetési Rendszer", "Termék", "Státusz"]);
      sheet.getRange("A1:G1").setFontWeight("bold").setBackground("#e2e8f0");
    }}
    
    var data = JSON.parse(e.postData.contents);
    var customerEmail = "";
    var customerName = "Kedves Vásárló";
    var amountTotal = "0";
    var provider = "Ismeretlen";
    var productName = "{product_name}";
    var driveLink = "{clean_drive_url}";

    // 1. ESET: STRIPE CHECKOUT ESEMÉNY (checkout.session.completed)
    if (data.type === 'checkout.session.completed' && data.data && data.data.object) {{
      var obj = data.data.object;
      customerEmail = obj.customer_details ? obj.customer_details.email : (obj.customer_email || "");
      customerName = obj.customer_details && obj.customer_details.name ? obj.customer_details.name : "Kedves Vásárló";
      amountTotal = obj.amount_total ? (obj.amount_total / 100).toFixed(2) + " " + (obj.currency || "HUF").toUpperCase() : "Fizetve";
      provider = "Stripe";
    }}
    // 2. ESET: GUMROAD PING / SALE ESEMÉNY
    else if (data.seller_id || data.email || data.price) {{
      customerEmail = data.email || "";
      customerName = data.full_name || "Kedves Vásárló";
      amountTotal = data.price ? (data.price / 100).toFixed(2) + " USD" : "Fizetve";
      provider = "Gumroad";
    }}
    // 3. ESET: EGYÉB FORM / ZAPIER / WEBHOOK
    else {{
      customerEmail = data.email || data.customer_email || "";
      customerName = data.name || data.customer_name || "Kedves Vásárló";
      amountTotal = data.amount || "Fizetve";
      provider = "Egyedi Webhook";
    }}

    // Ha nincs érvényes email cím, nem küldünk levelet
    if (!customerEmail || customerEmail.indexOf("@") === -1) {{
      return ContentService.createTextOutput(JSON.stringify({{ status: 'ignored', reason: 'No valid email found' }}))
        .setMimeType(ContentService.MimeType.JSON);
    }}

    // 1. LÉPÉS: NAPLÓZÁS A GOOGLE SHEETS TÁBLÁZATBA
    sheet.appendRow([
      new Date(),
      customerName,
      customerEmail,
      amountTotal,
      provider,
      productName,
      "✅ Kézbesítve"
    ]);

    // 2. LÉPÉS: AUTOMATIKUS DIGITÁLIS KÉZBESÍTŐ E-MAIL GMAILBŐL
    var emailSubject = "✝️ Köszönjük a vásárlást! Itt a hozzáférésed: " + productName;
    var emailBody = "Kedves " + customerName + "!\n\n" +
      "Hálás szívvel köszönjük, hogy megvásároltad a(z) '" + productName + "' digitális csomagot!\n\n" +
      "📁 AZONNALI LETÖLTÉSI LINK (Google Drive Privát Mappa):\n" +
      driveLink + "\n\n" +
      "📌 A csomag tartalma:\n" +
      "- Nyomdakész PDF munkafüzet & naplólapok (A4 és Letter méretben)\n" +
      "- Minden exkluzív bónusz és segédlet\n" +
      "- Örökös hozzáférés a jövőbeli frissítésekkel együtt\n\n" +
      "Ha bármilyen kérdésed vagy észrevételed van, bátran válaszolj erre az e-mailre.\n\n" +
      "Áldott és békességgel teli időtöltést kívánunk!\n\n" +
      "Üdvözlettel,\n" +
      "A Keresztény Digitális Alkotóműhely Csapata";

    // Gmail küldése
    MailApp.sendEmail(customerEmail, emailSubject, emailBody);

    return ContentService.createTextOutput(JSON.stringify({{ status: 'success', email: customerEmail }}))
      .setMimeType(ContentService.MimeType.JSON);

  }} catch (err) {{
    return ContentService.createTextOutput(JSON.stringify({{ status: 'error', message: err.toString() }}))
      .setMimeType(ContentService.MimeType.JSON);
  }}
}}

// Tesztelési funkció a Google Apps Script szerkesztőben való próbaküldéshez
function testLocalWebhook() {{
  var testEvent = {{
    postData: {{
      contents: JSON.stringify({{
        type: 'checkout.session.completed',
        data: {{
          object: {{
            customer_details: {{ email: Session.getActiveUser().getEmail(), name: 'Teszt Vásárló' }},
            amount_total: 999000,
            currency: 'huf'
          }}
        }}
      }})
    }}
  }};
  doPost(testEvent);
}}
"""


def get_stripe_setup_guide() -> str:
    """Returns markdown setup instructions for linking Stripe Webhook to Google Apps Script."""
    return """
### 🛠️ 3-Lépéses Stripe ➔ Google Sheets ➔ Gmail Beállítás (0 Ft-os Rendszer)

1. **1. Google Sheets & Apps Script Létrehozása:**
   - Nyiss egy új üres [Google Sheets](https://sheets.new) táblázatot.
   - Menj a felső menüben a **Bővítmények (Extensions) ➔ Apps Script** pontra.
   - Másold be a generált kódot, majd kattints a kék **Telepítés (Deploy) ➔ Új telepítés (New deployment)** gombra.
   - Válassz **Webes alkalmazást (Web App)**, és a hozzáférésnél állítsd be: **Bárki (Anyone)**.
   - Másold ki a kapott `https://script.google.com/macros/s/.../exec` webcímet!

2. **2. Stripe Webhook Beállítása:**
   - Lépj be a [Stripe Dashboard](https://dashboard.stripe.com) felületedre.
   - Keresd meg a **Developers (Fejlesztők) ➔ Webhooks** menüpontot.
   - Kattints a **+ Add endpoint (Végpont hozzáadása)** gombra.
   - **Endpoint URL:** Másold be a fenti Google Apps Script webcímet.
   - **Events to listen to:** Válaszd ki a `checkout.session.completed` eseményt.
   - Kattints az **Add endpoint** gombra.

3. **3. Kész! Automatikus Működés:**
   - Amint egy vásárló fizet a Stripe fizetési linkjén (pl. Google Sites-ról), a Stripe másodperceken belül meghívja a Google táblázatodat.
   - A vásárló adatai bekerülnek a táblázatba, és a Gmail fiókod **azonnal kiküldi a privát Google Drive letöltési linket!**
"""


def get_google_sites_embed_button(
    checkout_url: str = "https://buy.stripe.com/pelda",
    button_text: str = "👉 KÉREM A TELJES CSOMAGOT (AZONNALI LETÖLTÉS)",
    price_badge: str = "9.990 Ft / $27 · 14 Napos Garancia"
) -> str:
    """Generates an aesthetic, conversion-optimized HTML embed code for Google Sites."""
    return f"""<div style="text-align: center; margin: 30px auto; font-family: 'Segoe UI', system-ui, sans-serif;">
  <a href="{checkout_url}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: #ffffff; text-decoration: none; font-size: 1.15rem; font-weight: 700; padding: 18px 36px; border-radius: 12px; box-shadow: 0 10px 25px rgba(16, 185, 129, 0.35); transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 0.5px;">
    {button_text}
  </a>
  <div style="margin-top: 10px; font-size: 0.9rem; color: #64748b; font-weight: 500;">
    🔒 Biztonságos Stripe Fizetés · {price_badge}
  </div>
</div>"""
