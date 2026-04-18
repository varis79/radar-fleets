"""
Listado canónico de framing interno prohibido en la capa visible.

La fuente primaria es prompts/qa-checklist.md (generado en PR de MVP).
Este módulo expone dos cosas:
  - FORBIDDEN_PATTERNS: regex compilados para detección rápida
  - FORBIDDEN_HUMAN: lista legible para informes

Cuando hay que añadir una expresión nueva, se edita prompts/qa-checklist.md.
"""
from __future__ import annotations
import re

# Patrones visibles prohibidos. Cada entrada es (regex, descripción-humana).
# regex se aplica case-insensitive y con bordes \b cuando aplica.
_RAW = [
    # Framing competitivo
    (r"\bcompetidor(es)?\b", "Término 'competidor' (visible)"),
    (r"\bcompetidor\s+(directo|pulpopay|/)", "Competidor directo / Competidor PulpoPay"),
    (r"\bcompetitor watch\b", "Competitor Watch (encabezado interno)"),
    (r"\bvigilancia\s+competitiva\b", "Vigilancia competitiva"),
    (r"\bse[nñ]al\s+competitiva\b", "Señal competitiva"),

    # Oportunidad comercial
    (r"\boportunidad\s+(partner|de\s+partner|comercial)\b", "Oportunidad partner/comercial"),
    (r"\bargumento\s+(comercial|de\s+mercado\s+m[aá]s)\b", "Argumento comercial"),

    # Producto interno
    (r"\breferencia\s+de\s+producto\b", "Referencia de producto (label interno)"),
    (r"\binspiraci[oó]n\s+de\s+producto\b", "Inspiración de producto"),

    # Cliente interno
    (r"\beducaci[oó]n\s+al\s+cliente\b", "Educación al cliente"),

    # Pulpo como sujeto interno
    (r"\bpara\s+pulpo\b", "'Para Pulpo' (interno)"),
    (r"\bpulpo\s+debe\b", "'Pulpo debe' (interno)"),
    (r"\bpulpo\s+necesita\b", "'Pulpo necesita' (interno)"),
    (r"\bpulpopay\s+necesita\b", "'PulpoPay necesita' (interno)"),
    (r"\broadmap\s+de\s+pulpo\b", "Roadmap de Pulpo (interno)"),
    (r"\btesis\s+de\s+producto\s+de\s+pulpo\b", "Tesis de producto de Pulpo"),
    (r"\bimplicaci[oó]n\s+para\s+pulpo\b", "Implicación para Pulpo"),

    # Clasificación interna visible
    (r"<span[^>]*>[\s]*(competidor(\s+pulpopay|\s+directo|\s*/\s*referencia|\s*/\s*se[nñ]al)?|oportunidad\s+partner|referencia\s+de\s+producto|inspiraci[oó]n\s+de\s+producto|se[nñ]al\s+competitiva|educaci[oó]n\s+al\s+cliente)[\s]*</span>",
     "Pill o tag visible con clasificación interna"),
]

FORBIDDEN_PATTERNS = [(re.compile(rx, re.IGNORECASE | re.UNICODE), human) for rx, human in _RAW]
FORBIDDEN_HUMAN = [human for _, human in _RAW]


def scan_text(text: str) -> list[tuple[str, str]]:
    """Devuelve lista de (human_label, matched_substring) ocurrencias de framing prohibido."""
    hits: list[tuple[str, str]] = []
    for pat, human in FORBIDDEN_PATTERNS:
        for m in pat.finditer(text):
            matched = m.group(0)
            # limpia substring para legibilidad
            if len(matched) > 160:
                matched = matched[:157] + "..."
            hits.append((human, matched.strip()))
    return hits
