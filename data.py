from icalendar import Calendar, Event
from datetime import datetime
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
    if len(Day.classes) < 1: return out + "There are no classes today!"

    for c in Day.classes:
        out = out + str(f"{c.subject} - From {c.begin} To {c.end}\n")
    
    return out