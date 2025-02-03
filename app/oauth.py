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

# Session middleware: add session support to FastAPI
# Add this middleware in your FastAPI app (in main.py)
# app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

@router.get("/auth")
async def login(request: Request):
     # ✅ Create a new flow instance for each request
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    # Get the authorization URL to redirect the user for login
    authorization_url, state = flow.authorization_url(
        access_type='offline', 
        include_granted_scopes='true'
        
    )
    
    request.session['oauth_state'] = state
    
    return RedirectResponse(authorization_url)

@router.get("/auth/callback")
async def auth_callback(request: Request, code: str, state: str):
    session_state = request.session.get('oauth_state')
    
    # ✅ Debugging logs
    print("Session state:", session_state)
    print("Returned state:", state)
    
        # ✅ Recreate the flow for token exchange
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    # Exchange the authorization code for an access token
    flow.fetch_token(authorization_response=f'{REDIRECT_URI}?code={code}&state={state}')
    credentials = flow.credentials

    # Store access token in the session
    request.session['access_token'] = credentials.token

    return RedirectResponse(url="/reviews")

def get_account_info(access_token: str):
    url = "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    print("📡 Accounts API Status:", response.status_code)
    print("📊 Accounts API Response:", response.text)

    if response.status_code == 200:
        return response.json().get('accounts', [])
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch account information")

def get_locations(access_token: str, account_id: str):
    url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    print("📡 Locations API Status:", response.status_code)
    print("📊 Locations API Response:", response.text)

    if response.status_code == 200:
        return response.json().get('locations', [])
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch locations")

def fetch_reviews_from_google(request: Request):
    access_token = request.session.get('access_token')
    if not access_token:
        print("🚫 No access token found!")
        raise HTTPException(status_code=401, detail="Unauthorized")

    print(f"🔐 Using access token: {access_token[:10]}...")

    # ✅ Step 1: Get account info
    accounts = get_account_info(access_token)
    if not accounts:
        raise HTTPException(status_code=404, detail="No Google Business accounts found.")
    
    account_id = accounts[0]['name'].split('/')[-1]  # Extract the account ID
    print(f"✅ Account ID: {account_id}")

    # ✅ Step 2: Get locations for the account
    locations = get_locations(access_token, account_id)
    if not locations:
        raise HTTPException(status_code=404, detail="No locations found for this account.")
    
    location_id = locations[0]['name'].split('/')[-1]  # Extract the location ID
    print(f"✅ Location ID: {location_id}")

    # ✅ Step 3: Fetch reviews for the location
    reviews_data = get_reviews(access_token, account_id, location_id)
    print("🌐 Reviews Fetched:", reviews_data)

    return reviews_data.get("reviews", [])


def get_reviews(access_token: str, account_id: str, location_id: str):
    url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/reviews"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    print("📡 Reviews API Status:", response.status_code)
    print("📊 Reviews API Response:", response.text)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch reviews")

    



