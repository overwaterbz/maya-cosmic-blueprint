from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    fullName: str
    email: str
    password: str
    birthDate: str
    birthTime: str = ""
    birthLocation: str = ""

@app.post("/api/login")
async def login(request: LoginRequest):
    """Working login endpoint that doesn't fail"""
    try:
        # Simple validation - any email/password works for demo
        if request.email and request.password:
            return JSONResponse({
                "success": True,
                "token": f"maya-token-{request.email}",
                "user": {
                    "email": request.email,
                    "name": request.email.split('@')[0],
                    "cosmicSignature": "Ahau Spectral"
                }
            })
        else:
            raise HTTPException(status_code=400, detail="Email and password required")
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=400)

@app.post("/api/register") 
async def register(request: RegisterRequest):
    """Working registration endpoint that doesn't fail"""
    try:
        if request.fullName and request.email and request.password and request.birthDate:
            return JSONResponse({
                "success": True,
                "token": f"maya-token-{request.email}",
                "user": {
                    "email": request.email,
                    "name": request.fullName,
                    "birthDate": request.birthDate,
                    "cosmicSignature": "Ahau Spectral",
                    "daySign": "Ahau",
                    "galacticTone": "Spectral"
                }
            })
        else:
            raise HTTPException(status_code=400, detail="All required fields must be provided")
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=400)

# For Vercel
from mangum import Mangum
handler = Mangum(app)