import datetime as dt

import pandas as pd
import win32com.client

begin = dt.datetime(2021, 9, 1)
end = dt.datetime(2021, 10, 1)


def get_calendar(begin, end):
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
    calendar = outlook.getDefaultFolder(9).Items
    calendar.IncludeRecurrences = True
    calendar.Sort('[Start]')
    restriction = "[Start] >= '" + begin.strftime('%m/%d/%Y') + "' AND [END] <= '" + end.strftime('%m/%d/%Y') + "'"
    calendar = calendar.Restrict(restriction)
    return calendar


def get_appointments(calendar, body_kw=None):
    cal_subject = [app.subject for app in calendar if app.duration != 1440]
    cal_organizer = [app.Organizer for app in calendar if app.duration != 1440]
    cal_start = [((app.start).time()).strftime("%H:%M") for app in calendar if app.duration != 1440]
    cal_end = [((app.end).time()).strftime("%H:%M") for app in calendar if app.duration != 1440]
    cal_duration = [app.duration for app in calendar if app.duration != 1440]
    cal_date = [(app.end).date() for app in calendar if app.duration != 1440]
    df = pd.DataFrame({
        'subject': cal_subject,
        'organizer': cal_organizer,
        'date': cal_date,
        'start': cal_start,
        'end': cal_end,
        'duration': cal_duration
    })
    return df

cal = get_calendar(begin, end)
appointment = get_appointments(cal)
print(type(appointment))
filename = 'Meeting_data_of_' + str(begin.strftime("%B")) +'_month.xlsx'
summary = appointment.groupby('subject')['duration'].sum()
print(type(summary))

date_wise_details = appointment.groupby('date').sum()
with pd.ExcelWriter(filename) as writer:
    appointment.to_excel(writer, sheet_name='Detiled_info')
    summary.to_excel(writer,sheet_name='Meeting_wise_data')
    date_wise_details.to_excel(writer,sheet_name='Date_wise_data')

