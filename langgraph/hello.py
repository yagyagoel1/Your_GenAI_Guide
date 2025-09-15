from typing_extensions import TypedDict

from langgraph.graph import StateGraph,START,END
from typing import Literal
from dotenv import load_dotenv
from openai import OpenAI
from langsmith.wrappers import wrap_openai

from pydantic import BaseModel
load_dotenv()
class DetectCallResponse(BaseModel):
    is_coding_question:bool
client =wrap_openai(OpenAI())
class State(TypedDict):
    user_message:str
    is_coding_question:bool
    ai_message:str
SYSTEM_PROMPT_FOR_MINI_AI="you are an expert in answering general queries of the user given the query answer the user with the most optimal answer to the question he or she asks you can be rude"
SYSTEM_PROMPT = "YOU ARE AN EXPERT IN DETECTING QUERIES AND DECIDE THAT WHETHER THEY ARE CODING QUESTION OR NON CODING USE YOUR SKILLS TO RESPOND TO THE GIVEN QUERY THAT THE GIVEN QUESTION IS OF CODING OR NOT "
SYSTEM_PROMPT_FOR_CODING_QUESTION = "YOU ARE AN LEAD ENGINEER AND ARE VERY INTELLIGENT YOU CAN SOLVE ANY CODING QUESTION IN SECONDS AND VERY ACCURATELY GIVEN THE QUERY RESPOND WITH THE SOLUTION OF THE CODING PROBLEM "
class SolveCodingQuestionResponse(BaseModel):
    answer:str
class MiniAiCAllResponse(BaseModel):
    answer:str
    
def detect_query(state:State):
    user_message = state.get("user_message")
    
    response = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        response_format=DetectCallResponse,
        messages=[{"role":"system","content":SYSTEM_PROMPT},
                  {"role":"user","content":user_message}]
    )
    print(response.choices[0].message.parsed.is_coding_question)
    state["is_coding_question"]=response.choices[0].message.parsed.is_coding_question
    
    return state


def solve_coding_question(state:State):

    user_message = state.get("user_message")
    response = client.beta.chat.completions.parse(
        model="gpt-4.1",
        response_format=SolveCodingQuestionResponse,
        messages=[{"role":"system","content":SYSTEM_PROMPT_FOR_CODING_QUESTION},
                  {"role":"user","content":user_message}]
    )
    print(response.choices[0].message.parsed.answer)
    state["ai_message"] = response.choices[0].message.parsed.answer
    print("solve me hu ")
    return state

def mini_ai(state:State):

    user_message = state.get("user_message")
    response = client.beta.chat.completions.parse(
        model="gpt-4.1",
        response_format=MiniAiCAllResponse,
        messages=[{"role":"system","content":SYSTEM_PROMPT_FOR_MINI_AI},
                  {"role":"user","content":user_message}]
    )
    print(response.choices[0].message.parsed.answer)
    state["ai_message"] = response.choices[0].message.parsed.answer
    return state
def route_edge(state:State) -> Literal["solve_coding_question","mini_ai"]:
    is_coding_question = state.get("is_coding_question")
    if is_coding_question:
        return "solve_coding_question"
    else:
        return "mini_ai"
        
graph_builder = StateGraph(State)

graph_builder.add_node("detect_query",detect_query)
graph_builder.add_node("solve_coding_question",solve_coding_question)
graph_builder.add_node("mini_ai",mini_ai)
graph_builder.add_node("route_edge",route_edge)


graph_builder.add_edge(START,"detect_query")
graph_builder.add_conditional_edges("detect_query",route_edge)
graph_builder.add_edge("solve_coding_question",END)
graph_builder.add_edge("mini_ai",END)

graph = graph_builder.compile()

def call_graph():
    state={
        "user_message":"how many r are there in strawberry",
        "ai_message":"",
        "is_coding_question":False
    }
    graph.invoke(state)
    
    
call_graph()
    