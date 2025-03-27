import rioxarray
import numpy as np
import pandas as pd

all_data = []

def read_aws(hour, day, month, year):
    file_path = f'DATA_SV/Precipitation/AWS/{year}/{month:02}/{day:02}/AWS_{year}{month:02}{day:02}{hour:02}0000.tif'
    # print(file_path)
    dataset = rioxarray.open_rasterio(file_path)
    data = dataset[hour].values
    # print(data)
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] != -np.inf:
                # print(f'{i} {j} {data[i][j]}')
                all_data.append([i,j,float(data[i][j])])

def read_addition(hour, day, month, year, name1, name2):
    file_path = f'DATA_SV/{name1}/{name2}/{year}/{month:02}/{day:02}/{name2}_{year}{month:02}{day:02}{hour:02}0000.tif'
    dataset = rioxarray.open_rasterio(file_path)
    data = dataset[0].values
    for x in all_data:
        i = x[0]
        j = x[1]
        x.append(float(data[i][j]))

def read(hour, day, month, year):
    read_aws(hour, day, month, year)
    read_addition(hour, day, month, year, 'ERA5', 'CAPE')
    read_addition(hour, day, month, year, 'ERA5', 'CIN')
    read_addition(hour, day, month, year, 'ERA5', 'EWSS')
    read_addition(hour, day, month, year, 'ERA5', 'IE')
    read_addition(hour, day, month, year, 'ERA5', 'ISOR')
    read_addition(hour, day, month, year, 'ERA5', 'KX')
    read_addition(hour, day, month, year, 'ERA5', 'PEV')
    read_addition(hour, day, month, year, 'ERA5', 'R250')
    read_addition(hour, day, month, year, 'ERA5', 'R500')
    read_addition(hour, day, month, year, 'ERA5', 'R850')
    read_addition(hour, day, month, year, 'ERA5', 'SLHF')
    read_addition(hour, day, month, year, 'ERA5', 'SLOR')
    read_addition(hour, day, month, year, 'ERA5', 'SSHF')
    read_addition(hour, day, month, year, 'ERA5', 'TCLW')
    read_addition(hour, day, month, year, 'ERA5', 'TCW')
    read_addition(hour, day, month, year, 'ERA5', 'TCWV')
    read_addition(hour, day, month, year, 'ERA5', 'U250')
    read_addition(hour, day, month, year, 'ERA5', 'U850')
    read_addition(hour, day, month, year, 'ERA5', 'V250')
    read_addition(hour, day, month, year, 'ERA5', 'V850')
    
    excel_data = pd.DataFrame(all_data, columns=['ROW', 'COLUMN', 'AWS', 'CAPE', 'CIN', 'EWSS', 'IE', 'ISOR', 'KX', 'PEV', 'R250', 'R500', 'R850', 'SLHF', 'SLOR', 'SSHF', 'TCLW', 'TCW', 'TCWV', 'U250', 'U850', 'V250', 'V850'])
    excel_data.to_excel('data.xlsx', index=False)
    # for x in all_data:
    #     print(x)
    # print(all_data)
    
def main():
    read(0,1,4,2019)
    
if __name__ == '__main__':
    main()