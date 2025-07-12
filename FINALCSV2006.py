import rasterio
import numpy as np
import pandas as pd
from tqdm import tqdm
import pylandstats as pls
import os

# === File Paths ===
base_path = "D:/thesis/converting/2006"
output_csv = os.path.join(base_path, "local_metrics_final_3x3.csv")
year = 2006

# === MODIS IGBP Class Names ===
lulc_class_names = {
    0: 'Water',
    1: 'Evergreen Needleleaf Forest',
    2: 'Evergreen Broadleaf Forest',
    3: 'Deciduous Needleleaf Forest',
    4: 'Deciduous Broadleaf Forest',
    5: 'Mixed Forests',
    6: 'Closed Shrublands',
    7: 'Open Shrublands',
    8: 'Woody Savannas',
    9: 'Savannas',
    10: 'Grasslands',
    11: 'Permanent Wetlands',
    12: 'Croplands',
    13: 'Urban and Built-Up',
    14: 'Cropland/Natural Vegetation Mosaic',
    15: 'Snow and Ice',
    16: 'Barren or Sparsely Vegetated',
    254: 'Unclassified',
    255: 'Fill Value'
}

# === Parameters ===
window_size = 3
pad = window_size // 2

# === Initialize ===
all_data_rows = []
nodata_count_total = 0

# === Process Each Tile ===
for tile_id in range(4):
    print(f"\n🔹 Processing tile {tile_id}...")

    lulc_path = os.path.join(base_path, f"Bergamo_LULC_200608_Tile_{tile_id}.asc")
    lst_path = os.path.join(base_path, f"Bergamo_LST_200608_Tile_{tile_id}.tif")

    # Load LULC
    with rasterio.open(lulc_path) as src:
        lulc = src.read(1)
        lulc_transform = src.transform
        lulc_nodata = src.nodata or -9999
        lulc_res = src.res
        rows, cols = lulc.shape

    # Load LST
    with rasterio.open(lst_path) as lst_src:
        lst = lst_src.read(1)

    # Pad arrays
    lulc_padded = np.pad(lulc, pad, mode='constant', constant_values=lulc_nodata)
    lst_padded = np.pad(lst, pad, mode='constant', constant_values=np.nan)

    nodata_count_tile = 0

    for row in tqdm(range(pad, pad + rows), desc=f"Tile {tile_id}"):
        for col in range(pad, pad + cols):
            lulc_win = lulc_padded[row - pad:row + pad + 1, col - pad:col + pad + 1]
            lst_val = lst_padded[row, col]
            center_val = lulc_win[pad, pad]

            if center_val == lulc_nodata or np.isnan(lst_val):
                nodata_count_tile += 1
                continue

            try:
                landscape = pls.Landscape(lulc_win, res=lulc_res, nodata=lulc_nodata)
                class_metrics = landscape.compute_class_metrics_df()

                if center_val not in class_metrics.index:
                    continue

                metrics = class_metrics.loc[center_val]
                x, y = rasterio.transform.xy(lulc_transform, row - pad, col - pad)

                all_data_rows.append({
                    'X': x,
                    'Y': y,
                    'LULC_ID': center_val,
                    'LULC_Name': lulc_class_names.get(center_val, 'Unknown'),
                    'PLAND': metrics.get('proportion_of_landscape', np.nan),
                    'ED': metrics.get('edge_density', np.nan),
                    'FRAC': metrics.get('fractal_dimension_mn', np.nan),
                    'LSI': metrics.get('landscape_shape_index', np.nan),
                    'LPI': metrics.get('largest_patch_index', np.nan),
                    'LST': lst_val,
                    'Year': year,
                    'Tile_ID': tile_id
                })
            except Exception:
                continue

    print(f"❌ NoData pixels in tile {tile_id}: {nodata_count_tile}")
    nodata_count_total += nodata_count_tile

# === Save to CSV ===
df = pd.DataFrame(all_data_rows)
df.to_csv(output_csv, index=False)

# === Summary ===
print("\n✅ Done. File saved to:", output_csv)
print("✅ Total valid rows:", len(df))
print("❌ Total NoData pixels skipped:", nodata_count_total)
