from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OAuth client information from .env file
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")  # Path to the credentials file
SCOPES = ['https://www.googleapis.com/auth/business.manage']

# The redirect URI must match the one registered in the Google Cloud Console
REDIRECT_URI = "http://localhost:8000/auth/callback"  # Make sure this is the same as in the console

router = APIRouter()

# Initialize OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(
    CREDENTIALS_PATH, SCOPES
)

@router.get("/auth")
async def login():
    # Get the authorization URL to redirect the user for login
    authorization_url, state = flow.authorization_url(
        access_type='offline', 
        include_granted_scopes='true'
    )
    return RedirectResponse(authorization_url)

@router.get("/auth/callback")
async def auth_callback(code: str):
    # Use the authorization code to fetch the token
    flow.fetch_token(
        authorization_response=f'{REDIRECT_URI}?code={code}'  # Pass the code from the callback
    )
    
    # Retrieve the credentials
    credentials = flow.credentials
    
    # Save or use the credentials for making Google My Business API calls
    # Ideally, store the credentials securely (e.g., in a session or database)
    return {"access_token": credentials.token}
