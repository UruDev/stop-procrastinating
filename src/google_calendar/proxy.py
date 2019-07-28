import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

class User:
    def __init__(self):
        self.credentials = self.auth()

    def auth(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None

        # The file token.pickle stores the user"s access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(".token.pickle"):
            with open(".token.pickle", "rb") as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                script_dir = os.path.dirname(__file__)
                flow = InstalledAppFlow.from_client_secrets_file(
                    f"{script_dir}/.calendar_credentials.json",
                    SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return creds

    def getUserCredentials(self):
        return self.credentials


class Connection:
    def __init__(self):
        self.user = User()
        self.service = self.startService()
        self.startTime = datetime.datetime.now().isoformat() + \
            'Z'  # 'Z' indicates UTC time

    def startService(self):
        creds = self.user.getUserCredentials()
        return build("calendar", "v3", credentials=creds)