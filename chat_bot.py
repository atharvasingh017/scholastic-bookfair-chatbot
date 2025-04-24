
import os
import requests

class ChatBot:
    def __init__(self):
        self.api_key = os.environ["OPENROUTER_API_KEY"]
        self.book_data = self._load_book_data()
    
    def _load_book_data(self):
        with open("bookfair.txt", "r", encoding="utf-8") as f:
            return f.read()
    
    def ask(self, question):
        prompt = f"""
You are a friendly assistant at a school Book Fair. Based on the following information, answer the user's question clearly and politely.

Book Fair Info:
{self.book_data}

User: {question}
Assistant:
"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{
                "role": "user",
                "content": prompt
            }]
        }
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return "Sorry, something went wrong. 😢"
        except Exception as e:
            return f"Error: {str(e)}"
