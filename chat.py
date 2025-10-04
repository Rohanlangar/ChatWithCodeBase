import os
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

os.environ["PINECONE_API_KEY"] = "pcsk_6fjoqa_6JfqDfXQcyqfW3kozHJ6CqrDXbqpFhpFCmRyYEozP7g7uN5q2UzaLyRmtZpsjWs"
os.environ["GROQ_API_KEY"] = "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"  # Add your Groq API key

def chat_with_repo(index_name="code-base"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    # Using Groq instead of Ollama
    llm = ChatGroq(
        model="openai/gpt-oss-20b",  
        temperature=0.7
    )

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    print("💬 Ask questions about the repo (type 'exit' to quit):")
    while True:
        query = input("\n🧠 Your Question: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = qa.run(query)
        print(f"📘 Answer:\n{response}")