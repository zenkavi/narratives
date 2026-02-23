"""
Compare fMRIPrep outputs from two runs (with and without SDC).
For NIfTI files: load both, check if arrays differ, report max absolute difference.
For TSV files: load both as DataFrames, report which columns changed and by how much.
"""

import nibabel as nib
import numpy as np
import pandas as pd
from pathlib import Path

# ---- Configure paths to the two fMRIPrep output directories ----
run1_dir = Path("/path/to/fmriprep_without_sdc/sub-S01")
run2_dir = Path("/path/to/fmriprep_with_sdc/sub-S01")

# ---- Files to compare ----
# Anatomical files (should NOT change; serves as sanity check)
# Functional files (should change if SDC was applied)
files_to_compare = [
    # Anatomical sanity checks
    "ses-1/anat/sub-S01_ses-1_desc-preproc_T1w.nii.gz",
    "ses-1/anat/sub-S01_ses-1_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz",
    # Functional targets where SDC differences should appear
    "ses-2/func/sub-S01_ses-2_task-TheSecretNumber_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz",
    "ses-2/func/sub-S01_ses-2_task-TheSecretNumber_desc-confounds_timeseries.tsv",
    # Brain mask (SDC can shift mask boundaries)
    "ses-2/func/sub-S01_ses-2_task-TheSecretNumber_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
]


def compare_nifti(file1, file2):
    """Load two NIfTI files and report whether their data arrays differ."""
    img1 = nib.load(file1)
    img2 = nib.load(file2)

    data1 = img1.get_fdata()
    data2 = img2.get_fdata()

    if data1.shape != data2.shape:
        print(f"  Shapes differ: {data1.shape} vs {data2.shape}")
        return

    identical = np.array_equal(data1, data2)
    if identical:
        print("  Arrays are IDENTICAL (no SDC effect on this file)")
    else:
        abs_diff = np.abs(data1 - data2)
        print(f"  Arrays DIFFER")
        print(f"    Max absolute difference: {abs_diff.max():.6f}")
        print(f"    Mean absolute difference: {abs_diff.mean():.6f}")
        print(f"    Fraction of voxels that changed: {np.mean(abs_diff > 0):.4f}")


def compare_tsv(file1, file2):
    """Load two confounds TSV files and report which columns changed."""
    df1 = pd.read_csv(file1, sep="\t")
    df2 = pd.read_csv(file2, sep="\t")

    if list(df1.columns) != list(df2.columns):
        print(f"  Column sets differ between runs")
        added = set(df2.columns) - set(df1.columns)
        removed = set(df1.columns) - set(df2.columns)
        if added:
            print(f"    New columns in run2: {added}")
        if removed:
            print(f"    Columns missing in run2: {removed}")

    # Compare shared columns
    shared_cols = [c for c in df1.columns if c in df2.columns]
    changed_cols = []
    for col in shared_cols:
        try:
            if not np.allclose(df1[col].values, df2[col].values, equal_nan=True):
                max_diff = np.nanmax(np.abs(df1[col].values - df2[col].values))
                changed_cols.append((col, max_diff))
        except TypeError:
            # Non-numeric column
            if not df1[col].equals(df2[col]):
                changed_cols.append((col, "non-numeric"))

    if not changed_cols:
        print("  All shared columns are IDENTICAL")
    else:
        print(f"  {len(changed_cols)} columns DIFFER:")
        for col, diff in changed_cols:
            print(f"    {col}: max diff = {diff}")
