import pickle
import os.path
from backend.settings import GoogleCalendarSecretFilePath, TokenFile
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Secret JSON filepath here
# SECRETS_FILE = '/home/madhu/Downloads/credentials_calendar.json'

###########################################################################
#    I STRONGLY SUGGEST TO READ THE DOCUMENTATION HERE                    #
#    https://developers.google.com/calendar/v3/reference/events/insert    #
###########################################################################


def interview_schedule(interview_info):
    creds = None

    if os.path.exists(TokenFile):
        with open(TokenFile, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GoogleCalendarSecretFilePath, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TokenFile, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': interview_info["title"],  # Or whatever summary the API shall receive
        'description': interview_info["description"],  # can take API values
        'start': {
            'dateTime': interview_info["start_time"],  # formatted according to RFC3339
            'timeZone': interview_info["timezone"]
        },
        'end': {
            'dateTime': interview_info["end_time"],  # formatted according to RFC3339
            'timeZone': interview_info["timezone"],
        },
        'attendees': [{"email": email} for email in interview_info["recipients"]],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 120},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', sendUpdates='all', body=event).execute()
    return event







