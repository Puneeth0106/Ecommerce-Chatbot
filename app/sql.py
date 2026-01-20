import sqlite3
import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

# print(os.getenv("GROQ_MODEL"))


client= Groq()

sql_prompt= """You are an expert in understanding the database schema and generating SQL queries for a natural language question asked
pertaining to the data you have. The schema is provided in the schema tags. 
<schema> 
table: product 

fields: 
product_link - string (hyperlink to product)	
title - string (name of the product)	
brand - string (brand of the product)	
price - integer (price of the product in Indian Rupees)	
discount - float (discount on the product. 10 percent discount is represented as 0.1, 20 percent as 0.2, and such.)	
avg_rating - float (average rating of the product. Range 0-5, 5 is the highest.)	
total_ratings - integer (total number of ratings for the product)

</schema>
Make sure whenever you try to search for the brand name, the name can be in any case. 
So, make sure to use %LIKE% to find the brand in condition. Never use "ILIKE". 
Create a single SQL query for the question provided. 
The query should have all the fields in SELECT clause (i.e. SELECT *)

Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL></SQL> tags."""


comprehension_prompt = """You are an expert in understanding the context of the question and replying based on the data pertaining to the question provided. You will be provided with Question: and Data:. The data will be in the form of an array or a dataframe or dict. Reply based on only the data provided as Data for answering the question asked as Question. Do not write anything like 'Based on the data' or any other technical words. Just a plain simple natural language response.
The Data would always be in context to the question asked. For example is the question is “What is the average rating?” and data is “4.3”, then answer should be “The average rating for the product is 4.3”. So make sure the response is curated with the question and data. Make sure to note the column names to have some context, if needed, for your response.
There can also be cases where you are given an entire dataframe in the Data: field. Always remember that the data field contains the answer of the question asked. All you need to do is to always reply in the following format when asked about a product: 
Produt title, price in indian rupees, discount, and rating, and then product link. Take care that all the products are listed in list format, one line after the other. Not as a paragraph.
For example:
1. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
2. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
3. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>

"""


def generate_sql_query(prompt, query):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": query,
        }
    ],
    model=os.getenv("GROQ_MODEL"),
    temperature=0.2,
    max_tokens=1024
    )
    return chat_completion.choices[0].message.content.split("<SQL>")[1].split("</SQL>")[0].strip()


def sql_chain(question):
    try:
        sql_query = generate_sql_query(sql_prompt, question)
        df = fetch_data(sql_query)
        
        if df is None or df.empty:
            yield "I couldn't find any products matching your request."
            
        # Truncate to save tokens
        context = df.head().to_dict(orient='records')
        yield from comprehension_chain(question, context)
    except Exception as e:
        yield f"An error occurred: {str(e)}"


def comprehension_chain(question, data):
    # Converting dict to a cleaner string format saves tokens compared to raw JSON
    data_str = "\n".join([str(row) for row in data])
    
    stream = client.chat.completions.create(
        messages=[
            {"role": "system", "content": comprehension_prompt},
            {"role": "user", "content": f"Question: {question}\nData: {data_str}"}
        ],
        model=os.getenv("GROQ_MODEL"),
        temperature=0.2,
        # max_tokens can be higher if the response is a long list
        max_tokens=2048,
        stream=True 
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content



DB_PATH= os.path.join(os.path.dirname(__file__), 'resources', 'ecommerce_data.db')


def fetch_data(query):
    if query.strip().upper().startswith("SELECT"):
        with sqlite3.connect(DB_PATH) as conn:
            df= pd.read_sql_query(query, conn)
            return df

    


if __name__ == "__main__":
    query= "Do you have nike shoes with 50 percent discount?"


    print("Generating Results for query:", query)
    result= sql_chain(query)
    print(result)

    # sql_query = generate_sql_query(sql_prompt, query)
    # print(sql_query)
    # df = fetch_data(sql_query)
    # print(df.head())