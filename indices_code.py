import rasterio
import numpy as np
import os
# Input
tif_path = r"D:\Agri_Geospatial\Resampled\Prisma_downscaled_area2.tif"
hdr_template = r"D:\Agri_Geospatial\Resampled\Prisma_downscaled_area2.hdr" 
# Band mapping based on wavelengths in HDR 
BAND_RED = 32   # 664.894 nm
BAND_GREEN = 20 # 559.020 nm
BAND_BLUE = 10  # 482.548 nm
BAND_NIR = 50   # 849.209 nm
# Load bands
with rasterio.open(tif_path) as src:
    profile = src.profile
    red = src.read(BAND_RED + 1).astype('float32')
    green = src.read(BAND_GREEN + 1).astype('float32')
    blue = src.read(BAND_BLUE + 1).astype('float32')
    nir = src.read(BAND_NIR + 1).astype('float32')
# Avoid division errors 
np.seterr(divide='ignore', invalid='ignore')

# indices 
indices = {
    "NDVI": (nir - red) / (nir + red),
    "GNDVI": (nir - green) / (nir + green),
    "EVI": 2.5 * ((nir - red) / (nir + 6*red - 7.5*blue + 1)),
    "MSAVI": (2*nir + 1 - np.sqrt((2*nir + 1)**2 - 8*(nir - red))) / 2
}
# To save TIF and HDR 
def save_tif_and_hdr(index_name, data, profile, hdr_template):
    out_tif = os.path.splitext(tif_path)[0] + f"_{index_name}.tif"
    out_hdr = os.path.splitext(tif_path)[0] + f"_{index_name}.hdr"
    # Save TIF
    profile_single = profile.copy()
    profile_single.update(dtype=rasterio.float32, count=1)
    with rasterio.open(out_tif, 'w', **profile_single) as dst:
        dst.write(data.astype(rasterio.float32), 1)
    # Read template HDR to copy spatial info
    with open(hdr_template, 'r') as f:
        hdr_content = f.readlines()
    # Modify HDR for single band
    new_hdr_lines = []
    for line in hdr_content:
        if line.strip().startswith("bands"):
            new_hdr_lines.append("bands   = 1\n")
        elif line.strip().startswith("wavelength"):
            new_hdr_lines.append("wavelength = { }\n")  
        elif line.strip().startswith("fwhm"):
            continue 
        else:
            new_hdr_lines.append(line)
    with open(out_hdr, 'w') as f:
        f.writelines(new_hdr_lines)

    print(f"Saved {index_name} as {out_tif} and {out_hdr}")
# Save each index
for idx_name, idx_data in indices.items():
    save_tif_and_hdr(idx_name, idx_data, profile, hdr_template)
