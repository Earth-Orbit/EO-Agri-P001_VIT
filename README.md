# EO-Agri-P001_VIT
# Downscaling of Prisma Hyperspectral imagery and its accuracy assessment 
Downscaling of Prisma Hyperspectral imagery using Sentinel-2 MSI:

This performs spatial downscaling of PRISMA hyperspectral imagery using Sentinel-2 multispectral imagery as a reference.
The approach aligns the spatial resolution of PRISMA data to match that of Sentinel-2 (typically 10m or 20m), improving the usability of hyperspectral data for precision agriculture, environmental monitoring, and land cover analysis. The script uses GDAL Warp to resample the PRISMA image spatially, matching the georeferencing, projection, resolution, and extent of the Sentinel-2 image.

Dependencies: 
To run the script, the following dependencies must be installed:
1. gdal	- Used for geospatial raster processing
2. os	- Standard Python library for file operations

Steps to Run the Script:
1. Confirm that both the PRISMA and Sentinel-2 images are available and correctly organized in their respective folders.
2. Open the Python script and verify that the paths to the input PRISMA image, Sentinel-2 image, and output file are correctly set.
3. Open a terminal or command prompt and navigate to the folder containing your script.
4. Run the Python script.
5. Once the script completes, the output downscaled PRISMA image will be saved in the output folder. The new image will match the spatial resolution of Sentinel-2, be aligned with Sentinel-2 in terms of extent, projection, and pixel grid and get saved in GeoTIFF format with compression and tiling for efficient use in GIS tools.
6. Open the resulting image in GIS software (like QGIS, ENVI, or ArcMap) to visualize or analyze the downscaled data.


Accuracy Assessment of Downscaled PRISMA Imagery:

This step evaluates how well the downscaled PRISMA image aligns with Sentinel-2 data using unsupervised clustering (KMeans). It performs the following:
1. Applies KMeans clustering to both Sentinel-2 and PRISMA data
2. Matches clusters using the Hungarian algorithm
3. It Computes: Confusion matrix, Overall accuracy & Precision, recall, and F1-score for each class

Dependencies:

To run the accuracy assessment script, the following Python libraries are required:
1. NumPy – for efficient numerical operations
2. GDAL (osgeo) – for reading geospatial raster data
3. scikit-learn – for KMeans clustering and evaluation metrics
4. SciPy – for optimal label assignment using the Hungarian algorithm

Steps to Run the Script:

1. Ensure the downscaled PRISMA image (GeoTIFF format) is already generated and available.
2. Place the corresponding Sentinel-2 image in a separate folder; it should be coregistered with the PRISMA image and have similar spatial resolution.
3. Open the accuracy assessment Python script and update the file paths to point to the PRISMA and Sentinel-2 images.
4. Confirm that both input images have at least 3 bands for proper comparison.
5. Open a terminal or command prompt and navigate to the folder containing the script.
6. Run the Python script using your Python environment.
7. The script will perform KMeans clustering separately on both images, match cluster labels using the Hungarian algorithm, and compare the classifications.
8. Output will include the confusion matrix, overall accuracy, and detailed precision, recall, and F1-score for each of the classes.
9. Use these metrics to assess the similarity and quality of downscaling between the PRISMA and Sentinel-2 images.





