from flask import Flask, render_template, request, jsonify
import json
import random
import os

app = Flask(__name__)

# add JSON file
def load_data():
    with open("chatbot_responses_from_pdf.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

from fuzzywuzzy import fuzz

def get_response(user_input):
    user_input = user_input.lower()
    best_match = None
    best_score = 0
    best_response = "Συγγνώμη, δεν κατάλαβα. Θες να ρωτήσεις κάτι άλλο;"

    for category, info in data.items():
        for keyword in info["keywords"]:
            score = fuzz.partial_ratio(keyword.lower(), user_input)
            if score > best_score:
                best_score = score
                best_match = keyword
                best_response = random.choice(info["responses"])
    
    if best_score >= 80:
        return best_response
    else:
        return "Συγγνώμη, δεν κατάλαβα. Θες να ρωτήσεις κάτι άλλο;"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.form["message"]
    response = get_response(message)
    return jsonify({"response": response})

if __name__ == "__main__":
    # start server
    app.run(debug=True)
