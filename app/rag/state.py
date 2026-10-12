from typing import List, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_core.documents import Document

# Below class is to describe the tools which llm can use to get the response.
# In simple words: it is a set of tools that the llm can use to get the response.

class RouteDecision(BaseModel):
    # Literal is used because we are restricting the output of llm to only two values, 
    # if the question is related to IT/support then it will return "kb" 
    # else it will return "direct"
    route: Literal["kb", "direct"] = Field(description="kb for IT/support questions; direct for greetings/simple chat")

class EvidenceGrade(BaseModel):
    # This class is used to determine whether the evidence is sufficient to answer the question
    # Literal is used because we are restricting the output of llm to only two values, 
    # if the evidence is sufficient to answer the question then it will return "good"
    # else it will return "weak"
    grade: Literal["good", "weak"] = Field(description="Whether evidence is sufficient to answer")

# below class is to define the state of the agent
# in simple words: it is a dictionary that will store the state of the agent
# TypedDict is used here to define the structure of the dictionary
# which ensures type safety and better code completion
class AgentState(TypedDict):
    question: str # original question
    current_query: str # query to be used for search
    kb_docs: List[Document] # documents retrieved from knowledge base from pinecone
    web_results: str # results from web search
    kb_grade: str # grade for knowledge base results
    web_grade: str # grade for web search results
    answer: str # final answer
    source_used: str # source used to generate the answer
    retry_count: int # number of retries
    trace: List[str] # trace of the agent
    citations: List[dict] # citations means source document references