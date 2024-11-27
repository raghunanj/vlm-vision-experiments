import json
import os
import requests
import base64
import re

# Use environment variable for API key
api_key = os.environ.get('NVIDIA_API_KEY')
if not api_key:
    raise ValueError("NVIDIA_API_KEY environment variable must be set")

# Model endpoints
vlm_endpoint = "https://ai.api.nvidia.com/v1/vlm/adept/fuyu-8b"

# Fields to extract
fields = [
    ("full_name", "The complete name of the person on the ID card"),
    ("id_number", "The identification number or DNI number"),
    ("date_of_birth", "The date of birth in the format shown on the ID"),
    ("nationality", "The nationality of the ID holder"),
    ("expiry_date", "The expiration date of the ID card")
]

def verify_image_exists(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    return True

def extract_json_from_text(text):
    """Extract valid JSON from text, handling common formatting issues."""
    try:
        # Try to find JSON-like content between curly braces
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_str = text[start:end+1]
            # Clean up common formatting issues
            json_str = json_str.replace("'", '"')  # Replace single quotes with double quotes
            json_str = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)  # Add quotes to keys
            json_str = re.sub(r':\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([,}])', r':"\1"\2', json_str)  # Add quotes to string values
            return json.loads(json_str)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return None

def call_vlm_api(image_path, prompt, api_key):
    """Call the VLM API directly"""
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": f'IMPORTANT: Return ONLY this exact JSON structure with values from the Spanish ID card image - no other text: {{"full_name":"FULL_NAME_FROM_CARD","id_number":"ID_NUMBER_FROM_CARD","date_of_birth":"DD MM YYYY","nationality":"NATIONALITY_CODE","expiry_date":"DD MM YYYY"}} <img src="data:image/jpeg;base64,{image_b64}" />'
            }
        ],
        "max_tokens": 256,
        "temperature": 0.01,
        "stream": False
    }

    response = requests.post(vlm_endpoint, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

# Process an image
image_path = os.path.join("sample_data", "images", "esp_id_00.jpg")

try:
    # Verify image exists
    verify_image_exists(image_path)
    
    # Prepare fields
    field_names = [x[0] for x in fields]
    field_descriptions = [x[1] for x in fields]
    
    print(f"Processing image: {image_path}")
    print("Extracting fields:", ", ".join(field_names))

    # Call VLM API directly
    result = call_vlm_api(image_path, "", api_key)
    
    # Extract the content and parse JSON
    content = result["choices"][0]["message"]["content"]
    extracted_json = extract_json_from_text(content)
    
    # Print results
    print("\nExtracted Information:")
    if extracted_json:
        print(json.dumps(extracted_json, indent=2))
    else:
        print("Failed to extract valid JSON from response")
        print("Raw response:", content)

except FileNotFoundError as e:
    print(f"File Error: {str(e)}")
except requests.exceptions.RequestException as e:
    print(f"API Error occurred: {str(e)}")
    if hasattr(e, 'response'):
        print(f"Response status code: {e.response.status_code}")
        print(f"Response content: {e.response.text}")
except Exception as e:
    print(f"Error occurred: {str(e)}")
    if hasattr(e, '__dict__'):
        print(f"Error details: {e.__dict__}")
