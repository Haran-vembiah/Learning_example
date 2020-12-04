import datetime
import pytz


# today = datetime.date.today()
# print(today)
from dateutil.utils import today

birthday = datetime.date(1988,6,18)
print(birthday)

divy_birt = datetime.date(1990,9,14)
div_days_since = (today - divy_birt).days
print(div_days_since)

days_since_birth = (today - birthday).days
print(days_since_birth)

tdelta = datetime.timedelta(days=56)
recharge_date = datetime.date(2020,8,10)
print(today+tdelta)
print("expiry date",recharge_date+tdelta)
# Add 10 days to current
print(datetime.datetime.now() + tdelta)

print(today.day)
# monday = 0
print(today.weekday())

# datetime.time(h, m, s, ms)
print(datetime.time(7,2,20,200))

# datetime.date(Y,M,D)
print(datetime.date(2020,5,12))

# datetime.datetime(Y,M,D, h, m, s, ms)
print(datetime.datetime(2020,5,12,19,44,23,200))

# Add 10 hours to current
hour_delta = datetime.timedelta(hours=10)
print(datetime.datetime.now() + hour_delta)


datetime_today = datetime.datetime.now(tz=pytz.UTC)
print(datetime_today)
datetime_pacific = datetime_today.astimezone(pytz.timezone('US/pacific'))
print(datetime_pacific)


state_changed = '2020-09-09T14:54:53.707Z'
state_changed1 = '2020-08-09T14:54:53.707Z'
req_changed = '2020-10-14 19:40:13.305519-07:00'

print(state_changed >= state_changed1)

datetime_str = '09/19/18 13:55:26'

datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')