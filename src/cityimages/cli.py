import argparse
from pathlib import Path

from pixabay import download_pixabay_images


def main():
    print("Downloading images from Pixabay...")
    out_dir = Path("downloads/pixabay")
    paths = download_pixabay_images("Florence", out_dir, limit=1)


    # parser = argparse.ArgumentParser(description="Download images from Pixabay")
    # parser.add_argument("--query", default="cat", help="Search query")
    # parser.add_argument("--limit", type=int, default=5, help="Number of images")
    # parser.add_argument("--out-dir", default="downloads/pixabay", help="Output directory")

    # args = parser.parse_args()
    # paths = download_pixabay_images(args.query, Path(args.out_dir), args.limit)

    for p in paths:
        print(p)

if __name__ == "__main__":
    main()