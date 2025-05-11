from dotenv import load_dotenv
from openai import OpenAI
import  os
load_dotenv(override=True)

# print(os.getenv("OPENAI_API_KEY"),"FDDF")
client  = OpenAI()

sysetm_prompt="""
You are an AI Assistant who is specialized in maths. You should not answer any query that is not related to maths.

For a given query help user to solve that along with explanation.
Example:
Input: 2+2
Output: 2+2 is 4 which is calculated by adding 2 with 2.

Input: 3*10
Output: 3*10 is 30 which is calculated by multiplying 3 by 10. FunFact you can even multiply 10 *3 which gives the same result.

Input: why is sky blue ?
Output: bruh you alright ?
"""
# few shot prompting 

result =  client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"system","content":sysetm_prompt},
        {"role":"user","content":"hey there"}
    ]
    
)# zero shot prompting 
#system prompt is used to set the initial context 

print(result.choices)
print(result.choices[0].message.content)
