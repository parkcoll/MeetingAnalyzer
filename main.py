import streamlit as st
import pandas as pd
import plotly.express as px
from auth import authenticate_calendar_service, handle_google_callback, verify_environment_variables
from data_processor import analyze_calendar_data
from visualizer import create_visualizations
from email_sender import send_email_report
from scheduler import schedule_weekly_report
from utils import get_last_week_date_range
import os
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        st.set_page_config(page_title="Calendar Analyzer", layout="wide")
        st.title("Multi-Calendar Analyzer")

        if not verify_environment_variables():
            st.error("Application configuration error. Please contact the administrator.")
            return

        params = st.query_params
        logger.info(f"Query parameters: {params}")

        if "code" in params:
            logger.info("OAuth code found in query parameters")
            calendar_service = handle_google_callback(params["code"])
            if calendar_service:
                st.session_state.calendar_service = calendar_service
            st.rerun()

        calendar_type = st.sidebar.selectbox("Select Calendar Service", ["Google", "Outlook", "Apple"])
        
        if 'calendar_service' not in st.session_state or st.session_state.calendar_service is None:
            calendar_service = authenticate_calendar_service(calendar_type)
            if calendar_service:
                st.session_state.calendar_service = calendar_service
            else:
                if calendar_type == "Google":
                    st.info(f"To use this app, you need to authenticate with {calendar_type} Calendar. Follow the instructions above to start the authentication process.")
                else:
                    st.info(f"{calendar_type} Calendar integration is not yet implemented. Please choose Google Calendar for now.")
                return

        page = st.sidebar.selectbox("Select a page", ["Dashboard", "Manual Report", "Settings"])

        if page == "Dashboard":
            show_dashboard(st.session_state.calendar_service)
        elif page == "Manual Report":
            show_manual_report(st.session_state.calendar_service)
        elif page == "Settings":
            show_settings(st.session_state.calendar_service)

        # Add debug information
        st.sidebar.markdown("---")
        st.sidebar.subheader("Debug Information")
        st.sidebar.text(f"Redirect URI: https://meetmetricsanalyzer.streamlit.app")
        st.sidebar.text(f"Session State Keys: {list(st.session_state.keys())}")
        
    except Exception as e:
        logger.error(f"An error occurred in the main function: {str(e)}")
        st.error("An unexpected error occurred. Please try refreshing the page or contact support if the issue persists.")

def show_dashboard(calendar_service):
    st.header("Dashboard")
    st.write(f"Welcome to your {type(calendar_service).__name__} Analyzer dashboard!")
    
    start_date, end_date = get_last_week_date_range()
    
    with st.spinner("Fetching and analyzing your calendar data..."):
        calendar_service.authenticate()
        df = calendar_service.fetch_events(start_date, end_date)
        
        if df.empty:
            st.warning("No events found for the selected date range.")
            return
        
        analysis = analyze_calendar_data(df)
        
        st.subheader("Last Week's Calendar Statistics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Meetings", analysis['total_meetings'])
        col2.metric("Total Duration (hours)", f"{analysis['total_duration']:.2f}")
        col3.metric("Avg. Duration (hours)", f"{analysis['avg_duration']:.2f}")
        col4.metric("Avg. Attendees", f"{analysis['avg_attendees']:.1f}")
        
        st.subheader("Meetings by Day")
        fig_meetings_by_day = px.bar(
            analysis['meetings_by_day'].reset_index(),
            x='day',
            y='meetings_by_day',
            labels={'day': 'Date', 'meetings_by_day': 'Number of Meetings'},
            title='Meetings per Day'
        )
        st.plotly_chart(fig_meetings_by_day)
        
        st.subheader("Meetings by Category")
        fig_meetings_by_category = px.pie(
            analysis['meetings_by_category'].reset_index(),
            values='category',
            names='index',
            title='Distribution of Meetings by Category'
        )
        st.plotly_chart(fig_meetings_by_category)
        
        st.subheader("Duration by Category")
        fig_duration_by_category = px.bar(
            analysis['duration_by_category'].reset_index(),
            x='index',
            y='duration',
            labels={'index': 'Category', 'duration': 'Total Duration (hours)'},
            title='Total Duration of Meetings by Category'
        )
        st.plotly_chart(fig_duration_by_category)

def show_manual_report(calendar_service):
    st.header("Generate Manual Report")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now().date())
    
    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
    else:
        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                calendar_service.authenticate()
                df = calendar_service.fetch_events(start_date, end_date)
                
                if df.empty:
                    st.warning("No events found for the selected date range.")
                    return
                
                figs = create_visualizations(df)
                
                for fig in figs:
                    st.plotly_chart(fig)
                
                if 'user_email' in st.session_state and send_email_report(st.session_state.user_email, figs):
                    st.success("Report sent successfully!")
                else:
                    st.error("Failed to send report. Please make sure you've set your email in the Settings page.")

def show_settings(calendar_service):
    st.header("Settings")
    
    st.subheader("Email Settings")
    email = st.text_input("Email address for reports", value=st.session_state.get('user_email', ''))
    if st.button("Save Email"):
        st.session_state.user_email = email
        st.success("Email saved successfully!")
    
    st.subheader("Report Schedule")
    schedule_day = st.selectbox("Select day for weekly report", 
                                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    schedule_time = st.time_input("Select time for weekly report")
    
    if st.button("Save Schedule"):
        if 'user_email' in st.session_state:
            schedule_weekly_report(calendar_service, st.session_state.user_email, schedule_day, schedule_time)
            st.success("Weekly report scheduled successfully!")
        else:
            st.error("Please save your email address before scheduling reports.")

if __name__ == "__main__":
    main()