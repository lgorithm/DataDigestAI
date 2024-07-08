import os
from typing import Any, List, Dict

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from backend.consts import INDEX_NAME

pc = Pinecone(
    api_key=os.environ["PINECONE_API_KEY"]
)


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []) -> Any:
    embeddings = OpenAIEmbeddings()
    vectorStore = PineconeVectorStore(
        index_name=INDEX_NAME, embedding=embeddings
    )
    chat = ChatOpenAI(verbose=True, temperature=0)

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=vectorStore.as_retriever(), return_source_documents=False
    )

    return qa({"question": query, "chat_history": chat_history})


if __name__ == "__main__":
    print(run_llm(query="What is Time complexity of sliding window protocol?"))
