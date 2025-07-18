from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maya Cosmic Blueprint Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            padding: 40px;
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .star { font-size: 3rem; margin-bottom: 10px; display: block; }
        p {
            font-size: 1.2rem;
            margin-bottom: 15px;
            line-height: 1.6;
        }
        .health-link {
            display: inline-block;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
            margin-top: 20px;
        }
        .health-link:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .status {
            margin-top: 30px;
            padding: 15px;
            background: rgba(46, 204, 113, 0.2);
            border-radius: 10px;
            border-left: 4px solid #2ecc71;
        }
    </style>
</head>
<body>
    <div class="container">
        <span class="star">⭐</span>
        <h1>Maya Cosmic Blueprint Platform</h1>
        <p>Your spiritual guidance platform is now live and ready!</p>
        <div class="status">
            <strong>✓ Successfully Deployed on Vercel</strong>
        </div>
        <a href="/health" class="health-link">Check System Health</a>
    </div>
</body>
</html>""".encode('utf-8')
            self.wfile.write(html)
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({"status": "healthy", "platform": "Maya Cosmic Blueprint", "deployed": True})
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>404 - Not Found</h1><p><a href="/">Go Home</a></p></body></html>')