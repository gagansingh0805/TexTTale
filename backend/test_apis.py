import os
import google.generativeai as genai
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Gemini API connection with dummy data"""
    print("Testing Gemini API...")
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY not found in environment variables")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test with dummy prompt
        test_prompt = "Write a short 2-sentence story about a magical cat."
        
        print(f"Sending test prompt: '{test_prompt}'")
        response = model.generate_content(test_prompt)
        
        print("SUCCESS: Gemini API Response:")
        print(f"Story: {response.text}")
        return True
        
    except Exception as e:
        print(f"ERROR: Gemini API Error: {e}")
        return False

def test_huggingface_api():
    """Test Hugging Face API connection with dummy data"""
    print("\nTesting Hugging Face API...")
    
    HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
    
    if not HF_API_TOKEN:
        print("ERROR: HUGGINGFACE_API_TOKEN not found in environment variables")
        return False
    
    try:
        # Hugging Face API configuration
        HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        
        # Test with dummy prompt
        test_prompt = "a magical cat sitting on a rainbow, digital art, beautiful"
        
        payload = {
            "inputs": test_prompt,
            "parameters": {
                "negative_prompt": "blurry, low quality, distorted, ugly",
                "num_inference_steps": 10,  # Reduced for faster testing
                "guidance_scale": 7.5
            }
        }
        
        print(f"Sending test prompt: '{test_prompt}'")
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            print("SUCCESS: Hugging Face API Response: Image generated successfully!")
            print(f"Image size: {len(response.content)} bytes")
            
            # Save test image
            with open("test_image.png", "wb") as f:
                f.write(response.content)
            print("Test image saved as 'test_image.png'")
            return True
            
        elif response.status_code == 503:
            print("WARNING: Hugging Face model is loading... Please wait and try again.")
            return False
            
        else:
            print(f"ERROR: Hugging Face API Error: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: Hugging Face API Error: {e}")
        return False

def test_story_generation():
    """Test the story generation API"""
    url = "http://localhost:8001/api/generate-story"
    
    payload = {
        "text": "A magical cat discovers it can time travel",
        "style": "fantasy",
        "length": "short",
        "voice": "man"
    }
    
    try:
        print("Testing story generation...")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS!")
            print(f"Generated {len(data['story'])} scenes")
            for i, scene in enumerate(data['story']):
                print(f"Scene {i+1}: {scene['text'][:100]}...")
        else:
            print("ERROR!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_health():
    """Test the health endpoint"""
    url = "http://localhost:8001/health"
    
    try:
        response = requests.get(url)
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

def main():
    """Run all API tests"""
    print("Starting API Connection Tests...\n")
    
    # Test individual APIs
    gemini_ok = test_gemini_api()
    hf_ok = test_huggingface_api()
    
    # Test complete story generation
    story_ok = test_story_generation()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY:")
    print(f"Gemini API: {'SUCCESS' if gemini_ok else 'FAILED'}")
    print(f"Hugging Face API: {'SUCCESS' if hf_ok else 'FAILED'}")
    print(f"Story Generation: {'SUCCESS' if story_ok else 'FAILED'}")
    
    if gemini_ok and hf_ok and story_ok:
        print("\nAll APIs are working correctly!")
    else:
        print("\nSome APIs need attention. Check the errors above.")
    
    print("="*50)

if __name__ == "__main__":
    print("=== Testing TextTales API ===")
    test_health()
    print("\n=== Testing Story Generation ===")
    test_story_generation()
