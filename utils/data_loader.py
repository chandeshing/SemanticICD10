import pandas as pd
import numpy as np
from typing import Dict, List
import spacy

class ICD10DataLoader:
    def __init__(self):
        # Sample ICD-10 data structure
        self.data = {
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
        self.df = pd.DataFrame(self.data)
        self.nlp = spacy.load('en_core_web_sm')
        self._process_descriptions()

    def _process_descriptions(self):
        """Process descriptions with spaCy and create vectors"""
        self.vectors = np.array([
            self.nlp(desc).vector 
            for desc in self.df['description']
        ])

    def get_all_categories(self) -> List[str]:
        """Return unique categories"""
        return sorted(self.df['category'].unique())

    def get_data(self) -> pd.DataFrame:
        """Return the complete dataset"""
        return self.df

    def get_vectors(self) -> np.ndarray:
        """Return processed vectors"""
        return self.vectors
