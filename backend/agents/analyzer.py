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
You are scanning a contract, lease, or legal document for predatory, unfair, or illegal clauses under Indian Law.
Your goal is to protect the user (often a tenant, employee, or consumer).

Instructions:
1. Scan the provided document text for clauses that violate standard Indian laws (e.g. Rent Control Act, Consumer Protection Act, Labour Laws, Indian Contract Act).
2. Look for common predatory clauses:
   - Tenants: 11-month lock-in without exit, non-refundable deposits, arbitrary eviction, landlord right to enter without notice.
   - Employees: Illegal bonds, arbitrary termination without notice, withholding of PF/salary, extreme non-competes.
   - Consumers: Unfair penalties, waiver of right to sue, hidden charges.
3. If you find problematic clauses, list them clearly with:
   - The clause text (or summary).
   - Why it is unfair/illegal under Indian law.
   - What the user should negotiate or do about it.
4. If the document looks mostly fair, state that, but still point out any minor areas of concern.
5. Format your output nicely using Markdown headers, bullet points, and bold text. Keep it extremely readable and actionable. DO NOT hedge with "I am an AI, consult a lawyer" - just give the analysis."""),
    ("human", "Here is the extracted text from the document:\n\n{document_text}\n\nPlease analyze it for illegal or predatory clauses.")
])

def analyze_document_text(text: str) -> str:
    """Analyze document text for predatory clauses."""
    # Limit text length to avoid token limits (first ~10 pages)
    truncated_text = text[:15000]
    chain = analyzer_prompt | llm
    response = chain.invoke({"document_text": truncated_text})
    return strip_think(response.content)
