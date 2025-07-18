from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from mangum import Mangum

app = FastAPI()

@app.get("/")
async def read_root():
    try:
        return HTMLResponse("""
        <html>
        <head><title>Maya Cosmic Blueprint</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <h1>🌟 Maya Cosmic Blueprint Platform</h1>
            <p>Your spiritual guidance platform is now live!</p>
            <p><a href="/health" style="color: #fff; text-decoration: underline;">Check Health</a></p>
        </body>
        </html>
        """)
    except Exception as e:
        return JSONResponse({"error": str(e), "message": "Homepage error"})

@app.get("/health")
async def health():
    try:
        return {"status": "healthy", "platform": "Maya Cosmic Blueprint", "version": "1.0"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

# Add a simple API endpoint for testing
@app.get("/api/test")
async def test():
    return {"message": "API is working", "status": "success"}

handler = Mangum(app, lifespan="off")