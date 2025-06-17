from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import  OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
def storing_db():
    pdf_path = Path(__file__).parent / "nodejs.pdf"
    loader = PyPDFLoader(file_path=pdf_path)

    docs= loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000 ,chunk_overlap=200)
    splitted_chunks = text_splitter.split_documents(documents=docs)

    embeddigs_func = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key="")
    vector_store  = QdrantVectorStore.from_documents(
        documents=[],
        url="http://localhost:6333",
        embedding=embeddigs_func,
        collection_name="learning_langchain"    
    )
    vector_store.add_documents(documents=splitted_chunks)
    print("ingestion done")
    
def retrival(question):
    embeddigs_func = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key="")
    retriver = QdrantVectorStore.from_existing_collection(
        url= "http://localhost:6333",
        collection_name="learning_langchain",
        embedding=embeddigs_func
    )
    search_result = retriver.similarity_search(
        query=question
    )
    print("relevent_chunks" , search_result)
    # Assuming `docs` is your list of Document objects
    data=""
    for doc in search_result:
        page = doc.metadata.get('page')  # safely get page number
        content = doc.page_content       # get the content
        data+=f"\nPage: {page}\n"
        data+=content
        data+="\n" + "-"*80 + "\n"  # separator between documents

        
    SYSTEM_PROMPT=f"""you are an helpful AI assistant who respond based on the relevant context
    Context
    {data}
    THE question will be send by the user
    
    """
    client = OpenAI()
    result =  client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":question}
    ])

    print(result.choices)
    print(result.choices[0].message.content)
    

retrival("how to use verify  json web token")