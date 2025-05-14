from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
import os
load_dotenv()


client = OpenAI()
def get_weather(city:str):
    if(not city):
        return "city is required feild"
    response = requests.get(f"https://wttr.in/{city}?format=%C+%d")
    return response.text

def run_command(command: str):
    results  = os.system(command=command)
    return results
available_tools={
    "get_weather":{
        "fn":get_weather,
        "description":"Takes a city name as an input and return the current city's weather"
    },
    "run_command":{
        "fn":run_command,
        "description":"this function takes a command as an input and executes the command in the system."
    }
}
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
- get_weather: "Takes a city name as an input and return the current city's weather"
- run_command: "this function takes a command as an input and executes the command in the system."
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
messages = [
    {"role":"system","content":system_prompt}
    
]

user_query=input(">")

messages.append({"role":"user","content":user_query})
while True:
    response = client.completions.create(
    model= "gpt-4o",
    response_format={"type":"json_object"},
    messages=messages
    
)
    parsed_output = json.loads(response.choices[0].message.content)
    messages.append({"role":"assistant","content":json.dumps(parsed_output)})
    
    if parsed_output.get("step")=="plan":
        print(f"🧠: {parsed_output.get("content")}")
        continue
    if parsed_output.get("step")=="action":
        print(f" : calling the function {parsed_output.get("function")}")
        tool_name= parsed_output.get("function")
        tool_input= parsed_output.get("input")
        if available_tools.get(tool_name,False)!=False:
            output=available_tools["get_weather"].get("fn")(tool_input)
            messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":output})})
            
    if parsed_output.get("step")=="output":
        print(f"📝: {parsed_output.get("content")}")
        break
        
        
print("Done :)")