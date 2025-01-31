from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from app.oauth import router as oauth_router

app = FastAPI()

# Add session middleware with a secret key
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

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
@app.get("/reviews", response_class=HTMLResponse)
async def reviews_page(request: Request):
    return templates.TemplateResponse("reviews.html", {"request": request})




