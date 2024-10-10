from abc import ABC, abstractmethod
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd

class CalendarService(ABC):
    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def fetch_events(self, start_date, end_date):
        pass

class GoogleCalendarService(CalendarService):
    def __init__(self, credentials):
        self.credentials = credentials
        self.service = None

    def authenticate(self):
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def fetch_events(self, start_date, end_date):
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=start_date.isoformat() + 'Z',
            timeMax=end_date.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        
        df = pd.DataFrame(columns=['summary', 'start', 'end', 'duration', 'attendees', 'category'])
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
            duration = (end_dt - start_dt).total_seconds() / 3600  # Duration in hours
            
            attendees = len(event.get('attendees', []))
            
            category = self.categorize_meeting(event['summary'])
            
            df = df.append({
                'summary': event['summary'],
                'start': start_dt,
                'end': end_dt,
                'duration': duration,
                'attendees': attendees,
                'category': category
            }, ignore_index=True)
        
        return df

    def categorize_meeting(self, summary):
        summary = summary.lower()
        if 'project' in summary:
            return 'Project'
        elif 'department' in summary or 'team' in summary:
            return 'Department'
        elif 'client' in summary or 'customer' in summary:
            return 'Client'
        elif 'interview' in summary:
            return 'Recruitment'
        elif 'training' in summary or 'workshop' in summary:
            return 'Training'
        else:
            return 'Other'

# Placeholder for future calendar services
class OutlookCalendarService(CalendarService):
    def authenticate(self):
        # Implement Outlook authentication
        pass

    def fetch_events(self, start_date, end_date):
        # Implement Outlook event fetching
        pass

class AppleCalendarService(CalendarService):
    def authenticate(self):
        # Implement Apple Calendar authentication
        pass

    def fetch_events(self, start_date, end_date):
        # Implement Apple Calendar event fetching
        pass
