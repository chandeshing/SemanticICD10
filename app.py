from flask import Flask, render_template, request, jsonify
from utils.data_loader import ICD10DataLoader
from utils.search_engine import SemanticSearchEngine
from models import db, init_db
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
logger.info("Initializing database...")
init_db(app)

# Initialize search components within app context
with app.app_context():
    logger.info("Initializing search components...")
    data_loader = ICD10DataLoader()
    search_engine = SemanticSearchEngine(data_loader)
    logger.info("Application initialization complete")

@app.route('/')
def index():
    try:
        logger.info("Loading index page...")
        categories = data_loader.get_all_categories()
        return render_template('index.html', categories=categories)
    except Exception as e:
        logger.error(f"Error loading index: {str(e)}")
        return render_template('index.html', categories=[], error="Error loading categories")

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '')
        category = data.get('category', None)

        logger.info(f"Processing search request - Query: {query}, Category: {category}")

        if not query:
            return jsonify({'error': 'No search query provided'}), 400

        if category == "All":
            category = None

        results = search_engine.search(query, category)
        logger.info(f"Search completed - Found {len(results)} results")
        return jsonify({'results': results})

    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': 'An error occurred during search'}), 500

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000)