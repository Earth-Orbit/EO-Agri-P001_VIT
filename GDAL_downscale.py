from osgeo import gdal
import os

# INPUTS
prisma_path = r"D:\Agri_Geospatial\Coreg_output\Prisma_area3_coregistered.img"
sentinel_path = r"D:\Agri_Geospatial\Sentinel2_processed\S2_20250405_area3.img"
output_path = r"D:\Agri_Geospatial\Resampled\Prisma_downscaled_area3.tif"

# Ensure output folder exists 
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Open Sentinel for geotransform and projection
sentinel_ds = gdal.Open(sentinel_path)
if not sentinel_ds:
    raise RuntimeError("Cannot open Sentinel-2 reference image.")

geo_transform = sentinel_ds.GetGeoTransform()
projection = sentinel_ds.GetProjection()
pixel_size_x = geo_transform[1]
pixel_size_y = abs(geo_transform[5])

# Define output bounds to match Sentinel image 
xmin = geo_transform[0]
ymax = geo_transform[3]
xmax = xmin + sentinel_ds.RasterXSize * pixel_size_x
ymin = ymax - sentinel_ds.RasterYSize * pixel_size_y

# Perform the resampling using GDAL Warp
resampled_ds = gdal.Warp(
    destNameOrDestDS=output_path,
    srcDSOrSrcDSTab=prisma_path,
    format='GTiff',
    xRes=pixel_size_x,
    yRes=pixel_size_y,
    dstSRS=projection,
    outputBounds=(xmin, ymin, xmax, ymax),
    resampleAlg='cubic',
    multithread=True,
    warpOptions=["NUM_THREADS=ALL_CPUS"],
    creationOptions=[
        "COMPRESS=DEFLATE",   # Lossless compression
        "TILED=YES",          # Tiled for faster access in QGIS/ArcGIS
        "BIGTIFF=YES"         # Supports files >4GB
    ]
)

# Finalize 
if resampled_ds is None:
    raise RuntimeError("GDAL Warp failed.")
resampled_ds.FlushCache()
resampled_ds = None

print(f"Output saved at: {output_path}")
