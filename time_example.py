import datetime
import time
"""HOW ABOUT `arrow` module? (from arrow import Arrow)"""


print(help(datetime.date))

gvr = datetime.date(1965, 1, 31)
print(gvr)
print(gvr.day)
print(gvr.month)
print(gvr.year)

# timedelta calculates difference in dates
birthday_pablo = datetime.date(1985, 2, 13)
day_100_after_pablo_birthday = datetime.timedelta(100)
print(birthday_pablo + day_100_after_pablo_birthday) # result should be 1985-05-24


print('-----------------------------')


# format date printing:
message = 'Pablo was born on {:%A, %B, %d, %Y}'
print(message.format(birthday_pablo))

print('-----------------------------')

work_start_date = datetime.date(2018, 7, 16) # year-month-day
work_start_time = datetime.time(8, 0, 0) # hours-minutes-seconds
work_start_datetime = datetime.datetime(2018, 7, 16, 8, 0, 0) # year-month-day-hours-minutes-seconds
print(work_start_date)
print(work_start_time)
print(work_start_datetime)

print('-----------------------------')

# current time
now = datetime.datetime.today()
print(now)
print(now.microsecond)

print('-----------------------------')

# convert string datetime to datetime:

moon_landing = "7/20/1969"
moon_landing_datetime = datetime.datetime.strptime(moon_landing, "%m/%d/%Y") # strptime = string parse time
print(moon_landing_datetime)



now = datetime.datetime.today()
now_ts = time.time()
print(now_ts)
print(datetime.datetime.now(tz=None))
now = time.time() *1000
hour_berfore = int(now - 3600)
print(now)
print(int(now))
print(hour_berfore)
