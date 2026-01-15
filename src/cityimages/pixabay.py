import os
from dataclasses import dataclass
import re
from pathlib import Path

from dotenv import load_dotenv
import requests


# Load environment variables from .env file in the project root (if present)
load_dotenv()


@dataclass
class PixabayHit:
    id: int
    page_url: str
    tags: str
    image_url: str


def search_pixabay_images(query: str, per_page: int = 5):
    """Search Pixabay images and return hits."""
    key = os.getenv("PIXABAY_API_KEY", "")
    if not key:
        raise RuntimeError("Missing PIXABAY_API_KEY environment variable")

    # Pixabay requires per_page to be within a valid range.
    # According to the error message, very small values (like 1) are rejected.
    if per_page < 3:
        per_page = 3

    params = {
        "key": key,
        "q": query,
        "per_page": per_page,
        "safesearch": "true",
        "image_type": "photo",
    }

    resp = requests.get("https://pixabay.com/api/", params=params, timeout=30)
    # Helpful debug output so you can see Pixabay's error message, even on 400.
    print("Pixabay response:", resp.status_code, resp.text)
    resp.raise_for_status()  # put this back
    data = resp.json()

    hits: list[PixabayHit] = []
    for h in data.get("hits", []):
        image_url = h.get("largeImageURL") or h.get("webformatURL") or ""
        if image_url:
            hits.append(
                PixabayHit(
                    id=h.get("id", 0),
                    page_url=h.get("pageURL", ""),
                    tags=h.get("tags", ""),
                    image_url=image_url,
                )
            )
    return hits


def _safe_name(value: str) -> str:
    """Convert a query string into a safe folder/file name part."""
    value = value.strip()
    if not value:
        return "query"
    # Replace non-alphanumeric with hyphens, collapse duplicates.
    value = re.sub(r"[^A-Za-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "query"


def download_pixabay_images(query: str, out_dir: Path, limit: int = 5):
    """Download images from Pixabay."""
    hits = search_pixabay_images(query, per_page=limit)
    # Create a subfolder based on the query with Pixabay suffix, e.g. downloads/pixabay/Florence-Pixabay
    query_dir = out_dir / f"{_safe_name(query)}"
    query_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for i, hit in enumerate(hits, 1):
        dst = query_dir / f"{_safe_name(query)}--Pixabay--{i:02d}-{hit.id}.jpg"
        img_resp = requests.get(hit.image_url, timeout=60)
        img_resp.raise_for_status()
        dst.write_bytes(img_resp.content)
        saved.append(dst)
    return saved

