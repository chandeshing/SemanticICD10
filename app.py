import streamlit as st
import pandas as pd
from utils.data_loader import ICD10DataLoader
from utils.search_engine import SemanticSearchEngine

# Page configuration
st.set_page_config(
    page_title="ICD-10 Semantic Search",
    page_icon="🏥",
    layout="wide"
)

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_resource
def initialize_search_engine():
    data_loader = ICD10DataLoader()
    return SemanticSearchEngine(data_loader), data_loader

# Initialize search engine and data loader
search_engine, data_loader = initialize_search_engine()

# Header
st.title("🏥 ICD-10 Semantic Search")
st.markdown("""
    Search for ICD-10 medical codes using natural language. 
    Enter your query below and get relevant matches based on semantic similarity.
""")

# Search interface
with st.container():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Enter your search query",
            placeholder="Example: breast cancer, cholera, viral infection",
            key="search_input"
        )
    
    with col2:
        categories = ["All"] + data_loader.get_all_categories()
        selected_category = st.selectbox(
            "Filter by category",
            categories,
            key="category_filter"
        )

# Search button
search_button = st.button("Search", key="search_button", type="primary")

# Process search
if search_button and search_query:
    with st.spinner("Searching..."):
        results = search_engine.search(
            search_query,
            category=selected_category if selected_category != "All" else None
        )
        
        if results:
            st.markdown("### Search Results")
            
            for result in results:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"""
                            <div class="result-card">
                                <span class="code-badge">{result['code']}</span>
                                <h4>{result['description']}</h4>
                                <p>Category: {result['category']}</p>
                                <span class="score-badge">Relevance: {result['score']:.2f}</span>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("No results found. Please try a different search query.")

# Error handling
elif search_button and not search_query:
    st.error("Please enter a search query.")

# Help section
with st.expander("How to use this search"):
    st.markdown("""
        - Enter your search terms in natural language
        - Optionally filter by category
        - Results are ranked by relevance
        - Click on codes for detailed information
        - Use medical terms for better results
    """)

# Footer
st.markdown("---")
st.markdown(
    "Built with Streamlit and spaCy | ICD-10 Semantic Search Tool",
    help="Using semantic search technology for medical code lookup"
)
