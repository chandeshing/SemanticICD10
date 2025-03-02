import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from typing import List, Dict, Tuple
import pandas as pd

class SemanticSearchEngine:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.nlp = spacy.load('en_core_web_sm')

    def search(self, query: str, category: str = None, top_k: int = 5) -> List[Dict]:
        """
        Perform semantic search on ICD-10 codes
        
        Args:
            query: Search query string
            category: Optional category filter
            top_k: Number of results to return
        
        Returns:
            List of dictionaries containing search results
        """
        try:
            # Process query
            query_vector = self.nlp(query).vector
            
            # Get data and vectors
            df = self.data_loader.get_data()
            vectors = self.data_loader.get_vectors()
            
            # Calculate similarities
            similarities = cosine_similarity([query_vector], vectors)[0]
            
            # Create results DataFrame
            results_df = df.copy()
            results_df['similarity'] = similarities
            
            # Apply category filter if specified
            if category and category != "All":
                results_df = results_df[results_df['category'] == category]
            
            # Sort by similarity and get top results
            results_df = results_df.sort_values('similarity', ascending=False).head(top_k)
            
            # Convert to list of dictionaries
            results = []
            for _, row in results_df.iterrows():
                results.append({
                    'code': row['code'],
                    'description': row['description'],
                    'category': row['category'],
                    'score': float(row['similarity'])
                })
            
            return results
        
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
