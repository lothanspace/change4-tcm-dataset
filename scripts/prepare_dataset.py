#!/usr/bin/env python3
"""Prepare local derivatives from LabelMe JSON annotations.

By default this script generates indexed mask PNGs and a metadata.jsonl file.
It can also strip base64 imageData from the JSON files without generating any
derived assets, which is useful when publishing only the raw annotations to
Hugging Face.

Class mapping (index -> label):
    0: background
    1: crater
    2: shadow
    3: surface
    4: rock
    5: soil
    6: rover
    7: space
    8: rocker

Usage:
    python scripts/prepare_dataset.py
    python scripts/prepare_dataset.py --skip-strip   # keep imageData in JSONs
    python scripts/prepare_dataset.py --strip-only   # only strip imageData
"""

import argparse
import glob
import json
import os
import sys

from PIL import Image, ImageDraw

# Ordered by frequency (background=0 is reserved for unlabeled pixels)
CLASS_LABELS = {
    "background": 0,
    "crater": 1,
    "shadow": 2,
    "surface": 3,
    "rock": 4,
    "soil": 5,
    "rover": 6,
    "space": 7,
    "rocker": 8,
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASKS_DIR = os.path.join(ROOT, "data", "masks")
MASKS_PNG_DIR = os.path.join(ROOT, "data", "masks_png")
METADATA_PATH = os.path.join(ROOT, "data", "metadata.jsonl")


def render_mask(annotation: dict) -> Image.Image:
    """Render a LabelMe annotation dict as an indexed mask image."""
    w = annotation["imageWidth"]
    h = annotation["imageHeight"]
    mask = Image.new("L", (w, h), 0)  # 0 = background
    draw = ImageDraw.Draw(mask)

    for shape in annotation.get("shapes", []):
        label = shape["label"]
        class_idx = CLASS_LABELS.get(label, 0)
        points = shape["points"]

        if shape["shape_type"] == "polygon":
            polygon = [(p[0], p[1]) for p in points]
            if len(polygon) >= 3:
                draw.polygon(polygon, fill=class_idx)
        elif shape["shape_type"] == "rectangle":
            if len(points) == 2:
                x0, y0 = points[0]
                x1, y1 = points[1]
                draw.rectangle(
                    [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)],
                    fill=class_idx,
                )

    return mask


def strip_image_data(json_path: str) -> None:
    """Remove base64 imageData from a LabelMe JSON file in-place."""
    with open(json_path, "r") as f:
        data = json.load(f)

    if data.get("imageData") is None:
        return  # already stripped

    data["imageData"] = None
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Prepare HF dataset from LabelMe annotations")
    parser.add_argument("--skip-strip", action="store_true", help="Don't strip imageData from JSONs")
    parser.add_argument(
        "--strip-only",
        action="store_true",
        help="Only strip imageData from JSONs; don't generate PNGs or metadata",
    )
    args = parser.parse_args()

    if args.strip_only and args.skip_strip:
        parser.error("--strip-only and --skip-strip cannot be used together")

    json_files = sorted(glob.glob(os.path.join(MASKS_DIR, "*.json")))
    if not json_files:
        print(f"No JSON files found in {MASKS_DIR}", file=sys.stderr)
        sys.exit(1)

    if args.strip_only:
        stripped_count = 0
        for i, json_path in enumerate(json_files):
            with open(json_path, "r") as f:
                annotation = json.load(f)
            if annotation.get("imageData") is not None:
                strip_image_data(json_path)
                stripped_count += 1

            if (i + 1) % 50 == 0 or (i + 1) == len(json_files):
                print(f"  [{i + 1}/{len(json_files)}] processed")

        print(f"\nDone: stripped imageData from {stripped_count}/{len(json_files)} JSON files")
        return

    os.makedirs(MASKS_PNG_DIR, exist_ok=True)

    metadata_entries = []
    for i, json_path in enumerate(json_files):
        basename = os.path.splitext(os.path.basename(json_path))[0]
        png_name = f"{basename}.png"
        png_path = os.path.join(MASKS_PNG_DIR, png_name)

        with open(json_path, "r") as f:
            annotation = json.load(f)

        # Render mask PNG
        mask = render_mask(annotation)
        mask.save(png_path)

        # Build metadata entry — normalize Windows-style paths from LabelMe
        raw_image_path = annotation.get("imagePath", "")
        image_fname = os.path.basename(raw_image_path.replace("\\", "/"))
        metadata_entries.append({
            "file_name": f"masks_png/{png_name}",
            "annotation_json": f"masks/{os.path.basename(json_path)}",
            "image_filename": image_fname,
            "width": annotation["imageWidth"],
            "height": annotation["imageHeight"],
            "num_shapes": len(annotation.get("shapes", [])),
        })

        # Strip imageData
        if not args.skip_strip:
            strip_image_data(json_path)

        if (i + 1) % 50 == 0 or (i + 1) == len(json_files):
            print(f"  [{i + 1}/{len(json_files)}] processed")

    # Write metadata.jsonl
    with open(METADATA_PATH, "w") as f:
        for entry in metadata_entries:
            f.write(json.dumps(entry) + "\n")

    print(f"\nDone: {len(json_files)} masks written to {MASKS_PNG_DIR}")
    print(f"Metadata written to {METADATA_PATH}")
    if not args.skip_strip:
        print(f"Stripped imageData from {len(json_files)} JSON files")

    # Write class mapping as a separate reference file
    class_map_path = os.path.join(ROOT, "data", "class_labels.json")
    with open(class_map_path, "w") as f:
        json.dump(CLASS_LABELS, f, indent=2)
    print(f"Class labels written to {class_map_path}")


if __name__ == "__main__":
    main()
