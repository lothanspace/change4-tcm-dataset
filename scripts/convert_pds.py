#!/usr/bin/env python3
"""
Convert Chang'E-4 PDS4 image files to PNG format.

Usage:
    python scripts/convert_pds.py data/raw data/images

This script reads PDS4 files from the input directory, applies debayering
and contrast stretching, then saves the results as PNG images.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from pds4_tools import pds4_read
from skimage import exposure
from skimage.util import img_as_float
from colour_demosaicing import demosaicing_CFA_Bayer_Menon2007
import colour


def read_pds(path: Path) -> np.ndarray:
    """Read a PDS4 image file and return as float array."""
    data = pds4_read(str(path), quiet=True)
    img = np.array(data[0].data)
    return img_as_float(img)


def debayer(img: np.ndarray, pattern: str = "RGGB") -> np.ndarray:
    """Convert Bayer pattern image to RGB."""
    debayered = demosaicing_CFA_Bayer_Menon2007(img, pattern)
    return colour.cctf_encoding(debayered)


def stretch(img: np.ndarray, percentile: float = 2.0) -> np.ndarray:
    """Apply linear contrast stretch using percentile clipping."""
    p_low, p_high = np.percentile(img, (percentile, 100 - percentile))
    return exposure.rescale_intensity(img, in_range=(p_low, p_high))


def save_image(img: np.ndarray, path: Path) -> None:
    """Save float image array as PNG."""
    img_uint8 = np.uint8(np.clip(img, 0, 1) * 255)
    Image.fromarray(img_uint8).save(path)


def convert_pds_file(input_path: Path, output_path: Path) -> bool:
    """
    Convert a single PDS file to PNG.

    Returns True on success, False on failure.
    """
    try:
        img = read_pds(input_path)

        # PCAM full resolution images need debayering
        # Dimensions: 1728x2352 for raw Bayer, 864x1176 for already processed
        if img.shape == (1728, 2352):
            img = debayer(img)
        elif len(img.shape) == 2 and img.shape not in [(864, 1176)]:
            # Unknown grayscale format, try debayering if dimensions suggest Bayer
            if img.shape[0] > 500 and img.shape[1] > 500:
                img = debayer(img)

        img = stretch(img)
        save_image(img, output_path)
        return True

    except Exception as e:
        print(f"Error converting {input_path}: {e}", file=sys.stderr)
        return False


def find_pds_files(directory: Path) -> list[Path]:
    """Find all PDS4 image files in directory (recursively)."""
    pds_files = []

    # PDS4 data files typically end with these extensions
    patterns = ["*.*L", "*.img", "*.IMG", "*.dat", "*.DAT"]

    for pattern in patterns:
        pds_files.extend(directory.rglob(pattern))

    # Filter out XML label files
    pds_files = [f for f in pds_files if not f.suffix.lower() == ".xml"]

    return sorted(set(pds_files))


def main():
    parser = argparse.ArgumentParser(
        description="Convert Chang'E-4 PDS4 files to PNG images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/convert_pds.py data/raw data/images
    python scripts/convert_pds.py ./PCAM ./output --flat
        """,
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing PDS4 files",
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Directory for output PNG images",
    )
    parser.add_argument(
        "--flat",
        action="store_true",
        help="Output all files to single directory (ignore subdirectory structure)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be converted without converting",
    )

    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"Error: Input directory does not exist: {args.input_dir}", file=sys.stderr)
        sys.exit(1)

    pds_files = find_pds_files(args.input_dir)

    if not pds_files:
        print(f"No PDS files found in {args.input_dir}")
        sys.exit(0)

    print(f"Found {len(pds_files)} PDS files")

    if args.dry_run:
        for f in pds_files:
            print(f"  {f}")
        sys.exit(0)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    fail_count = 0

    for pds_file in pds_files:
        # Determine output path
        if args.flat:
            output_path = args.output_dir / f"{pds_file.stem}.png"
        else:
            # Preserve subdirectory structure
            rel_path = pds_file.relative_to(args.input_dir)
            output_path = args.output_dir / rel_path.with_suffix(".png")
            output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Converting: {pds_file.name} -> {output_path.name}")

        if convert_pds_file(pds_file, output_path):
            success_count += 1
        else:
            fail_count += 1

    print(f"\nDone: {success_count} converted, {fail_count} failed")


if __name__ == "__main__":
    main()
