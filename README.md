#  The province of Bergamo LULC–LST Processing ( from2002 to 2022, a 4-year interval)

This repository contains code and visual documentation for extracting spatial landscape metrics from MODIS satellite data to analyze the relationship between **land use/land cover (LULC)** and **land surface temperature (LST)** in the **province of Bergamo, Italy**.

The focus of this dataset is on **August 2006**, as part of a broader temporal analysis from **2002 to 2022**, with **4-year intervals**.

---

## 📁 Contents

### 🔹 Scripts

- **`2006EXTRACTN.py`**  
  Processes MODIS tiles by separating LULC and LST bands. Converts LULC to ASCII grid format for landscape metrics analysis.

- **`FINALCSV2006.py`**  
  Calculates landscape metrics using `pylandstats` over 3x3 pixel windows and exports a final structured CSV.

---

### 📊 Output

- **`local_metrics_final_3x3.csv`**  
  Contains spatial metrics (PLAND, ED, FRAC, LSI, LPI) for 3x3 pixel patches, ready for machine learning or statistical analysis.

---

## 🧮 Extracted Metrics

- **PLAND**: % of each land type within the patch  
- **ED**: Edge density, total length of edge per unit area  
- **FRAC**: Fractal dimension, patch shape complexity  
- **LSI**: Landscape shape index, relative to standard shape  
- **LPI**: Largest patch index, dominance of the largest patch  

---

## 📦 Requirements

- `rasterio`  
- `pylandstats`  
- `pandas`  
- `numpy`  
- `tqdm`

---

## 🗺️ Data Source & Extraction

All data were extracted from **MODIS** via **Google Earth Engine (GEE)** using shapefiles generated in QGIS. The steps are illustrated in the diagram below:

![Processing Flowchart](path/to/flowchart.png) <!-- ← replace with actual relative path -->

---

## 🖼️ Visual Output – Example for August 2002

These figures illustrate the type of LST and LULC classification used in this project. Although this repository focuses on **2006**, the procedure is identical across all years.

### 🔥 LST map for Bergamo (MODIS MOD11A2 – August 2002)
![LST Map](path/to/LST_map.png) <!-- ← replace with actual relative path -->

### 🌱 LULC classification (MODIS MCD12Q1 – August 2002)
![LULC Map](path/to/LULC_map.png) <!-- ← replace with actual relative path -->

---

## 📌 Project Scope

This work is part of a broader **landscape metrics & urban heat study**, which analyzes the spatial and temporal evolution of land cover and surface temperature across **six years**:

- **2002**, 2006, 2010, 2014, 2018, **2022**

Each year focuses on **August** to minimize seasonal variability.

---

## 📬 Contact

For questions, suggestions, or collaboration, feel free to reach out via GitHub Issues or email.
