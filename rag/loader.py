import os
from git import Repo
from langchain_core.documents import Document
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
# import hashlib
GITHUB_API = "https://api.github.com/repos"
MAX_WORKERS = 8

def parse_repo_url(repo_url: str):
    parts = repo_url.rstrip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]
    return owner, repo

def fetch_file_content(item):
    try:
        content = requests.get(item["download_url"]).text
        return Document(
            page_content=content,
            metadata={"source": item["path"]}
        )
    except Exception:
        return None

def fetch_repo_files(repo_url: str):
    owner, repo = parse_repo_url(repo_url)
    documents = []
    file_items = []

    def collect_files(path=""):
        url = f"{GITHUB_API}/{owner}/{repo}/contents/{path}"
        response = requests.get(url)

        if response.status_code != 200:
            return

        for item in response.json():
            if item["type"] == "dir":
                collect_files(item["path"])
            elif item["type"] == "file" and item["name"].endswith((
                ".py", ".js", ".java", ".ts", ".md", ".css", ".html"
            )):
                file_items.append(item)

    # Step 1: collect all file metadata
    collect_files()

    # Step 2: fetch files in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_file_content, item) for item in file_items]

        for future in as_completed(futures):
            result = future.result()
            if result:
                documents.append(result)

    return documents
# def clone_repo(repo_url):
#     repo_hash = hashlib.md5(repo_url.encode()).hexdigest()
#     local_path = f"repo_{repo_hash}"

#     if not os.path.exists(local_path):
#         Repo.clone_from(repo_url, local_path)

#     return local_path


# def load_code_files(repo_path: str):
#     documents = []

#     for root, _, files in os.walk(repo_path):
#         for file in files:
#             if file.endswith((".py", ".js", ".java", ".ts", ".md", ".css", ".html")):
#                 path = os.path.join(root, file)
#                 try:
#                     with open(path, "r", encoding="utf-8") as f:
#                         documents.append(Document(
#                             page_content=f.read(),
#                             metadata={"source": path}
#                         ))
#                 except Exception:
#                     continue
#     return documents