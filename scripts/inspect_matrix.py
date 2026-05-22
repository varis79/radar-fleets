"""
Inspeccion de la matriz long-tail.

Imprime estadísticas y muestra ejemplos de páginas. Útil para validar la
matriz ANTES de invertir en generación de contenido masivo.

Uso:
    python -m scripts.inspect_matrix              # stats global
    python -m scripts.inspect_matrix --tier 1     # solo Tier 1
    python -m scripts.inspect_matrix --market mexico
    python -m scripts.inspect_matrix --topic telematica
    python -m scripts.inspect_matrix --csv > matrix.csv   # exportar a CSV
    python -m scripts.inspect_matrix --slugs       # solo lista de slugs
"""
from __future__ import annotations
import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.lib.pillar import enumerate_pages, summarize, PillarPage


def print_summary(pages: list[PillarPage]) -> None:
    s = summarize(pages)
    print("══════════════════════════════════════════════════════════════════════")
    print(f"  Matriz long-tail · {s['total_pages']} páginas planeadas")
    print("══════════════════════════════════════════════════════════════════════")
    print()
    print("Por DIMENSIÓN (origen de la página):")
    for dim, n in sorted(s["by_dimension"].items(), key=lambda kv: -kv[1]):
        bar = "█" * int(n / max(s["by_dimension"].values()) * 30)
        print(f"  {dim:20s} {n:>4}  {bar}")
    print()
    print("Por tier (ciclo de vida):")
    for tier in [1, 2, 3]:
        n = s["by_tier"][tier]
        review = s["review_schedule_days"][tier]
        bar = "█" * int(n / max(s["by_tier"].values()) * 30) if max(s["by_tier"].values()) else ""
        print(f"  T{tier} ({review:>3}d revisión)  {n:>4}  {bar}")
    print()
    print("Por mercado:")
    for m, n in s["by_market"].items():
        bar = "█" * int(n / max(s["by_market"].values()) * 30)
        print(f"  {m:25s} {n:>4}  {bar}")
    print()
    print("Por topic/dimension item (top 15):")
    for i, (t, n) in enumerate(s["by_topic"].items()):
        if i >= 15:
            break
        bar = "█" * int(n / max(s["by_topic"].values()) * 25)
        print(f"  {t:35s} {n:>4}  {bar}")
    print()
    print("Por intent:")
    for it, n in s["by_intent"].items():
        bar = "█" * int(n / max(s["by_intent"].values()) * 30)
        print(f"  {it:20s} {n:>4}  {bar}")
    print()
    print(f"Páginas con slot PulpoPay: {s['pulpopay_relevant']}")
    print()


def print_samples(pages: list[PillarPage], n_per_tier: int = 5) -> None:
    print("══════════════════════════════════════════════════════════════════════")
    print(f"  Muestras por tier ({n_per_tier} por cada)")
    print("══════════════════════════════════════════════════════════════════════")
    for tier in [1, 2, 3]:
        tier_pages = [p for p in pages if p.tier == tier]
        print(f"\n  ── Tier {tier} ({len(tier_pages)} páginas) ──")
        for p in tier_pages[:n_per_tier]:
            pp = " 💳" if p.pulpopay_relevant else "   "
            print(f"    {pp} /temas/{p.slug}/")
            print(f"        {p.label}")


def print_slugs(pages: list[PillarPage]) -> None:
    for p in pages:
        print(p.slug)


def export_csv(pages: list[PillarPage]) -> None:
    w = csv.writer(sys.stdout)
    w.writerow(["dimension", "slug", "label", "market", "topic_code", "intent", "tier",
                "review_days", "schema_type", "pulpopay", "url_path"])
    for p in pages:
        w.writerow([p.dimension, p.slug, p.label, p.market_code, p.topic_code,
                    p.intent_code, p.tier, p.review_days, p.schema_type,
                    p.pulpopay_relevant, p.url_path()])


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--tier", type=int, choices=[1, 2, 3])
    p.add_argument("--market")
    p.add_argument("--topic")
    p.add_argument("--intent")
    p.add_argument("--dimension", choices=["topic", "use-case", "vertical", "subgeo"])
    p.add_argument("--csv", action="store_true")
    p.add_argument("--slugs", action="store_true")
    p.add_argument("--samples", type=int, default=5)
    args = p.parse_args(argv)

    pages = enumerate_pages()

    if args.tier:
        pages = [p for p in pages if p.tier == args.tier]
    if args.market:
        pages = [p for p in pages if p.market_code == args.market]
    if args.topic:
        pages = [p for p in pages if p.topic_code == args.topic]
    if args.intent:
        pages = [p for p in pages if p.intent_code == args.intent]
    if args.dimension:
        pages = [p for p in pages if p.dimension == args.dimension]

    if args.csv:
        export_csv(pages)
    elif args.slugs:
        print_slugs(pages)
    else:
        print_summary(pages)
        print_samples(pages, n_per_tier=args.samples)

    return 0


if __name__ == "__main__":
    sys.exit(main())
