import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Simple test story generation
            test_story = [
                {
                    "text": f"Once upon a time, {data.get('text', 'there was a magical adventure')}...",
                    "sceneNumber": 1,
                    "audioUrl": None,
                    "backgroundNoiseUrl": None
                },
                {
                    "text": "The story continued with exciting twists and turns that kept everyone on the edge of their seats.",
                    "sceneNumber": 2,
                    "audioUrl": None,
                    "backgroundNoiseUrl": None
                }
            ]
            
            response = {
                "success": True,
                "story": test_story,
                "characters": ["Hero", "Villain", "Helper"],
                "introduction": "Welcome to this amazing story!",
                "message": "Test story generated successfully"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": False,
                "message": f"Error: {str(e)}"
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()