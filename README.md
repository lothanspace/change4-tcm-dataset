---
license: cc-by-nc-4.0
task_categories:
  - image-segmentation
tags:
  - lunar
  - chang-e-4
  - terrain-classification
  - segmentation
  - planetary-science
pretty_name: Chang'E-4 Terrain Classification Dataset
---

# Chang'E-4 TCM Dataset

Tools and data for terrain classification using Chang'E-4 Yutu-2 rover imagery.

> **Dataset:** Segmentation masks are available on [Hugging Face](https://huggingface.co/datasets/lothanspace/change4-tcm-dataset).

> **Note:** Original Chang'E-4 images are not included due to copyright restrictions. You must download the source images directly from CLPDS (see instructions below).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Convert PDS files to images
python scripts/convert_pds.py data/raw data/images
```

## Downloading Chang'E-4 Data

Data is available from China's Lunar and Planetary Data System (CLPDS).

### 1. Register an Account

1. Go to https://clpds.bao.ac.cn
2. Create an account (check spam folder for confirmation email from NAOC)

### 2. Download Data

1. Navigate to Chang'E-4 data search: https://clpds.bao.ac.cn/ce5web/searchOrder-ce4En.do
2. Select an instrument:
   - **PCAM** - Panoramic Camera (rover, stereo pairs)
   - **TCAM** - Terrain Camera (lander)
   - **LPR** - Lunar Penetrating Radar
   - **VNIS** - Visible/Near-IR Spectrometer
3. Choose data level (L2A or higher for calibrated data)
4. Add files to cart and process order
5. Download and extract to `data/raw/`

### Data Format

Chang'E-4 uses PDS4 format:
- XML label file (`.xml`) - metadata
- Data file (`.img`, `*L`) - image data

## Converting to Images

The conversion script applies debayering and contrast stretching:

```bash
# Convert all PDS files in data/raw to PNG
python scripts/convert_pds.py data/raw data/images

# Preview files without converting
python scripts/convert_pds.py data/raw data/images --dry-run

# Flatten output to single directory
python scripts/convert_pds.py data/raw data/images --flat
```

### Processing Steps

1. Read PDS4 file using `pds4_tools`
2. Debayer raw Bayer images (PCAM full-resolution)
3. Apply 2% linear contrast stretch
4. Save as PNG

## Project Structure

```
├── data/
│   ├── masks/        # Segmentation mask annotations (JSON)
│   ├── raw/          # Downloaded PDS4 files (you provide)
│   └── images/       # Converted PNG images (generated)
├── docs/
│   └── chinese-moon-data-access.md
├── scripts/
│   └── convert_pds.py
└── requirements.txt
```

## References

- [CLPDS Data Portal](https://clpds.bao.ac.cn)
- [Chang'E-4 Data Releases](https://moon.bao.ac.cn/pubMsg/detail-CE4EN.jsp)
- [CLPDS Overview Paper](https://link.springer.com/article/10.1007/s11214-021-00862-3)

## Citation

If you use this dataset in your research, please cite:

```bibtex
@misc{chang4tcm2025,
  author       = {Yu, Sam and Huang, Christoper and Nasika, Tanvi and Shao, Yi and Singhania, Amay},
  title        = {Chang'E-4 Terrain Classification Dataset},
  year         = {2026},
  organization = {Lothan Space, IHS Maker Club},
  publisher    = {HuggingFace},
  url          = {https://huggingface.co/datasets/lothanspace/change4-tcm-dataset}
}
```

Please also cite the original data source:

```bibtex
@misc{clpds2025,
  author       = {{Ground Research and Application System of China's Lunar and Planetary Exploration Program}},
  title        = {Chang'E-4 Scientific Data},
  publisher    = {China National Space Administration},
  url          = {https://moon.bao.ac.cn}
}
```

## License

The code and segmentation masks in this repository are licensed under [CC BY-NC 4.0](LICENSE) (Creative Commons Attribution-NonCommercial 4.0). You are free to use, share, and adapt for non-commercial purposes with attribution.

Original Chang'E-4 imagery is owned by CLPDS/NAOC and must be downloaded directly from their portal. See [docs/chinese-moon-data-access.md](docs/chinese-moon-data-access.md) for their citation requirements.
