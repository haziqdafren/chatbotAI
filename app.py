from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from profitpal import ProfitPal

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
chatbot = ProfitPal()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get response from chatbot
    response = chatbot.chat(user_message)
    
    return jsonify({
        'response': response
    })

@app.route('/api/statistics')
def get_statistics():
    # Calculate statistics
    total_intents = len(chatbot.intents)
    total_keywords = sum(len(keywords) for keywords in chatbot.intents.values())
    total_responses = sum(len(responses) for responses in chatbot.responses.values())
    
    return jsonify({
        'total_intents': total_intents,
        'total_keywords': total_keywords,
        'total_responses': total_responses
    })

if __name__ == '__main__':
    app.run(debug=True) 