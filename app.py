from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

app = Flask(__name__)


history = []


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.json.get("message")

    history.append({"role": "user", "parts": [user_message]})

    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_message)

    bot_message = response.text
    history.append({"role": "model", "parts": [bot_message]})

    return jsonify({"response": bot_message})

if __name__ == "__main__":
    app.run(debug=True)
