"""
Jurisdiction Engine for JanSaathi
====================================
A purely deterministic rules engine — NO LLM involved.
Given a case type, state, claim amount, and date, it returns the exact:
- Which forum to file in (District / State / National Commission, RERA, etc.)
- Exact filing fees
- Limitation period (deadline to file)
- Escalation path
- Specific portal URLs and helpline numbers

This is the core "hallucination prevention" layer. The LLM can NEVER give 
the wrong court or fee because this engine provides the answer first.
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import date, timedelta


@dataclass
class JurisdictionResult:
    case_type: str
    applicable_law: str
    key_sections: list[str]
    primary_forum: str
    filing_fee: str
    limitation_period: str
    limitation_deadline: Optional[str]
    portal: str
    helplines: list[str]
    escalation_path: list[str]
    documents_required: list[str]
    immediate_steps: list[str]
    special_notes: list[str] = field(default_factory=list)

    def to_prompt_string(self) -> str:
        """Formats the jurisdiction data as a structured string for LLM injection."""
        lines = [
            f"\n=== JURISDICTION ENGINE OUTPUT (Deterministic — Ground Truth) ===",
            f"Case Type: {self.case_type}",
            f"Applicable Law: {self.applicable_law}",
            f"Key Sections: {', '.join(self.key_sections)}",
            f"\nPrimary Forum: {self.primary_forum}",
            f"Filing Fee: {self.filing_fee}",
            f"Limitation Period: {self.limitation_period}",
        ]
        if self.limitation_deadline:
            lines.append(f"⚠️ Deadline to File: {self.limitation_deadline}")
        
        lines.append(f"Online Portal: {self.portal}")
        
        if self.helplines:
            lines.append(f"Helplines: {' | '.join(self.helplines)}")
        
        lines.append("\nEscalation Path (if primary forum fails):")
        for i, step in enumerate(self.escalation_path, 1):
            lines.append(f"  {i}. {step}")
        
        lines.append("\nDocuments Required:")
        for doc in self.documents_required:
            lines.append(f"  • {doc}")
        
        lines.append("\nImmediate Steps:")
        for i, step in enumerate(self.immediate_steps, 1):
            lines.append(f"  Step {i}: {step}")
        
        if self.special_notes:
            lines.append("\n⚠️ Special Notes:")
            for note in self.special_notes:
                lines.append(f"  • {note}")
        
        lines.append("=== END JURISDICTION DATA ===\n")
        return "\n".join(lines)


class JurisdictionEngine:
    """
    Deterministic rules engine for Indian legal jurisdiction.
    Maps {case_type, claim_amount_lakhs} → exact forum, fees, deadlines.
    """

    def get_consumer_jurisdiction(self, claim_amount_lakhs: float, cause_date: Optional[date] = None) -> JurisdictionResult:
        """Consumer Protection Act 2019 jurisdiction rules."""
        
        limitation_deadline = None
        if cause_date:
            deadline = cause_date + timedelta(days=365 * 2)  # 2 years
            limitation_deadline = deadline.strftime("%d %b %Y") + " (2 years from cause of action)"
        
        if claim_amount_lakhs <= 50:
            forum = "District Consumer Disputes Redressal Commission (DCDRC)"
            fee = "₹0 (claims up to ₹5 lakh) | ₹200 (₹5L-₹10L) | ₹400 (₹10L-₹20L) | ₹500 (₹20L-₹50L)"
            escalation = [
                "State Consumer Disputes Redressal Commission (SCDRC) — if District Commission order unsatisfactory",
                "National Consumer Disputes Redressal Commission (NCDRC), New Delhi — if State order unsatisfactory",
                "Supreme Court of India — final appeal on questions of law"
            ]
        elif claim_amount_lakhs <= 200:
            forum = "State Consumer Disputes Redressal Commission (SCDRC)"
            fee = "₹2,000 (₹50L-₹1Cr) | ₹4,000 (₹1Cr-₹2Cr)"
            escalation = [
                "National Consumer Disputes Redressal Commission (NCDRC), New Delhi",
                "Supreme Court of India — final appeal"
            ]
        else:
            forum = "National Consumer Disputes Redressal Commission (NCDRC), New Delhi"
            fee = "₹5,000"
            escalation = [
                "Supreme Court of India — final appeal"
            ]

        return JurisdictionResult(
            case_type="Consumer Dispute",
            applicable_law="Consumer Protection Act, 2019",
            key_sections=["S.2(7) — Consumer definition", "S.35 — Filing complaint", "S.69 — Relief powers", "S.72 — Penalty for non-compliance"],
            primary_forum=forum,
            filing_fee=fee,
            limitation_period="2 years from the date of cause of action",
            limitation_deadline=limitation_deadline,
            portal="https://edaakhil.nic.in (e-Daakhil — file online)",
            helplines=["National Consumer Helpline: 1800-11-4000 (toll-free)", "SMS 'NCHHELP' to 8800001915", "NCH App on Play Store"],
            escalation_path=escalation,
            documents_required=[
                "Purchase receipt / invoice / order confirmation",
                "Proof of payment (bank statement / UPI screenshot)",
                "Warranty card or service agreement (if applicable)",
                "All communication with the company (emails, WhatsApp, chat screenshots)",
                "Copy of legal notice sent to company + postal receipt",
                "Photos/videos of defective product (if applicable)",
                "ID proof (Aadhaar / PAN)",
            ],
            immediate_steps=[
                "Send a formal legal notice to the company via Registered Post (give them 15 days to respond)",
                f"Register complaint online at https://edaakhil.nic.in (file under {forum})",
                "Attach all documents scanned as PDF",
                "Pay the filing fee online",
                "Commission will issue notice to the company — attend hearings as scheduled",
            ],
            special_notes=[
                "No advocate required — you can represent yourself (in-person or online)",
                "If claim is under ₹5 lakh, filing is completely free",
                "E-Daakhil allows 100% online filing — no need to travel to the forum",
            ]
        )

    def get_rti_jurisdiction(self, is_state_govt: bool = False, state: str = "") -> JurisdictionResult:
        """RTI Act 2005 jurisdiction rules."""
        
        if is_state_govt:
            commission = f"{state} State Information Commission (SIC)" if state else "State Information Commission (SIC)"
            portal = f"Check your state's official RTI portal (search '{state} RTI online')"
        else:
            commission = "Central Information Commission (CIC), New Delhi"
            portal = "https://rtionline.gov.in (for Central Government departments)"

        return JurisdictionResult(
            case_type="RTI Application",
            applicable_law="Right to Information Act, 2005",
            key_sections=["S.6(1) — How to file application", "S.7 — PIO must respond in 30 days", "S.19(1) — First Appeal (if no response)", "S.19(3) — Second Appeal to Information Commission", "S.20 — Penalty on PIO"],
            primary_forum="Public Information Officer (PIO) of the relevant department",
            filing_fee="₹10 (BPL card holders: EXEMPT from fee)",
            limitation_period="No limitation period to file RTI. But First Appeal must be within 30 days of PIO deadline.",
            limitation_deadline=None,
            portal=portal,
            helplines=["NALSA Free Legal Aid: 15100", "CIC: 011-26180532"],
            escalation_path=[
                "First Appeal: Appellate Authority of the same department (if PIO doesn't respond in 30 days or unsatisfactory)",
                f"Second Appeal: {commission} (if First Appeal fails or no response in 45 days)",
                "High Court Writ Petition (for extraordinary situations)"
            ],
            documents_required=[
                "Written application clearly stating information needed",
                "₹10 demand draft / postal order / court fee stamp (or BPL card for exemption)",
                "Your name, address, and contact details",
                "Copy of any previous correspondence with the department (if any)",
            ],
            immediate_steps=[
                "Write a clear, specific application stating EXACTLY what information you need",
                f"Send to the PIO by Registered Post OR file online at {portal}",
                "Keep the postal receipt and copy of your application",
                "If no response in 30 days, file First Appeal with the Appellate Authority",
                "If First Appeal fails, file Second Appeal with the Information Commission",
            ],
            special_notes=[
                "You do NOT need to give a reason for your RTI request",
                "If the information concerns life/liberty, PIO must respond within 48 hours",
                f"PIO can be penalized ₹250/day (max ₹25,000) under Section 20 for wrongful denial",
                "Third-party information may be exempt under Section 8",
            ]
        )

    def get_rera_jurisdiction(self, state: str = "") -> JurisdictionResult:
        """RERA 2016 jurisdiction rules."""
        
        rera_portals = {
            "Maharashtra": "https://maharera.mahaonline.gov.in",
            "Karnataka": "https://rera.karnataka.gov.in",
            "Delhi": "https://dda.gov.in/hrera",
            "UP": "https://up-rera.in",
            "Uttar Pradesh": "https://up-rera.in",
            "Gujarat": "https://gujrera.gujarat.gov.in",
            "Tamil Nadu": "https://tnrera.in",
            "Telangana": "https://rera.telangana.gov.in",
            "Rajasthan": "https://rera.rajasthan.gov.in",
        }
        portal = rera_portals.get(state, f"Search '{state} RERA portal' — each state has its own authority")

        return JurisdictionResult(
            case_type="Real Estate / Builder Dispute",
            applicable_law="Real Estate (Regulation and Development) Act, 2016",
            key_sections=["S.18 — Refund/interest for delayed possession", "S.31 — Filing complaint before RERA Authority", "S.71 — Adjudicating Officer for compensation", "S.43 — RERA Appellate Tribunal"],
            primary_forum=f"{state} RERA Authority" if state else "State RERA Authority",
            filing_fee="Varies by state (typically ₹1,000-₹5,000). Check your state RERA portal.",
            limitation_period="5 years from cause of action (delayed possession / defect)",
            limitation_deadline=None,
            portal=portal,
            helplines=["NALSA Free Legal Aid: 15100", "Contact your state RERA authority directly"],
            escalation_path=[
                "RERA Adjudicating Officer — for compensation claims",
                "RERA Appellate Tribunal — if RERA Authority order unsatisfactory",
                "High Court — for questions of law",
            ],
            documents_required=[
                "Sale Agreement / Builder-Buyer Agreement",
                "All payment receipts / demand letters from builder",
                "Possession letter (or proof of non-receipt)",
                "All correspondence with builder (emails, letters)",
                "Proof of registration of builder's project on RERA portal",
                "RERA registration number of the project",
            ],
            immediate_steps=[
                "Verify builder's project is registered on RERA portal (all new projects must be)",
                "Calculate total delay in days and interest owed under Section 18",
                "Send legal notice to builder demanding possession or refund",
                f"File complaint on {portal} (most states allow online filing)",
                "If no response in 60 days, escalate to RERA Appellate Tribunal",
            ],
            special_notes=[
                "Under Section 18, you can claim SBI MCLR + 2% interest for EVERY month of delay",
                "RERA complaints are typically resolved in 60 days",
                "Builder cannot force you to accept alternate flat without your consent",
                "Project must be RERA-registered — if not, file police complaint for cheating",
            ]
        )

    def get_workplace_jurisdiction(self, issue_type: str = "") -> JurisdictionResult:
        """Workplace dispute jurisdiction rules."""
        return JurisdictionResult(
            case_type="Workplace Dispute",
            applicable_law="Industrial Disputes Act, 1947 + Employees' Provident Funds Act, 1952 + POSH Act, 2013",
            key_sections=["ID Act S.25F — Wrongful termination compensation", "EPF Act S.7A — PF recovery proceedings", "POSH Act S.4 — Mandatory ICC in every company", "IPC S.406 — Criminal breach of trust (for salary theft)"],
            primary_forum="Labour Commissioner Office (your district) OR Internal Complaints Committee (POSH)",
            filing_fee="Free for most labour complaints",
            limitation_period="3 years from cause of action (for most labour disputes)",
            limitation_deadline=None,
            portal="https://shramsuvidha.gov.in | https://epfindia.gov.in (PF complaints)",
            helplines=["Labour Helpline: 1800-11-2522", "EPFO Helpline: 1800-118-005", "NALSA Legal Aid: 15100"],
            escalation_path=[
                "Labour Commissioner / Conciliation Officer",
                "Labour Court / Industrial Tribunal",
                "High Court",
            ],
            documents_required=[
                "Employment contract / offer letter",
                "Salary slips for last 3-6 months",
                "PF passbook / UAN details",
                "Any written communication about termination or issues",
                "Bank statements showing salary credits/non-payment",
                "Attendance records if available",
            ],
            immediate_steps=[
                "Document everything — screenshot all communications immediately",
                "File complaint with Labour Commissioner of your district (free)",
                "File PF complaint at https://epfindia.gov.in if PF is being withheld",
                "For POSH: file complaint with company's ICC within 3 months of incident",
                "For salary theft > ₹1 lakh: file FIR under IPC Section 406 (criminal breach of trust)",
            ],
            special_notes=[
                "Company with 10+ employees MUST have an Internal Complaints Committee (ICC) under POSH",
                "PF is mandatory for companies with 20+ employees — employer cannot withhold it",
                "Wrongful termination without notice: entitled to 1 month salary per year of service",
            ]
        )

    def resolve(self, intent: str, message: str = "", claim_amount_lakhs: float = 0, state: str = "") -> Optional[JurisdictionResult]:
        """Main resolver — picks the right jurisdiction based on intent."""
        intent_lower = intent.lower()
        
        if intent_lower in ["rti"]:
            is_state = any(word in message.lower() for word in ["state", "municipal", "panchayat", "corporation", "tehsil"])
            return self.get_rti_jurisdiction(is_state_govt=is_state, state=state)
        
        elif intent_lower in ["complaint", "consumer"]:
            return self.get_consumer_jurisdiction(claim_amount_lakhs)
        
        elif intent_lower in ["rera", "builder", "real estate"]:
            return self.get_rera_jurisdiction(state=state)
        
        elif intent_lower in ["workplace", "employment", "labour"]:
            return self.get_workplace_jurisdiction()
        
        return None


# Singleton
_engine = JurisdictionEngine()

def get_jurisdiction_engine() -> JurisdictionEngine:
    return _engine
