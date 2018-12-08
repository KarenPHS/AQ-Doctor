# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 16:13:25 2018

@author: user
"""
import geopandas as gpd
import pandas as pd
import numpy as np
import psycopg2

# CEMS 整理
conn = psycopg2.connect(dbname = " ", user="", password="")
cur = conn.cursor()
sql = ('SELECT abbr, longitude, latitude, towncode from cems_metadata')
cems_metadata = pd.read_sql(sql,conn)
conn.close()

cems_amount = cems_metadata.groupby(cems_metadata['towncode'], as_index=False).count()
cems_amount = cems_amount[['towncode','abbr']]
cems_amount.rename(columns = {'abbr':'cems'}, inplace = True)

# factory 整理
conn = psycopg2.connect(dbname = "", user="", password="")
cur = conn.cursor()
sql = ('SELECT number, longitude, latitude, towncode from factory')
factory_data = pd.read_sql(sql,conn)
conn.close()

factory_amount = factory_data.groupby(factory_data['towncode'], as_index = False).count()
factory_amount = factory_amount[['towncode','number']]
factory_amount.rename(columns = {'number':'factory'}, inplace = True)

#找個行政區中間值
def get_centroid(x):
    if x.geometryType() == 'Polygon':
        return x.centroid
    else:
        index = np.argmax([x[i].area for i in range(len(x))])
        return x[index].centroid
#拆點座標
def split_point(point):
    longitude = point.x
    latitude = point.y
    return latitude, longitude

# 行政區整理
district_data = gpd.read_file("./mapdata/TOWN_MOI_1070516.shp", encoding = 'utf8')
district_data.columns = district_data.columns.str.lower()
district_data['geometry'] = district_data['geometry'].apply(lambda x: get_centroid(x))
district_data['geometry'] = district_data['geometry'].apply(lambda x: split_point(x))
district_data[['latitude','longitude']] = district_data['geometry'].apply(pd.Series)
del district_data['geometry']
district_data = district_data[['towncode', 'countyname', 'townname', 'latitude','longitude']]
district_data = pd.DataFrame(district_data)
cems_dis = pd.merge(cems_amount, district_data, how='right', on = 'towncode')
factory_dis = pd.merge(factory_amount, district_data, how='right', on = 'towncode')

# 把多餘的column 處理掉，再合併
factory_dis = factory_dis[['towncode', 'factory']]
result = pd.merge(factory_dis, cems_dis,on = ['towncode'])
result.rename(columns={'factory': '一般工廠', 'cems': '監督工廠'}, inplace=True)

result.to_csv('./cems_factory.csv', index=False, encoding='utf8')
