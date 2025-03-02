# ICD-10 Semantische Suche / ICD-10 Semantic Search

🏥 Eine semantische Suchmaschine für ICD-10 medizinische Codes mit mehrsprachiger Unterstützung.

A semantic search engine for ICD-10 medical codes with multilingual support.

## Features / Funktionen

- 🔍 Semantische Suche mit natürlicher Sprache / Semantic search with natural language
- 📊 Kategoriefilter / Category filtering
- 🌐 Deutsch & Englisch / German & English
- 💻 Moderne Web-Oberfläche / Modern web interface
- 🏗 Flask & spaCy Backend

## Technologie-Stack / Technology Stack

- Flask (Web Framework)
- spaCy (NLP)
- scikit-learn (Semantic Search)
- PostgreSQL (Database)
- Bootstrap (Frontend)

## Installation

```bash
# Klonen Sie das Repository / Clone the repository
git clone [repository-url]
cd icd10-semantic-search

# Stellen Sie sicher, dass Python 3.11 installiert ist / Ensure Python 3.11 is installed
python --version

# Installieren Sie die Abhängigkeiten / Install dependencies
pip install flask flask-sqlalchemy numpy pandas psycopg2-binary scikit-learn spacy sqlalchemy

# Laden Sie das spaCy-Modell / Download spaCy model
python -m spacy download en_core_web_sm

# Starten Sie die Anwendung / Start the application
python app.py
```

## Umgebungsvariablen / Environment Variables

Die Anwendung benötigt folgende Umgebungsvariablen / The application requires the following environment variables:

- `DATABASE_URL`: PostgreSQL Datenbankverbindung / PostgreSQL database connection
  Format: `postgresql://user:password@host:port/database`

## Datenbank Setup / Database Setup

Die Anwendung erstellt automatisch die erforderlichen Datenbanktabellen und fügt Beispieldaten ein, wenn Sie die Anwendung zum ersten Mal starten.

The application automatically creates the required database tables and inserts sample data when you first start the application.

## Features

### Semantische Suche / Semantic Search
- Natürliche Sprachverarbeitung für präzise Suchergebnisse
- Natural language processing for accurate search results

### Kategoriefilter / Category Filtering
- Filtern Sie nach medizinischen Kategorien
- Filter by medical categories

### Mehrsprachige Unterstützung / Multilingual Support
- Deutsch und Englisch
- German and English

## Entwicklung / Development

### Projektstruktur / Project Structure
```
icd10-search/
├── app.py                 # Flask application
├── models.py             # Database models
├── utils/
│   ├── data_loader.py   # Data loading utilities
│   └── search_engine.py # Search functionality
├── static/
│   └── style.css        # CSS styles
└── templates/           # HTML templates
    ├── index.html
    ├── impressum.html
    └── datenschutz.html
```

### Lokale Entwicklung / Local Development

1. Stellen Sie sicher, dass PostgreSQL installiert ist / Ensure PostgreSQL is installed
2. Erstellen Sie eine lokale Datenbank / Create a local database
3. Setzen Sie die Umgebungsvariablen / Set up environment variables
4. Starten Sie den Entwicklungsserver / Start the development server

### Deployment

Die Anwendung kann auf jeder Plattform deployed werden, die Python und PostgreSQL unterstützt.
The application can be deployed on any platform that supports Python and PostgreSQL.

1. Setzen Sie die Umgebungsvariablen / Set environment variables
2. Installieren Sie die Abhängigkeiten / Install dependencies
3. Starten Sie die Anwendung / Start the application

### Beitragen / Contributing

1. Fork das Repository
2. Erstellen Sie einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit Ihre Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

1. Fork the repository
2. Create a Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Lizenz / License

MIT

## Support

Bei Fragen oder Problemen erstellen Sie bitte ein Issue im GitHub Repository.

For questions or issues, please create an issue in the GitHub repository.