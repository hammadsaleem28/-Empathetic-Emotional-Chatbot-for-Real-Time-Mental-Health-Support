from flask import Flask, request, jsonify, render_template
from models.model_loader import ModelLoader
import logging
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

model_loader = ModelLoader()

logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response_route():
    try:
        user_input = request.json.get('message')
        if not user_input:
            return jsonify(response="No input provided."), 400
        # user_input = str(user_input)
        bot_response = model_loader.process_input(user_input)
        return jsonify(response=bot_response)
    except Exception as e:
        logging.error(f"Error processing input: {e}")
        return jsonify(response="An error occurred while processing your input. Please try again later."), 500

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
