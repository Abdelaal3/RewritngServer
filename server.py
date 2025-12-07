import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# ============================================
#  CONFIG
# ============================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

MODEL = "gemini-1.5-flash-8b"   # تقدر تغيره لأي موديل أعلى

@app.route("/rewrite", methods=["POST"])
def rewrite():
    try:
        data = request.json
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "Missing text"}), 400

        prompt = f"""
أعد صياغة النص التالي بالكامل بالعربية الفصحى البسيطة بصياغة صحفية احترافية.
أعد كتابة العنوان واجعله جذاباً دون مبالغة.
أعد كتابة المحتوى بالكامل.

اكتب الناتج بهذا الشكل:

###TITLE###
(العنوان الجديد)

###CONTENT###
(المحتوى الجديد)

النص:
{text}
"""

        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)

        return jsonify({"result": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/summary", methods=["POST"])
def summary():
    try:
        data = request.json
        text = data.get("text", "")

        prompt = f"لخص النص التالي في 40–60 كلمة بدون مبالغة:\n{text}"

        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)

        return jsonify({"summary": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/excerpt", methods=["POST"])
def excerpt():
    try:
        data = request.json
        text = data.get("text", "")

        prompt = f"أنشئ مقتطف (Excerpt) من 20 كلمة للنص التالي:\n{text}"

        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)

        return jsonify({"excerpt": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "FG Gemini Python Server is running!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
