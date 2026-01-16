import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions



filepath=Path(__file__).parent /"resources/faq_data.csv"

chroma_client= chromadb.Client()
client_collection_name= "faq"
ef=embedding_functions.SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")



def ingest_faq_data(file):
    if client_collection_name not in [i.name for i in chroma_client.list_collections() ]:
        print("Ingesting data into chromadb with embedding questions as doc and answers as metadata")
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


if __name__== "__main__":
    ingest_faq_data(filepath)
    