import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Gemini AI API Key
API_KEY = "AIzaSyBc_RdmRi9ESMDmo5LQjuWjnA4x2WM0zF8"
genai.configure(api_key=API_KEY)

# Load Model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Function to generate medical response from the AI model
def generate_medical_response(query):
    if not query.strip():
        return "Error: Please enter symptoms."

    prompt = f"""
    A patient reports: "{query}".
    As an experienced doctor, provide a concise response with:
    - Likely diagnosis
    - Possible causes
    - Specific medications (prescription in Indian brand)
    - Key medical advice (1-2 lines)
    Format the response clearly.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, "text") else "Error: No valid response."
    except:
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
if __name__ == "__main__":
    app.run(debug=True, port=5000)
