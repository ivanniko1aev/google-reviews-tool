from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from app.oauth import router as oauth_router

app = FastAPI()

# Include the OAuth routes
app.include_router(oauth_router)

# Initialize Jinja2 template rendering
templates = Jinja2Templates(directory="app/templates")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route for fetching reviews (optional)
@app.get("/reviews")
async def reviews(access_token: str):
    # Use the access token to fetch reviews
    reviews_data = get_reviews(access_token)
    return {"reviews": reviews_data}




