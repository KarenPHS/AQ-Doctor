# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 11:54:10 2018

@author: user
"""

from shapely.geometry import Point, shape
import geopandas as gpd
import psycopg2
import pandas as pd

multipolygon_key = [3, 4, 25, 26, 27, 28, 30, 65, 147, 148, 149, 150, 151, 163, 175, 216, 320, 357, 358, 359, 360]
polygon_data = gpd.read_file(r"TOWN_MOI_1070516.shp", encoding = 'utf8')
polygon_data = pd.DataFrame(polygon_data)

conn = psycopg2.connect(dbname = "", user="", password="")
cur = conn.cursor()
cur.execute('select distinct latitude, longitude from pm25_year where towncode is NULL')
rows = cur.fetchall()
for row in rows:
    latitude = row[0]
    longitude = row[1]
    point = Point(longitude, latitude)
    i = 0
    while True:
        try:
            poly_temp = polygon_data.loc[i,'geometry']
            
            # 判斷為 multipolygon
            if i in multipolygon_key:
                polygons = list(poly_temp.geoms)
                j = 0
                # 繞到為正確的 multipolygon 為止，是的話連結資料庫傳資料，傳完後到下一筆，跳出此迴圈
                # 不是的話 j +1 繼續跑，跑到都不是的話，跳出迴圈
                while True:
                    try:
                        if polygons[j].contains(point) == True:
                            towncode = polygon_data["TOWNCODE"][i]
                            cur.execute("UPDATE pm25_year SET towncode = {} WHERE latitude = {} AND longitude = {}".format(towncode, latitude, longitude))
                            conn.commit()
                            break
                        elif polygons[j].contains(point) == False:
                            j += 1
                    
                    except IndexError:
                        break
            
            # 判斷為 polygon
            else:
                polygons = poly_temp
                # 判斷為真的話，回傳資料
                if polygons.contains(point) == True:                    
                    towncode = polygon_data["TOWNCODE"][i]
                    cur.execute("UPDATE pm25_year SET towncode = {} WHERE latitude = {} AND longitude = {}".format(towncode, latitude, longitude))
                    conn.commit()

                # 判斷為假，不做任何事
                elif polygons.contains(point) == False:
                    pass
            
            # 紀錄跑到哪個區的polygon
            i += 1
        #index 超過        
        except KeyError:
            break
conn.close()