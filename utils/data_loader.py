import pandas as pd
import numpy as np
from typing import Dict, List
import spacy
import json
from models import db, MedicalCode

class MedicalDataLoader:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self._initialize_database()

    def _initialize_database(self):
        """Initialize database with sample data if empty"""
        if MedicalCode.query.count() == 0:
            sample_data = {
                'ICD-10': {
                    'codes': ['A00.0', 'A00.1', 'C50.1'],
                    'descriptions': [
                        'Cholera due to Vibrio cholerae',
                        'Cholera due to Vibrio eltor',
                        'Malignant neoplasm of breast'
                    ],
                    'categories': ['Infectious', 'Infectious', 'Neoplasms']
                },
                'ICF': {
                    'codes': ['b110', 'b114', 'd450'],
                    'descriptions': [
                        'Consciousness functions',
                        'Orientation functions',
                        'Walking'
                    ],
                    'categories': ['Mental Functions', 'Mental Functions', 'Mobility']
                },
                'ICD-11': {
                    'codes': ['1A00', '1B01', '2A00'],
                    'descriptions': [
                        'Cholera',
                        'Typhoid fever',
                        'Oral cavity neoplasms'
                    ],
                    'categories': ['Infectious', 'Infectious', 'Neoplasms']
                },
                'DRG': {
                    'codes': ['F01A', 'F03A', 'G01A'],
                    'descriptions': [
                        'Cardiac valve procedure',
                        'Cardiac defibrillator implant',
                        'Neurological procedure'
                    ],
                    'categories': ['Cardiac', 'Cardiac', 'Neurology']
                },
                'OPS': {
                    'codes': ['5-01', '5-02', '5-03'],
                    'descriptions': [
                        'Operation on skull',
                        'Operation on brain',
                        'Operation on spine'
                    ],
                    'categories': ['Surgery', 'Surgery', 'Surgery']
                },
                'Morbi-RSA': {
                    'codes': ['HCC001', 'HCC002', 'HCC003'],
                    'descriptions': [
                        'HIV/AIDS',
                        'Septicemia',
                        'Opportunistic Infections'
                    ],
                    'categories': ['Infectious', 'Infectious', 'Infectious']
                },
                'DSM-5': {
                    'codes': ['300.00', '300.02', '300.29'],
                    'descriptions': [
                        'Anxiety Disorder',
                        'Generalized Anxiety',
                        'Specific Phobia'
                    ],
                    'categories': ['Anxiety', 'Anxiety', 'Anxiety']
                }
            }

            for classifier, data in sample_data.items():
                for i in range(len(data['codes'])):
                    vector = self.nlp(data['descriptions'][i]).vector
                    code = MedicalCode(
                        code=data['codes'][i],
                        description=data['descriptions'][i],
                        category=data['categories'][i],
                        classifier_type=classifier,
                        vector=json.dumps(vector.tolist())
                    )
                    db.session.add(code)
            db.session.commit()

    def get_classifier_types(self) -> List[str]:
        """Return available classifier types"""
        classifiers = db.session.query(MedicalCode.classifier_type).distinct().all()
        return sorted([c[0] for c in classifiers])

    def get_all_categories(self, classifier_type: str = None) -> List[str]:
        """Return unique categories for a specific classifier"""
        query = db.session.query(MedicalCode.category).distinct()
        if classifier_type:
            query = query.filter(MedicalCode.classifier_type == classifier_type)
        categories = query.all()
        return sorted([cat[0] for cat in categories])

    def get_data(self, classifier_type: str = None) -> pd.DataFrame:
        """Return the complete dataset for a specific classifier"""
        query = MedicalCode.query
        if classifier_type:
            query = query.filter(MedicalCode.classifier_type == classifier_type)
        codes = query.all()

        data = {
            'code': [],
            'description': [],
            'category': [],
            'classifier_type': [],
            'vector': []
        }

        for code in codes:
            data['code'].append(code.code)
            data['description'].append(code.description)
            data['category'].append(code.category)
            data['classifier_type'].append(code.classifier_type)
            data['vector'].append(np.array(json.loads(code.vector)))

        return pd.DataFrame(data)

    def get_vectors(self, classifier_type: str = None) -> np.ndarray:
        """Return processed vectors for a specific classifier"""
        df = self.get_data(classifier_type)
        return np.vstack(df['vector'].values)