import calendar

# create a plain test calendar
c = calendar.TextCalendar(calendar.SUNDAY)
st = c.formatmonth(2021, 11, 0, 0)
print(st)

# create an HTML formatted calendar
hc = calendar.HTMLCalendar(calendar.SUNDAY)
st = hc.formatmonth(2021, 10)
print(st)

# Loop over the days of month
for monthname in calendar.month_name:
    print(monthname)

for dayname in calendar.day_name:
    print(dayname)

# Team meeting on the first friday of every month
# To figure out what days that would be for each month
print("Team meetings will be on: ")
for m in range(1, 13):
    cal = calendar.monthcalendar(2021, m)  # It returns list of list, list of week days in a list of every week.
    # print(cal)
    weekone = cal[0]
    weektwo = cal[1]

    if weekone[calendar.FRIDAY] != 0:
        meetday = weekone[calendar.FRIDAY]
    else:
        meetday = weektwo[calendar.FRIDAY]

    print("%10s %2d" % (calendar.month_name[m], meetday))
