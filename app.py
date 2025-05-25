from flask import Flask, request, jsonify, render_template
from profitpal import ProfitPal
import os

app = Flask(__name__)
bot = ProfitPal()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        response = bot.chat(data['message'])
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics')
def get_statistics():
    try:
        total_intents = len(bot.intents)
        total_keywords = sum(len(keywords) for keywords in bot.intents.values())
        total_responses = sum(len(responses) for responses in bot.responses.values())
        
        return jsonify({
            'total_intents': total_intents,
            'total_keywords': total_keywords,
            'total_responses': total_responses
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# This is for local development
if __name__ == '__main__':
    app.run(debug=True)

# This is for Vercel
app = app 