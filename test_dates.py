import datetime

x = datetime.datetime(2022, 4, 19, 13, 52, 43)
n = x - datetime.timedelta(seconds=2)
print(n)
