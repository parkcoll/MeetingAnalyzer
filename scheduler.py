from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from data_processor import analyze_calendar_data
from visualizer import create_visualizations
from email_sender import send_email_report
from utils import get_last_week_date_range

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_weekly_report(calendar_service, email, day, time):
    # Remove existing job if it exists
    scheduler.remove_job('weekly_report')
    
    # Schedule the new job
    scheduler.add_job(
        generate_and_send_report,
        CronTrigger(day_of_week=day.lower()[:3], hour=time.hour, minute=time.minute),
        id='weekly_report',
        args=[calendar_service, email]
    )

def generate_and_send_report(calendar_service, email):
    start_date, end_date = get_last_week_date_range()
    
    # Fetch and process data
    calendar_service.authenticate()
    df = calendar_service.fetch_events(start_date, end_date)
    
    # Analyze data
    analysis = analyze_calendar_data(df)
    
    # Create visualizations
    figs = create_visualizations(df)
    
    # Send email report
    send_email_report(email, figs)
