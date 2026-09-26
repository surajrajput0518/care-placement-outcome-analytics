import os
import shutil
import subprocess

base_dir = r'C:\Users\Suraj Rajput\.gemini\antigravity\scratch\care-transition-analytics'
dirs = ['data', 'src', 'reports', 'tests', '.streamlit']
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

src_csv = os.path.join(base_dir, 'dataset.csv')
dst_csv = os.path.join(base_dir, 'data', 'raw_uac_data.csv')
if os.path.exists(src_csv):
    shutil.copyfile(src_csv, dst_csv)
    print(f"Copied {src_csv} to {dst_csv}")

subprocess.run(["git", "init"], cwd=base_dir, check=True)
print("Git initialized successfully.")
