from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import OpenAIEncoder, HuggingFaceEncoder
# from semantic_router.index import QdrantIndex
from dotenv import load_dotenv


load_dotenv()

#Define Routes
faq = Route(
    name='faq',
    utterances=[
        # Return policy variations
        "What is the defect policy?",
        "How do I return a defective product?",
        "Can I return a damaged item?",
        "What is your policy on defective products?",
        "What is your return policy?",
        "How do I return a product?",
        "Can I return an item if I'm not satisfied?",
        "What is the timeframe for returns?",
        "How long do I have to return a product?",
        "Do you accept product returns?",
        "What is the process to return an item?",
        "Can I return faulty or damaged products?",
        "How do I return defective products?",
        "Are refunds available for returned items?",
        "Do I get a refund for defective products?",
        "How long does it take to process a refund?",
        "When will I get my money back after a return?",
        "What is your refund policy?",
        "Do you provide full refunds or store credit?",

        # Payment-related questions
        "What payment methods do you accept?",
        "Can I pay using a credit card?",
        "Do you accept debit cards or net banking?",
        "Is cash on delivery available?",
        "Can I use HDFC credit card for a discount?",
        "Do you offer any discounts for HDFC cardholders?",
        "Are there any ongoing discounts or offers?",
        "How can I apply a promo code or discount?",

        # Order tracking
        "How can I track my order?",
        "Where is my package?",
        "Can I check the status of my delivery?",
        "When will my order arrive?",
        "Is there a way to see shipment tracking details?",

        # General product questions
        "Do you sell genuine products?",
        "Are your products covered by warranty?",
        "What is the warranty policy?",
        "Can I get help with product installation?",
        "How can I contact customer support?",
    ]
)

sql = Route(
    name='sql',
    utterances=[
        # Product queries with discounts and brands
        f"I want to buy NIKE shoes with a 50% discount.",
        "Are there any Puma shoes on sale?",
        "Shoes with at least 20 percent off.",
        "Shoes with Average rating above 4.",
        "Shoes with more than 1000 ratings.",
        "Shoes with price above 5000 rupees.",
        "Shoes with price below 3000 rupees.",
        "Find me Nike shoes with a discount of 30 percent or more.",
        "Show me Adidas shoes with at least 15% discount.",
        "List Puma shoes that are on sale with a discount of 25% or higher.",
        "Shoes with a discount between 10% and 40%.",
        "Find shoes from Nike or Adidas with a discount of 20% or more.",
        "Shoes with more than 500 ratings and a discount of at least 15%.",
        "Cheapest shoes from Sparx with a discount of 10% or more.",
        "Find CAMPUS shoes with a discount of at least 20% and price below 4000 rupees.",
        "Find Fabbmate shoes with a discount of at least 15% and average rating above 4.",
        "Find shoes HRX by Hrithik Roshan ",
        "Do you have Adidas sneakers available?",
        "Show me running shoes under Rs. 3000.",
        "Are there any formal shoes in size 9?",
        "I need casual shoes in size 8.",
        "Find me sports shoes under 2500 rupees.",
        "What is the price of Puma running shoes?",
        "List all Nike shoes available in size 10.",
        "Show me all shoes under Rs. 2000.",
        "Are there any shoes with a discount right now?",
        "I want shoes that cost less than 1500.",
        "Find formal black shoes in size 9.",
        "Do you have red sneakers in size 7?",
        "Are there any white running shoes available?",
        "What is the cheapest running shoe you have?",
        "Show me Nike shoes that are on discount.",
        "Do you stock Adidas shoes with cashback offers?",
        "Find me sneakers for under 3000 rupees.",
        "I want to buy shoes with free shipping.",
    ]
)

small_talk = Route(
    name='small_talk',
    utterances=[
        "Hello",
        "Hi",
        "How are you?",
        "What's up?",
        "Tell me a joke",
        "What's the weather like?",
        "Goodbye",
        "See you later",
        "Thank you",
        "Thanks",
        "How's it going?",
        "What do you do for fun?",
        "Do you have any hobbies?",
        "What is your favorite movie?",
        "Tell me a fun fact",   
        "say something funny",
        "What are your capabilities?",
        "Bye",
        "exit",
        "quit",
        "Hello there!",
        "hello bot",
        "Hi bot",
        "Hey!",
        "Hey bot",
        "Good morning",
        "Good afternoon",
        "Good evening",
        "See you soon",
        "Thanks a lot",
        "How are you?",
        "What is your name?",
        "Are you a robot?",
        "What are you?",
        "What do you do?",
        "Can you help me?",
        "Do you have feelings?",
        "What is the meaning of life?",
        "Tell me something interesting",
        "Do you like music?",
        "What is your favorite color?", 
    ]
)




# Define Encoder
encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

# Define Semantic Router
router = SemanticRouter(routes=[faq, sql, small_talk], encoder=encoder, auto_sync="local" )


if __name__ == "__main__":
    print("Testing Router...")
    # Now the index is ready for queries
    res1 = router("What is the policy on defected products?")
    print(f"Query 1 matched: {res1.name}")

    res2 = router("what is the price of formal shoes with size 10")
    print(f"Query 2 matched: {res2.name}")

    res3 = router("How can I get a refund for my order?")
    print(f"Query 3 matched: {res3.name}")

    res4 = router("Do you have Adidas shoes with 30% discount?")
    print(f"Query 4 matched: {res4.name}")

    res5 = router("What payment methods are accepted?")
    print(f"Query 5 matched: {res5.name}")

    res6 = router("Are there any shoes under Rs. 2000?")
    print(f"Query 6 matched: {res6.name}")

    res7= router("How long does it take to process a refund?")
    print(f"Query 7 matched: {res7.name}")

    res8= router("Hello, how are you?")
    print(f"Query 8 matched: {res8.name}")

    res9= router("Tell me a joke?")
    print(f"Query 9 matched: {res9.name}")

    res10= router("What is your favorite color?")
    print(f"Query 10 matched: {res10.name}")
    
    res11= router("Hi")
    print(f"Query 11 matched: {res11.name}")

    res12= router("help me with")
    print(f"Query 12 matched: {res12.name}")
