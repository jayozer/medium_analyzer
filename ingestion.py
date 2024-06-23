import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


load_dotenv()


if __name__ == "__main__":
    print("Ingesting...")
    loader = TextLoader(
        "/Users/acrobat/Documents/GitHub/medium_analyzer/mediumblog1.txt"
    )
    document = loader.load()

    print("splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", openai_api_key=os.environ.get("OPENAI_API_KEY")
    )
    print("ingesting...")
    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=os.environ["INDEX_NAME"]
    )
