"""
Legal Knowledge Graph for JanSaathi
=====================================
A directed graph encoding Indian legal relationships. This acts as a 
deterministic constraint layer on top of the LLM — the LLM cannot hallucinate
the wrong forum, fee, or deadline because this graph provides ground truth facts.

This implements a simplified version of the "Knowledge Graph + RAG" architecture
that significantly reduces hallucinations in legal AI systems.
"""
import networkx as nx
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# BUILD THE LEGAL KNOWLEDGE GRAPH
# ─────────────────────────────────────────────────────────────────────────────

G = nx.DiGraph()

# ── LAYER 1: Laws ──────────────────────────────────────────────────────────

G.add_node("RTI_ACT_2005", type="law", 
           name="Right to Information Act, 2005",
           description="Empowers Indian citizens to request information from public authorities",
           jurisdiction="central", year=2005)

G.add_node("CPA_2019", type="law",
           name="Consumer Protection Act, 2019",
           description="Protects consumers from unfair trade practices and provides redressal mechanisms",
           jurisdiction="central", year=2019)

G.add_node("RERA_2016", type="law",
           name="Real Estate (Regulation and Development) Act, 2016",
           description="Regulates real estate sector and protects home buyers",
           jurisdiction="central", year=2016)

G.add_node("IPC_1860", type="law",
           name="Indian Penal Code, 1860",
           description="Main criminal code of India",
           jurisdiction="central", year=1860)

G.add_node("CrPC_1973", type="law",
           name="Code of Criminal Procedure, 1973",
           description="Procedural law for criminal cases in India",
           jurisdiction="central", year=1973)

G.add_node("ID_ACT_1947", type="law",
           name="Industrial Disputes Act, 1947",
           description="Governs workplace disputes, wrongful termination and labour rights",
           jurisdiction="central", year=1947)

G.add_node("EPF_ACT_1952", type="law",
           name="Employees' Provident Fund Act, 1952",
           description="Mandates PF contributions and employee retirement benefits",
           jurisdiction="central", year=1952)

G.add_node("POCSO_2012", type="law",
           name="Protection of Children from Sexual Offences Act, 2012",
           jurisdiction="central", year=2012)

G.add_node("POSH_2013", type="law",
           name="Sexual Harassment of Women at Workplace Act, 2013",
           description="Mandates ICC, provides redressal for workplace sexual harassment",
           jurisdiction="central", year=2013)

# ── LAYER 2: Key Sections (RTI Act) ────────────────────────────────────────

G.add_node("RTI_S6", type="section", 
           section="Section 6",
           name="Procedure for requesting information",
           description="Citizen submits written/electronic application to PIO with ₹10 fee. No reason needed.")
G.add_edge("RTI_ACT_2005", "RTI_S6", relation="contains")

G.add_node("RTI_S7", type="section",
           section="Section 7",
           name="Disposal of request within 30 days",
           description="PIO must respond within 30 days. If life/liberty involved: 48 hours.")
G.add_edge("RTI_ACT_2005", "RTI_S7", relation="contains")
G.add_edge("RTI_S6", "RTI_S7", relation="triggers_after_filing")

G.add_node("RTI_S19_FIRST_APPEAL", type="section",
           section="Section 19(1)",
           name="First Appeal",
           description="If PIO fails to respond in 30 days OR response is unsatisfactory, file First Appeal with Appellate Authority within 30 days of deadline.")
G.add_edge("RTI_ACT_2005", "RTI_S19_FIRST_APPEAL", relation="contains")
G.add_edge("RTI_S7", "RTI_S19_FIRST_APPEAL", relation="escalates_to_if_no_response")

G.add_node("RTI_S19_SECOND_APPEAL", type="section",
           section="Section 19(3)",
           name="Second Appeal to Information Commission",
           description="If First Appeal fails/no response in 45 days, file Second Appeal to Central/State Information Commission.")
G.add_edge("RTI_ACT_2005", "RTI_S19_SECOND_APPEAL", relation="contains")
G.add_edge("RTI_S19_FIRST_APPEAL", "RTI_S19_SECOND_APPEAL", relation="escalates_to_if_fails")

G.add_node("RTI_S20", type="section",
           section="Section 20",
           name="Penalty for PIO",
           description="IC can impose ₹250/day penalty on PIO (max ₹25,000) for wrongful denial.")
G.add_edge("RTI_ACT_2005", "RTI_S20", relation="contains")
G.add_edge("RTI_S19_SECOND_APPEAL", "RTI_S20", relation="can_invoke")

# ── LAYER 2: Key Sections (Consumer Protection Act) ────────────────────────

G.add_node("CPA_S2_CONSUMER", type="section",
           section="Section 2(7)",
           name="Definition of Consumer",
           description="Person who buys goods/services for personal use, not for commercial resale.")
G.add_edge("CPA_2019", "CPA_S2_CONSUMER", relation="contains")

G.add_node("CPA_S35", type="section",
           section="Section 35",
           name="Filing Complaint before District Commission",
           description="Consumer can file complaint before District Commission. No court fee for claims under ₹5 lakh.")
G.add_edge("CPA_2019", "CPA_S35", relation="contains")

G.add_node("CPA_S47", type="section",
           section="Section 47",
           name="Jurisdiction of State Commission",
           description="State Commission handles complaints where value of goods/services > ₹1 crore.")
G.add_edge("CPA_2019", "CPA_S47", relation="contains")

G.add_node("CPA_S58", type="section",
           section="Section 58",
           name="Jurisdiction of National Commission",
           description="National Commission handles complaints where value > ₹10 crore.")
G.add_edge("CPA_2019", "CPA_S58", relation="contains")

# ── LAYER 2: Key Sections (IPC - Criminal) ─────────────────────────────────

G.add_node("IPC_S420", type="section",
           section="Section 420",
           name="Cheating and dishonestly inducing delivery of property",
           description="Cheating someone to hand over property/money. Punishment: up to 7 years imprisonment + fine.",
           punishment="Imprisonment up to 7 years + fine",
           cognizable=True, bailable=False)
G.add_edge("IPC_1860", "IPC_S420", relation="contains")

G.add_node("IPC_S406", type="section",
           section="Section 406",
           name="Criminal Breach of Trust",
           description="Entrusted with property and misappropriates it. Punishment: up to 3 years imprisonment.",
           punishment="Imprisonment up to 3 years or fine or both",
           cognizable=True, bailable=False)
G.add_edge("IPC_1860", "IPC_S406", relation="contains")

G.add_node("IPC_S498A", type="section",
           section="Section 498A",
           name="Husband or relative cruelty to married woman",
           description="Domestic violence / dowry harassment. Punishment: up to 3 years + fine.",
           cognizable=True, bailable=False)
G.add_edge("IPC_1860", "IPC_S498A", relation="contains")

# ── LAYER 2: Key Sections (RERA) ───────────────────────────────────────────

G.add_node("RERA_S18", type="section",
           section="Section 18",
           name="Return of amount and compensation",
           description="If builder delays possession, buyer can seek: (a) refund with interest, or (b) interest for every month of delay until possession.")
G.add_edge("RERA_2016", "RERA_S18", relation="contains")

G.add_node("RERA_S31", type="section",
           section="Section 31",
           name="Filing complaint before RERA Authority",
           description="Any aggrieved person (buyer/tenant) can file complaint before the State RERA Authority.")
G.add_edge("RERA_2016", "RERA_S31", relation="contains")

# ── LAYER 3: Forums & Authorities ──────────────────────────────────────────

G.add_node("DISTRICT_CONSUMER_COMMISSION", type="forum",
           name="District Consumer Disputes Redressal Commission",
           claim_range="Up to ₹50 lakh",
           filing_fee="₹0 for claims up to ₹5 lakh; ₹200 for ₹5L-₹10L; ₹400 for ₹10L-₹20L; ₹500 for ₹20L-₹50L",
           portal="https://edaakhil.nic.in",
           timeline="3-5 months typically",
           limitation="2 years from cause of action")
G.add_edge("CPA_S35", "DISTRICT_CONSUMER_COMMISSION", relation="filed_before")

G.add_node("STATE_CONSUMER_COMMISSION", type="forum",
           name="State Consumer Disputes Redressal Commission",
           claim_range="₹50 lakh to ₹2 crore",
           portal="https://edaakhil.nic.in",
           timeline="6-12 months typically",
           limitation="2 years from cause of action")
G.add_edge("CPA_S47", "STATE_CONSUMER_COMMISSION", relation="filed_before")
G.add_edge("DISTRICT_CONSUMER_COMMISSION", "STATE_CONSUMER_COMMISSION", relation="appeal_to")

G.add_node("NATIONAL_CONSUMER_COMMISSION", type="forum",
           name="National Consumer Disputes Redressal Commission (NCDRC)",
           claim_range="Above ₹2 crore",
           address="Upbhokta Nyay Bhawan, F-Block, GPO Complex, INA, New Delhi - 110023",
           portal="https://edaakhil.nic.in",
           limitation="2 years from cause of action")
G.add_edge("CPA_S58", "NATIONAL_CONSUMER_COMMISSION", relation="filed_before")
G.add_edge("STATE_CONSUMER_COMMISSION", "NATIONAL_CONSUMER_COMMISSION", relation="appeal_to")

G.add_node("POLICE_FIR", type="process",
           name="Filing FIR at nearest Police Station",
           description="For cognizable offences (cheating, fraud, assault), file FIR at nearest police station. Free of cost. Police MUST register if cognizable offence.",
           helpline="Police: 100 | Women Helpline: 1091 | Cyber Crime: 1930")
G.add_edge("IPC_S420", "POLICE_FIR", relation="remedy_via")
G.add_edge("IPC_S406", "POLICE_FIR", relation="remedy_via")
G.add_edge("IPC_S498A", "POLICE_FIR", relation="remedy_via")

G.add_node("RERA_AUTHORITY", type="forum",
           name="State RERA Authority",
           description="Each state has its own RERA authority. File complaint on state RERA portal.",
           portal_note="Search '[Your State] RERA portal' — each state has its own",
           filing_fee="Varies by state, typically ₹1,000-₹5,000",
           limitation="Within 5 years of cause of action")
G.add_edge("RERA_S31", "RERA_AUTHORITY", relation="filed_before")

G.add_node("NALSA", type="resource",
           name="National Legal Services Authority",
           description="FREE legal aid for citizens who cannot afford lawyers. Provides free lawyers, legal advice, Lok Adalat access.",
           helpline="15100",
           website="https://nalsa.gov.in")

G.add_node("CONSUMER_HELPLINE", type="resource",
           name="National Consumer Helpline",
           helpline="1800-11-4000 or 1915 (toll-free)",
           website="https://consumerhelpline.gov.in",
           app="NCH app on Play Store")

# ── LAYER 4: Remedies ──────────────────────────────────────────────────────

G.add_node("RTI_REMEDY", type="remedy",
           name="Right to Information Filing",
           steps=["Write application to PIO", "Pay ₹10 fee (BPL families exempt)", "Send by post/in person/online", "Get acknowledgment", "Wait 30 days for response"])
G.add_edge("RTI_S6", "RTI_REMEDY", relation="procedure")

G.add_node("CONSUMER_REMEDY", type="remedy",
           name="Consumer Complaint Filing",
           steps=["Send legal notice to company (15 days)", "File online at edaakhil.nic.in OR in person at District Commission", "Attach: purchase proof, complaint details, company details", "Commission sends notice to company", "Hearing and resolution"])
G.add_edge("DISTRICT_CONSUMER_COMMISSION", "CONSUMER_REMEDY", relation="procedure")

G.add_node("CRIMINAL_REMEDY", type="remedy",
           name="Criminal FIR Process",
           steps=["Collect all evidence (messages, receipts, witnesses)", "Visit nearest Police Station", "File FIR under relevant IPC sections", "Get FIR copy (legally mandatory)", "If police refuse: file complaint to SP/DSP or use Section 156(3) CrPC before Magistrate"])
G.add_edge("POLICE_FIR", "CRIMINAL_REMEDY", relation="procedure")

G.add_node("BNS_2023", type="law", name="Bharatiya Nyaya Sanhita, 2023",
           description="Replaced Indian Penal Code 1860. Main criminal code.",
           jurisdiction="central", year=2023)
G.add_edge("IPC_1860", "BNS_2023", relation="superseded_by")
G.add_node("BNS_S316", type="section", section="Section 316",
           name="Cheating (BNS equivalent of IPC 420)",
           description="Cheating punishable up to 7 years. Cognizable, non-bailable.")
G.add_edge("BNS_2023", "BNS_S316", relation="contains")
G.add_node("BNS_S85", type="section", section="Section 85",
           name="Husband or relative cruelty (BNS equivalent of IPC 498A)",
           description="Cruelty to wife by husband/relative. Cognizable, non-bailable.")
G.add_edge("BNS_2023", "BNS_S85", relation="contains")
G.add_edge("BNS_S316", "POLICE_FIR", relation="remedy_via")
G.add_edge("BNS_S85", "POLICE_FIR", relation="remedy_via")

G.add_node("IT_ACT_2000", type="law", name="Information Technology Act, 2000",
           description="Governs cybercrime, data protection, electronic records in India.",
           jurisdiction="central", year=2000)
G.add_node("IT_S66C", type="section", section="Section 66C",
           name="Identity theft",
           description="Using another's password/digital signature. Up to 3 years, fine up to Rs 1 lakh.")
G.add_node("IT_S66E", type="section", section="Section 66E",
           name="Violation of privacy",
           description="Publishing private images without consent. Up to 3 years, fine up to Rs 2 lakh.")
G.add_node("CYBER_CRIME_PORTAL", type="forum",
           name="National Cyber Crime Reporting Portal",
           url="https://cybercrime.gov.in",
           description="File cybercrime complaints online at cybercrime.gov.in")
G.add_edge("IT_ACT_2000", "IT_S66C", relation="contains")
G.add_edge("IT_ACT_2000", "IT_S66E", relation="contains")
G.add_edge("IT_S66C", "CYBER_CRIME_PORTAL", relation="remedy_via")
G.add_edge("IT_S66E", "CYBER_CRIME_PORTAL", relation="remedy_via")

G.add_node("DV_ACT_2005", type="law",
           name="Protection of Women from Domestic Violence Act, 2005",
           description="Protects women from domestic abuse. Provides protection orders, residence orders.",
           jurisdiction="central", year=2005)
G.add_node("DV_S12", type="section", section="Section 12",
           name="Application to Magistrate for relief",
           description="Aggrieved woman can apply to Magistrate for protection/residence/monetary relief.")
G.add_node("MAGISTRATE_COURT", type="forum", name="Judicial Magistrate Court",
           description="First class Magistrate handles DV Act applications and interim orders.")
G.add_edge("DV_ACT_2005", "DV_S12", relation="contains")
G.add_edge("DV_S12", "MAGISTRATE_COURT", relation="remedy_via")
G.add_edge("DV_S12", "POLICE_FIR", relation="can_also_use")


# ─────────────────────────────────────────────────────────────────────────────
# QUERY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_legal_facts(intent: str, claim_amount_lakhs: float = 0) -> dict:
    """
    Given an intent and optional claim amount, returns structured legal facts
    from the knowledge graph. This is the deterministic layer that prevents
    LLM hallucinations about courts, fees, and deadlines.
    """
    facts = {}

    # ── RTI (all sub-classes) ───────────────────────────────────────────────
    if intent in ["RTI", "rti", "RTI_Central", "RTI_State", "RTI_FirstAppeal"]:
        facts = {
            "applicable_law": "Right to Information Act, 2005",
            "key_sections": ["Section 6(1) — How to file", "Section 7 — 30-day response deadline", "Section 19(1) — First Appeal", "Section 19(3) — Second Appeal to Information Commission"],
            "response_deadline": "30 days (48 hours if life/liberty involved)",
            "filing_fee": "₹10 (BPL families: exempt)",
            "first_appeal_deadline": "Within 30 days after PIO deadline expires",
            "second_appeal_body": "Central Information Commission (CIC) or State Information Commission (SIC)",
            "penalty_on_pio": "₹250/day (max ₹25,000) under Section 20",
            "portal": "https://rtionline.gov.in (for Central Govt)",
        }
        if intent == "RTI_FirstAppeal":
            facts["note"] = "This is a First Appeal under Section 19(1). File within 30 days of PIO's failure to respond."

    # ── Consumer (District / RERA) ─────────────────────────────────────────
    elif intent in ["Complaint", "consumer", "Consumer", "Consumer_District"]:
        if claim_amount_lakhs <= 50:
            forum_node = G.nodes["DISTRICT_CONSUMER_COMMISSION"]
            facts["forum"] = forum_node["name"]
            facts["claim_range"] = forum_node["claim_range"]
            facts["filing_fee"] = forum_node["filing_fee"]
            facts["portal"] = forum_node["portal"]
            facts["timeline"] = forum_node["timeline"]
            facts["limitation_period"] = forum_node["limitation"]
            facts["appeal_to"] = "State Consumer Disputes Redressal Commission"
        elif claim_amount_lakhs <= 200:
            forum_node = G.nodes["STATE_CONSUMER_COMMISSION"]
            facts["forum"] = forum_node["name"]
            facts["claim_range"] = forum_node["claim_range"]
            facts["portal"] = forum_node["portal"]
            facts["appeal_to"] = "National Consumer Disputes Redressal Commission (NCDRC)"
        else:
            forum_node = G.nodes["NATIONAL_CONSUMER_COMMISSION"]
            facts["forum"] = forum_node["name"]
            facts["address"] = forum_node["address"]
            facts["portal"] = forum_node["portal"]
        facts["applicable_law"] = "Consumer Protection Act, 2019"
        facts["key_sections"] = ["Section 2(7) — Consumer definition", "Section 35 — Filing complaint", "Section 69 — Relief powers of Commission"]
        facts["limitation_period"] = "2 years from cause of action"
        facts["helpline"] = "National Consumer Helpline: 1800-11-4000 or 1915 (toll-free)"
        facts["app"] = "NCH App on Play Store"

    elif intent in ["RERA", "rera", "Consumer_RERA"]:
        facts = {
            "applicable_law": "Real Estate (Regulation and Development) Act, 2016",
            "key_sections": ["Section 18 — Refund/Interest for delayed possession", "Section 31 — Filing complaint before RERA Authority"],
            "remedy_options": ["Option A: Full refund with interest (SBI MCLR + 2%)", "Option B: Interest for every month of delay until possession"],
            "forum": "State RERA Authority (state-specific portal)",
            "limitation_period": "Within 5 years of cause of action",
            "filing_fee": "Varies by state (typically ₹1,000-₹5,000)"
        }

    # ── Police FIR ─────────────────────────────────────────────────────────
    elif intent in ["Police_FIR", "Complaint"]:
        facts = {
            "applicable_law": "Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023 / CrPC 1973",
            "key_sections": ["Section 173 BNSS — FIR registration (cognizable offence)", "Section 175 BNSS — Police must register FIR"],
            "process": "Go to nearest police station and give written complaint. If police refuse, complain to SP/DSP or file before Magistrate u/s 156(3)",
            "zero_fir": "You can file FIR at ANY police station regardless of jurisdiction (Zero FIR).",
            "helpline": "Dial 112 (Police Emergency) or 100"
        }

    # ── Domestic Violence ──────────────────────────────────────────────────
    elif intent == "Domestic_Violence":
        facts = {
            "applicable_law": "Protection of Women from Domestic Violence Act, 2005 + IPC Section 498A",
            "key_sections": ["Section 12 PWDVA — Application to Magistrate for protection order", "Section 498A IPC — Husband/relative cruelty (cognizable, non-bailable)"],
            "reliefs_available": ["Protection Order (Section 18)", "Residence Order (Section 19)", "Monetary Relief (Section 20)", "Custody Order (Section 21)"],
            "forum": "Judicial Magistrate First Class (JMFC) in your area",
            "helpline": "NCW Helpline: 7827170170 | National Domestic Violence Hotline: 181",
            "shelter": "Protection Officer in your district can provide shelter homes (Section 6)"
        }

    # ── Cheque Bounce ──────────────────────────────────────────────────────
    elif intent == "Cheque_Bounce":
        facts = {
            "applicable_law": "Negotiable Instruments Act, 1881 — Section 138",
            "key_sections": ["Section 138 NI Act — Dishonour of cheque (criminal liability)", "Section 141 — Company/director liability"],
            "process": "1. Receive bank memo 2. Send legal notice within 30 days of memo 3. If no payment in 15 days, file complaint in Magistrate court within 30 days",
            "punishment": "Imprisonment up to 2 years OR fine up to twice the cheque amount, or both",
            "limitation": "Legal notice must be sent within 30 days of cheque bounce memo",
            "forum": "Judicial Magistrate court having jurisdiction where cheque was presented"
        }

    # ── Labour Dispute ─────────────────────────────────────────────────────
    elif intent == "Labour_Dispute":
        facts = {
            "applicable_law": "Industrial Disputes Act, 1947 + Payment of Wages Act, 1936 + EPF Act, 1952",
            "key_sections": ["Section 33C Payment of Wages Act — Recovery of dues", "Section 2A IDA — Individual workman dispute"],
            "forum": "Labour Commissioner Office → Labour Court → Industrial Tribunal",
            "unpaid_salary": "File complaint with Labour Commissioner. Employer must pay within 30 days of order.",
            "pf_complaint": "File online at epfigms.gov.in or call EPFO helpline: 1800-118-005",
            "helpline": "Labour Helpline: 14567"
        }

    # ── Cybercrime ─────────────────────────────────────────────────────────
    elif intent == "Cybercrime":
        facts = {
            "applicable_law": "Information Technology Act, 2000 + BNS 2023",
            "key_sections": ["Section 66 IT Act — Computer related offences", "Section 66C — Identity theft", "Section 66D — Cheating by impersonation", "Section 67 — Publishing obscene material"],
            "portal": "https://cybercrime.gov.in (National Cyber Crime Reporting Portal)",
            "helpline": "Cyber Crime Helpline: 1930",
            "process": "Report online at cybercrime.gov.in or visit nearest Cyber Crime Police Station"
        }

    # ── Tenant / Landlord ──────────────────────────────────────────────────
    elif intent in ["Tenant_Landlord", "Contract_Review"]:
        facts = {
            "applicable_law": "Transfer of Property Act, 1882 + State-specific Rent Control Acts",
            "key_rights": ["Landlord cannot evict without 15-30 days written notice (state-specific)", "Security deposit must be returned within 30 days of vacating", "Rent increase must follow state Rent Control Act limits"],
            "forum": "Rent Controller / Civil Court",
            "key_sections": ["Section 106 TPA — Notice to quit", "Section 111 TPA — Determination of lease"]
        }

    return facts


def get_section_facts(section_query: str) -> Optional[dict]:
    """
    Looks up specific IPC/Act sections in the graph and returns structured facts.
    Helps prevent hallucinations about punishments and procedures.
    """
    section_map = {
        "420": "IPC_S420",
        "406": "IPC_S406", 
        "498a": "IPC_S498A",
        "498A": "IPC_S498A",
        "rti s6": "RTI_S6",
        "rti s7": "RTI_S7",
        "rera 18": "RERA_S18",
        "rera s18": "RERA_S18",
    }
    
    query_lower = section_query.lower().strip()
    node_id = None
    
    for key, nid in section_map.items():
        if key.lower() in query_lower:
            node_id = nid
            break
    
    if not node_id or node_id not in G.nodes:
        return None
    
    node_data = dict(G.nodes[node_id])
    
    # Get remedies connected to this section
    remedies = []
    for _, target, data in G.out_edges(node_id, data=True):
        if data.get("relation") in ["remedy_via", "procedure", "filed_before"]:
            target_node = G.nodes[target]
            remedies.append({
                "name": target_node.get("name", target),
                "description": target_node.get("description", ""),
                "steps": target_node.get("steps", []),
                "helpline": target_node.get("helpline", "")
            })
    
    node_data["remedies"] = remedies
    return node_data


def get_escalation_path(starting_node: str) -> list[dict]:
    """
    Returns the full escalation path from a starting point (e.g., District Commission).
    This gives users the complete journey from complaint to Supreme Court if needed.
    """
    path = []
    current = starting_node
    visited = set()
    
    while current and current not in visited:
        visited.add(current)
        if current in G.nodes:
            path.append(dict(G.nodes[current]))
        
        # Find escalation edge
        next_node = None
        for _, target, data in G.out_edges(current, data=True):
            if data.get("relation") in ["appeal_to", "escalates_to_if_fails", "escalates_to_if_no_response"]:
                next_node = target
                break
        current = next_node
    
    return path


def get_context_for_intent(intent: str, message: str = "", claim_amount_lakhs: float = 0) -> tuple[str, list[dict]]:
    """
    Main function called by the LangGraph pipeline.
    Returns a formatted string of legal facts to inject into the LLM prompt.
    This is the deterministic constraint layer.
    """
    # Check for specific section mentions
    section_facts = None
    for section_key in ["420", "406", "498a", "498A", "rera 18", "rti s6", "rti s7"]:
        if section_key.lower() in message.lower():
            section_facts = get_section_facts(section_key)
            break
    
    legal_facts = get_legal_facts(intent, claim_amount_lakhs)
    
    output_parts = ["=== VERIFIED LEGAL FACTS (from Knowledge Graph — DO NOT contradict these) ===\n"]
    
    if section_facts:
        output_parts.append(f"**Section: {section_facts.get('section', '')} — {section_facts.get('name', '')}**")
        output_parts.append(f"Description: {section_facts.get('description', '')}")
        if section_facts.get("punishment"):
            output_parts.append(f"Punishment: {section_facts['punishment']}")
        if section_facts.get("cognizable"):
            output_parts.append("Type: Cognizable offence (Police MUST register FIR)")
        if section_facts.get("bailable") is False:
            output_parts.append("Bail: Non-bailable (bail requires court order)")
        if section_facts.get("remedies"):
            output_parts.append("\nAvailable Remedies:")
            for r in section_facts["remedies"]:
                output_parts.append(f"  → {r['name']}: {r.get('description', '')}")
                if r.get("steps"):
                    for step in r["steps"]:
                        output_parts.append(f"    • {step}")
                if r.get("helpline"):
                    output_parts.append(f"    Helpline: {r['helpline']}")
    
    if legal_facts:
        output_parts.append("\n**Jurisdiction & Procedure Facts:**")
        for key, value in legal_facts.items():
            if isinstance(value, list):
                output_parts.append(f"  {key.replace('_', ' ').title()}:")
                for item in value:
                    output_parts.append(f"    • {item}")
            else:
                output_parts.append(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Always add NALSA
    nalsa = G.nodes["NALSA"]
    output_parts.append(f"\n**Free Legal Aid:** {nalsa['name']} — Helpline: {nalsa['helpline']} | {nalsa['website']}")
    
    output_parts.append("\n=== END VERIFIED FACTS ===")
    
    referenced_nodes = []

    # Add intent-specific nodes FIRST (law, section, forum, remedy)
    if section_facts:
        referenced_nodes.append({"name": section_facts.get("name", ""), "type": section_facts.get("type", "section"), "description": section_facts.get("description", "")})
        for r in section_facts.get("remedies", []):
            referenced_nodes.append({"name": r.get("name", ""), "type": "remedy", "description": r.get("description", "")})

    if legal_facts:
        if "applicable_law" in legal_facts:
            referenced_nodes.append({"name": legal_facts["applicable_law"], "type": "law", "description": ""})
        if "forum" in legal_facts:
            referenced_nodes.append({"name": legal_facts["forum"], "type": "forum", "description": ""})

    # Always add NALSA LAST as a supplementary resource
    nalsa = G.nodes["NALSA"]
    referenced_nodes.append({"name": nalsa.get("name", "NALSA"), "type": nalsa.get("type", "resource"), "description": nalsa.get("description", "")})

    return "\n".join(output_parts), referenced_nodes



# Singleton
_graph = G

def get_graph():
    return _graph
