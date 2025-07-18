from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <head><title>Maya Cosmic Blueprint</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <h1>🌟 Maya Cosmic Blueprint Platform</h1>
                <p>Your spiritual guidance platform is now live on Vercel!</p>
                <p><a href="/health" style="color: #fff;">Health Check</a></p>
            </body>
            </html>
            """.encode()
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