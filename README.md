# AI Catalog Assistant 🛍️

An AI-powered product recommendation assistant that helps users search a product catalog using natural language queries.

## Features

- **Natural Language Search**: Type queries like "I want a baby gift under $50" or "compact cooking gear for camping"
- **AI-Powered Recommendations**: Uses OpenAI GPT to understand user intent and provide relevant product suggestions
- **Smart Explanations**: Each recommendation includes an explanation of why the product matches your needs
- **Web Interface**: Simple and intuitive Streamlit-based interface
- **Product Catalog**: Sample catalog with baby gifts and outdoor gear

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/KazukoToda/ai-catalog-assistant.git
cd ai-catalog-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Run the application:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Enter a natural language query** in the search box, such as:
   - "I want a baby gift under $50"
   - "compact cooking gear for camping"
   - "affordable baby toys for teething"
   - "lightweight outdoor equipment under $100"

2. **Click Search** to get AI-powered product recommendations

3. **Review recommendations** with explanations of why each product matches your needs

## Sample Catalog

The application includes a sample catalog with 20 products across two categories:
- **Baby gifts**: Toys, feeding sets, monitors, blankets, and more
- **Outdoor gear**: Camping equipment, cooking gear, hiking accessories

## Tech Stack

- **Python**: Core programming language
- **Streamlit**: Web interface framework
- **OpenAI GPT**: Natural language processing and product matching
- **Pandas**: Data handling and CSV processing
- **python-dotenv**: Environment variable management

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Azure OpenAI settings (if using Azure instead)
# AZURE_OPENAI_ENDPOINT=your_azure_endpoint
# AZURE_OPENAI_API_KEY=your_azure_api_key
# AZURE_OPENAI_API_VERSION=2023-12-01-preview
```

### Customizing the Catalog

You can customize the product catalog by editing `catalog.csv`. The file should have the following columns:
- `id`: Unique product identifier
- `name`: Product name
- `description`: Product description
- `category`: Product category
- `price`: Product price (numeric)

## Development

### Project Structure

```
ai-catalog-assistant/
├── app.py              # Main Streamlit application
├── catalog.csv         # Product catalog data
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variable template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

### Key Components

- **CatalogAssistant**: Main class handling AI interactions and product search
- **load_catalog()**: Loads and validates the CSV product catalog
- **search_products()**: Uses OpenAI to analyze queries and recommend products
- **display_recommendations()**: Renders product recommendations in the UI

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## License

This project is open source and available under the MIT License.
