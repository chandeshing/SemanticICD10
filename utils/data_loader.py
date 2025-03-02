import pandas as pd
import numpy as np
from typing import Dict, List
import spacy
import json
from models import db, ICD10Code

class ICD10DataLoader:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self._initialize_database()

    def _initialize_database(self):
        """Initialize database with sample data if empty"""
        if ICD10Code.query.count() == 0:
            sample_data = {
                'code': [
                    'A00.0', 'A00.1', 'A00.9',
                    'B01.0', 'B01.1', 'B01.9',
                    'C50.1', 'C50.2', 'C50.9'
                ],
                'description': [
                    'Cholera due to Vibrio cholerae 01, biovar cholerae',
                    'Cholera due to Vibrio cholerae 01, biovar eltor',
                    'Cholera, unspecified',
                    'Varicella meningitis',
                    'Varicella encephalitis',
                    'Varicella without complication',
                    'Malignant neoplasm of central portion of breast',
                    'Malignant neoplasm of upper-inner quadrant of breast',
                    'Malignant neoplasm of breast, unspecified'
                ],
                'category': [
                    'Infectious diseases',
                    'Infectious diseases',
                    'Infectious diseases',
                    'Viral infections',
                    'Viral infections',
                    'Viral infections',
                    'Neoplasms',
                    'Neoplasms',
                    'Neoplasms'
                ]
            }

            for i in range(len(sample_data['code'])):
                vector = self.nlp(sample_data['description'][i]).vector
                code = ICD10Code(
                    code=sample_data['code'][i],
                    description=sample_data['description'][i],
                    category=sample_data['category'][i],
                    vector=json.dumps(vector.tolist())
                )
                db.session.add(code)
            db.session.commit()

    def get_all_categories(self) -> List[str]:
        """Return unique categories"""
        categories = db.session.query(ICD10Code.category).distinct().all()
        return sorted([cat[0] for cat in categories])

    def get_data(self) -> pd.DataFrame:
        """Return the complete dataset"""
        codes = ICD10Code.query.all()

        data = {
            'code': [],
            'description': [],
            'category': [],
            'vector': []
        }

        for code in codes:
            data['code'].append(code.code)
            data['description'].append(code.description)
            data['category'].append(code.category)
            data['vector'].append(np.array(json.loads(code.vector)))

        return pd.DataFrame(data)

    def get_vectors(self) -> np.ndarray:
        """Return processed vectors"""
        df = self.get_data()
        return np.vstack(df['vector'].values)