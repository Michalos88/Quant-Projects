from pandas_datareader import data as web
import datetime


start1 = datetime.datetime(2016, 9, 21)
end1 = datetime.datetime(2016, 9, 21)
start2 = datetime.datetime(2016, 9, 22)
end2 = datetime.datetime(2016, 9, 22)

SPY1 = web.DataReader("SPY", 'yahoo', start1, end1)
VIX1 = web.DataReader("VIX",'yahoo', start1, end1)


SPY1['Time of Download'] = datetime.datetime.time(datetime.datetime.now())
print(SPY1)

path = 'C:/Users/Class2017/Desktop/University/FE621/HW/HW1/Code/'
SPY1.to_csv(path+'DATA1.csv')
VIX1.to_csv(path+'DATA1a.csv')

