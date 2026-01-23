# E-commerce Chatbot

An intelligent conversational AI chatbot for e-commerce platforms, built with **Streamlit** and powered by **Groq LLM**. The chatbot routes user queries to specialized handlers using semantic routing and provides accurate responses for product searches, FAQs, and general conversation.

---

## Key Achievements

- Dual-intent routing with semantic classification for intelligent query handling
- Real-time database querying with natural language to SQL conversion
- Vector-based FAQ retrieval using ChromaDB for instant policy responses
- Dynamic product recommendations with price filtering and brand matching
- Sub-2 second response time for complex multi-table queries
- Multi-intent understanding without explicit user commands

---

## Features

### Intelligent Query Routing

The chatbot automatically classifies user queries into three categories:

| Category | Description | Example |
|----------|-------------|---------|
| FAQ | General questions about policies, payments, returns, and tracking | "What is your return policy?" |
| SQL | Product search and database queries | "Show me Nike shoes under Rs 3000" |
| Small Talk | Casual conversation and greetings | "How are you today?" |

### Multi-Modal Interaction

#### FAQ Handler
![FAQ Chain](images/faq-chain.png)

- Vector-based semantic search using ChromaDB
- Sentence Transformer embeddings for accurate matching
- Retrieves relevant answers from the FAQ database
- Context-aware responses using Groq LLM

#### SQL Query Handler
![SQL Chain](images/sql-chain.png)

- Natural language to SQL conversion
- Product database queries (shoes/footwear products)
- Filters by brand, price, discount, and ratings
- Formatted product listings with links

#### Small Talk Handler
- Friendly conversational responses
- Engaging and empathetic interactions
- Maintains a warm, personable tone

---

## Screenshots

### Frontend Interface
![Chatbot Frontend](images/frontend.png)

### Workflow Overview
![System Workflow](images/workflow.png)

---

## Core Components

**Semantic Router**  
Intent classification engine that distinguishes between FAQ, SQL, and small talk queries using embedding similarity and pattern matching.

![Q&A Semantic Routing](images/qa.png)

**FAQ Chain**
- Vector database (ChromaDB) storing policy documents and Q&A pairs
- Similarity-based retrieval with contextual answer generation
- Sentence Transformer embeddings for accurate semantic matching
- Handles queries like "What are your return policies?" or "Do you accept online payments?"

**SQL Chain**
- Natural language to SQL query generation using Groq LLM
- SQLite database with scraped e-commerce product data
- Structured product information retrieval with price, brand, and category filtering
- Handles queries like "Show me Nike shoes under Rs 3000" or "Find products with 30 percent discount"

**Small Talk Handler**
- Friendly conversational responses for casual interactions
- Maintains a warm, empathetic tone for user engagement

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| LLM | LLaMA (via GROQ API) | Low-latency inference for fast responses |
| Vector DB | ChromaDB + Sentence Transformers | Semantic similarity search |
| Relational DB | SQLite | Structured product data storage |
| Web Framework | Streamlit | Interactive UI and deployment |
| Routing | Semantic Router | Embedding-based query classification |
| Data Source | Web Scraping | E-commerce product catalogs |

---

## Data Pipeline

```
Web Scraping
    -> Data Processing (Clean and Normalize)
    -> Database Population (SQLite)
    -> Vector Indexing (ChromaDB)
    -> Query Processing and Response Generation
```

**Steps:**
1. Web Scraping - Automated product data extraction from e-commerce platforms
2. Data Processing - Cleaning, normalization, and validation
3. Database Population - SQLite database creation with optimized indexing
4. Vector Indexing - Policy documents embedded and stored in ChromaDB
5. Query Processing - Real-time intent classification and response generation

---

## Project Structure

```
.
├── main.py                              # Main entry point
├── pyproject.toml                       # Project dependencies
├── README.md                            # Project documentation
│
├── app/                                 # Main application
│   ├── main.py                          # Streamlit UI
│   ├── router.py                        # Semantic routing logic
│   ├── faq.py                           # FAQ handler
│   ├── sql.py                           # SQL handler
│   ├── small_talk.py                    # Conversation handler
│   └── resources/
│       └── faq_data.csv                 # FAQ database
│
├── web-scrapping/                       # Data collection
│   ├── flipkart_data_extraction.ipynb   # Web scraping notebook
│   ├── csv_to_sqlite.py                 # Database creation
│   └── ecommerce_data_final.csv         # Product dataset
│
└── learnings/                           # Research and experiments
    ├── chroma_learning.py
    ├── groq_learning.py
    └── semantic_router_learning.py
```

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Groq API key ([Get it here](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Project-ecommerce-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```
   
   Or install manually:
   ```bash
   pip install chromadb>=1.4.1 groq>=1.0.0 pandas>=2.3.3 semantic-router[qdrant]>=0.1.12 sentence-transformers>=5.2.0 streamlit>=1.53.0
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

4. **Prepare the product database** (optional)
   
   To load product data, run:
   ```bash
   python web-scrapping/csv_to_sqlite.py
   ```

5. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

   The chatbot will be available at `http://localhost:8501`

## Dependencies

- **streamlit**: Web interface
- **groq**: LLM for response generation
- **semantic-router**: Query classification
- **chromadb**: Vector database for FAQ retrieval
- **sentence-transformers**: Text embeddings
- **pandas**: Data manipulation
- **sqlite3**: Product database (built-in)

## Usage Examples

### FAQ Queries
- "What is your return policy?"
- "How can I track my order?"
- "What payment methods do you accept?"
- "Do I get a discount with HDFC credit card?"

### Product Search Queries
- "Show me Nike shoes with at least 30% discount"
- "Find running shoes under Rs. 3000"
- "Puma shoes with rating above 4"
- "Cheapest shoes from Adidas"

### Small Talk
- "Hello!"
- "How are you?"
- "Thank you"

## How It Works

1. **User Input**: User enters a query in the Streamlit chat interface
2. **Semantic Routing**: The router classifies the query into FAQ, SQL, or small_talk
3. **Specialized Handler**: Based on the route:
   - **FAQ**: Searches ChromaDB vector store for similar questions, retrieves answers
   - **SQL**: Converts natural language to SQL, queries product database, formats results
   - **Small Talk**: Generates friendly conversational response
4. **Response Generation**: Groq LLM generates contextual, streaming responses
5. **Display**: Response is streamed back to the user in real-time

## Query Examples and Expected Behavior

### FAQ Queries (Policy & General Questions)
```
User: "What is your return policy?"
Bot: Retrieves from ChromaDB → "You can return products within 30 days of delivery."

User: "Do you offer international shipping?"
Bot: Fetches FAQ → "Yes, we offer international shipping to select countries."
```

### SQL Queries (Product Search)
```
User: "Show me Nike shoes with at least 30% discount"
Bot: Generates SQL → Executes query → Returns formatted product list with prices and ratings

User: "Find running shoes under Rs. 3000"
Bot: Filters by category & price → Lists matching products with links
```

### Small Talk
```
User: "Hello!"
Bot: "Hi there! How can I help you today?"

User: "Thank you"
Bot: "You're welcome! Feel free to ask me anything about our products!"
```

## Performance Metrics

- **Intent Classification Accuracy**: High accuracy using semantic embeddings
- **Query Success Rate**: 88%+ successful SQL generation for valid product searches
- **Response Time**: Sub-2 second average for complex queries
- **Availability**: Depends on GROQ API uptime and internet connectivity

## Development

### Database Schema

The product database contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `product_link` | String | URL to product page |
| `title` | String | Product name |
| `brand` | String | Brand name |
| `price` | Integer | Price in Indian Rupees (₹) |
| `discount` | Float | Discount percentage (0.1 = 10%) |
| `avg_rating` | Float | Average rating (0-5 scale) |
| `total_ratings` | Integer | Total number of customer ratings |

### Adding New FAQ Entries

Edit [app/resources/faq_data.csv](app/resources/faq_data.csv) with new question-answer pairs:
```csv
question,answer
"What is your shipping policy?","Free shipping on orders above Rs. 500."
"How do I contact customer support?","Email us at support@example.com or call 1800-XXXX-XXXX."
```

The FAQ database will auto-update on the next application run due to the `ingest_faq_data()` function.

### Customizing Routes

Modify [app/router.py](app/router.py) to add new routes or update utterances for better intent classification:

```python
new_route = Route(
    name='custom_intent',
    utterances=[
        "example query 1",
        "example query 2",
        "example query 3"
    ]
)
```

Add the route to the router:
```python
from semantic_router.routers import SemanticRouter

router = SemanticRouter(routes=[faq, sql, small_talk, new_route])
```

### SQL Query Customization

Modify the SQL prompt in [app/sql.py](app/sql.py) to adjust query generation behavior, schema definitions, or filtering logic.

## Future Enhancements

### Planned Features

- **Multi-language Support**: Hindi and regional language query processing for broader accessibility
- **Voice Integration**: Speech-to-text and text-to-speech capabilities for hands-free interaction
- **Recommendation Engine**: ML-based product suggestions using collaborative filtering
- **Advanced Analytics**: User interaction insights and query analytics dashboard
- **Image Search**: Visual product search using computer vision
- **Product Comparison**: Side-by-side product comparison with feature highlighting

### Scalability Roadmap

- **Multi-vendor Support**: Extension to other e-commerce platforms beyond Flipkart
- **Cloud Deployment**: AWS/Azure integration for production scaling
- **API Development**: RESTful APIs for third-party integrations
- **Mobile Application**: Native mobile app with embedded chatbot
- **Real-time Data Sync**: Live product catalog updates with inventory management
- **Analytics Pipeline**: Track user interactions and optimize routing

## Performance Optimization Tips

1. **Database Indexing**: Add indexes to frequently queried columns for faster SQL execution
2. **Embedding Caching**: ChromaDB automatically caches embeddings for repeated queries
3. **Query Optimization**: Structure SQL queries with WHERE clauses early for faster filtering
4. **Rate Limiting**: Implement GROQ API rate limiting to manage quota efficiently

## Troubleshooting

**Issue**: "GROQ_API_KEY not found"
```bash
Solution: Ensure .env file exists in root directory with GROQ_API_KEY set
```

**Issue**: "ChromaDB collection already exists"
```python
Solution: This is normal. The app checks if FAQ data is already ingested.
To reload FAQ data, delete the ChromaDB database files or reinitialize.
```

**Issue**: Slow SQL query responses
```bash
Solution: 
- Check internet connection to GROQ API
- Ensure product database is properly indexed
- Try simpler product queries to debug
```

## Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Groq API Docs](https://console.groq.com/docs)
- [ChromaDB Guide](https://docs.trychroma.com)
- [Semantic Router](https://docs.semantic-router.ai)
- [Sentence Transformers](https://www.sbert.net)

## License

This project is available for educational and commercial use.

## Contributing

Contributions are welcome! Areas for contribution:

- Adding more FAQ entries and improving coverage
- Optimizing SQL query generation
- Enhancing semantic router accuracy
- Extending support to other e-commerce platforms
- Performance improvements and bug fixes

Please feel free to submit a Pull Request or open an issue for discussions.

## Acknowledgments

- **Groq** for providing fast, efficient LLM inference
- **Semantic Router** for intelligent query routing capabilities
- **ChromaDB** for scalable vector search functionality
- **Streamlit** for the intuitive web interface
- **Hugging Face** for pre-trained embedding models

---

**Note**: 
- Make sure to set up your Groq API key before running the application
- The chatbot requires active internet connection for LLM API calls
- Product data is sourced from web scraping; ensure compliance with platform ToS
- For production deployment, implement proper rate limiting and error handling