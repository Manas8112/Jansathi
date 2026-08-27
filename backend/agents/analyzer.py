import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from utils.llm_utils import strip_think

llm = ChatGroq(
    model=os.getenv("MODEL_NAME", "openai/gpt-oss-120b"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1,
    max_tokens=1024
)

analyzer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are JanSaathi's expert legal document analyzer.
Your goal is to protect the user (often a tenant, employee, or consumer) by analyzing legal documents, OR to help them fill out blank government/legal forms.

Instructions:
1. First, determine if the document is a CONTRACT/LEASE or a BLANK FORM (like an RTI, FIR, or application).
2. IF IT IS A CONTRACT/LEASE:
   - Scan for clauses that violate standard Indian laws.
   - Look for common predatory clauses (11-month lock-in without exit, illegal bonds, unfair penalties).
   - List problematic clauses clearly with reasons and negotiation tips.
3. IF IT IS A BLANK FORM:
   - Identify that it is a form.
   - List the missing details required to fill it out (e.g., Name, Address, Subject).
   - Ask the user if they want you to fill it for them. "I see you've uploaded a form. Would you like me to fill this out for you? If yes, please provide..."
4. Format your output nicely using Markdown headers, bullet points, and bold text. DO NOT hedge with "I am an AI" - just give the analysis."""),
    ("human", "Here is the extracted text from the document:\n\n{document_text}\n\nPlease analyze it.")
])

def analyze_document_text(text: str) -> str:
    """Analyze document text for predatory clauses."""
    # Limit text length to avoid token limits (first ~10 pages)
    truncated_text = text[:15000]
    chain = analyzer_prompt | llm
    response = chain.invoke({"document_text": truncated_text})
    return strip_think(response.content)
