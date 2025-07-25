# EO-Agri-P001_VIT
Downscaling of prisma using Sentinel-2:  

This project performs spatial downscaling of PRISMA hyperspectral imagery using Sentinel-2 multispectral imagery as a reference.
The approach aligns the spatial resolution of PRISMA data to match that of Sentinel-2 (typically 10m or 20m), improving the usability of hyperspectral data for precision agriculture, environmental monitoring, and land cover analysis. The script uses GDAL Warp to resample the PRISMA image spatially, matching the georeferencing, projection, resolution, and extent of the Sentinel-2 image.

Dependencies: 
To run the script, the following dependencies must be installed:
1. gdal	- Used for geospatial raster processing
2. os	- Standard Python library for file operations

Steps to Run the Script:

File Structure:
Ensure your project folder contains the following:
1. A folder with the coregistered PRISMA image
2. A folder with the processed Sentinel-2 image (same area and date)
3. A script file for running the downscaling
4. A designated output folder for saving the downscaled result

Execution Steps:
1. Confirm that both the PRISMA and Sentinel-2 images are available and correctly organized in their respective folders.
2. Open the Python script and verify that the paths to the input PRISMA image, Sentinel-2 image, and output file are correctly set.
3. Open a terminal or command prompt and navigate to the folder containing your script.
4. Run the Python script.
5. Once the script completes, the output downscaled PRISMA image will be saved in the output folder. The new image will match the spatial resolution of Sentinel-2, be aligned with Sentinel-2 in terms of extent, projection, and pixel grid and get saved in GeoTIFF format with compression and tiling for efficient use in GIS tools.
6. Open the resulting image in GIS software (like QGIS, ENVI, or ArcMap) to visualize or analyze the downscaled data.

