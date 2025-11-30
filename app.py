import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/openai-chat", methods=["POST"])
def openai_chat():
    body = request.get_json()
    user_message = body.get("message", "")

    # Gọi OpenAI Responses API
    res = client.responses.create(
        model="gpt-4.1-mini",
        input=user_message
    )

    # Lấy text từ response mới
    try:
        output = res.output[0].content[0].text
    except:
        output = "⚠️ Lỗi đọc output từ OpenAI."

    # Thêm prefix để test xem Playbook có dùng tool hay không
    return jsonify({
        "reply": f"⚡OPENAI-GW⚡ {output}"
    })


@app.route("/", methods=["GET"])
def home():
    return "Welllab OpenAI Gateway Running", 200


if __name__ == "__main__":
    app.run(port=8080)
