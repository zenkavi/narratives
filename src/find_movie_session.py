import csv
from pathlib import Path

# Define base directory
base_dir = Path("/hopper/groups/enkavilab/data/ds004892")

# Store results
results = []

# Loop through all subject directories
for sub_dir in sorted(base_dir.glob("sub-S*")):
    # Extract subject number (e.g., "S01" from "sub-S01")
    subnum = sub_dir.name.replace("sub-", "")
    
    # Loop through all session directories for this subject
    for ses_dir in sorted(sub_dir.glob("ses-*")):
        # Extract session number (e.g., "01" from "ses-01")
        sesnum = ses_dir.name.replace("ses-", "")
        
        # Build path to scans.tsv file
        scans_file = ses_dir / f"sub-{subnum}_ses-{sesnum}_scans.tsv"
        
        # Check if file exists and search for the task
        if scans_file.exists():
            with open(scans_file, 'r') as f:
                content = f.read()
                # If the movie task is found, save subject and session
                if "task-TheSecretNumber_bold" in content:
                    results.append([subnum, sesnum])
                    break  # Found it, move to next subject

# Write results to CSV
with open("secret_number_sessions.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(["subject", "session"])
    # Write data
    writer.writerows(results)

print(f"Found {len(results)} subjects who watched 'The Secret Number'")
print("Results saved to secret_number_sessions.csv")