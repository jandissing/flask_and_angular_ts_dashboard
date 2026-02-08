#!/usr/bin/env python3
"""
Minimal Flask test to verify basic server functionality
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "working", "message": "Flask is running!"})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "message": "Health check passed"})

if __name__ == '__main__':
    print("Starting minimal Flask test server on http://localhost:8000")
    app.run(debug=True, host='0.0.0.0', port=6000)
