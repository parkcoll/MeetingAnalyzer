import os
import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from calendar_services import GoogleCalendarService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_calendar_service(calendar_type):
    if calendar_type == "Google":
        return authenticate_google()
    elif calendar_type == "Outlook":
        return authenticate_outlook()
    elif calendar_type == "Apple":
        return authenticate_apple()
    else:
        st.error(f"Unsupported calendar type: {calendar_type}")
        return None

def authenticate_google():
    logger.info("Starting Google authentication process")
    credentials = st.session_state.get('google_credentials')

    if not credentials or not credentials.valid:
        if not verify_environment_variables():
            logger.error("Authentication failed: Missing Google API credentials")
            st.error("Authentication failed: Missing Google API credentials. Please contact the administrator.")
            return None

        logger.info("No existing Google credentials found, starting OAuth flow")
        client_config = {
            "web": {
                "client_id": os.environ['GOOGLE_CLIENT_ID'],
                "client_secret": os.environ['GOOGLE_CLIENT_SECRET'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
        
        # Updated redirect URI
        redirect_uri = 'https://meetmetricsanalyzer.streamlit.app/'
        logger.info(f"Using redirect URI: {redirect_uri}")
        
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )

        auth_url, _ = flow.authorization_url(prompt='consent')

        logger.info(f"Generated authorization URL: {auth_url}")
        st.write("Please visit this URL to authorize the application:")
        st.write(auth_url)

    if credentials:
        return GoogleCalendarService(credentials)
    return None

def authenticate_outlook():
    # Placeholder for Outlook authentication
    logger.info("Outlook authentication not yet implemented")
    st.error("Outlook Calendar integration is not yet available.")
    return None

def authenticate_apple():
    # Placeholder for Apple Calendar authentication
    logger.info("Apple Calendar authentication not yet implemented")
    st.error("Apple Calendar integration is not yet available.")
    return None

def verify_environment_variables():
    logger.info("Verifying environment variables")
    if not os.environ.get('GOOGLE_CLIENT_ID') or not os.environ.get('GOOGLE_CLIENT_SECRET'):
        logger.error("GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET environment variables are not set")
        return False
    logger.info("Environment variables verified successfully")
    return True

def handle_google_callback(code):
    try:
        logger.info("Starting Google authentication callback process")
        if not verify_environment_variables():
            logger.error("Authentication failed: Missing Google API credentials")
            st.error("Authentication failed: Missing Google API credentials. Please contact the administrator.")
            return None

        client_config = {
            "web": {
                "client_id": os.environ['GOOGLE_CLIENT_ID'],
                "client_secret": os.environ['GOOGLE_CLIENT_SECRET'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
        
        # Updated redirect URI
        redirect_uri = 'https://meetmetricsanalyzer.streamlit.app/'
        logger.info(f"Using redirect URI in callback: {redirect_uri}")
        
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        logger.info("Flow object created successfully")
        
        try:
            flow.fetch_token(code=code)
            logger.info("Token fetched successfully")
        except Exception as token_error:
            logger.error(f"Error fetching token: {str(token_error)}")
            st.error("Failed to authenticate. Please try again or contact support if the issue persists.")
            return None
        
        credentials = flow.credentials
        st.session_state.google_credentials = credentials
        logger.info("Google authentication successful")
        st.success("Google authentication successful! You can now use the app.")
        return GoogleCalendarService(credentials)
    except Exception as e:
        logger.error(f"Error during Google authentication: {str(e)}")
        st.error("Authentication failed. Please try again or contact support if the issue persists.")
        return None
