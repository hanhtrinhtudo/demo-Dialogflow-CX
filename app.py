import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# ===== OpenAI SDK (new Responses API) =====
try:
    from openai import OpenAI
except ImportError:
    raise Exception("Chưa cài openai SDK. Chạy: pip install openai")

# ===== Load ENV =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    raise Exception("Thiếu biến môi trường OPENAI_API_KEY")

# ===== Init App =====
app = Flask(__name__)
CORS(app)  # Cho phép web client gọi API mà không bị chặn

client = OpenAI(api_key=OPENAI_API_KEY)


# ============================================================================
#   API CHÍNH: /openai-chat
#   Body cần gửi:
#       { "message": "nội dung câu hỏi" }
#
#   Response trả về:
#       { "reply": "câu trả lời" }
# ============================================================================
@app.route("/openai-chat", methods=["POST"])
def openai_chat():
    try:
        body = request.get_json(force=True)
        user_message = body.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Em chưa nhận được câu hỏi của anh/chị."})

        # ===== Gọi OpenAI Responses API =====
        res = client.responses.create(
            model="gpt-4.1-mini",
            input=user_message,
        )

        # Lấy nội dung trả về
        reply_text = res.output_text.strip() if hasattr(res, "output_text") else ""

        if not reply_text:
            reply_text = "Hiện tại em không nhận được kết quả từ hệ thống OpenAI."

        # Trả về cho web / Playbook
        return jsonify({"reply": reply_text})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({
            "reply": "Xin lỗi, hiện tại hệ thống đang gặp lỗi. Anh/chị vui lòng thử lại sau nhé."
        }), 500


@app.route("/", methods=["GET"])
def home():
    return "🔥 Welllab OpenAI Gateway đang chạy ngon lành!", 200


# ============================================================================
#   Run Local
# ============================================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

