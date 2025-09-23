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

# Other Downscaling Techniques
In addition to the primary downscaling workflow, multiple alternative methods were applied to PRISMA hyperspectral imagery using Sentinel-2 as a reference:
1. Bilinear Resampling
The PRISMA image was resampled using bilinear interpolation to match the spatial resolution of Sentinel-2, producing a smooth high-resolution output.

2. Nearest Neighbor Resampling
Nearest Neighbor (NN) resampling was applied to preserve original pixel values while aligning the PRISMA image with Sentinel-2.

3. HySure Fusion (Sparse Regression)
Fast HySure fusion was applied using Lasso-based sparse regression on a random subset of pixels to estimate high-resolution hyperspectral data.

4. CNMF Fusion (Coupled Non-negative Matrix Factorization)
NMF decomposition of Sentinel-2 bands was performed to extract key components, which were then used to reconstruct high-resolution hyperspectral data.

5. Bayesian Fusion
Bayesian fusion combined PRISMA and Sentinel-2 data with a weighted approach, balancing spatial and spectral contributions to generate enhanced resolution outputs.

6. Filter-Based Fusion (PCA + Wavelet)
PCA was applied to Sentinel-2 bands, the first principal component was replaced with PRISMA information, and wavelet decomposition was used for spatial refinement.

All fused and resampled images were saved as GeoTIFFs and used for subsequent index extraction and LULC classification.


# Extraction of Vegetation Indices

Vegetation indices were derived from both the downscaled PRISMA hyperspectral imagery and the Sentinel-2 multispectral imagery to enhance vegetation characterization and improve classification accuracy. Four indices—NDVI, GNDVI, EVI, and MSAVI—were computed as follows:

1) NDVI (Normalized Difference Vegetation Index):
NDVI = (NIR − Red) / (NIR + Red)
Highlights healthy vegetation and overall biomass presence.

2) GNDVI (Green Normalized Difference Vegetation Index):
GNDVI = (NIR − Green) / (NIR + Green)
Sensitive to chlorophyll concentration and canopy stress.

3) EVI (Enhanced Vegetation Index):
EVI = 2.5 × (NIR − Red) / (NIR + 6 × Red − 7.5 × Blue + 1)
Reduces atmospheric and soil background influences, particularly in dense vegetation areas.

4) MSAVI (Modified Soil-Adjusted Vegetation Index):
MSAVI = (2 × NIR + 1 − √((2 × NIR + 1)² − 8 × (NIR − Red))) / 2
Minimizes soil influence, improving vegetation detection in sparse cover regions.

From these indices, training CSV files were prepared for both Sentinel-2 and PRISMA datasets by extracting spectral values and assigning land cover labels. The classes considered were:
1. Waterbody
2. Settlement
3. Barren Land
4. Moderate Vegetation
5. Stressed Vegetation
6. Healthy Vegetation


# Land Use / Land Cover Classification using Machine Learning Models
Models Used
1. Random Forest (RF):
Ensemble learning method combining multiple decision trees.
Robust against overfitting and effective for high-dimensional data.
Used as a baseline classifier due to its reliability in remote sensing applications.

2. Support Vector Machine (SVM):
Kernel-based classifier effective in handling non-linear boundaries.
Radial Basis Function (RBF) kernel applied for separating complex vegetation classes.
Scaled features before training to improve performance.

3. K-Nearest Neighbors (KNN):
Instance-based learning method.
Classified unknown samples by majority voting among nearest neighbors.
Weighted distance used to reduce noise effects.

4. Logistic Regression (LR):
Multinomial logistic regression model applied for multi-class classification.
Useful for probability-based classification and interpretability.

Evaluation: 
For each model:
Training and testing datasets were generated using stratified 80:20 split.
Performance was assessed using:
1. Overall Accuracy
2. Confusion Matrix
3. Precision, Recall, and F1-Score per class
Results were compiled into Word reports containing metrics, class mapping, and confusion matrices for each classifier.

Raster Classification: 
After evaluation, each trained model was applied to the input vegetation index rasters (e.g., NDVI) to generate spatially continuous LULC maps. The classification outputs were saved as compressed GeoTIFFs with class codes aligned to the defined LULC categories.

