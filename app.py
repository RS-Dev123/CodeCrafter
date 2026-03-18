from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
import os

app = Flask(__name__)
CORS(app) 
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

@app.route('/api/analyze', methods=['POST'])
def analyze_claim():
    data = request.json
    user_input = data.get('claim', '')

    if not user_input.strip():
        return jsonify({"error": "Please enter a valid claim."}), 400

    prompt = f"""
    You are a strict AI fact-checking system.
    Return ONLY valid JSON. Do NOT include any extra text or markdown formatting like ```json.
    Format:
    {{
    "verdict": "Likely True" or "Uncertain" or "Fake News",
    "confidence": integer between 0 and 100,
    "reason": "clear and short explanation",
    "category": "Health", "Politics", "Tech", etc.
    }}
    Claim: {user_input}
    """

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        if result_text.startswith("```json"):
            result_text = result_text.replace("```json", "").replace("```", "").strip()
        elif result_text.startswith("```"):
            result_text = result_text.replace("```", "").strip()
        result = json.loads(result_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)