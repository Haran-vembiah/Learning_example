from tkinter import *
import datetime

window = Tk()
window.title("Validity Calculator")
window.geometry('450x200')

lbl = Label(window, text="Recharged Date")
lbl.place(x=10, y=10)

_date = Entry()
_date.place(x=100, y=10)

lbl_val = Label(window, text="validity in days")
lbl_val.place(x=10, y=50)

_date_val = Entry()
_date_val.place(x=100, y=50)


def calc():
    tdelta = datetime.timedelta(days=int(_date_val.get()))
    rec_date = datetime.datetime.strptime(_date.get(), '%d/%m/%y')
    expiry_date = rec_date + tdelta
    lbl_expiry.configure(text=expiry_date)


btn1 = Button(window, text='Find Expiry Date', command=calc)
btn1.place(x=100, y=100)

lbl_expiry = Label(window, text="Expiry date??")
# lbl.grid(column=0, row=0)
lbl_expiry.place(x=50, y=150)

window.mainloop()
