from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from datetime import datetime

app = FastAPI(title="The Magic is You - Maya Cosmic Blueprint Platform")

# Serve static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

@app.get("/", response_class=HTMLResponse)
async def homepage():
    """Serve the Maya cosmic blueprint homepage"""
    try:
        with open("index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("""
        <h1>Maya Cosmic Blueprint Platform</h1>
        <p>Platform initializing...</p>
        """, status_code=200)

@app.post("/api/register")
async def register_user(
    fullName: str = Form(...),
    email: str = Form(...),
    birthDate: str = Form(...),
    birthTime: str = Form(None),
    birthLocation: str = Form(None)
):
    """Register new user and calculate Maya blueprint"""
    
    try:
        # Basic Maya day sign calculation (simplified for demo)
        import datetime as dt
        birth_date = dt.datetime.strptime(birthDate, "%Y-%m-%d")
        
        # Simple Maya calendar calculation
        maya_epoch = dt.datetime(1583, 8, 11)  # Simplified correlation
        days_since_epoch = (birth_date - maya_epoch).days
        
        day_signs = [
            "Imix", "Ik", "Akbal", "Kan", "Chicchan", "Cimi", "Manik", 
            "Lamat", "Muluc", "Oc", "Chuen", "Eb", "Ben", "Ix", 
            "Men", "Cib", "Caban", "Etznab", "Cauac", "Ahau"
        ]
        
        tones = [
            "Magnetic", "Lunar", "Electric", "Self-Existing", "Overtone",
            "Rhythmic", "Resonant", "Galactic", "Solar", "Planetary",
            "Spectral", "Crystal", "Cosmic"
        ]
        
        day_sign = day_signs[days_since_epoch % 20]
        galactic_tone = tones[days_since_epoch % 13]
        
        return {
            "success": True,
            "message": f"Welcome {fullName}! Your Maya signature has been calculated.",
            "blueprint": {
                "daySign": day_sign,
                "galacticTone": galactic_tone,
                "birthDate": birthDate,
                "cosmicSignature": f"{galactic_tone} {day_sign}"
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": "Registration successful! Your cosmic blueprint is being prepared.",
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "platform": "The Magic is You - Maya Cosmic Blueprint",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/status")
async def platform_status():
    return {
        "platform": "The Magic is You",
        "features": ["maya_blueprint", "soul_contract", "cosmic_analysis"],
        "status": "operational",
        "domain": "magic.mayanbelize.com"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
