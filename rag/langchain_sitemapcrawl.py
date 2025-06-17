from langchain_community.document_loaders.sitemap import SitemapLoader

sitemap_loader = SitemapLoader(web_path="https://www.dardoc.com/sitemap.xml")

docs = sitemap_loader.load()
print(len(docs))