import csv
import subprocess
from pathlib import Path

# Define base directory
base_dir = Path("/hopper/groups/enkavilab/data/ds004892")

# Read the session information from the CSV
sessions_data = []
with open("secret_number_sessions.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sessions_data.append((row['subject'], row['session']))

print(f"Processing {len(sessions_data)} subjects")

# Loop through each subject and get necessary files
for subnum, sesnum in sessions_data:
    print(f"\nProcessing sub-{subnum}, ses-{sesnum}")
    
    # 1. Get functional files for The Secret Number
    func_pattern = f"sub-{subnum}/ses-{sesnum}/func/sub-{subnum}_ses-{sesnum}_task-TheSecretNumber_*"
    func_cmd = f"datalad get {base_dir / func_pattern}"
    print(f"Getting functional files: {func_cmd}")
    subprocess.run(func_cmd, shell=True, cwd=base_dir)
    
    # 2. Get functional acquisition/events information
    events_pattern = f"sub-{subnum}/ses-{sesnum}/func/sub-{subnum}_ses-{sesnum}_task-scan_acq-TheSecretNumber_events.*"
    events_cmd = f"datalad get {base_dir / events_pattern}"
    print(f"Getting events files: {events_cmd}")
    subprocess.run(events_cmd, shell=True, cwd=base_dir)
    
    # 3. Get fieldmaps for this session
    fmap_pattern = f"sub-{subnum}/ses-{sesnum}/fmap/*"
    fmap_cmd = f"datalad get {base_dir / fmap_pattern}"
    print(f"Getting fieldmap files: {fmap_cmd}")
    subprocess.run(fmap_cmd, shell=True, cwd=base_dir)
    
    # 4. Get anatomical files from session 1
    anat_pattern = f"sub-{subnum}/ses-1/anat/*"
    anat_cmd = f"datalad get {base_dir / anat_pattern}"
    print(f"Getting anatomical files: {anat_cmd}")
    subprocess.run(anat_cmd, shell=True, cwd=base_dir)

print("\nDatalad get complete!")