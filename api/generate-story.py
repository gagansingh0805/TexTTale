import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services import story_service, StoryRequest, StoryResponse

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Create StoryRequest object
            request = StoryRequest(**data)
            
            # Validate request
            validation = story_service.validate_story_request(
                request.text, 
                request.style, 
                request.length
            )
            
            if not validation["valid"]:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "message": "; ".join(validation["errors"])
                }).encode())
                return
            
            # Generate story
            result = story_service.generate_story(
                prompt=request.text,
                style=request.style,
                length=request.length,
                characters=request.characters,
                background_noise=request.background_noise,
                include_audio=True
            )
            
            if not result["success"]:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "message": result["message"]
                }).encode())
                return
            
            # Return success response
            response = StoryResponse(
                success=True,
                story=result["story"],
                characters=result["characters"],
                introduction=result["introduction"],
                message=result["message"]
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
