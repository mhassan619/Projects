from flask import Flask, render_template,request,jsonify
import requests
app = Flask(__name__)
SYSTEM_PROMPT = """
You are a professional bussiness support chatbot. You are a helpful assistant. Give a very short answer.
"""
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    prompt = SYSTEM_PROMPT + "\nUser: " + user_message + "\nAssistant:"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"tinyllama",
            "prompt":prompt,
            "stream":False,
            "options":{
                "num_predict":100,
                "temperature":1.0,
                "stop":["User:"]
            }
            }
    )
    data = response.json()
    bot_reply = data['response']
    return jsonify({"reply":bot_reply})
if __name__ == ("__main__"):
    app.run(debug=True)