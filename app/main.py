from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from app.oauth import router as oauth_router, fetch_reviews_from_google
import os

# ✅ Load environment variables
load_dotenv()

# ✅ Get the secret key from .env
SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

app = FastAPI()

# Add session middleware with a secret key
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, same_site="lax", https_only=False)

# Include the OAuth routes
app.include_router(oauth_router)

# Initialize Jinja2 template rendering
templates = Jinja2Templates(directory="app/templates")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to render the reviews page (reviews.html)
@app.get("/reviews")
async def reviews_page(request: Request):
    # ✅ Debug logs
    print("📥 Received request to /reviews")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        print("🔍 Detected AJAX (fetch) request")
        try:
            reviews = fetch_reviews_from_google(request)
            print(f"✅ Fetched {len(reviews)} reviews")  # Log the number of reviews
            return JSONResponse({"reviews": reviews})
        except HTTPException as e:
            print(f"❌ Error fetching reviews: {e.detail}")
            return JSONResponse({"error": e.detail}, status_code=e.status_code)
    else:
        print("🖥️ Rendering reviews.html")
        return templates.TemplateResponse("reviews.html", {"request": request})




