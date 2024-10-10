import pandas as pd

def analyze_calendar_data(df):
    # Perform analysis on the calendar data
    total_meetings = len(df)
    total_duration = df['duration'].sum()
    avg_duration = df['duration'].mean()
    avg_attendees = df['attendees'].mean()
    
    # Group meetings by day
    df['day'] = df['start'].dt.date
    meetings_by_day = df.groupby('day').size()
    
    # Group meetings by category
    meetings_by_category = df.groupby('category').size()
    duration_by_category = df.groupby('category')['duration'].sum()
    
    return {
        'total_meetings': total_meetings,
        'total_duration': total_duration,
        'avg_duration': avg_duration,
        'avg_attendees': avg_attendees,
        'meetings_by_day': meetings_by_day,
        'meetings_by_category': meetings_by_category,
        'duration_by_category': duration_by_category
    }
