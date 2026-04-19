from icalendar import Calendar, Event
import datetime
from datetime import date, timedelta
from dataclasses import dataclass

@dataclass
class Class:
    subject: str 
    begin: list
    end: list
    exam: bool

@dataclass
class Day:
    day: str
    classes: list[Class]

def print_day(Day):
    out = "The day is " + Day.day + "\n"
    if len(Day.classes) < 1: return out + "There are no classes today!\n"

    for c in Day.classes:
        out = out + str(f"{c.subject}: {c.begin} — {c.end}\n")
    
    return out.replace("-","/")

def detect_week(dt):
    i = 0

    if datetime.datetime.strftime(dt,"%A") == "Saturday" or datetime.datetime.strftime(dt,"%A") == "Sunday":
        while (datetime.datetime.strftime(dt,"%A") != "Monday") : 
            dt = dt + timedelta(days=i)
            i = i + 1
        return dt
    
    while (datetime.datetime.strftime(dt,"%A") != "Monday") : 
        dt = dt - timedelta(days=i)
        i = i + 1
    return dt

def print_week(Week,begin):
    out = "**The week is " + str(begin)[5:10] + "**\n\n"

    for d in Week:
        out = out + print_day(d) + "\n"

    return out.replace("-","/")

def detect_diff(prev,new):
    out = None