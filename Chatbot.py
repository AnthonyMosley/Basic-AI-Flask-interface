from flask import Flask, request, jsonify, render_template
import logging
import ollama
from ollama import Client

app = Flask(__name__)

client = Client(host='http://localhost:11434')
MODEL_NAME = 'llama3:8b'

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')

def talk_to_bot(user_message: str) -> str:
    try:
        response = client.chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': user_message}])
        message_content = get_response_content(response)
        return message_content
    except Exception as e:
        logging.error("Error in talk_to_bot: %s", str(e))
        return 'Error communicating with the AI'

def get_response_content(response) -> str:
    if isinstance(response, dict):
        if 'message' in response and 'content' in response['message']:
            return response['message']['content']
    elif 'choices' in response and response['choices'] and 'message' in response['choices'][0] and 'content' in response['choices'][0]['message']:
        return response['choices'][0]['message']['content']
    return 'No response from the AI'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    ai_response = talk_to_bot(user_message)
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)