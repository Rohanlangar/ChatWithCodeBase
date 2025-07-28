import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import pinecone

os.environ["PINECONE_API_KEY"] = "pcsk_6fjoqa_6JfqDfXQcyqfW3kozHJ6CqrDXbqpFhpFCmRyYEozP7g7uN5q2UzaLyRmtZpsjWs"


def vectorStore(indexname='code-base', namespace='default',code_path='cloned_repo'):
    docs = []
    for root, _, files in os.walk(code_path):
        for file in files:
            print(f"Found file: {file}")
            if file.endswith((".py", ".js", ".ts", ".java", ".html", ".md")):
                print(f"✅ Accepted file: {file}")
                loader = TextLoader(os.path.join(root, file), encoding="utf-8")
                docs.extend(loader.load())
                print(f"Total documents loaded: {len(docs)}")


    splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    print(f"Loaded {len(docs)} documents from {code_path}")
    chunks=splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectors = PineconeVectorStore.from_documents(
        chunks,embedding=embeddings,index_name='code-base'
    )

    print('code indexed to pinecone')