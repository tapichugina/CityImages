import os
from pathlib import Path

import pytest

from cityimages.pixabay import download_pixabay_images


@pytest.mark.skipif(
    not os.getenv("PIXABAY_API_KEY"),
    reason="PIXABAY_API_KEY is not set; real Pixabay API key required for this test.",
)
def test_download_one_new_york_image(tmp_path: Path) -> None:
    """Integration test: download a single 'New York' image from Pixabay."""
    out_dir = tmp_path / "images"

    paths = download_pixabay_images("New York", out_dir, limit=1)

    assert len(paths) == 1
    img_path = paths[0]

    # File should exist and be non-empty
    assert img_path.is_file()
    assert img_path.stat().st_size > 0

