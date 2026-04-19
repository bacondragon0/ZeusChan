from icalendar import Calendar, Event
from datetime import datetime
from datetime import date, timedelta
from data import Day, Class

def convert(date_time):
    format = '%b %d %Y %I:%M%p'
    datetime_str = datetime.datetime.strptime(date_time, format)

    return datetime_str

def compare_day(dt,day):
    str_dt = str(dt)
    return str_dt[10:20] == day

def to_class_data(sub,dts,dte):
    cls = Class(sub,add_2h(str(dts)[21:26]),add_2h(str(dte)[21:26]),False)
    return cls

def add_2h(strs):
    return str(int(strs[:2]) + 2) + strs[2:]

class ICS:
    def __init__(self,filepath):
        self.file = filepath
        self.ics = None

    def open(self):
        self.file = open(self.file,'rb')
        self.ics = Calendar.from_ical(self.file.read())

    def read_all(self,day):
        for component in self.ics.walk():
            if component.name == "VEVENT" and compare_day(component.get('dtstart'),day):
                print(component.get('summary'))
                print(component.get('dtstart'))
                print(component.get('dtend'))
                print(component.get('dtstamp'))

    def parse_day(self,day):
        out = Day(day,[])
        for component in self.ics.walk():
            if component.name == "VEVENT" and compare_day(component.get('dtstart'),day):
                cls = to_class_data(component.get('summary'),component.get('dtstart'),component.get('dtend'))
                out.classes.append(cls)
                
        return out

    def close(self):
        self.file.close()