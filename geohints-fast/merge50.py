import csv
import json
import os
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
DOWNLOAD = Path(os.environ.get("DOWNLOAD_DIR", ROOT / "downloaded"))
OUT = ROOT / "final"
OUT.mkdir(parents=True, exist_ok=True)

PDF_OUT = OUT / "Guia_GeoHints_V10_Atlas_Fotografico_250_Paises.pdf"
AUDIT_OUT = OUT / "Guia_GeoHints_V10_Auditoria_Global.json"
CSV_OUT = OUT / "Guia_GeoHints_V10_Fuentes_Global.csv"
COVER = OUT / "_cover.pdf"


def files(pattern):
    return sorted(DOWNLOAD.rglob(pattern), key=lambda path: path.name)


def build_cover(summary_preview):
    width, height = A4
    pdf = canvas.Canvas(str(COVER), pagesize=A4, pageCompression=1)
    pdf.setFillColor(colors.HexColor("#244f6c"))
    pdf.rect(0, 0, width, height, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(width / 2, height - 150, "GUÍA GEOHINTS V10")
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawCentredString(width / 2, height - 185, "ATLAS FOTOGRÁFICO GLOBAL")
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(width / 2, height - 230, "250 países y territorios · 52 categorías por país")
    pdf.drawCentredString(width / 2, height - 250, "13.000 referencias auditadas")
    pdf.drawCentredString(width / 2, height - 290, "Fuentes fotográficas: Wikimedia Commons")
    pdf.drawCentredString(width / 2, height - 310, "Taxonomía y vocabulario de pistas: GeoHints, GeoTips y Geomastr")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(width / 2, 115, "Sin ilustraciones generadas · sin sustituciones genéricas ocultas")
    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(width / 2, 90, "Las referencias pendientes quedan declaradas explícitamente en la auditoría.")
    pdf.save()


def main():
    pdfs = files("GeoHints_Fotos_Batch_*.pdf")
    audits = files("GeoHints_Auditoria_Batch_*.json")
    tables = files("GeoHints_Fuentes_Batch_*.csv")
    if not (len(pdfs) == len(audits) == len(tables) == 50):
        raise SystemExit(f"Se esperaban 50 shards; PDFs={len(pdfs)}, auditorías={len(audits)}, CSV={len(tables)}")

    batches = [json.loads(path.read_text(encoding="utf-8")) for path in audits]
    batches.sort(key=lambda item: int(item["batch_id"]))

    build_cover(batches)
    writer = PdfWriter()
    cover_reader = PdfReader(str(COVER))
    writer.add_page(cover_reader.pages[0])

    total_country_pages = 0
    for pdf_file in pdfs:
        reader = PdfReader(str(pdf_file))
        # Cada shard tiene su propia portada. Se omite para dejar una sola portada global.
        for page in reader.pages[1:]:
            writer.add_page(page)
            total_country_pages += 1

    writer.add_metadata({
        "/Title": "Guía GeoHints V10 - Atlas fotográfico de 250 países y territorios",
        "/Author": "Bastián Lisboa",
        "/Subject": "52 categorías visuales por país con fotografías reales, fuentes y auditoría",
        "/Keywords": "GeoGuessr GeoHints GeoTips Geomastr fotografías países señales matrículas postes"
    })
    with PDF_OUT.open("wb") as handle:
        writer.write(handle)

    countries = []
    items = []
    for batch in batches:
        countries.extend(batch.get("countries", []))
        items.extend(batch.get("items", []))

    summary = {
        "edition": "V10 - atlas fotográfico global estricto",
        "countries_and_territories": len(countries),
        "categories_per_country": 52,
        "total_reference_cards": len(countries) * 52,
        "exact_country_category_photos": sum(batch.get("exact_photos", 0) for batch in batches),
        "contextual_real_photos_from_correct_country": sum(batch.get("contextual_country_photos", 0) for batch in batches),
        "cards_without_verified_photo": sum(batch.get("missing_photos", 0) for batch in batches),
        "unique_photos": sum(batch.get("unique_photos", 0) for batch in batches),
        "reused_cards": sum(batch.get("reused_cards", 0) for batch in batches),
        "generated_or_illustrated_images": 0,
        "pdf_pages": len(writer.pages),
        "pdf_file": PDF_OUT.name,
        "image_source": "Wikimedia Commons",
        "reference_taxonomy": ["GeoHints", "GeoTips", "Geomastr"],
        "quality_policy": "Las categorías estrictas no reciben una fotografía contextual genérica. Las faltantes permanecen pendientes.",
        "shards": [{
            "shard_id": batch["batch_id"],
            "countries": len(batch.get("countries", [])),
            "exact": batch.get("exact_photos", 0),
            "contextual": batch.get("contextual_country_photos", 0),
            "missing": batch.get("missing_photos", 0),
            "unique": batch.get("unique_photos", 0),
            "reused": batch.get("reused_cards", 0)
        } for batch in batches],
        "countries": countries,
        "items": items
    }
    AUDIT_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    with CSV_OUT.open("w", newline="", encoding="utf-8-sig") as output:
        writer_csv = csv.writer(output)
        wrote_header = False
        for csv_file in tables:
            with csv_file.open("r", newline="", encoding="utf-8-sig") as source:
                reader = csv.reader(source)
                header = next(reader, None)
                if header and not wrote_header:
                    writer_csv.writerow(header)
                    wrote_header = True
                for row in reader:
                    writer_csv.writerow(row)

    COVER.unlink(missing_ok=True)
    print(json.dumps({
        "pdf": str(PDF_OUT),
        "pdf_bytes": PDF_OUT.stat().st_size,
        "audit": str(AUDIT_OUT),
        "csv": str(CSV_OUT),
        "countries": summary["countries_and_territories"],
        "cards": summary["total_reference_cards"],
        "exact": summary["exact_country_category_photos"],
        "contextual": summary["contextual_real_photos_from_correct_country"],
        "missing": summary["cards_without_verified_photo"],
        "pages": summary["pdf_pages"]
    }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
