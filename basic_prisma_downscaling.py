import numpy as np
import os
from spectral.io import envi
from scipy.ndimage import zoom
from osgeo import gdal

# INPUT PATHS 
prisma_hdr = r"D:\Agri_Geospatial\PRS_L2D_STD_20250407052539_20250407052543_0001\PRS_L2D_STD_20250407052539_20250407052543_0001_VNIR_Cube.hdr"
sentinel_folder = r"D:\Agri_Geospatial\Sentinel2_processed\S2_resampled"
sentinel_band_names = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12']
output_img = r"D:\Agri_Geospatial\PRISMA_downscaled.img"

# Load PRISMA Hyperspectral Image 
prisma = envi.open(prisma_hdr)
prisma_data = prisma.load().astype(np.float32)
H, W, L = prisma_data.shape
print(f"PRISMA Loaded: {prisma_data.shape}")

# Load All Sentinel-2 Bands and Check for Consistency 
sample_shape = None
for bname in sentinel_band_names:
    hdr_path = os.path.join(sentinel_folder, f"{bname}.hdr")
    img_path = hdr_path.replace(".hdr", ".img")
    band = np.squeeze(envi.open(hdr_path, img_path).load().astype(np.float32))  # <-- Fix here

    if sample_shape is None:
        sample_shape = band.shape
    elif band.shape != sample_shape:
        raise ValueError(f"Shape mismatch in {bname}: expected {sample_shape}, got {band.shape}")

target_H, target_W = sample_shape
zoom_y = target_H / H
zoom_x = target_W / W
print(f"Target size from Sentinel-2: {target_H} x {target_W}")
print(f"Zoom factors: Y={zoom_y:.3f}, X={zoom_x:.3f}")

# Create Output File in ENVI Format 
driver = gdal.GetDriverByName("ENVI")
output_ds = driver.Create(output_img, target_W, target_H, L, gdal.GDT_Float32)

# Downscale PRISMA Bands 
for i in range(L):
    band = prisma_data[:, :, i]
    downscaled_band = zoom(band, (zoom_y, zoom_x), order=3)  
    output_ds.GetRasterBand(i + 1).WriteArray(downscaled_band)
    print(f"Band {i+1}/{L} written")

output_ds.FlushCache()
output_ds = None
print(f"Saved downscaled PRISMA image to: {output_img}")

# Applying Georeferencing 
ref_band_img = os.path.join(sentinel_folder, "B4.img")
ref_ds = gdal.Open(ref_band_img)

if ref_ds is None:
    raise FileNotFoundError("Sentinel-2 B4 reference image not found!")

target_ds = gdal.Open(output_img, gdal.GA_Update)
target_ds.SetGeoTransform(ref_ds.GetGeoTransform())
target_ds.SetProjection(ref_ds.GetProjection())
target_ds = None
print("Georeferencing applied successfully")
