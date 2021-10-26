from datetime import date, datetime, timedelta


def main():
    # Date objects
    # Get today's date from simple today()
    today = date.today()
    print("Today's date is ", today)

    # get the date individual component
    print("Date components:", today.day, today.month, today.year)

    # Retrieve today's weekday(0=Monday, 6=saturday)
    print("Today's weekday is :", today.weekday())

    # Datetime objects
    # Get today's date from datetime class
    today = datetime.now()
    print("Today's date is ", today)

    # get time from datetime class
    time_now = datetime.time(datetime.now())
    print("The current time is ", time_now)

    ###### Date formatting #####
    now = datetime.now()

    # %y/%Y - year, %a/%A - weekday, %b/%B -month, %d - day of month
    print(now.strftime("%a, %d %B, %y"))

    # %c - locale's date and time, %x- locale's date, %X- locale's time
    print(now.strftime("Locale date and time: %c"))
    print(now.strftime("Locale date: %x"))
    print(now.strftime("Locale time: %X"))

    ##### Time delta ####
    print(timedelta(days=365, hours=5, minutes=1))

    # print todays date one year from now
    print("one year from now it will be :" + str(now + timedelta(days=365)))

    # time delta that uses more than one argument
    print("In 2 days and 3 weeks, it will be: " + str(now + timedelta(days=2, weeks=3)))

    # calculate the date one week ago
    t = datetime.now() - timedelta(weeks=1)
    s = t.strftime("%A %B %d, %Y")
    print("One week ago it was: " + s)


main()
