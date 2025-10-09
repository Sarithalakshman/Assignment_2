import os
import yaml
import pandas as pd

# Root directory containing monthly folders with YAML files
ROOT_DIR = r"D:\yaml_data"

# Dictionary to hold stock-wise data
stock_dict = {}

# Optional: keep track of skipped files
skipped_files = []




# Populate stock_dict from YAML files
skipped_files = []

for file in os.listdir(ROOT_DIR):
    if file.endswith(".yaml"):
        stock_name = file.replace(".yaml", "")
        file_path = os.path.join(ROOT_DIR, file)
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)

            df = pd.DataFrame(data)

            if df.empty:
                print(f"⚠️ {stock_name} YAML is empty, skipping")
                skipped_files.append(stock_name)
                continue

            stock_dict[stock_name] = df

        except Exception as e:
            print(f"❌ Error loading {file}: {e}")
            skipped_files.append(stock_name)

print(f"✅ Loaded {len(stock_dict)} stocks")
if skipped_files:
    print(f"⚠️ Skipped files: {skipped_files}")



def process_yaml_file(file_path):
    """
    Load a YAML file and append records to stock_dict.
    Handles cases where the root is:
      - dict keyed by date
      - list of dicts keyed by date
    Each record stored in stock_dict[symbol] will have:
      date, open, close, high, low, volume
    """
    try:
        with open(file_path, "r") as f:
            raw_data = yaml.safe_load(f)

        if not raw_data:
            return  # Skip empty YAMLs

        # --- Normalize the root structure ---
        if isinstance(raw_data, dict):
            # Convert dict {date: {stocks}} → list of {date: {stocks}}
            date_entries = [{date: stocks} for date, stocks in raw_data.items()]
        elif isinstance(raw_data, list):
            date_entries = raw_data
        else:
            skipped_files.append(file_path)
            return  # Skip unexpected structure

        # --- Iterate over date entries ---
        for date_entry in date_entries:
            if not isinstance(date_entry, dict):
                continue  # skip malformed entry

            for date_str, stocks in date_entry.items():
                if not isinstance(stocks, dict):
                    continue  # skip if stocks section not dict

                # 'stocks' should look like {'TCS': {...}, 'INFY': {...}}
                for symbol, values in stocks.items():
                    if not isinstance(values, dict):
                        continue  # skip malformed stock record

                    # Initialize stock list if not present
                    if symbol not in stock_dict:
                        stock_dict[symbol] = []

                    # Create clean record
                    record = {
                        "date": date_str,
                        "open": values.get("open"),
                        "close": values.get("close"),
                        "high": values.get("high"),
                        "low": values.get("low"),
                        "volume": values.get("volume"),
                    }

                    stock_dict[symbol].append(record)

    except Exception as e:
        skipped_files.append(file_path)
        print(f"❌ Error reading {file_path}: {e}")


for folder in os.listdir(ROOT_DIR):
    folder_path = os.path.join(ROOT_DIR, folder)

    # Process only directories (e.g., month folders)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):

            # Process only YAML/YML files
            if file.endswith((".yaml", ".yml")):
                file_path = os.path.join(folder_path, file)

                # Parse the YAML file and update stock_dict
                process_yaml_file(file_path)

print(f"✅ All YAML files processed successfully.")
print(f"ℹ️ Total skipped files: {len(skipped_files)}")


for stock, records in stock_dict.items():
    df = pd.DataFrame(records)

    # Convert types
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    for col in ['open', 'close', 'volume', 'high', 'low']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop missing values, duplicates, and sort
    df = df.dropna().drop_duplicates(subset='date').sort_values('date')

    stock_dict[stock] = df  # overwrite with cleaned DataFrame

print("✅ Data cleaned for all stocks")


skipped_stocks = []

for stock, df in stock_dict.items():
    if df.empty:
        print(f"⚠️ Skipping {stock} because DataFrame is empty")
        skipped_stocks.append(stock)
        continue
    
    try:
        csv_path = os.path.join(ROOT_DIR, f"{stock}.csv")
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved {csv_path}")
    except Exception as e:
        print(f"❌ Error saving CSV for {stock}: {e}")
        skipped_stocks.append(stock)

print("✅ All possible CSV files saved")
if skipped_stocks:
    print(f"⚠️ Skipped stocks: {skipped_stocks}")


