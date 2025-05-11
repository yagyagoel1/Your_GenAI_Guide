from dotenv import load_dotenv
from openai import OpenAI
import  os
load_dotenv(override=True)

# print(os.getenv("OPENAI_API_KEY"),"FDDF")
client  = OpenAI()



result =  client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"user","content":"hey there"}
    ]
    
)

print(result.choices)
print(result.choices[0].message.content)
