from pydantic import BaseModel
from typing import Literal

class LawCitation(BaseModel):
    act_name: str
    section: str
    relevance: str

class Remedy(BaseModel):
    name: str
    priority: int
    cost: str
    timeline: str
    difficulty: Literal["easy", "medium", "hard"]
    description: str

class ActionStep(BaseModel):
    step_number: int
    action: str
    deadline: str | None
    details: str

class LegalResponse(BaseModel):
    summary: str
    applicable_laws: list[LawCitation]
    rights_identified: list[str]
    remedies: list[Remedy]
    action_steps: list[ActionStep]
    confidence: Literal["high", "medium", "low"]
    disclaimer: str
    escalation_needed: bool

class RTIApplication(BaseModel):
    addressed_to: str
    department: str
    subject: str
    information_points: list[str]
    fee_info: str
    applicant_placeholder: str
    date: str
    legal_reference: str
    next_steps: list[str]

class LegalNotice(BaseModel):
    addressed_to: str
    subject: str
    facts: list[str]
    legal_basis: list[LawCitation]
    demand: str
    deadline_days: int
    consequence: str

class SchemeMatch(BaseModel):
    scheme_name: str
    eligibility_status: Literal["eligible", "likely_eligible", "check_locally"]
    benefit: str
    documents_needed: list[str]
    where_to_apply: str
    website: str | None
