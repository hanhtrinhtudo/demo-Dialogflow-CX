import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/openai-chat", methods=["POST"])
def openai_chat():
    body = request.get_json()
    user_message = body.get("message", "")

    res = client.responses.create(
        model="gpt-4.1-mini",
        input=user_message
    )

    output = res.output_text

    return jsonify({
        "reply": output
    })

@app.route("/", methods=["GET"])
def home():
    return "Welllab OpenAI Webhook Running", 200

if __name__ == "__main__":
    app.run(port=8080)
