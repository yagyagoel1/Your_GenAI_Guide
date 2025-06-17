from dotenv import load_dotenv
from openai import OpenAI
import json 
import  os
load_dotenv(override=True)

# print(os.getenv("OPENAI_API_KEY"),"FDDF")
client  = OpenAI()


system_prompt="""
You are an AI assistant who is expert in breaking down the complex problems and then resolving it 

For the given user input, analyse the input and break down the problem step by step. 
Atleast  think 5-6 steps on how to solve the problem before solving it down 

The steps are you get the user input, you analyze , you think , you again think for several times and then return an output with the explaination and then you  validate the final output before giving the result .

Follow the steps in sequence that is "analyze" , "think" , "output", "validate" and finally "result"


Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input 
3. Carefully analyse the user query

Output Format:
{{step:"string",content:"string"}}

Example:
Input: what is 2+2
Output: {{step:"analyze",content:"Alright! the user is intrested in maths query and is asking a basic arthmetic operation"}}
Output:{{step:"think:,content:"To perform the addtion I must go from left to right and add all the operands" }}
Output:{{step:"output",content:"4" }}
Output:{{step:"validate",content:"Seems like 4 is the correct answer to 2+2"}}
Output:{{step:"result",content:"2+2=4 and that is calculated by adding all the numbers "}}"""

messages=[{
        "role":"system",
        "content":system_prompt
    }]
query = input("> ")
messages.append({"role":"user","content":query})
while True:
    result  = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type":"json_object"},
        messages=messages)
    parsed_response = json.loads(result.choices[0].message.content)
    if parsed_response.get("step")!="output":
        print(f"🧠: {parsed_response.get("content")}")
    else:
        print(f"📝: {parsed_response.get("content")}")
        break
        
    messages.append({"role":"assistant","content":json.dumps(parsed_response)})
    

print(result)