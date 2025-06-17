from fastapi import FastAPI
from ollama import Client
from fastapi import Body


app = FastAPI()
client =  Client(
    host='http://localhost:11434'
)
client.pull("gemma3:1b")
@app.post("/chat")
def chat(content:str=Body(...,description="Chat Message")):
    response = client.chat(model="gemma3:1b",messages=[
        {"role":"system","content":"""you are a really cool and creative AI based summerizer that summerize the news  along with that you ensure that the tone of yours changes according to the news.
         Rules
         - Only give out the news
         - dont change the meaning or the core of the news
         - keep the news clear and easy to understand
         - Use easy grammer words
         - keep it as concise as possible
         - Never give anything extra other than the format given below
         - Use the format given below

         Headline
         summary 


         Example Output:
         Breaking I love working at home
         my home is pretty nice and cool i love my chair there
         my table is big and tidy."""},
        {"role":"user","content":content}
    ])
    return response["message"]["content"]