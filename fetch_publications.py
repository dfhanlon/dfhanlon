#!/usr/bin/env python3
"""
Fetch publications from Google Scholar and write _data/publications.yml.

Usage:
    python3 fetch_publications.py

Run this whenever you want to refresh your publications list.
Requires: pip install scholarly pyyaml
"""

import time
import yaml
from scholarly import scholarly

SCHOLAR_ID = "vN1PrFsAAAAJ"
OUTPUT_FILE = "_data/publications.yml"


def infer_type(citation: str, journal: str = "") -> str:
    citation_lower = citation.lower()
    journal_lower = journal.lower()
    if "arxiv" in citation_lower or "arxiv" in journal_lower:
        return "preprint"
    if any(k in citation_lower for k in ["memorial university", "thesis", "dissertation"]):
        return "thesis"
    if any(k in citation_lower for k in ["march meeting", "conference", "symposium", "abstract"]):
        return "conference"
    return "journal"


def fetch_publications():
    print(f"Fetching author profile for {SCHOLAR_ID}...")
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["publications"])
    pubs = author["publications"]
    print(f"Found {len(pubs)} publications. Fetching details...")

    records = []
    for i, pub in enumerate(pubs):
        print(f"  [{i+1}/{len(pubs)}] fetching details...")
        try:
            filled = scholarly.fill(pub)
        except Exception as e:
            print(f"    Warning: could not fill pub {i+1}: {e}")
            filled = pub

        bib = filled.get("bib", {})
        pub_type = infer_type(
            bib.get("citation", ""),
            bib.get("journal", bib.get("booktitle", "")),
        )

        record = {
            "id": i + 1,
            "title": bib.get("title", ""),
            "authors": bib.get("author", ""),
            "year": int(bib.get("pub_year", 0)) if bib.get("pub_year") else None,
            "journal": bib.get("journal") or bib.get("booktitle") or bib.get("school") or "",
            "citation": bib.get("citation", ""),
            "abstract": bib.get("abstract", ""),
            "url": filled.get("pub_url", ""),
            "num_citations": filled.get("num_citations", 0),
            "type": pub_type,
        }
        records.append(record)
        time.sleep(1)

    # Sort: journals first, then preprints, then others; newest first within each group
    order = {"journal": 0, "preprint": 1, "conference": 2, "thesis": 3}
    records.sort(key=lambda r: (order.get(r["type"], 9), -(r["year"] or 0)))

    with open(OUTPUT_FILE, "w") as f:
        yaml.dump(records, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"\nWrote {len(records)} publications to {OUTPUT_FILE}")


if __name__ == "__main__":
    fetch_publications()
