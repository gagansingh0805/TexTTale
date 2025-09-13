import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services import audio_service, AudioRequest, AudioResponse

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Create AudioRequest object
            request = AudioRequest(**data)
            
            # Generate audio
            audio_url = audio_service.generate_speech(request.text, request.voice)
            
            if audio_url:
                response = AudioResponse(
                    success=True,
                    audioUrl=audio_url,
                    message="Audio generated successfully"
                )
            else:
                response = AudioResponse(
                    success=False,
                    audioUrl=None,
                    message="Failed to generate audio"
                )
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response.dict()).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": False,
                "message": str(e)
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
