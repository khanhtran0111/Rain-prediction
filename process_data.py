import os
import rioxarray
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

FEATURES = ['AWS', 'CAPE', 'CIN', 'EWSS', 'IE', 'ISOR', 'KX', 'PEV', 'R250', 'R500', 'R850',
            'SLHF', 'SLOR', 'SSHF', 'TCLW', 'TCW', 'TCWV', 'U250', 'U850', 'V250', 'V850']

def read_tif(filepath):
    if not os.path.exists(filepath): return None
    try:
        dataset = rioxarray.open_rasterio(filepath)
        return dataset[0].values
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def get_feature_paths(base_time, delta_hour, feature_name):
    time = base_time + timedelta(hours=delta_hour)
    filename = f"{feature_name}_{time.strftime('%Y%m%d%H')}0000.tif"
    path = f"DATA_SV/ERA5/{feature_name}/{time.year}/{time.month:02}/{time.day:02}/{filename}"
    return path

def get_aws_path(base_time, delta_hour):
    time = base_time + timedelta(hours=delta_hour)
    filename = f"AWS_{time.strftime('%Y%m%d%H')}0000.tif"
    path = f"DATA_SV/Precipitation/AWS/{time.year}/{time.month:02}/{time.day:02}/{filename}"
    return path

def extract_features(base_time, history=6, target_shift=6):
    data_rows = []

    # Load target AWS (label)
    label_time = base_time + timedelta(hours=target_shift)
    label_path = get_aws_path(base_time, target_shift)
    label_data = read_tif(label_path)
    if label_data is None: return []

    # Loop over entire 90x250 grid
    for i in range(90):
        for j in range(250):
            row = {'row': i, 'col': j}
            values = []

            # Load AWS history
            for h in range(-history+1, 1):
                aws_path = get_aws_path(base_time, h)
                aws_data = read_tif(aws_path)
                if aws_data is None or aws_data[i][j] in [-np.inf, np.nan, -9999]:
                    values = None
                    break
                values.append(aws_data[i][j])
            
            if values is None: continue

            # Load ERA5 features at base_time
            skip = False
            for f in FEATURES[1:]:  # Skip AWS
                f_path = get_feature_paths(base_time, 0, f)
                f_data = read_tif(f_path)
                if f_data is None or f_data[i][j] in [-np.inf, np.nan, -9999]:
                    skip = True
                    break
                values.append(f_data[i][j])

            if skip: continue

            # Get label
            label_value = label_data[i][j]
            if label_value in [-np.inf, np.nan, -9999]: continue

            # Final row
            for idx in range(len(values)):
                row[f'AWS_t-{history - 1 - idx}'] = values[idx]
            for idx, f in enumerate(FEATURES[1:]):
                row[f] = values[history + idx - 1]
            row['label'] = label_value
            data_rows.append(row)

    return data_rows

def main():
    all_rows = []
    start_time = datetime(2019, 4, 1, 6)
    end_time = datetime(2019, 4, 30, 18)

    cur_time = start_time
    while cur_time <= end_time:
        print(f"Processing {cur_time}")
        rows = extract_features(cur_time)
        all_rows.extend(rows)
        cur_time += timedelta(hours=1)

    df = pd.DataFrame(all_rows)
    df.to_csv("cleaned_dataset.csv", index=False)
    print("Saved to cleaned_dataset.csv")

if __name__ == "__main__":
    main()
