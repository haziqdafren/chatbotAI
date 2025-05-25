from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from profitpal import ProfitPal
import os

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes and origins
bot = ProfitPal()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        response = bot.chat(data['message'])
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")  # Add logging
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET', 'OPTIONS'])
def get_statistics():
    if request.method == 'OPTIONS':
        return '', 200
        
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
        print(f"Error in statistics endpoint: {str(e)}")  # Add logging
        return jsonify({'error': str(e)}), 500

# This is for local development
if __name__ == '__main__':
    app.run(debug=True)

# This is for Vercel
app = app 