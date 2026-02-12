"""
Flask API for Nextleap RAG Chatbot.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from api.chatbot import NextleapChatbot

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Initialize chatbot
vector_db_path = Path(__file__).parent.parent.parent / 'phase_2' / 'database' / 'vector_db'
metadata_db_path = Path(__file__).parent.parent.parent / 'phase_2' / 'database' / 'metadata.db'

chatbot = NextleapChatbot(
    vector_db_path=str(vector_db_path),
    metadata_db_path=str(metadata_db_path)
)

print("\n[SUCCESS] Flask API server initialized!")


@app.route('/')
def index():
    """Serve frontend."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/styles.css')
def styles():
    """Serve CSS file."""
    return send_from_directory(app.static_folder, 'styles.css')


@app.route('/script.js')
def script():
    """Serve JavaScript file."""
    return send_from_directory(app.static_folder, 'script.js')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat queries."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        # Get response from chatbot
        response = chatbot.answer_query(query)
        
        return jsonify(response)
    
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "chatbot": "initialized"
    })


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print(" NEXTLEAP RAG CHATBOT API SERVER")
    print("=" * 70)
    print("\nServer running at: http://localhost:5000")
    print("Frontend: http://localhost:5000")
    print("API endpoint: http://localhost:5000/api/chat")
    print("\nPress CTRL+C to stop the server")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
