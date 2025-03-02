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
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and search components
init_db(app)
with app.app_context():
    data_loader = MedicalDataLoader()
    search_engine = SemanticSearchEngine(data_loader)

@app.route('/')
def index():
    try:
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

        if not query:
            return jsonify({'error': 'No search query provided'}), 400

        if category == "All":
            category = None

        results = search_engine.search(query, classifier_type, category)
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
    return render_template('impressum.html')

@app.route('/datenschutz')
def datenschutz():
    return render_template('datenschutz.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)