from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OAuth client information from .env file
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SCOPES = ['https://www.googleapis.com/auth/business.manage']

# The redirect URI must match the one registered in the Google Cloud Console
REDIRECT_URI = "http://localhost:8000/auth/callback"  # Make sure this is the same as in the console

router = APIRouter()

# ✅ Define OAuth Client Config in the Correct Format
CLIENT_CONFIG = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "redirect_uris": [REDIRECT_URI]
    }
}

# ✅ Initialize OAuth Flow Using the Correct Format
flow = Flow.from_client_config(CLIENT_CONFIG, scopes=SCOPES, redirect_uri=REDIRECT_URI)

# Session middleware: add session support to FastAPI
# Add this middleware in your FastAPI app (in main.py)
# app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

@router.get("/auth")
async def login():
    # Get the authorization URL to redirect the user for login
    authorization_url, state = flow.authorization_url(
        access_type='offline', 
        include_granted_scopes='true',
        redirect_uri=REDIRECT_URI
    )
    return RedirectResponse(authorization_url)

@router.get("/auth/callback")
async def auth_callback(request: Request, code: str):
    # Use the authorization code to fetch the token
    flow.fetch_token(authorization_response=f'{REDIRECT_URI}?code={code}')
    
    # Retrieve the credentials
    credentials = flow.credentials
    
    # Store the token in session
    request.session['access_token'] = credentials.token
    
    # Redirect user to the reviews page
    return RedirectResponse(url="/reviews")

# Function to fetch reviews using the user's access token
def get_reviews(access_token: str):
    url = "https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/reviews"
    
    # Replace with the actual account and location IDs (either hardcoded or fetched dynamically)
    url = url.format(account_id="your_account_id", location_id="your_location_id")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Returns review data in JSON format
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch reviews")
