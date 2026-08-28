#!/usr/bin/env python3
"""
normalize_dataset.py
=====================
Normaliza valores inconsistentes en columnas categoricas del dataset de
StreamAI (genero, pais) que llegan mezclados por venir de 5 fuentes de
Kaggle con esquemas distintos (Netflix/Prime Video vs Disney+/Apple TV+/
HBO Max).

Problemas detectados:
  - genero: 63 valores distintos por mezcla de mayusculas/minusculas,
    singular/plural y sinonimos (Drama/Dramas/drama, Comedy/Comedies/comedy,
    Horror/Horror Movies, etc.)
  - pais: mezcla de nombres completos y codigos ISO-2 (US/United States,
    GB/United Kingdom, CA/Canada, FR/France, JP/Japan, IN/India, DE/Germany,
    IT/Italy, CN/China, AU/Australia, MX/Mexico)

Este script:
  1. Lee data/streaming_dataset_full.csv
  2. Aplica la normalizacion
  3. Sobreescribe el CSV y regenera dataset_embed.js con el mismo formato
     (para que el dashboard siga funcionando igual, ahora con valores
     unificados)

Uso:
    python3 normalize_dataset.py
"""
import csv
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "streaming_dataset_full.csv")
EMBED_PATH = os.path.join(BASE_DIR, "dataset_embed.js")

GENRE_MAP = {
    "action": "Action & Adventure",
    "Action": "Action & Adventure",
    "adventure": "Action & Adventure",
    "Adventure": "Action & Adventure",
    "Action & Adventure": "Action & Adventure",
    "TV Action & Adventure": "Action & Adventure",

    "animation": "Animation",
    "Animation": "Animation",
    "Anime": "Animation",
    "Anime Series": "Animation",

    "comedy": "Comedy",
    "Comedy": "Comedy",
    "Comedies": "Comedy",
    "TV Comedies": "Comedy",
    "Stand-Up Comedy": "Comedy",
    "Stand-Up Comedy & Talk Shows": "Comedy",

    "drama": "Drama",
    "Drama": "Drama",
    "Dramas": "Drama",

    "Crime TV Shows": "Crime",

    "Documentary": "Documentary",
    "Documentaries": "Documentary",
    "documentation": "Documentary",
    "Docuseries": "Documentary",

    "horror": "Horror",
    "Horror": "Horror",
    "Horror Movies": "Horror",
    "TV Horror": "Horror",

    "fantasy": "Sci-Fi & Fantasy",
    "Fantasy": "Sci-Fi & Fantasy",
    "Sci-Fi & Fantasy": "Sci-Fi & Fantasy",
    "Science Fiction": "Sci-Fi & Fantasy",
    "scifi": "Sci-Fi & Fantasy",

    "thriller": "Thriller",
    "Thrillers": "Thriller",
    "Suspense": "Thriller",

    "romance": "Romance",
    "Romance": "Romance",
    "Romantic TV Shows": "Romance",

    "family": "Family",
    "Kids": "Family",
    "Kids' TV": "Family",
    "Children & Family Movies": "Family",

    "reality": "Reality",
    "Reality TV": "Reality",
    "Unscripted": "Reality",

    "music": "Music",
    "Music Videos and Concerts": "Music",

    "sport": "Sports & Fitness",
    "Fitness": "Sports & Fitness",

    "International": "International",
    "International Movies": "International",
    "International TV Shows": "International",
    "British TV Shows": "International",

    "Classic Movies": "Classics",
    "Cult Movies": "Classics",
    "Arthouse": "Arts",
    "Arts": "Arts",

    "history": "History",
    "Faith and Spirituality": "Faith & Spirituality",

    "western": "Western",
    "Western": "Western",

    "TV Shows": "Other",
    "Special Interest": "Other",
    "": "Unclassified",
}

COUNTRY_MAP = {
    "US": "United States",
    "GB": "United Kingdom",
    "CA": "Canada",
    "FR": "France",
    "JP": "Japan",
    "IN": "India",
    "DE": "Germany",
    "IT": "Italy",
    "CN": "China",
    "AU": "Australia",
    "MX": "Mexico",
    "PR": "Puerto Rico",
    "IL": "Israel",
    "ES": "Spain",
    "BR": "Brazil",
    "HK": "Hong Kong",
    "SG": "Singapore",
    "NL": "Netherlands",
}


def normalize_genero(raw):
    v = (raw or "").strip()
    return GENRE_MAP.get(v, v)


def normalize_pais(raw):
    v = (raw or "").strip()
    return COUNTRY_MAP.get(v, v)


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames


def main():
    rows, fieldnames = load_rows()

    genre_before = set(r["genero"] for r in rows)
    pais_before = set(r["pais"] for r in rows if r["pais"])

    for r in rows:
        r["genero"] = normalize_genero(r["genero"])
        r["pais"] = normalize_pais(r["pais"])

    genre_after = set(r["genero"] for r in rows)
    pais_after = set(r["pais"] for r in rows if r["pais"])

    print(f"genero: {len(genre_before)} valores distintos -> {len(genre_after)}")
    print(f"pais:   {len(pais_before)} valores distintos -> {len(pais_after)}")
    unmapped = [g for g in genre_after if g not in set(GENRE_MAP.values())]
    if unmapped:
        print("ADVERTENCIA - valores de genero sin mapear (revisar GENRE_MAP):", unmapped)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    def to_js_value(key, value):
        if key == "anio_lanzamiento":
            return "NaN" if value in (None, "", "nan") else str(int(float(value)))
        if key in ("duracion", "puntaje"):
            if value in (None, "", "nan"):
                return "NaN"
            return repr(float(value))
        if key == "fecha_agregado":
            if value in (None, "", "nan"):
                return "NaN"
            return json.dumps(value)
        return json.dumps(value if value is not None else "")

    lines = []
    lines.append("// ============================================================")
    lines.append("// DATASET EMBEBIDO")
    lines.append("// Generado a partir de datasets REALES de Kaggle (Netflix, Prime Video,")
    lines.append("// Disney+, Apple TV+, HBO Max), unificados y procesados en")
    lines.append("// preprocessing/preprocessing_streamai.ipynb, con normalizacion adicional")
    lines.append("// de 'genero' y 'pais' via preprocessing/normalize_dataset.py")
    lines.append("// Muestra proporcional de 800 titulos sobre un total")
    lines.append("// de 23529 titulos unificados de las 5 plataformas.")
    lines.append("// ============================================================")

    obj_strs = []
    for r in rows:
        parts = []
        for key in fieldnames:
            parts.append(f'"{key}": {to_js_value(key, r.get(key))}')
        obj_strs.append("{" + ", ".join(parts) + "}")

    lines.append("const DATASET = [" + ", ".join(obj_strs) + "];")
    lines.append("")

    with open(EMBED_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"OK -> {CSV_PATH}")
    print(f"OK -> {EMBED_PATH}")


if __name__ == "__main__":
    main()
