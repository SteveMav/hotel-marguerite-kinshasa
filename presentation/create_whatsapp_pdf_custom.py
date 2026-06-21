from __future__ import annotations

from io import BytesIO
from pathlib import Path

import qrcode
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "hotel-marguerite-presentation-whatsapp.pdf"
MESSAGE_OUTPUT = ROOT / "message-whatsapp.txt"
SITE_URL = "https://stevemav.github.io/hotel-marguerite-kinshasa/"
COMPANY = "Hotel Marguerite de Kinshasa"


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", r"C:\Windows\Fonts\georgiab.ttf"))


def paragraph(styles: dict[str, ParagraphStyle], html_text: str, style_name: str = "body") -> Paragraph:
    return Paragraph(html_text, styles[style_name])


def make_qr() -> Image:
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
    qr.add_data(SITE_URL)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return Image(buffer, width=3.4 * cm, height=3.4 * cm)


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    primary = colors.HexColor("#164B3A")
    burgundy = colors.HexColor("#7B2D3A")
    brass = colors.HexColor("#B98A52")
    ivory = colors.HexColor("#F7F1E6")
    muted = colors.HexColor("#5E6259")
    return {
        "eyebrow": ParagraphStyle(
            "eyebrow",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=8.5,
            leading=11,
            textColor=brass,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "hero": ParagraphStyle(
            "hero",
            parent=base["Title"],
            fontName="Georgia-Bold",
            fontSize=29,
            leading=36,
            textColor=colors.white,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=13,
            leading=18,
            textColor=ivory,
            alignment=TA_CENTER,
        ),
        "label": ParagraphStyle(
            "label",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=9,
            leading=12,
            textColor=burgundy,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Arial-Bold",
            fontSize=19,
            leading=23,
            textColor=primary,
            spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=10.8,
            leading=16,
            textColor=muted,
            spaceAfter=8,
        ),
        "strong": ParagraphStyle(
            "strong",
            parent=base["BodyText"],
            fontName="Arial-Bold",
            fontSize=11,
            leading=15,
            textColor=primary,
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=8.8,
            leading=12,
            textColor=muted,
        ),
        "link": ParagraphStyle(
            "link",
            parent=base["BodyText"],
            fontName="Arial-Bold",
            fontSize=10.6,
            leading=15,
            textColor=burgundy,
            spaceAfter=5,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["BodyText"],
            fontName="Arial-Bold",
            fontSize=8.8,
            leading=12,
            textColor=ivory,
            alignment=TA_CENTER,
        ),
    }


def build_pdf() -> None:
    register_fonts()
    styles = build_styles()
    primary = colors.HexColor("#164B3A")
    burgundy = colors.HexColor("#7B2D3A")
    ivory = colors.HexColor("#F7F1E6")
    line = colors.HexColor("#D5C6AE")

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=1.35 * cm,
        rightMargin=1.35 * cm,
        topMargin=1.15 * cm,
        bottomMargin=1.05 * cm,
        title=f"Proposition de site - {COMPANY}",
        author="Steve Mavuela",
    )

    hero = Table(
        [
            [paragraph(styles, "PROPOSITION DE SITE WEB", "eyebrow")],
            [paragraph(styles, COMPANY, "hero")],
            [paragraph(styles, "H&ocirc;tel au centre-ville de Kinshasa, RDC", "subtitle")],
        ],
        colWidths=[18.3 * cm],
    )
    hero.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), primary),
                ("TOPPADDING", (0, 0), (-1, -1), 22),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
            ]
        )
    )

    link_block = Table(
        [
            [
                [
                    paragraph(styles, "LIEN DIRECT DU SITE", "label"),
                    Paragraph(f'<a href="{SITE_URL}">{SITE_URL}</a>', styles["link"]),
                    paragraph(
                        styles,
                        "Le QR code et le lien peuvent &ecirc;tre envoy&eacute;s dans WhatsApp avec ce PDF.",
                        "small",
                    ),
                ],
                make_qr(),
            ]
        ],
        colWidths=[13.7 * cm, 4.2 * cm],
    )
    link_block.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ivory),
                ("BOX", (0, 0), (-1, -1), 0.8, burgundy),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ]
        )
    )

    cards = Table(
        [
            [
                [
                    paragraph(styles, "Clart&eacute;", "strong"),
                    paragraph(
                        styles,
                        "Adresse, t&eacute;l&eacute;phone, chambres et contacts regroup&eacute;s sans ambigu&iuml;t&eacute;.",
                        "small",
                    ),
                ],
                [
                    paragraph(styles, "Confiance", "strong"),
                    paragraph(
                        styles,
                        "Une premi&egrave;re impression plus cr&eacute;dible avant l'appel ou la visite.",
                        "small",
                    ),
                ],
                [
                    paragraph(styles, "Contact", "strong"),
                    paragraph(
                        styles,
                        "Un parcours WhatsApp direct pour demander disponibilit&eacute; et tarif.",
                        "small",
                    ),
                ],
            ]
        ],
        colWidths=[5.95 * cm, 5.95 * cm, 5.95 * cm],
    )
    cards.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.55, line),
                ("INNERGRID", (0, 0), (-1, -1), 0.55, line),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    footer = Table(
        [[paragraph(styles, "Steve Mavuela | WhatsApp: 0833650168 | stevemavuela@gmail.com", "footer")]],
        colWidths=[18.3 * cm],
    )
    footer.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), primary),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    flow = [
        hero,
        Spacer(1, 0.42 * cm),
        paragraph(styles, "Pourquoi cette proposition", "label"),
        paragraph(
            styles,
            "Vos informations existent d&eacute;j&agrave; sur Facebook, cartes et annuaires, mais elles sont dispers&eacute;es. Cette proposition montre comment une vitrine officielle peut centraliser l'adresse, le contact WhatsApp, les chambres et les informations pratiques pour faciliter la r&eacute;servation directe.",
        ),
        paragraph(
            styles,
            "Le site reste une base de discussion : avant publication officielle, il faudra valider l'adresse exacte, les photos, les horaires, les services disponibles et les textes d&eacute;finitifs avec la direction.",
        ),
        Spacer(1, 0.18 * cm),
        link_block,
        Spacer(1, 0.42 * cm),
        paragraph(styles, "Ce que le site de d&eacute;monstration met en avant", "h2"),
        cards,
        Spacer(1, 0.42 * cm),
        paragraph(styles, "Prochaine &eacute;tape", "h2"),
        paragraph(
            styles,
            "Si cette approche parle &agrave; la direction, l'&eacute;tape suivante est un court &eacute;change pour confirmer les pages prioritaires : accueil, chambres, s&eacute;jour, r&eacute;servation et contact.",
        ),
        paragraph(
            styles,
            "Apr&egrave;s validation, les visuels de d&eacute;monstration seront remplac&eacute;s par de vraies photos de l'h&ocirc;tel et le site pourra devenir une vitrine officielle, claire et partageable.",
        ),
        Spacer(1, 0.24 * cm),
        footer,
        Spacer(1, 0.12 * cm),
        paragraph(styles, "Portfolio : https://stevemav.github.io/portfolio/", "small"),
    ]
    doc.build(flow)


def write_message() -> None:
    MESSAGE_OUTPUT.write_text(
        """Bonjour,

Je vous envoie une courte présentation PDF de la proposition de site préparée pour Hotel Marguerite de Kinshasa.

Lien du site de présentation : https://stevemav.github.io/hotel-marguerite-kinshasa/

L'idée est simplement de vous montrer à quoi pourrait ressembler une vitrine digitale plus claire, plus crédible et plus facile à partager avec vos clients.

Je reste disponible sur WhatsApp pour en parler rapidement.

Steve Mavuela
WhatsApp : 0833650168
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    build_pdf()
    write_message()
    print(f"PDF written to {OUTPUT}")
    print(f"Message written to {MESSAGE_OUTPUT}")

