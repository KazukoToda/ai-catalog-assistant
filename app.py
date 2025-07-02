import streamlit as st
import pandas as pd
import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class CatalogAssistant:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            st.error("🔑 OpenAI API key not found!")
            st.markdown("""
            **To use the AI features, please:**
            1. Copy `.env.example` to `.env`
            2. Add your OpenAI API key to the `.env` file
            3. Restart the application
            
            **For now, you can still browse the catalog below.**
            """)
            st.info("💡 You can get an OpenAI API key from: https://platform.openai.com/api-keys")
            self.openai_available = False
            self.client = None
        else:
            # Initialize OpenAI client
            try:
                self.client = openai.OpenAI(api_key=self.openai_api_key)
                self.openai_available = True
            except Exception as e:
                st.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
                self.openai_available = False
                self.client = None
        
        # Load product catalog
        self.catalog = self.load_catalog()
    
    def load_catalog(self):
        """Load the product catalog from CSV file"""
        try:
            catalog = pd.read_csv("catalog.csv")
            return catalog
        except FileNotFoundError:
            st.error("Catalog file not found. Please ensure catalog.csv exists in the project directory.")
            st.stop()
    
    def search_products(self, user_query, max_results=5):
        """
        Use OpenAI to analyze the user query and recommend products
        """
        if not self.openai_available:
            st.error("❌ OpenAI is not available. Please configure your API key.")
            return []
        
        # Create a prompt that includes the catalog and user query
        catalog_text = self.catalog.to_string(index=False)
        
        prompt = f"""
You are a helpful product recommendation assistant. A user is looking for products and has made the following request:

User Query: "{user_query}"

Here is the available product catalog:
{catalog_text}

Please analyze the user's request and recommend 2-5 products that best match their needs. 
Consider factors like:
- Price range mentioned or implied
- Category/type of product
- Use case or purpose
- Any specific features mentioned

Return your response as a JSON object with the following structure:
{{
    "recommendations": [
        {{
            "product_id": "id",
            "name": "product name",
            "price": price,
            "description": "product description",
            "category": "category",
            "explanation": "Why this product matches the user's needs"
        }}
    ]
}}

Focus on products that truly match the user's criteria. If they mention a budget, respect it. Provide clear explanations for why each product is recommended.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful product recommendation assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            # Parse the JSON response
            response_text = response.choices[0].message.content
            
            # Try to extract JSON from the response
            try:
                # Find JSON content in the response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                json_str = response_text[start_idx:end_idx]
                
                result = json.loads(json_str)
                return result.get("recommendations", [])
            except (json.JSONDecodeError, ValueError):
                # If JSON parsing fails, return a fallback response
                st.error("❌ Failed to parse AI response. Please try a different query.")
                st.info("💡 This might be due to rate limits or API issues.")
                return []
                
        except Exception as e:
            st.error(f"❌ Error calling OpenAI API: {str(e)}")
            st.info("💡 Please check your API key and internet connection.")
            return []
    
    def display_recommendations(self, recommendations):
        """Display the recommended products in the Streamlit interface"""
        if not recommendations:
            st.warning("No products found matching your criteria. Please try a different search.")
            return
        
        st.success(f"Found {len(recommendations)} product(s) matching your request:")
        
        for i, product in enumerate(recommendations, 1):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {i}. {product.get('name', 'Unknown Product')}")
                    st.markdown(f"**Category:** {product.get('category', 'N/A')}")
                    st.markdown(f"**Description:** {product.get('description', 'N/A')}")
                    
                    # Show explanation
                    if product.get('explanation'):
                        st.markdown(f"**Why this matches:** {product['explanation']}")
                
                with col2:
                    st.markdown(f"### ${product.get('price', 'N/A')}")
                
                st.markdown("---")

def main():
    st.set_page_config(
        page_title="AI Catalog Assistant",
        page_icon="🛍️",
        layout="wide"
    )
    
    st.title("🛍️ AI Catalog Assistant")
    st.markdown("Find products by describing what you need in natural language!")
    
    # Initialize the assistant
    assistant = CatalogAssistant()
    
    # Display catalog info
    st.sidebar.markdown("### 📋 Catalog Info")
    st.sidebar.markdown(f"Total products: {len(assistant.catalog)}")
    categories = assistant.catalog['category'].unique()
    st.sidebar.markdown(f"Categories: {', '.join(categories)}")
    
    # Sample queries
    st.sidebar.markdown("### 💡 Sample Queries")
    sample_queries = [
        "I want a baby gift under $50",
        "compact cooking gear for camping",
        "affordable baby toys for teething",
        "lightweight outdoor equipment under $100",
        "baby sleep products"
    ]
    
    for query in sample_queries:
        if st.sidebar.button(f"'{query}'", key=f"sample_{hash(query)}"):
            st.session_state.user_query = query
    
    # Main search interface
    user_query = st.text_input(
        "What are you looking for?",
        placeholder="e.g., 'I need a baby gift under $50' or 'compact cooking gear for camping'",
        value=st.session_state.get('user_query', '')
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        search_button = st.button("🔍 Search", type="primary")
    
    if search_button and user_query:
        if not assistant.openai_available:
            st.warning("⚠️ OpenAI is not configured. Please add your API key to use AI search features.")
        else:
            with st.spinner("🤖 AI is analyzing your request..."):
                recommendations = assistant.search_products(user_query)
                assistant.display_recommendations(recommendations)
    
    elif search_button and not user_query:
        st.warning("Please enter a search query.")
    
    # Show catalog preview
    with st.expander("📋 View Full Catalog"):
        st.dataframe(assistant.catalog, use_container_width=True)

if __name__ == "__main__":
    main()