import rioxarray
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

HEIGHT = 90
WIDTH = 250

all_data = [[[] for _ in range(WIDTH)] for _ in range(HEIGHT)]
cordinates = {}

tmp_name = ['AWS', 'CAPE', 'CIN', 'EWSS', 'IE', 'ISOR', 'KX', 'PEV',
            'R250', 'R500', 'R850', 'SLHF', 'SLOR', 'SSHF',
            'TCLW', 'TCW', 'TCWV', 'U250', 'U850', 'V250', 'V850']

file_name = [['Precipitation', 'AWS']]
for i in range(1, len(tmp_name)):
    file_name.append(['ERA5', tmp_name[i]])

def get_AWS_cordinates(hour_list, day_list, month_list, year_list, cordinates):
    for year in year_list:
        for month in month_list:
            for day in day_list:
                for hour in hour_list:
                    file_path = f'DATA_SV/Precipitation/AWS/{year}/{month:02}/{day:02}/AWS_{year}{month:02}{day:02}{hour:02}0000.tif'
                    path = Path(file_path)
                    if not path.is_file():
                        continue
                    try:
                        dataset = rioxarray.open_rasterio(file_path)
                    except Exception as e:
                        print(f"Lỗi mở file {file_path}: {e}")
                        continue
                    data = dataset[0].values
                    for i in range(HEIGHT):
                        for j in range(WIDTH):
                            if data[i][j] != -np.inf:
                                cordinates[(i, j)] = True
    return sorted(cordinates.keys())

def read(hour, day, month, year, file, cordinates, all_data):
    data = []
    for item in file:
        folder = item[0]
        param = item[1]
        file_path = f'DATA_SV/{folder}/{param}/{year}/{month:02}/{day:02}/{param}_{year}{month:02}{day:02}{hour:02}0000.tif'
        path = Path(file_path)
        if not path.is_file():
            return
        try:
            dataset = rioxarray.open_rasterio(file_path)
            data.append(dataset[0].values)
        except Exception as e:
            print(f"Lỗi đọc file {file_path}: {e}")
            return

    if data:
        for pos in cordinates:
            i, j = pos
            valid = True
            tmp = [datetime(year, month, day, hour)]
            for arr in data:
                value = arr[i][j]
                if value == -np.inf or value == np.inf or np.isnan(value):
                    valid = False
                    break
                tmp.append(value)
            if valid:
                all_data[i][j].append(tmp)

def main():
    global all_data, cordinates
    for i in range(HEIGHT):
        for j in range(WIDTH):
            all_data[i][j] = []

    hour_list = list(range(24))
    day_list = list(range(1, 32))
    month_list = [4, 10]
    year_list = [2019, 2020]

    print("Đang lấy tọa độ AWS hợp lệ...")
    cordinates_list = get_AWS_cordinates(hour_list, day_list, month_list, year_list, cordinates)
    print(f"Tìm được {len(cordinates_list)} tọa độ hợp lệ.")

    print("Đang đọc dữ liệu theo thời gian...")
    for year in year_list:
        for month in month_list:
            for day in day_list:
                for hour in hour_list:
                    read(hour, day, month, year, file_name, cordinates_list, all_data)

    records = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            for rec in all_data[i][j]:
                records.append([i, j] + rec)

    columns = ['row', 'col', 'datetime'] + tmp_name
    df = pd.DataFrame(records, columns=columns)

    output_file = "data_readed.xlsx"
    try:
        df.to_excel(output_file, index=False)
        print(f"Dữ liệu đã được ghi thành công vào file {output_file}")
    except Exception as e:
        print(f"Lỗi khi ghi file Excel: {e}")

if __name__ == "__main__":
    main()
