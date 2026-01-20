import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(override=True)

filepath=Path(__file__).parent /"resources/faq_data.csv"
groq_client= Groq()
chroma_client= chromadb.Client()
client_collection_name= "faq"
ef=embedding_functions.SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")



def ingest_faq_data(file):
    if client_collection_name not in [i.name for i in chroma_client.list_collections() ]:
        #print("Ingesting data into chromadb with embedding questions as doc and answers as metadata")
        collection= chroma_client.get_or_create_collection(
            name= client_collection_name,
            embedding_function= ef)
        df= pd.read_csv(file)
        docs= df['question'].to_list()
        metadata=  [{'answers':ans} for ans in df['answer'].to_list()]
        ids= [f"id_{i}" for i in range(len(docs))]
        collection.add(
            documents= docs,
            metadatas= metadata,
            ids= ids
        )
        print(f"FAQ data successfully ingested into chromadb")
    else:
        print(f"Collection {client_collection_name} already exists")

def query_qa_results(query):
    #print("Invoking query_qa_results which provided associated questions for query")
    collection= chroma_client.get_collection(name= client_collection_name)
    results= collection.query(
        query_texts= query,
        n_results=2
    )
    #print("Results associated with query:  ", results, "\n")
    return results

def faq_chain(query):
    results= query_qa_results(query)
    #print("Query:",query)
    context= ''.join([r.get('answers') for r in results['metadatas'][0]])
    #print("Context:",context)
    #print("Generating the answer with provided context and query")
    answer= generate_answer(query,context)
    return answer

def generate_answer(query, context):
    #print("Invoking generate_answer function")
    query= query
    context= context
    prompt= f"""
            Given the user query: {query} and the given context{context},
            answer the query using the context only. Do not go out of context,
            if dont know say you dont know 
            """
    stream= groq_client.chat.completions.create(
        messages=[{
            'role':'user',
            'content':prompt
        }],
        model=os.environ.get("GROQ_MODEL"),
        stream= True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content



if __name__== "__main__":
    ingest_faq_data(filepath)
    exit_list = ['none', 'exit', 'bye', 'quit', 'q']

    print("\n--- FAQ System Active ---")
    while True:
        query= input("Enter you query:  ")
        if query=="" or query.lower() in exit_list:
            break
        print("Query:", query)
        answer= faq_chain(query)
        print("Response:", answer)
            

            
        
