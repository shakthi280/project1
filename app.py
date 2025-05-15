from flask import Flask, request, jsonify
import openai
import base64
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup Flask app
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/api/", methods=["POST"])
def answer_question():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' in request"}), 400

    question = data["question"]
    image_data = data.get("image")

    prompt = f"Answer the student's question:\n\n{question}"

    if image_data:
        prompt += "\n\nAlso consider the image provided."

    try:
        # Ask OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4o if you want
            messages=[
                {"role": "system", "content": "You are a helpful assistant for course-related queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )

        answer = response["choices"][0]["message"]["content"].strip()

        # Dummy links (replace with actual logic if needed)
        links = [
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
                "text": "Use the model that’s mentioned in the question."
            },
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3",
                "text": "You may just need to tokenize and multiply by the rate."
            }
        ]

        return jsonify({
            "answer": answer,
            "links": links
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run app on Render-compatible port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
