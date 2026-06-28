import json
import os
from collections import Counter
from pathlib import Path

import build as b

SHARD_ID = int(os.environ.get("SHARD_ID", os.environ.get("BATCH_ID", "0")))
SHARD_SIZE = int(os.environ.get("SHARD_SIZE", os.environ.get("BATCH_SIZE", "5")))

# Categorías donde una fotografía contextual real del país sigue siendo informativa.
CONTEXT_ALLOWED = {
    "Arquitectura", "Países y cobertura", "Monedas", "Lado de conducción", "Banderas",
    "Animales", "ATV", "Barcos", "Teleféricos", "Automóviles", "Motocicletas",
    "Otros vehículos", "Motos de nieve", "Trenes", "Naturaleza", "Paisajes", "Ríos",
    "Nieve", "Años de captura"
}

# Categorías donde la imagen debe mostrar explícitamente el elemento; nunca se rellena
# con una fotografía genérica del país.
STRICT_CATEGORIES = set(b.CATS) - CONTEXT_ALLOWED

MAX_REUSE_EXACT = 3
MAX_REUSE_CONTEXT = 1


def matched_tokens(item: dict, category_index: int) -> list[str]:
    text = item.get("text", "")
    tokens = [token for token in b.norm(b.KEYS[category_index]).split() if len(token) >= 4]
    return sorted({token for token in tokens if token in text})


def choose_downloadable(candidates, country_code, category_index, suffix_prefix):
    for attempt, item in enumerate(candidates[:20]):
        suffix = f"{suffix_prefix}{attempt}" if attempt else suffix_prefix
        path = b.get_image(item, country_code, category_index, suffix)
        if path:
            return item, path
    return None, None


def rank_candidates(candidates, category_index, usage, exact_required):
    ranked = []
    for item in candidates:
        country_ok = item.get("country_match", 0) == 1
        tokens = matched_tokens(item, category_index)
        exact_ok = country_ok and bool(tokens)
        if exact_required and not exact_ok:
            continue
        if not exact_required and not country_ok:
            continue
        limit = MAX_REUSE_EXACT if exact_ok else MAX_REUSE_CONTEXT
        if usage[item["image_url"]] >= limit:
            continue
        score = b.score(item, category_index)
        if exact_ok:
            score += 100
        score -= usage[item["image_url"]] * 15
        ranked.append((score, item, tokens, exact_ok))
    ranked.sort(key=lambda row: row[0], reverse=True)
    return ranked


def resolve_country(country: dict) -> dict:
    code = country["code"]
    name = country["name"]
    print(f"::group::[{SHARD_ID:02d}] {code} · {name}", flush=True)
    print(f"[{SHARD_ID:02d}][{code}] Buscando banco fotográfico del país...", flush=True)

    pool = b.pool(country)
    usage = Counter()
    entries = []

    for index, category in enumerate(b.CATS, start=1):
        category_index = index - 1
        strict = category in STRICT_CATEGORIES
        status_prefix = f"[{SHARD_ID:02d}][{code}][{index:02d}/52] {category}"
        print(f"{status_prefix} -> búsqueda", flush=True)

        # 1. Aprovecha el banco del país si los metadatos contienen la categoría.
        ranked = rank_candidates(pool, category_index, usage, exact_required=True)

        # 2. Si el banco general no basta, realiza una consulta específica país + categoría.
        if not ranked:
            targeted = b.direct(country, category_index)
            ranked = rank_candidates(targeted, category_index, usage, exact_required=True)
        else:
            targeted = []

        chosen = None
        path = None
        tokens = []
        match_type = "sin_foto"

        if ranked:
            _, candidate, tokens, _ = ranked[0]
            candidates = [row[1] for row in ranked]
            chosen, path = choose_downloadable(candidates, code, category_index, "x")
            if chosen and path:
                tokens = matched_tokens(chosen, category_index)
                match_type = "exacta"

        # 3. Solo determinadas categorías admiten una fotografía contextual real del país.
        if not path and not strict:
            contextual_ranked = rank_candidates(pool, category_index, usage, exact_required=False)
            contextual_candidates = [row[1] for row in contextual_ranked]
            chosen, path = choose_downloadable(contextual_candidates, code, category_index, "c")
            if chosen and path:
                tokens = matched_tokens(chosen, category_index)
                match_type = "exacta" if tokens else "contextual"

        if chosen and path:
            usage[chosen["image_url"]] += 1
            entry = dict(chosen)
            entry.update({
                "category": category,
                "local": str(path),
                "match_type": match_type,
                "hint": f"Observe {category.lower()}: forma, color, material, montaje, idioma y relación con el entorno.",
                "matched_tokens": tokens,
                "why_matched": (
                    f"Metadatos vinculados con {country['english']} y términos: {', '.join(tokens)}"
                    if match_type == "exacta"
                    else f"Fotografía contextual verificada del país {country['english']}"
                ),
                "confidence": "alta" if match_type == "exacta" else "media",
                "reference_model": "Taxonomía GeoHints/GeoTips/Geomastr; fotografía y licencia desde Wikimedia Commons"
            })
            entries.append(entry)
            print(
                f"{status_prefix} -> {match_type.upper()} · {chosen.get('title', '')[:80]} · "
                f"licencia={chosen.get('license', 'N/D')}",
                flush=True
            )
        else:
            entries.append({
                "category": category,
                "local": "",
                "match_type": "sin_foto",
                "hint": f"Observe {category.lower()}.",
                "title": "Pendiente: no se encontró una fotografía real con coincidencia verificable",
                "source_url": "",
                "author": "",
                "license": "",
                "matched_tokens": [],
                "why_matched": "No se forzó una imagen genérica o dudosa",
                "confidence": "ninguna",
                "reference_model": "Taxonomía GeoHints/GeoTips/Geomastr"
            })
            print(f"{status_prefix} -> PENDIENTE (sin sustitución falsa)", flush=True)

    result = {
        "country": country,
        "entries": entries,
        "exact": sum(item["match_type"] == "exacta" for item in entries),
        "contextual": sum(item["match_type"] == "contextual" for item in entries),
        "missing": sum(item["match_type"] == "sin_foto" for item in entries),
        "unique_photos": len(usage),
        "reused_cards": sum(max(0, count - 1) for count in usage.values())
    }
    print(
        f"[{SHARD_ID:02d}][{code}] COMPLETADO exactas={result['exact']} "
        f"contextuales={result['contextual']} pendientes={result['missing']} "
        f"fotos_unicas={result['unique_photos']}",
        flush=True
    )
    print("::endgroup::", flush=True)
    return result


def main():
    all_countries = b.countries()
    start = SHARD_ID * SHARD_SIZE
    selected = all_countries[start:start + SHARD_SIZE]
    if len(selected) != SHARD_SIZE:
        raise SystemExit(f"Shard {SHARD_ID} incompleto: esperaba {SHARD_SIZE}, obtuvo {len(selected)}")

    print(
        f"SHARD {SHARD_ID:02d} INICIO · países {start + 1}-{start + len(selected)} de {len(all_countries)}",
        flush=True
    )
    results = []
    for position, country in enumerate(selected, start=1):
        print(
            f"SHARD {SHARD_ID:02d} · país {position}/{SHARD_SIZE} · {country['code']} {country['name']}",
            flush=True
        )
        results.append(resolve_country(country))

    pdf_path = b.build_pdf(results)
    audit_path, csv_path = b.write_outputs(results, pdf_path)
    summary = {
        "shard": SHARD_ID,
        "countries": len(results),
        "cards": len(results) * 52,
        "exact": sum(item["exact"] for item in results),
        "contextual": sum(item["contextual"] for item in results),
        "missing": sum(item["missing"] for item in results),
        "unique_photos": sum(item["unique_photos"] for item in results),
        "reused_cards": sum(item["reused_cards"] for item in results),
        "pdf": str(pdf_path),
        "audit": str(audit_path),
        "csv": str(csv_path)
    }
    Path(os.environ.get("GITHUB_STEP_SUMMARY", "/tmp/geohints_summary.md")).write_text(
        "\n".join([
            f"## GeoHints shard {SHARD_ID:02d}",
            f"- Países: {summary['countries']}",
            f"- Tarjetas: {summary['cards']}",
            f"- Fotos exactas: {summary['exact']}",
            f"- Fotos contextuales permitidas: {summary['contextual']}",
            f"- Pendientes por falta de coincidencia verificable: {summary['missing']}",
            f"- Fotografías únicas: {summary['unique_photos']}",
            f"- Reutilizaciones controladas: {summary['reused_cards']}"
        ]),
        encoding="utf-8"
    )
    print("SHARD_RESULT=" + json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
