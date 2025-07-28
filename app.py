from clonerepo import clone_repository
from index import vectorStore
from chat import chat_with_repo

if __name__ == "__main__":
    repo_url = input("🔗 Enter GitHub repo URL: ")
    path = clone_repository(repo_url)
    vectorStore(path)
    chat_with_repo()
