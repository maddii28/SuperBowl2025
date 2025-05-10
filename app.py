from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load the JSON data
with open("comments_with_sentiment.json", "r") as file:
    comments_data = json.load(file)

@app.route('/data')
def get_data():
    return jsonify(comments_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
