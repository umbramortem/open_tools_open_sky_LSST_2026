#!/usr/bin/env python3
"""Download public hackathon data products from Google Drive.

Usage:
    python scripts/download_drive_data.py --config config/data_sources.json
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import zipfile
from pathlib import Path

import gdown


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download public Google Drive files or folders listed in a JSON configuration."
    )
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to data_sources.json",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing output files or folders.",
    )
    return parser.parse_args()


def load_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as stream:
        config = json.load(stream)
    if "downloads" not in config or not isinstance(config["downloads"], list):
        raise ValueError("The configuration must contain a 'downloads' list.")
    return config


def remove_existing(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def unpack_zip(path: Path) -> Path:
    target = path.with_suffix("")
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "r") as archive:
        archive.extractall(target)
    return target


def download_entry(entry: dict, overwrite: bool) -> None:
    name = entry.get("name", "unnamed_product")
    url = entry.get("url")
    output = Path(entry.get("output", f"data/{name}"))
    is_folder = bool(entry.get("folder", False))
    should_unpack = bool(entry.get("unpack", False))

    if not url or url.startswith("REPLACE_WITH"):
        print(f"[SKIP] {name}: replace the placeholder Drive URL first.")
        return

    if output.exists():
        if not overwrite:
            print(f"[SKIP] {name}: {output} already exists. Use --overwrite to replace it.")
            return
        remove_existing(output)

    output.parent.mkdir(parents=True, exist_ok=True)
    print(f"[DOWNLOAD] {name}")
    print(f"  URL: {url}")
    print(f"  Output: {output}")

    if is_folder:
        output.mkdir(parents=True, exist_ok=True)
        result = gdown.download_folder(
            url=url,
            output=str(output),
            quiet=False,
            use_cookies=False,
        )
        if not result:
            raise RuntimeError(f"Folder download failed: {name}")
    else:
        result = gdown.download(
            url=url,
            output=str(output),
            quiet=False,
            fuzzy=True,
            resume=True,
        )
        if result is None:
            raise RuntimeError(f"File download failed: {name}")

    if should_unpack:
        if output.suffix.lower() != ".zip":
            raise ValueError(f"Automatic unpacking currently supports ZIP files only: {output}")
        unpacked = unpack_zip(output)
        print(f"[UNPACKED] {unpacked}")

    print(f"[DONE] {name}")


def main() -> int:
    args = parse_args()
    config = load_config(args.config)

    for entry in config["downloads"]:
        download_entry(entry, overwrite=args.overwrite)

    print("All configured downloads have been processed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise
