#! /usr/bin/env python3

from google_calendar.proxy import Connection
from google_calendar.calendar_model import Calendar
from google_calendar.reminder import remind

def invoke_operation(args):
    connection = Connection()
    calendar = Calendar(connection, "primary")
    calendar.getEventList("next week")#

def main():
    invoke_operation("a")
    remind.run()


if __name__ == "__main__":
    main()