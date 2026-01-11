# Accessing Chang'E-4 Rover Data

This guide explains how to access and download images and scientific data from China's Chang'E-4 mission and Yutu-2 rover.

## Chang'E-4 Mission Overview

Chang'E-4 achieved humanity's first soft landing on the lunar far side on January 3, 2019, landing in the Von Kármán crater. The mission includes a lander and the Yutu-2 rover, which continues to operate and explore the lunar surface.

**Key Facts:**
- **Launch**: December 8, 2018
- **Landing**: January 3, 2019
- **Location**: Von Kármán crater, lunar far side
- **Rover**: Yutu-2 (玉兔二号)
- **Data Format**: PDS4

## Chang'E-4 Instruments

| Instrument | Abbreviation | Description |
|------------|--------------|-------------|
| Landing Camera | LCAM | Descent imaging during landing |
| Terrain Camera | TCAM | Surface imaging from lander |
| Panoramic Camera | PCAM | 360° surface imaging from rover |
| Lunar Penetrating Radar | LPR | Subsurface structure detection |
| Visible and Near-Infrared Imaging Spectrometer | VNIS | Mineral composition analysis |
| Low Frequency Spectrometer | LFS | Radio astronomy observations |

## Data Portal

**Primary access point for Chang'E-4 data:**

- **Chang'E-4 Data Search**: https://clpds.bao.ac.cn/ce5web/searchOrder-ce4En.do
- **Main Portal**: https://moon.bao.ac.cn/web/enmanager/home
- **Contact**: lpdc@nao.cas.cn

The data is hosted by **China's Lunar and Planetary Data System (CLPDS)**, operated by the National Astronomical Observatories of China (NAOC).

## Registration Process

1. **Navigate to the portal**: Go to https://clpds.bao.ac.cn
2. **Create an account**: Click on the registration/login link
3. **Fill in the registration form**: Provide required information
4. **Download and submit registration form**: Some datasets require an additional form
5. **Check your spam folder**: Confirmation emails from NAOC may be incorrectly encoded

## Downloading Chang'E-4 Data

The download process works like online shopping:

1. **Log in** to your account
2. **Go to Chang'E-4 search**: https://clpds.bao.ac.cn/ce5web/searchOrder-ce4En.do
3. **Select an instrument**: PCAM, TCAM, LPR, VNIS, etc.
4. **Choose data level**: Typically Level 2A or higher for calibrated data
5. **Set time range** (optional): Filter by lunar day or date range
6. **Add to cart**: Select the data products you need
7. **Process order**: Submit to initiate download

## Data Processing Levels

| Level | Description | Availability |
|-------|-------------|--------------|
| L0 | Raw telemetry data | Not public |
| L1 | Depacketized, time-tagged | Not public |
| L2A | Calibrated, geolocated | Public |
| L2B | Mosaics and derived products | Public |
| L2C | Higher-level products | Public |

**Note:** Only calibrated L2+ data is publicly available. Raw L0/L1 telemetry remains proprietary.

## PDS4 Data Format

Chang'E-4 data uses PDS4 format. Each data product consists of:

- **XML label file** (`.xml`): Metadata describing the observation
- **Data file**: Image or measurement data (format varies by instrument)

Common image formats include `.img` or `.fits` files paired with their XML labels.

## Data Releases

Chang'E-4 data is released periodically in batches organized by lunar day. Check the data release announcements for the latest available data:

- [Chang'E-4 Data Release Announcements](https://moon.bao.ac.cn/pubMsg/detail-CE4EN.jsp)

## Usage Requirements

1. **Non-commercial use**: Data is for research and educational purposes
2. **Citation required**: Acknowledge the data source in publications
3. **Submit results**: Send publications to lpdc@nao.cas.cn

### Suggested Citation

```
Ground Research and Application System of China's Lunar and Planetary
Exploration Program. Chang'E-4 [Instrument] Data. China National Space
Administration, [Year]. https://moon.bao.ac.cn
```

## Troubleshooting

- **Service instability**: The portal may be slow for overseas users. Retry if needed.
- **Language**: Some pages are Chinese-only. Use browser translation.
- **JavaScript required**: The data portal requires JavaScript enabled.

## Other Chang'E Missions

For context, other missions in the Chinese Lunar Exploration Program:

| Mission | Year | Description |
|---------|------|-------------|
| Chang'E-1 | 2007 | Lunar orbiter |
| Chang'E-2 | 2010 | Lunar orbiter, higher resolution |
| Chang'E-3 | 2013 | Near-side lander + Yutu rover |
| Chang'E-5 | 2020 | Sample return (1,731g) |
| Chang'E-6 | 2024 | Far-side sample return (1,935g) |

## References

- [CLPDS Overview Paper (Space Science Reviews)](https://link.springer.com/article/10.1007/s11214-021-00862-3)
- [Planetary Society Guide to Downloading Chang'e Data](http://www.planetary.org/blogs/guest-blogs/2016/01221450-china-invites-public-on-board.html)
- [Chang'E-4 Data Release Announcement](https://moon.bao.ac.cn/pubMsg/detail-CE4EN.jsp)
