from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

#Define Routes
faq= Route(
    name='faq',
    utterances=[
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
    ]
)

sql= Route(
    name= 'sql',
    utterances=[
        f"I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
    ]
)

routes= [faq,sql]

#Define Encoder
encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2")

#Define routing layer
rl= SemanticRouter(encoder=encoder,routes=routes,auto_sync='local')

if __name__ == "__main__":
    # Force the router to process the routes and prepare the vector index
    # This is the missing piece that fixes "Index is not ready"
    
    print("Testing Router...")
    
    # Now the index is ready for queries
    res1 = rl("can i pay by cash")
    print(f"Query 1 matched: {res1.name}")
    
    res2 = rl("what is the price of formal shoes with size 10")
    print(f"Query 2 matched: {res2.name}")