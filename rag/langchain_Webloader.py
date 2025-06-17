from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://firecrawl.com/")
docs = loader.load()

print(docs[0])