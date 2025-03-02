from flask import Flask, render_template, request, jsonify
from utils.data_loader import MedicalDataLoader
from utils.search_engine import SemanticSearchEngine
from models import db, init_db
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Get DATABASE_URL from environment, with fallback
database_url = os.getenv('DATABASE_URL')
# Railway uses DATABASE_URL, but we need to handle potential postgres:// format
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database only if DATABASE_URL is provided
logger.info("Initializing database...")
if database_url:
    init_db(app)
else:
    logger.warning("No DATABASE_URL found, skipping database initialization")

# Initialize search components within app context
with app.app_context():
    logger.info("Initializing search components...")
    data_loader = MedicalDataLoader()
    search_engine = SemanticSearchEngine(data_loader)
    logger.info("Application initialization complete")

@app.route('/')
def index():
    try:
        logger.info("Loading index page...")
        classifiers = data_loader.get_classifier_types()
        categories = data_loader.get_all_categories()
        return render_template('index.html', classifiers=classifiers, categories=categories)
    except Exception as e:
        logger.error(f"Error loading index: {str(e)}")
        return render_template('index.html', classifiers=[], categories=[], error="Error loading data")

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '')
        category = data.get('category', None)
        classifier_type = data.get('classifier_type', None)

        logger.info(f"Processing search request - Query: {query}, Category: {category}, Classifier: {classifier_type}")

        if not query:
            return jsonify({'error': 'No search query provided'}), 400

        if category == "All":
            category = None

        results = search_engine.search(query, classifier_type, category)
        logger.info(f"Search completed - Found {len(results)} results")
        return jsonify({'results': results})

    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': 'An error occurred during search'}), 500

@app.route('/categories/<classifier_type>')
def get_categories(classifier_type):
    try:
        categories = data_loader.get_all_categories(classifier_type)
        return jsonify({'categories': categories})
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        return jsonify({'error': 'Error fetching categories'}), 500

@app.route('/impressum')
def impressum():
    logger.info("Loading impressum page...")
    return render_template('impressum.html')

@app.route('/datenschutz')
def datenschutz():
    logger.info("Loading datenschutz page...")
    return render_template('datenschutz.html')

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)