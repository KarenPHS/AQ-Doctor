# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import geopandas as gpd
import pandas as pd
import psycopg2
import datetime

now_year = datetime.datetime.now().year - 1
conn = psycopg2.connect(dbname = "", user="", password="",port=5432,host='')
cur = conn.cursor()
sql = ('SELECT date, device_id, pm25, longitude, latitude, towncode from pm25_year' 
       ' Where extract(isoyear from date) = ' + str(now_year) + 
       ' AND towncode is not null limit 5000')
pm25_data = pd.read_sql(sql,conn)
conn.close()

pm25_mean = pm25_data.groupby('towncode', as_index = False).mean()
pm25_mean = pm25_mean[['towncode','pm25']]

district_data = gpd.read_file("./mapdata/TOWN_MOI_1070516.shp", encoding = 'utf8')
district_data = pd.DataFrame(district_data)
district_data.columns = district_data.columns.str.lower()
district_data = district_data[['towncode', 'countyname', 'townname', 'geometry']]
result = pd.merge(pm25_mean, district_data, how = 'outer', on = 'towncode')

result = gpd.GeoDataFrame(result, geometry='geometry')
result.to_file('./pm25/pm25_mean.shp', driver='ESRI Shapefile', encoding='utf8')


