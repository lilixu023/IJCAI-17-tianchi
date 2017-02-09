#-*- coding=gbk -*-
import pandas as pd
import time
import  numpy as np
import matplotlib.pyplot as plt
from  matplotlib.dates  import datestr2num
from  matplotlib.dates  import num2date,datestr2num,drange,DateFormatter
import datetime
import re
import function_collection as fc
from pylab import mpl
# map(num2date, map(datestr2num, all_view_data[all_view_data.shopid == 2]['time'].tolist()))
'''
Ԥ����������Ϣ�������µ�������Ϣ��csv�ļ�
'''
def Decode(obstr):
   '''
   :param obstr: Ŀ�������ַ���
   :return:�����������ַ���
   '''
   return obstr.decode('gb2312')

def numDatetoStr1(DT):
     '''
     :param DT: input datetime
     :return: converted string;fomat:'%Y/%m/%d'
     2015/3/2 not 2015/03/02
     '''
     temp_date=str(num2date(DT)).split(' ')[0]
     words=temp_date.split('-')
     if words[1][0]=='0':
         temp_str=words[1][1]
         words[1]=temp_str
     if words[2][0]=='0':
         temp_str=words[2][1]
         words[2]=temp_str
     return words[0]+'/'+words[1]+'/'+words[2]


def numDatetoStr2(DT):
    '''
    :param DT: input datetime
    :return: converted string;fomat:'%Y-%m-%d'
    2015-3-2 not 2015-03-02
    '''
    temp_date = str(num2date(DT)).split(' ')[0]
    words = temp_date.split('-')
    if words[1][0] == '0':
        temp_str = words[1][1]
        words[1] = temp_str
    if words[2][0] == '0':
        temp_str = words[2][1]
        words[2] = temp_str
    return words[0] + '-' + words[1] + '-' + words[2]

def StrToDate_1(datestr):
    '''

    :param datestr: %Y/%m/%d
    :return: date:datetime
    '''
    return datetime.datetime.strptime(datestr,'%Y/%m/%d')

def DateToStr_1(date):
    '''

    :param date: datetime
    :return: datestr: %Y-%m-%d
    '''
    return datetime.datetime.strftime(date,'%Y-%m-%d')

def StrDate1ToStrDate(datestr):
    '''

    :param datestr: %Y/%m/%d
    :return: datestr:%Y-%m-%d
    '''
    return DateToStr_1(StrToDate_1(datestr))
def IsSubStr(list,fatherStr):
   '''
   :param list:listType
   :param fatherStr:
   :return: true or false
   '''
   # print 'fatherstr',fatherStr
   for childStr in list:
      # print 'childStr', childStr
      if childStr in fatherStr:
         return True
weather_path='data/ijcai17-weather_1.csv'
weather_info = pd.read_csv(weather_path, encoding="gb2312")
print weather_info.head()
holiday_info=pd.read_csv('data/holiday.csv',names=['date','label'])
print holiday_info.loc[0].label
weather_info['weather_level'] = 0
# weather_info[weather_info.area=='����']
level_0 = ''
level_2 = map(fc.Decode, ['��', 'ѩ'])
level_1 = map(fc.Decode, ['С��'])
# level_2 = ['��', 'ѩ']
# level_1 =['С��']
for i, row in enumerate(weather_info.weather):
    # row=row.decode('utf-8')
    if type(row) == float:
        row = 'nn'
    row_date = weather_info.loc[i,:].date
    formatted_str = fc.DateStr_1ToDatestr_3(row_date)
    formatted_int=int(formatted_str)
    # print formatted_int
    if formatted_int<20150701 or formatted_int>20161031:
        continue
    Is_h = holiday_info[holiday_info['date']==int(formatted_str)].label.values[0]
    # print row_date
    _row_date = datetime.datetime.strptime(row_date, '%Y/%m/%d')

    _row_week = datetime.datetime.isoweekday(_row_date)

    if IsSubStr(level_2, row) and (_row_week < 6):  # ����ĩ������ѩ�ȼ�����Ϊ2
        weather_info.loc[i, 'weather_level'] = 2

    if IsSubStr(level_1, row) and (_row_week < 6):  # ����ĩ����С��ȼ�����Ϊ1
        weather_info.loc[i, 'weather_level'] = 1



    if (_row_week >= 6):  # ��ĩ�������������ȼ�����Ϊ3
        weather_info.loc[i, 'weather_level'] = 3

    if IsSubStr(level_2, row) and (_row_week >= 6):  # ��ĩ������ѩ�ȼ�����Ϊ5
        weather_info.loc[i, 'weather_level'] = 5

    if IsSubStr(level_1, row) and (_row_week >= 6):  # ��ĩ����С��ȼ�����Ϊ4
        weather_info.loc[i, 'weather_level'] = 4
    if (Is_h == -1):  # �����������������ȼ�����Ϊ-3
        weather_info.loc[i, 'weather_level'] = -3

    if IsSubStr(level_2, row) and (Is_h == -1):  # ����������ѩ�ȼ�����Ϊ-1
        weather_info.loc[i, 'weather_level'] = -1

    if IsSubStr(level_1, row) and (Is_h == -1):  # ��������С��ȼ�����Ϊ-2
        weather_info.loc[i, 'weather_level'] = -2
weather_info.to_csv('data\\weather_info.csv', encoding='gb2312', index=False)







