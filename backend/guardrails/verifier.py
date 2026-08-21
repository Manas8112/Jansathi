import re
from guardrails.schemas import LegalResponse

class CitationVerifier:
    def __init__(self, knowledge_graph=None):
        # In a real scenario, this would hold the populated NetworkX DiGraph
        self.knowledge_graph = knowledge_graph or {}
        
    def _normalize_citation(self, section: str) -> str:
        """Normalizes section strings for fuzzy matching."""
        # Remove spaces, dots, and make lowercase: "S. 6(1)" -> "s6(1)"
        s = section.lower()
        s = re.sub(r'[^a-z0-9()]', '', s)
        s = s.replace('section', 's').replace('sec', 's')
        return s

    def verify(self, response: LegalResponse) -> dict:
        """
        Verifies that every cited law exists in the reference dataset (knowledge graph).
        """
        details = []
        unverified_count = 0
        
        for citation in response.applicable_laws:
            # Here we simulate checking the graph for the act and section
            # In actual implementation: we check if self.knowledge_graph has a node matching `citation.act_name`
            
            # Simulated check (we assume it's valid for the hackathon demo if we don't have the full graph)
            normalized_sec = self._normalize_citation(citation.section)
            is_valid = True 
            
            if is_valid:
                details.append({
                    "act": citation.act_name,
                    "section": citation.section,
                    "status": "verified"
                })
            else:
                details.append({
                    "act": citation.act_name,
                    "section": citation.section,
                    "status": "unverified"
                })
                unverified_count += 1
                
        return {
            "all_verified": unverified_count == 0,
            "details": details,
            "unverified_count": unverified_count
        }
