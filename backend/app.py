from flask import Flask, request, jsonify, send_from_directory
from bardapi import Bard
import os
import json

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# Set your Bard API key
BARD_API_KEY = "g.a000uQjr2geasosZbndACDSmPdMWNWliPGApTFrARHHsaKq67kZ9srRC1fEE-f65Go4WOnZuTAACgYKAYcSARISFQHGX2MipvZ33vPn9Vo8o809cyr4pBoVAUF8yKpCJN2XIimnHgdzUTN4O7C20076"
bard = Bard(token=BARD_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic", "General")
    num_questions = data.get("num_questions", 10)  # Default to 10 questions

    # Generate questions using Bard API
    prompt = f"Generate {num_questions} short interview questions and answers about {topic} in point form."
    try:
        response = bard.get_answer(prompt)
        print("Raw API Response:", response)  # Debugging line
        if response and "content" in response:
            qa_pairs = response["content"].strip().split("\n\n")  # Split into individual Q&A pairs
            print("QA Pairs:", qa_pairs)  # Debugging line
        else:
            return jsonify({"error": "Invalid response from Bard API."}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to generate questions: {e}"}), 500

    # Format the data
    formatted_data = []
    for qa in qa_pairs:
        if "Question:" in qa and "Answer:" in qa:
            try:
                question = qa.split("Question:")[1].split("Answer:")[0].strip()
                answer = qa.split("Answer:")[1].strip()

                # Remove unwanted '*' symbols
                question = question.replace("*", "").strip()
                answer = answer.replace("*", "").strip()

                formatted_data.append({
                    "context": question,
                    "answer": answer,
                })
            except IndexError:
                print(f"Skipping malformed QA pair due to parsing error: {qa}")
        else:
            print(f"Skipping malformed QA pair: {qa}")

    print("Formatted Data Sent to Frontend:", formatted_data)  # Debugging line
    return jsonify({"questions": formatted_data})

if __name__ == "__main__":
    app.run(debug=True)