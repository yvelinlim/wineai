from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Templates folder
templates = Jinja2Templates(directory="templates")

# Root route for friendly message
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/wine_ai")
async def wine_ai(
    guests: int = Form(...),
    duration: int = Form(...),
    budget: float = Form(...),
    menu: str = Form("beef,chicken")
):
    try:
        menu_items = [item.strip() for item in menu.split(",")]

        # Estimate drinks
        wine_bottles = round(0.5 * guests * duration / 4)
        beer_liters = round(0.3 * guests * duration / 4, 1)
        liquor_liters = round(0.1 * guests * duration / 4, 1)

        # Pairings
        pairings_map = {
            "beef": "Red wine",
            "chicken": "White wine",
            "fish": "White wine",
            "vegetarian": "Rosé wine",
            "dessert": "Sweet wine"
        }
        pairings = [f"{pairings_map.get(item.lower(),'Red wine')} with {item}" for item in menu_items]

        result = {
            "wine_bottles": wine_bottles,
            "beer_liters": beer_liters,
            "liquor_liters": liquor_liters,
            "pairings": pairings
        }

        return templates.TemplateResponse("index.html", {"request": request, "result": result})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)