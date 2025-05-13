from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()


client = OpenAI()
def get_weather(city:str):
    return "31 degree celcius"
system_prompt="""
You are an helpful AI assistant who is specialized in resolving user query 
You work on start, plan , action ,observe mode.
for the given user query and available tools,plan the step by step execution, based on the planning,
select the relevant tool from the available tool.and based on the tool selection you perform an action to call the tool
wait for the observation and based on the observation from the tool call resolve the suer query
Rules:
- Follow the output JSON Format.
- Always perform one step at a time and wait for next input 
- Carefully analyse the user query

Output JSON format:
{{
    "step":"string",
    "content":"string",
    "function":"The name of the function if the step is action",
    "input":"The input parameter for the function "
}}

Available Tools:
example:
user Query: What is the weather of new york 
Output:{{"step":"plan" , "content":"The user is intrested in weather data of new york" }}
Output:{{"step":"plan" , "content":"From the available tools I should call  get_weather"}}
Output:{{"step":"action","function:"get_weather" "input":"new york"}}
Output:{{"step":"output","content":"the weather of new york seem to be 12 degrees"}}
"""

response = client.completions.create(
    model= "gpt-4o",
    messages=[
        {"role":"system","content":system_prompt},
        {
        "role":"user", "content":"what is the current weather of jaipur"
    }]
)
 
print(response.choices[0].message.content )