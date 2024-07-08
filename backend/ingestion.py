import os
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from backend.consts import INDEX_NAME
from dotenv import load_dotenv

load_dotenv()
pc = Pinecone(
    api_key=os.environ["PINECONE_API_KEY"]
)

def ingest_docs(urls) -> None:

     # load data
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    
    # split data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000,
        chunk_overlap=100,
    )
    docs = text_splitter.split_documents(data)
 
    # create embeddings and save it to Pinecone index
    embeddings = OpenAIEmbeddings()
    PineconeVectorStore.from_documents(docs, embeddings, index_name=INDEX_NAME)
  
    print("****** Added to Pinecone vectorstore vectors")


if __name__ == "__main__":
    ingest_docs(["https://www.geeksforgeeks.org/window-sliding-technique/"])
