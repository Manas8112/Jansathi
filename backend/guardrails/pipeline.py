import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from guardrails.schemas import LegalResponse

class HallucinationDetector:
    def __init__(self):
        # We use a fast, cheap model for verification
        self.llm = ChatGroq(
            model=os.getenv("MODEL_CHEAP", "llama-3.1-8b-instant"),
            temperature=0.0
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a strict Indian Legal Fact Checker. 
Your job is to verify if the claims in the 'Response' are fully supported by the 'Retrieved Context'.
Output a JSON object exactly matching this format:
{{
    "is_grounded": true/false,
    "grounding_score": 0.0 to 1.0,
    "unsupported_claims": ["list of claims that are not in the context, if any"]
}}"""),
            ("user", "Retrieved Context:\n{context}\n\nResponse:\n{response}")
        ])
        self.chain = self.prompt | self.llm
        
    def check(self, response_text: str, retrieved_context: list[str]) -> dict:
        context = "\n\n".join(retrieved_context)
        try:
            res = self.chain.invoke({"context": context, "response": response_text})
            # Naive JSON parsing from LLM output
            output_text = res.content.strip()
            if "```json" in output_text:
                output_text = output_text.split("```json")[1].split("```")[0].strip()
            return json.loads(output_text)
        except Exception as e:
            print(f"Hallucination detection failed: {e}")
            return {"is_grounded": True, "grounding_score": 1.0, "unsupported_claims": []}

class ConfidenceScorer:
    def __init__(self):
        self.llm = ChatGroq(
            model=os.getenv("MODEL_CHEAP", "llama-3.1-8b-instant"),
            temperature=0.0
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are evaluating the confidence of an AI-generated legal response.
Analyze the response and output a JSON object:
{{
    "confidence": "high", "medium", or "low",
    "reason": "short explanation"
}}"""),
            ("user", "{response}")
        ])
        self.chain = self.prompt | self.llm
        
    def score(self, response_text: str) -> dict:
        try:
            res = self.chain.invoke({"response": response_text})
            output_text = res.content.strip()
            if "```json" in output_text:
                output_text = output_text.split("```json")[1].split("```")[0].strip()
            return json.loads(output_text)
        except Exception:
            return {"confidence": "medium", "reason": "Fallback"}
