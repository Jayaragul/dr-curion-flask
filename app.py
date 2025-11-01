import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Gemini AI API Key
API_KEY = "AIzaSyCleNExe_HUTo7aZ5N0kxUEDSoYdyxKmvg"
genai.configure(api_key=API_KEY)

# Primary and fallback models
primary_model_name ="gemini-1.5-flash-latest"
fallback_model_name = "gemini-1.5-flash-001-tuning"

# Load models
primary_model = genai.GenerativeModel(primary_model_name)
fallback_model = genai.GenerativeModel(fallback_model_name)

# Function to generate medical response
def generate_medical_response(query):
    if not query.strip():
        return "Error: Please enter symptoms."

    prompt = f"""
    A patient reports: "{query}".
    As an experienced doctor, provide a concise response with:
    - Likely diagnosis
    - Possible causes
    - Specific medications (eg suggest prescription in Indian brand)
    - Key medical advice (1-3 lines)
    Format the response clearly.
    """

    # Try primary model
    try:
        response = primary_model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, "text") else "Error: No valid response from flash model."
    except Exception as e:
        print("Primary model failed:", str(e))
    
    # Try fallback model
    try:
        response = fallback_model.generate_content(prompt)
        fallback_msg = "\n\n⚠️ *Note: Fallback model used due to an error with the main model.*"
        return (response.text.strip() + fallback_msg) if response and hasattr(response, "text") else "Error: Fallback model also failed."
    except Exception as e:
        print("Fallback model failed:", str(e))
        return "Error: AI model encountered an issue."

@app.route('/')
def home():
    return render_template('index.html')  

@app.route('/get_diagnosis', methods=['POST'])
def get_diagnosis():
    data = request.get_json()
    query = data.get("query", "")
    response = generate_medical_response(query)
    return jsonify({"response": response})

# Run the Flask app
import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
