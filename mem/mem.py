import os 
from mem0 import Memory
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai = OpenAI()
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")



config = {
    "version":"v1.1",
    "embedder":{
        "provider":"openai",
        "config":{
            "model":"text-embedding-3-small",
            "api_key":os.getenv("OPENAI_API_KEY")
        }
    },
    "llm":{
        "provider":"openai",
        "config":{
            "model":"gpt-4.1",
            "api_key":os.getenv("OPENAI_API_KEY")
        }
},
    "vector_store":{
        "provider":"qdrant",
        "config":{
            "host": os.getenv("QDRANT_HOST"),
            "port": os.getenv("QDRANT_PORT"),
        }
    },
    "graph_store":{
        "provider":"neo4j",
        "config":{
            "url":NEO4J_URL,
            "username":NEO4J_USERNAME,
            "password":NEO4J_PASSWORD
        }
    },
}


mem_client = Memory.from_config(config)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat(message):
    messages=[
        {"role":"user","content":message}
    ]
    memory = mem_client.search(query=message,user_id="user_1",limit=2)
    print(f"\n\nMemory: {memory}\n\n")
    memories = ""
    for mem in memory.get("results",[]):
        memories+= f"{str(mem['memory'])}: {str(mem['score'])} \n"
    print(memories)
    messages.append({"role":"system","content":f"Relevant information from memory: {memories}"})
    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )
    messages.append({"role":"assistant","content":response.choices[0].message.content})
    mem_client.add(messages,user_id="user_1")
    return response.choices[0].message.content



while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break
    response = chat(user_input)
    print(f"AI: {response}")
    