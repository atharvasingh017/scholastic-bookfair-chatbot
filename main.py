
from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

def load_context():
    with open('bookfair.txt', 'r') as f:
        return f.read()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    context = load_context()
    
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful bookfair assistant. Here's the context: {context}"},
            {"role": "user", "content": user_message}
        ]
    )
    
    return jsonify({"response": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
