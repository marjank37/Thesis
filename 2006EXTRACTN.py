import rasterio
from osgeo import gdal
import os

# map
tiles_folder = r"D:\thesis\converting\2006"

# each tif
for i in range(4):
    tile_path = os.path.join(tiles_folder, f"Bergamo_2006_Tile_{i}.tif")

    with rasterio.open(tile_path) as src:
        print(f"Tile {i} - Bands:", src.count)

        #  read
        band1 = src.read(1)  # LULC
        band2 = src.read(2)  # LST

        profile = src.profile
        profile.update(count=1)

        # save LULC
        lulc_path = os.path.join(tiles_folder, f"Bergamo_LULC_200608_Tile_{i}.tif")
        with rasterio.open(lulc_path, 'w', **profile) as dst:
            dst.write(band1, 1)

        # save LST
        lst_path = os.path.join(tiles_folder, f"Bergamo_LST_200608_Tile_{i}.tif")
        with rasterio.open(lst_path, 'w', **profile) as dst:
            dst.write(band2, 1)

        #  ASCII Grid (.asc)
        asc_path = os.path.join(tiles_folder, f"Bergamo_LULC_200608_Tile_{i}.asc")
        gdal.Translate(asc_path, lulc_path, format="AAIGrid")

        print(f"✅ Tile {i} done - ASC created: {asc_path}")

print("🎯 All tiles processed!")
