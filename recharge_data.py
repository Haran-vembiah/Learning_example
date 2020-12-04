import datetime

tdelta = datetime.timedelta(days=24)
recharge_date = datetime.date(2020,12,2)

print("expiry date",recharge_date+tdelta)
