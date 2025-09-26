import numpy as np
import rasterio
from sklearn.linear_model import Lasso
from sklearn.decomposition import NMF, PCA
import pywt  
import cv2
import os

# Fusion Methods 
def hysure_fusion(Yh, Ym, alpha=0.05, sample_frac=0.05):
    rows, cols, bands_m = Ym.shape
    bands_h = Yh.shape[2]
    X_hat = np.zeros((rows, cols, bands_h), dtype=np.float32)
    Ym_2d = Ym.reshape(-1, bands_m).astype(np.float32)
    Ym_2d = (Ym_2d - Ym_2d.mean(axis=0)) / (Ym_2d.std(axis=0) + 1e-6)
    # Random sample (5% of pixels)
    n_samples = int(Ym_2d.shape[0] * sample_frac)
    idx = np.random.choice(Ym_2d.shape[0], n_samples, replace=False)
    Ym_sample = Ym_2d[idx]
    for b in range(bands_h):
        y = Yh[:, :, b].ravel()[idx]
        lasso = Lasso(alpha=alpha, max_iter=1000)
        lasso.fit(Ym_sample, y)
        X_hat[:, :, b] = lasso.predict(Ym_2d).reshape(rows, cols)
    return X_hat

def cnmf_fusion(Yh, Ym, n_components=10, max_iter=100):
    rows, cols, bands_m = Ym.shape
    Ym_2d = Ym.reshape(-1, bands_m).astype(np.float32)
    nmf = NMF(n_components=n_components, init="random", random_state=42, max_iter=max_iter)
    W = nmf.fit_transform(Ym_2d)
    H = nmf.components_
    fused = np.dot(W, H).astype(np.float32)
    return fused.reshape(rows, cols, bands_m)

def bayesian_fusion(Yh, Ym, lam=0.5):
    rows, cols, bands_m = Ym.shape
    bands_h = Yh.shape[2]
    
    hs_resized = cv2.resize(Yh.reshape(Yh.shape[0], Yh.shape[1] * bands_h),
                            (cols * bands_h, rows),
                            interpolation=cv2.INTER_NEAREST)
    hs_resized = hs_resized.reshape(rows, cols, bands_h)

    hs_matched = hs_resized[:, :, :bands_m]
    X_hat = (Ym + lam * hs_matched) / (1 + lam)
    return X_hat.astype(np.float32)


def filter_based_fusion(Yh, Ym):
    rows, cols, bands_m = Ym.shape
    Ym_2d = Ym.reshape(-1, bands_m).astype(np.float32)

    pca = PCA(n_components=bands_m)
    Ym_pca = pca.fit_transform(Ym_2d)

    hs_mean = np.resize(Yh.mean(axis=2), Ym_2d.shape[0])
    Ym_pca[:, 0] = hs_mean

    Ym_fused = pca.inverse_transform(Ym_pca).astype(np.float32)
    X_hat = Ym_fused.reshape(rows, cols, bands_m)
    
    coeffs2 = pywt.dwt2(X_hat[:, :, 0], 'haar')
    cA, (cH, cV, cD) = coeffs2
    fused_band = pywt.idwt2((cA, (cH, cV, cD)), 'haar')
    X_hat[:, :, 0] = fused_band[:rows, :cols]

    return X_hat.astype(np.float32)

# Save 
def save_geotiff(output_path, array, reference_path):
    with rasterio.open(reference_path) as ref:
        profile = ref.profile
        profile.update(
            dtype=rasterio.float32,
            count=array.shape[2],
            driver="GTiff",
            compress="deflate",
            bigtiff="yes"
        )
    with rasterio.open(output_path, "w", **profile) as dst:
        for i in range(array.shape[2]):
            dst.write(array[:, :, i].astype(np.float32), i + 1)
            dst.set_band_description(i + 1, f"Band_{i+1}")
    print(f"Saved GeoTIFF: {output_path}")


# Main
if __name__ == "__main__":
    prisma_path = r"D:\Agri_Geospatial\Coreg_output\Prisma_area3_coregistered.img"
    sentinel_path = r"D:\Agri_Geospatial\Sentinel2_processed\S2_20250405_area3.img"
    out_dir = r"D:\Agri_Geospatial\Resampled"
    os.makedirs(out_dir, exist_ok=True)
    # Read PRISMA
    with rasterio.open(prisma_path) as src:
        Yh = src.read().astype(np.float32)
        Yh = np.transpose(Yh, (1, 2, 0))
    # Read Sentinel (resize to PRISMA)
    with rasterio.open(sentinel_path) as src:
        Ym = src.read([1, 2, 3],
                      out_shape=(3, Yh.shape[0], Yh.shape[1]),
                      resampling=rasterio.enums.Resampling.nearest)
        Ym = np.transpose(Ym, (1, 2, 0)).astype(np.float32)
    print("PRISMA shape:", Yh.shape)
    print("Sentinel resized shape:", Ym.shape)
    # Run fusion methods
    fused_hysure = hysure_fusion(Yh, Ym)
    fused_cnmf = cnmf_fusion(Yh, Ym)
    fused_bayes = bayesian_fusion(Yh, Ym)
    fused_filter = filter_based_fusion(Yh, Ym)
    # Save results
    save_geotiff(os.path.join(out_dir, "prisma_area3_hysure.tif"), fused_hysure, sentinel_path)
    save_geotiff(os.path.join(out_dir, "prisma_area3_cnmf.tif"), fused_cnmf, sentinel_path)
    save_geotiff(os.path.join(out_dir, "prisma_area3_bayes.tif"), fused_bayes, sentinel_path)
    save_geotiff(os.path.join(out_dir, "prisma_area3_filter.tif"), fused_filter, sentinel_path)
    print("All fused outputs saved.")
