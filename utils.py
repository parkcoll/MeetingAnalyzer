from datetime import datetime, timedelta

def get_last_week_date_range():
    today = datetime.now().date()
    last_week_end = today - timedelta(days=today.weekday() + 1)
    last_week_start = last_week_end - timedelta(days=6)
    return last_week_start, last_week_end
