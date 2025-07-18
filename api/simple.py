from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
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

@app.get("/health")
def health():
    return {"status": "healthy", "platform": "Maya Cosmic Blueprint"}

handler = Mangum(app, lifespan="off")