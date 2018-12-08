#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import psycopg2
import pandas as pd
import urllib
from os import walk
from os.path import join
import json
from datetime import datetime
import re
import numpy as np


# # NOx, SOx api

# In[2]:


def one_week_data(item):
    #連接資料庫，取得一個禮拜nox資料
    conn = psycopg2.connect(dbname = "", user="", password="",port=5432,host='')
    cur = conn.cursor()
    data = pd.read_sql_query("select * from cems_new WHERE m_time BETWEEN  (NOW() AT TIME ZONE 'Asia/Taipei') - interval '604800' AND (NOW() AT TIME ZONE 'Asia/Taipei') AND item='%s';"%(922),con=conn)
    conn.close()
    #計算各label總數
    data['code2desc'] = data['code2desc'].fillna('空值')
    tmp = data.groupby(['abbr','cno','code2desc']).size()
    tmp = tmp.reset_index()

    #數值格式轉換用
    abbr2codedesc = dict()
    for row in tmp.itertuples():
        if row[1] not in abbr2codedesc:
            abbr2codedesc[row[1]] = dict()
    #     if row[2] not in abbr2codedesc[row[1]]:
    #         abbr2codedesc[row[1]][row[2]] = None
        abbr2codedesc[row[1]]['cno'] = row[2]
        abbr2codedesc[row[1]][row[3]] = row[4]
    #empty dataframe
    tmp = pd.DataFrame(columns=['公司','cno','固定污染源暫停運轉時監測設施之量測值','正常排放量測值',
                      '每日定期零點或全幅偏移測試量測值','無效數據',
                     '監測設施維修保養量測值','超過排放標準量測值','其它無效量測值'])

    # #數值填入emtpy dataframe
    for k,v in abbr2codedesc.items():
        v.update({'公司':k})
        tmp = tmp.append(v, ignore_index=True)
    tmp.iloc[:,2:] = tmp.apply(lambda x: x[2:]/np.sum(x[2:]),axis=1).round(2)
    #計算ratio
    return tmp


# In[3]:


def Nox():
    return one_week_data(923)
def Sox():
    return one_week_data(922)


# # def instant_24(cno:text )

# In[42]:


def instant_24(cno):
    conn = psycopg2.connect(dbname = "", user="", password="",port=5432,host='')
    cur = conn.cursor()

    data = pd.read_sql_query("select * from cems_new WHERE m_time BETWEEN         (NOW() AT TIME ZONE 'Asia/Taipei') - interval '86400' AND (NOW() AT TIME ZONE 'Asia/Taipei') AND (item='923' or item='922') AND cno='%s';"%(cno),con=conn)
    data = data[['m_time','item','m_val','polno']]
    data['m_time'] = data['m_time'].apply(lambda x : x.tz_localize('Asia/Taipei'))
    #製造時間軸
    #取得現在時間，round minutes
    now = pd.Timestamp.now('Asia/Taipei')
    minute = now.minute
    now = now.replace(second=0,microsecond=0)
    now = now - pd.offsets.Minute(minute%15)
    before = now - pd.offsets.Hour(24)
    time_series = pd.date_range(before, now, freq="15min")

    #篩選24小時內的data
    data = data[ (data.m_time <= now) & (data.m_time >= before)]
    #時間軸與data outer merge
    df = pd.DataFrame({'m_time':time_series})
    tmp2 = data.merge(df,how='outer',on=['m_time'])

    conn.close()
    return tmp2

def dataframe_trans(tmp):
    tmp2 = tmp.set_index(['m_time','item','polno']).unstack("polno").reset_index()
    tmp2 = tmp2.set_index(["m_time","item"])
    tmp2.columns = tmp2.columns.droplevel()
    tmp = tmp2.reset_index()
    return tmp
