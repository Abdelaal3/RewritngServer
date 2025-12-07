from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# ========= CONFIG ==========
API_KEY = "AIzaSyD2lqGF23CJo8kKYUrx0aJUJAT4k5ah0ZM"
genai.configure(api_key=API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "Rewriting Server Running"

@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.json
    
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    original = data["text"]

    prompt = f"""
أعد صياغة النص التالي بالكامل:
- بأسلوب صحفي احترافي
- إعادة كتابة بدون حذف معلومات
- غير العنوان واجعله جذاب
- لا تضف عناوين فرعية

اكتب الناتج بهذا التنسيق بالضبط:

###TITLE###
(العنوان الجديد)

###CONTENT###
(المحتوى بعد إعادة الكتابة)

النص:
{original}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        output = response.text

        return jsonify({"result": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run (for local debugging only)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
