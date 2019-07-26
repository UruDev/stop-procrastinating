import datetime

class Calendar:
    def __init__(self, connection, calendarId):
        self.calendarId = calendarId
        self.events = connection.service.events()

    def getEvent(self, eventId):
        event = self.events.get(self.calendarId, eventId)
        print('\n'+event)

    def getEventList(
        self,
        filterBy=None,
        maxResults=250,
        showDeleted=False,
        orderBy="startTime",
        showHiddenInvitations=False,
        # Change this for filter implementation
        timeMin="2011-06-03",
        timeMax="2021-06-03",
    ):
        if filterBy:
            today = datetime.date.today()

            filter = {
                "prev week": self.prevWeek,
                "prev month": self.prevMonth,
                "prev year": self.prevYear,
                "next week": self.nextWeek,
                "next month": self.nextMonth,
                "next year": self.nextYear,
            }
            filtered = filter[filterBy](today)
            timeMin = filtered["timeMin"].isoformat()
            timeMax = filtered["timeMax"].isoformat()

        events_result = self.events.list(
            calendarId=self.calendarId,
            showDeleted=showDeleted,

            # Research about -07:00 format
            timeMin=timeMin + "T00:00:00-01:00",
            timeMax=timeMax + "T00:00:00-01:00",
            maxResults=maxResults,
            singleEvents=True,  # Throws an error on False
            orderBy=orderBy,
            showHiddenInvitations=showHiddenInvitations
        ).execute()
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
        for event in events:
            try:
                start = event["start"].get(
                    "dateTime", event["start"].get("date"))
                print(start, event["summary"])
            except:
                print(Exception)

            print(event)

        return events

    def prevWeek(self, date):
        if date.weekday() == 0:
            monday = date
        else:
            monday = date - datetime.timedelta(days=date.weekday()-1)

        prev = {
            "timeMin": monday - datetime.timedelta(weeks=1),
            "timeMax": monday - datetime.timedelta(days=1),
        }
        return prev

    def prevMonth(self, date):
        prev = {
            "timeMin": date.replace(day=1) - datetime.timedelta(months=1),
            "timeMax": date.replace(day=1) - datetime.timedelta(days=1),
        }
        return prev

    def prevYear(self, date):
        prev = {
            "timeMin": date.replace(day=1, month=1) - datetime.timedelta(years=1),
            "timeMax": date.replace(day=31, month=12) - datetime.timedelta(years=1),
        }
        return prev

    def nextWeek(self, date):
        sunday = date + datetime.timedelta(days=6-date.weekday())
        nextW = {
            "timeMin": sunday + datetime.timedelta(days=1),
            "timeMax": sunday + datetime.timedelta(weeks=1),
        }
        return nextW

    def nextMonth(self, date):
        nextM = {
            "timeMin": date.replace(day=1) - datetime.timedelta(months=1),
            "timeMax": date.replace(day=1) - datetime.timedelta(days=1),
        }
        return nextM

    def nextYear(self, date):
        nextY = {
            "timeMin": date.replace(day=1, month=1) + datetime.timedelta(years=1),
            "timeMax": date.replace(day=31, month=12) + datetime.timedelta(years=1),
        }
        return nextY
