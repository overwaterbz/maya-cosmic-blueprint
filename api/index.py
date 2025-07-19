from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Maya Cosmic Blueprint Platform</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; }
            .container { max-width: 800px; margin: 0 auto; padding: 40px; background: rgba(255,255,255,0.1); border-radius: 20px; }
            h1 { font-size: 3em; margin-bottom: 20px; }
            p { font-size: 1.2em; line-height: 1.6; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌟 Maya Cosmic Blueprint Platform</h1>
            <p>Your spiritual guidance platform is now live!</p>
            <p>Features coming online:</p>
            <ul style="text-align: left; display: inline-block;">
                <li>Maya cosmic blueprint analysis</li>
                <li>AI-powered spiritual guidance</li>
                <li>Soul contract generation</li>
                <li>Ix Chel chatbot companion</li>
            </ul>
            <p><strong>Platform Status: LIVE ✅</strong></p>
        </div>
    </body>
    </html>
    """)

@app.get("/health")
def health_check():
    return {"status": "healthy", "platform": "Maya Cosmic Blueprint", "version": "1.0"}

@app.get("/api/status")
def api_status():
    return {"api": "online", "features": ["cosmic_analysis", "spiritual_guidance", "soul_contracts"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
