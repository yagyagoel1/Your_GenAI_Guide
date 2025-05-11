from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()


client = OpenAI()

text= "Eiffel tower is in apris and is a famous landmark, it is 324 meters tall"


response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
)

print("vector embeddings",response.data[0].embedding)