from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# ======================================================
# 🔒 Load API KEY from Render Environment Variable
# مثل: GEMINI_API_KEY في لوحة التحكم
# ======================================================
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("❌ ERROR: No GEMINI_API_KEY found in environment variables!")

genai.configure(api_key=API_KEY)


@app.route("/rewrite", methods=["POST"])
def rewrite_text():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    original = data["text"]

    prompt = f"""
أعد صياغة النص التالي بالكامل بصياغة صحفية جذابة:
اكتب المخرجات بالشكل التالي فقط:
###TITLE###
(العنوان)
###CONTENT###
(المقال بعد إعادة الصياغة)

النص الأصلي:
{original}
"""

    try:
        # أفضل موديل مجاني حالياً
        model = genai.GenerativeModel("gemini-1.5-flash-8b")

        response = model.generate_content(prompt)
        result = response.text

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "Rewriting Server Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
