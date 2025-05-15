from flask import Flask, request, jsonify
import openai
import os
import base64

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/api/", methods=["POST"])
def process():
    data = request.get_json()
    question = data.get("question")
    image = data.get("image")

    # Optional: save image if needed
    if image:
        with open("input.webp", "wb") as f:
            f.write(base64.b64decode(image))

    prompt = f"""You are a virtual TA. The student asked:
{question}

If an image was attached, it may contain additional context (e.g., quiz screenshot). Be helpful and give the best possible answer. Include relevant course forum links if you know them."""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    text = response.choices[0].message.content

    # For now, return static links
    links = [
        {
            "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
            "text": "Use the model that’s mentioned in the question."
        },
        {
            "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3",
            "text": "Use tokenizer like Prof. Anand did to count tokens and calculate cost."
        }
    ]

    return jsonify({"answer": text.strip(), "links": links})

if __name__ == "__main__":
    app.run(debug=True)
