import rioxarray
import numpy as np
import pandas as pd
from datascience import *   
# %matplotlib inline
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint
HEIGHT = 90
WIDTH = 250
# all_data = [[[] for _ in range(WIDTH)] for _ in range(HEIGHT)]
m4_y19 = [[[] for _ in range(WIDTH)] for _ in range(HEIGHT)]
m10_y19 = [[[] for _ in range(WIDTH)] for _ in range(HEIGHT)]
m4_y20 = [[[] for _ in range(WIDTH)] for _ in range(HEIGHT)]
m10_y20 = [[[] for _ in range(WIDTH)] for _ in range(HEIGHT)]
cordinates = {}
tmp_name = ['AWS', 'CAPE', 'CIN', 'EWSS', 'IE', 'ISOR', 'KX', 'PEV', 'R250', 'R500', 'R850', 'SLHF', 'SLOR', 'SSHF', 'TCLW', 'TCW', 'TCWV', 'U250', 'U850', 'V250', 'V850']
file_name = [['Precipitation','AWS']]
for i in range(1,len(tmp_name)):
    file_name.append(['ERA5',tmp_name[i]])
# file_name
def get_AWS_cordinates(hour_list, day_list, month_list, year_list, cordinates):
    for year in year_list:
        for month in month_list:
            for day in day_list:
                for hour in hour_list:
                    file_path = f'DATA_SV/Precipitation/AWS/{year}/{month:02}/{day:02}/AWS_{year}{month:02}{day:02}{hour:02}0000.tif'
                    path = Path(file_path)
                    if not path.is_file():
                        continue
                    dataset = rioxarray.open_rasterio(file_path)
                    data = dataset[0].values
                    for i in range(HEIGHT):
                        for j in range(WIDTH):
                            if data[i][j] != -np.inf:
                                cordinates[(i,j)] = True
                                # print(i,j)
    cordinates = sorted(cordinates)
    
def read(hour, day, month, year, file, cordinates, all_data):
    data = []
    for i in range(len(file)):
        name1 = file[i][0]
        name2 = file[i][1]
        file_path = f'DATA_SV/{name1}/{name2}/{year}/{month:02}/{day:02}/{name2}_{year}{month:02}{day:02}{hour:02}0000.tif'
        # print(file_path)
        path = Path(file_path)
        if not path.is_file():
            return
        # print(file_path)
        dataset = rioxarray.open_rasterio(file_path)
        data.append(dataset[0].values)
        
    # print(len(data))
    if(data != []): 
        for pos in cordinates:
            i = pos[0]
            j = pos[1]
            check = True
            tmp = [datetime(year,month,day,hour)]
            for z in range(len(data)):
                if(data[z][i][j] == -np.inf or data[z][i][j] == np.inf or data[z][i][j] == np.nan):
                    check = False
                    break
                tmp.append(data[z][i][j])
            if check:
                all_data[i][j].append(tmp)
                # print(all_data[i][j])
    # print(all_data)

for i in range(HEIGHT):
    for j in range(WIDTH):
        m4_y19[i][j] = []
        m10_y19[i][j] = []
        m4_y20[i][j] = []
        m10_y20[i][j] = []
cordinates.clear
# hour = [0]
hour = [i for i in range(24)]
# day = [1]
# day = [i for i in range(27,28)]
day = [i for i in range(1,32)]
# month = [4]
month = [4,10]
# year = [2019] 
year = [2019,2020]
get_AWS_cordinates(hour, day, month, year, cordinates)
cordinates_list = list(cordinates)
for k in day:
    for l in hour:
        read(l, k, month[0], year[0], file_name, cordinates_list, m4_y19)
        read(l, k, month[1], year[0], file_name, cordinates_list, m10_y19)
        read(l, k, month[0], year[1], file_name, cordinates_list, m4_y20)
        read(l, k, month[1], year[1], file_name, cordinates_list, m10_y20)
# print(len(cordinates_list))