import google.generativeai as genai

# Set up the API key
genai.configure(api_key="AIzaSyBc_RdmRi9ESMDmo5LQjuWjnA4x2WM0zF8")

# List available models
for m in genai.list_models():
    print(m.name)
