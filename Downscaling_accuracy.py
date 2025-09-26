from osgeo import gdal
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from scipy.optimize import linear_sum_assignment

# INPUT FILES
downscaled_prisma_path = r"D:\Agri_Geospatial\Resampled\Prisma_downscaled_area3.tif"
sentinel_path = r"D:\Agri_Geospatial\Sentinel2_processed\S2_20250405_area3.img"

# Function to read multi-band raster as array
def read_multiband_image(path, num_bands=None):
    ds = gdal.Open(path)
    if not ds:
        raise RuntimeError(f"Failed to open image: {path}")
    bands = []
    count = num_bands if num_bands else ds.RasterCount
    for i in range(1, count + 1):
        band = ds.GetRasterBand(i).ReadAsArray()
        bands.append(band)
    array = np.stack(bands, axis=-1)
    return array

# Preprocessing: reshape and normalize
def preprocess(img):
    img_2d = img.reshape(-1, img.shape[-1]).astype(np.float32)
    img_2d = (img_2d - np.min(img_2d)) / (np.max(img_2d) - np.min(img_2d) + 1e-6)
    return img_2d

# Cluster matching using Hungarian algorithm
def match_labels(true_labels, pred_labels, num_classes):
    conf_matrix = confusion_matrix(true_labels, pred_labels, labels=range(num_classes))
    row_ind, col_ind = linear_sum_assignment(-conf_matrix)
    mapping = dict(zip(col_ind, row_ind))
    matched_pred = np.array([mapping[label] for label in pred_labels])
    return matched_pred

# Load and preprocess images
sentinel_arr = read_multiband_image(sentinel_path, num_bands=3)
prisma_arr = read_multiband_image(downscaled_prisma_path, num_bands=3)

sentinel_flat = preprocess(sentinel_arr)
prisma_flat = preprocess(prisma_arr)

# KMeans clustering
k = 3
kmeans_sentinel = KMeans(n_clusters=k, random_state=42).fit(sentinel_flat)
kmeans_prisma = KMeans(n_clusters=k, random_state=42).fit(prisma_flat)

labels_sentinel = kmeans_sentinel.labels_
labels_prisma = kmeans_prisma.labels_

# Match PRISMA labels to Sentinel labels
matched_labels_prisma = match_labels(labels_sentinel, labels_prisma, k)

# Accuracy assessment
conf_matrix = confusion_matrix(labels_sentinel, matched_labels_prisma)
accuracy = accuracy_score(labels_sentinel, matched_labels_prisma)
report = classification_report(labels_sentinel, matched_labels_prisma, output_dict=True)

# Print clean results
print("Confusion Matrix")
print(conf_matrix)

print("\nOverall Accuracy")
print(f"{accuracy:.4f}")

print("\nClassification Report")
print(f"{'':<12}{'precision':>10}{'recall':>10}{'f1-score':>10}")
for cls in range(k):
    metrics = report[str(cls)]
    print(f"{str(cls):<12}{metrics['precision']:>10.2f}{metrics['recall']:>10.2f}{metrics['f1-score']:>10.2f}")
