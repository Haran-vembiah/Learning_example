import datetime as dt
from pprint import pprint

import pandas as pd
import win32com.client
import openpyxl

begin = dt.datetime(2021, 6, 1)
end = dt.datetime(2021, 6, 30)

def get_calendar(begin, end):
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
    calendar = outlook.getDefaultFolder(6).Items
    # calendar.IncludeRecurrences = True
    calendar.Sort('[Start]')
    restriction = "[Start] >= '" + begin.strftime('%m/%d/%Y') + "' AND [END] <= '" + end.strftime('%m/%d/%Y') + "'"
    calendar = calendar.Restrict(restriction)
    return calendar


# def get_appointments(calendar, body_kw=None):
#     cal_subject = [app.subject for app in calendar if app.duration != 1440]
#     cal_organizer = [app.Organizer for app in calendar if app.duration != 1440]
#     cal_start = [((app.start).time()).strftime("%H:%M") for app in calendar if app.duration != 1440]
#     cal_end = [((app.end).time()).strftime("%H:%M") for app in calendar if app.duration != 1440]
#     cal_duration = [app.duration for app in calendar if app.duration != 1440]
#     cal_date = [(app.end).date() for app in calendar if app.duration != 1440]
#     df = pd.DataFrame({
#         'subject': cal_subject,
#         'organizer': cal_organizer,
#         'date': cal_date,
#         'start': cal_start,
#         'end': cal_end,
#         'duration': cal_duration
#     })
#     # return cal_subject,cal_organizer,cal_start,cal_end,cal_duration
#     return df

cal = get_calendar(begin, end)
for app in cal:
    print(type(app))
    print(dir(app))
    print(app)
# appointment = get_appointments(cal)
# filename = 'meeting hours' + str((dt.datetime.now()).strftime("%Y_%m_%d")) + '.xlsx'
# cons_filename = 'meeting hours grouped' + str((dt.datetime.now()).strftime("%Y_%m_%d")) + '.xlsx'
# datewise_filename = 'meeting date grouped' + str((dt.datetime.now()).strftime("%Y_%m_%d")) + '.xlsx'
# summary = appointment.groupby('subject')['duration'].sum()
# date_wise_details = appointment.groupby('date').sum()
# summary.to_excel(cons_filename)
# appointment.to_excel(filename)
# date_wise_details.to_excel(datewise_filename)

