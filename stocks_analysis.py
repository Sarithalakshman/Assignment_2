import os
import pandas as pd

# Folder where all your generated stock CSVs are stored
ROOT_DIR = r"D:\yaml_data"

# Dictionary to hold DataFrames keyed by stock symbol
csv_dict = {}

# To log issues
skipped_files = {}
loaded_files = []

# Expected columns
expected_cols = {"date", "open", "close", "high", "low", "volume"}

for file in os.listdir(ROOT_DIR):
    if file.endswith(".csv"):
        symbol = file.replace(".csv", "")
        csv_path = os.path.join(ROOT_DIR, file)

        try:
            df = pd.read_csv(csv_path)

            # Check required columns
            missing = expected_cols - set(df.columns)
            if missing:
                skipped_files[file] = f"Missing columns: {list(missing)}"
                continue  # skip this file

            # Ensure correct data types 
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])  # drop only rows where date is invalid

            for col in ['open', 'close', 'high', 'low', 'volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            # Handle duplicates + sort
            df = df.drop_duplicates(subset='date').sort_values('date')

            # Save to dictionary
            csv_dict[symbol] = df
            loaded_files.append(file)

        except Exception as e:
            skipped_files[file] = f"Error: {e}"
print(f"✅ Loaded {len(loaded_files)} CSVs successfully.")
print(f"⚠️ Skipped {len(skipped_files)} CSVs.")

if skipped_files:
    print("\nSkipped files log:")
    for f, reason in skipped_files.items():
        print(f" - {f}: {reason}")


