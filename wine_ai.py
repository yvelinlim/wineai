from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/wine_ai")
async def wine_ai(request: Request):
    """
    Input JSON:
    {
        "guests": int,
        "duration": int,
        "budget": float,
        "menu": ["beef", "chicken"] (optional)
    }
    Output JSON:
    {
        "wine_bottles": int,
        "beer_liters": float,
        "liquor_liters": float,
        "pairings": ["Red wine with beef", ...]
    }
    """
    try:
        data = await request.json()
        guests = int(data.get("guests", 50))
        duration = int(data.get("duration", 4))
        budget = float(data.get("budget", 500))
        menu = data.get("menu", ["beef", "chicken"])

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
        pairings = [f"{pairings_map.get(item.lower(),'Red wine')} with {item}" for item in menu]

        result = {
            "wine_bottles": wine_bottles,
            "beer_liters": beer_liters,
            "liquor_liters": liquor_liters,
            "pairings": pairings
        }

        return JSONResponse({"result": result})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
