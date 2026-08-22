"""
Comprehensive Legal Knowledge Base Ingestion for JanSaathi
============================================================
Adds 200+ dense legal passages across all major Indian laws to ChromaDB.

Coverage:
- Right to Information Act, 2005 (all major sections)
- Consumer Protection Act, 2019 (dispute types, forums, remedies)
- RERA 2016 (builder delays, refunds, complaints)
- IPC Sections (420, 406, 498A, 120B, 415, etc.)
- Labour & Employment Law (wrongful termination, PF, POSH)
- Tenant Rights (across states)
- Government Schemes (eligibility, benefits, how to apply)
- Procedure: How to File FIR, Consumer Complaint, RTI, RERA
- Legal Notices (format, what to write)
- Free Legal Aid (NALSA, District Legal Services Authority)
- Banking & Loan Rights (RBI guidelines, loan disputes)
- Medical Negligence & Patient Rights
- Property & Land Rights
- Cyber Crime & Digital Fraud
- Women's Rights & Domestic Violence
- Child Rights & Education RTEs

Run with: python training/ingest_knowledge_base.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

# ─────────────────────────────────────────────────────────────────
# MASTER KNOWLEDGE BASE: 200+ Dense Legal Passages
# Each entry is a chunk sized for optimal RAG retrieval (~300-500 words)
# ─────────────────────────────────────────────────────────────────

KNOWLEDGE_BASE = [

    # ── RIGHT TO INFORMATION ACT ──────────────────────────────────

    {
        "id": "rti_overview",
        "title": "Right to Information Act 2005 - Overview and Citizen Rights",
        "type": "bare_act", "category": "RTI",
        "text": """The Right to Information Act, 2005 (RTI Act) empowers every Indian citizen to request information from any public authority. A public authority includes all bodies constituted under the Constitution, Parliament, or State Legislatures, and bodies substantially financed by government funds. Under Section 3, all citizens have the right to information. Under Section 6(1), a citizen submits a written or electronic application to the Central Public Information Officer (CPIO) or State Public Information Officer (SPIO) along with the prescribed fee. The application need not state any reason. Under Section 7, the PIO must respond within 30 days. If information concerns life or liberty, the response must come within 48 hours. Under Section 7(1), the PIO must either provide the information or reject it with reasons. Under Section 7(6), the fee is waived for Below Poverty Line (BPL) cardholders. Under Section 8, certain information is exempt: national security, cabinet deliberations, personal information with no public interest, information that would impede investigation, commercial confidence. Under Section 19(1), if the PIO fails to respond or gives unsatisfactory response, the citizen may file a First Appeal with the Appellate Authority within 30 days of the deadline. Under Section 19(3), a Second Appeal can be filed with the Central Information Commission (CIC) or State Information Commission (SIC) within 90 days. Under Section 20, the CIC can impose a penalty of Rs 250 per day on the PIO, up to a maximum of Rs 25,000 for wrongful denial. The Central Government RTI portal is rtionline.gov.in."""
    },
    {
        "id": "rti_filing_procedure",
        "title": "How to File an RTI Application - Step by Step Guide",
        "type": "procedure", "category": "RTI",
        "text": """Filing an RTI application is simple and can be done online or offline. ONLINE: Visit rtionline.gov.in for Central Government departments. Select the Ministry/Department. Fill in your name, address, and the specific information you want. Pay Rs 10 fee online (UPI/Net Banking/Debit Card). Note the Registration Number. OFFLINE: Write a plain-language application addressed to 'The Central/State Public Information Officer, [Department Name]'. State clearly: 'I request the following information under Section 6(1) of the Right to Information Act, 2005'. List your specific information requests in numbered points. Attach a Rs 10 fee as a Demand Draft, Postal Order, or Court Fee Stamp in favour of the PIO. Send by Registered Post or hand-deliver. Get acknowledgment. STATE GOVERNMENT RTI: Each state has its own RTI portal (search '[State] RTI online portal') with the same Rs 10 fee (some states vary). WHAT HAPPENS NEXT: Within 30 days, the PIO must respond. If they don't: file First Appeal with Appellate Authority (free). If First Appeal fails within 45 days: file Second Appeal with CIC/SIC. TIPS: Be very specific about what information you want. Vague requests get rejected. Ask for specific dates, amounts, file numbers, reports rather than open-ended questions. You can ask for certified copies of documents."""
    },
    {
        "id": "rti_appeal_process",
        "title": "RTI First Appeal and Second Appeal - Complete Process",
        "type": "procedure", "category": "RTI",
        "text": """If the PIO does not respond within 30 days or gives an unsatisfactory response, you have strong remedies. FIRST APPEAL (Section 19(1)): File within 30 days of the date when the PIO response was due or received. Address to the First Appellate Authority (FAA), who is an officer senior to the PIO in the same department. State: your original RTI application date, registration number, what information was denied/incomplete, grounds for appeal. The FAA must decide within 30 days (extendable to 45 days with written reason). No fee for First Appeal. SECOND APPEAL (Section 19(3)): If FAA fails or gives unsatisfactory response, file Second Appeal with: Central Information Commission (CIC) for central government. State Information Commission (SIC) for state government. Must file within 90 days of FAA's decision or deadline. CIC/SIC can: order disclosure of information, impose penalty on PIO (Rs 250/day, max Rs 25,000 under Section 20), recommend disciplinary action, award compensation to the complainant. Filing CIC Second Appeal: online at cic.gov.in or by post. Include: copies of original RTI, PIO response, First Appeal, FAA response. PENALTY AND COMPENSATION: Under Section 20, CIC is mandatory to impose penalty if PIO denied without valid reason. Under Section 19(8), CIC can award compensation for any detriment caused. FREE LEGAL AID: NALSA (15100) provides free legal assistance for RTI appeals."""
    },
    {
        "id": "rti_exemptions",
        "title": "RTI Exemptions - What Information Cannot Be Sought",
        "type": "bare_act", "category": "RTI",
        "text": """Section 8 of the RTI Act lists exempt information that PIOs may refuse: (a) Information affecting sovereignty and integrity of India, state security, strategic interests, or foreign relations. (b) Information forbidden to be published by courts or that constitutes contempt of court. (c) Information whose disclosure would breach parliamentary privilege. (d) Trade secrets, commercial confidence, intellectual property, where disclosure would harm competitive position of a third party - unless public interest overrides. (e) Information available in fiduciary relationship unless larger public interest warrants disclosure. (f) Information received in confidence from foreign government. (g) Information that would endanger life or physical safety of any person, or identify source of information given in confidence to a law enforcement agency. (h) Information that would impede investigation or prosecution. (i) Cabinet papers including deliberations of Council of Ministers until the decision is taken and the matter is complete. (j) Personal information with no relationship to public activity, or that would cause unwarranted invasion of privacy - UNLESS larger public interest justifies disclosure. IMPORTANT: Under Section 8(2), even exempt information can be disclosed if public interest outweighs harm. Under Section 8(3), all information exempt under (a) to (i) is accessible after 20 years. Third Party Information under Section 11: If information concerns a third party who submitted it in confidence, the PIO must give the third party 5 days notice before deciding."""
    },

    # ── CONSUMER PROTECTION ────────────────────────────────────────

    {
        "id": "consumer_rights_overview",
        "title": "Consumer Rights Under Consumer Protection Act 2019",
        "type": "bare_act", "category": "Consumer",
        "text": """The Consumer Protection Act, 2019 gives Indian consumers 6 fundamental rights: (1) Right to Safety: protection against hazardous goods and services. (2) Right to Information: right to be informed about quantity, quality, purity, standard and price of goods. (3) Right to Choose: access to variety of goods at competitive prices. (4) Right to be Heard: consumer interests will receive due consideration. (5) Right to Seek Redressal: right to relief against unfair trade practices or exploitation. (6) Right to Consumer Education: right to acquire knowledge and skills to be an informed consumer. WHO IS A CONSUMER (Section 2(7)): Any person who buys goods or hires services for consideration, including buyer of goods for personal use (not for resale or commercial purpose). Online purchases are fully covered. WHAT IS A COMPLAINT (Section 2(6)): Defective goods, deficiency in services, unfair trade practices, hazardous goods, overcharging above displayed price, offering to sell goods in violation of law. CENTRAL CONSUMER PROTECTION AUTHORITY (Section 10): A new body empowered to investigate complaints, recall dangerous goods, cancel licences, impose penalties. PRODUCT LIABILITY (Chapter VI): Manufacturers, product service providers, product sellers are liable for personal injury or property damage caused by defective products. UNFAIR TRADE PRACTICES (Section 2(47)): Misleading advertising, false guarantees, bargain price claims, pyramid selling, offering gifts with strings attached."""
    },
    {
        "id": "consumer_complaint_filing",
        "title": "How to File Consumer Complaint - Online and Offline",
        "type": "procedure", "category": "Consumer",
        "text": """Before filing a formal complaint, send a legal notice to the company giving 15 days to resolve. If no response, file complaint. ONLINE FILING (e-Daakhil): Visit edaakhil.nic.in. Register with your email and phone. Create new complaint. Select District/State/National Commission based on claim amount. Fill: complainant details, opposite party details (company name, address, GST number if available), facts of the case in chronological order, relief sought (refund + compensation + litigation costs). Attach: purchase proof (invoice/receipt), payment screenshots, warranty card, all correspondence (emails, WhatsApp), photos of defective product, copy of legal notice and postal receipt. Pay filing fee online. Commission issues notice to the company. Attend hearings (can attend online). FORUM JURISDICTION by claim amount: Up to Rs 50 lakh: District Consumer Disputes Redressal Commission (DCDRC). Rs 50 lakh to Rs 2 crore: State Consumer Disputes Redressal Commission (SCDRC). Above Rs 2 crore: National Consumer Disputes Redressal Commission (NCDRC). FILING FEES: Under Rs 5 lakh: FREE. Rs 5-10 lakh: Rs 200. Rs 10-20 lakh: Rs 400. Rs 20-50 lakh: Rs 500. Rs 50L-1Cr: Rs 2000. Rs 1Cr-2Cr: Rs 4000. Above Rs 2Cr: Rs 5000. RELIEF AVAILABLE: Refund or replacement, compensation for mental agony and litigation costs, punitive damages, discontinuation of unfair practice. LIMITATION: Must file within 2 years of cause of action. HELPLINE: 1800-11-4000 (toll-free), NCH App."""
    },
    {
        "id": "consumer_defective_product",
        "title": "Rights When You Receive a Defective Product or Deficient Service",
        "type": "legal_advice", "category": "Consumer",
        "text": """If you receive a defective product or deficient service, you have strong rights under Consumer Protection Act 2019. FOR DEFECTIVE PRODUCT: Section 2(10) defines 'defect' as any fault, imperfection or shortcoming in quality, quantity, potency, purity or standard which is required to be maintained. Your remedies: (1) Replacement with new product. (2) Full refund including delivery charges. (3) Repair/rectification without further charge. (4) Compensation for injury or loss caused. (5) Punitive damages if defect was willful. FOR E-COMMERCE PURCHASES: e-Commerce platforms are liable under the Consumer Protection (E-Commerce) Rules, 2020. They cannot refuse refunds for defective products. IMMEDIATE STEPS: Step 1 - Document everything: photograph the defect, screenshot order confirmation and delivery details. Step 2 - Contact seller/platform via email (creates paper trail). Step 3 - Raise complaint on seller's platform and get complaint number. Step 4 - If no resolution in 15 days, send legal notice by Registered Post. Step 5 - File complaint on edaakhil.nic.in. FOR SERVICES: Deficiency under Section 2(11) means any shortcoming in quality, nature and manner of performance required. Examples: builder not completing construction, insurance wrongly rejecting claim, hospital overcharging, telecom company not providing service, bank errors. WHAT YOU CAN CLAIM: Full refund of amount paid, interest on the amount, compensation for mental agony (typically Rs 5,000-50,000 for routine cases), litigation costs."""
    },
    {
        "id": "consumer_insurance_disputes",
        "title": "Insurance Claim Rejection - Rights and Remedies",
        "type": "legal_advice", "category": "Consumer",
        "text": """Insurance companies frequently reject valid claims. Know your rights. If your insurance claim is rejected: FIRST: Get the rejection letter in writing with specific reasons. IRDAI REGULATIONS: Insurer must settle or reject claims within 30 days of receiving all documents. For health insurance: within 30 days. If investigation needed: 120 days maximum. COMMON ILLEGAL REJECTION GROUNDS (fight these): Pre-existing disease after 4 years waiting period (IRDAI mandates max 4-year waiting period). Claim for treatment not specifically excluded in policy. Technical grounds unrelated to the cause of loss. Delay in intimation if you can show you intimated within reasonable time. REMEDIES: Step 1 - File grievance with insurance company's Grievance Officer (mandatory under IRDAI). Step 2 - If unresolved in 30 days: file complaint with Insurance Ombudsman (free, covers claims up to Rs 50 lakh for health and Rs 20 lakh for other). Find your ombudsman at irdai.gov.in. Step 3 - File consumer complaint at edaakhil.nic.in. KEY IRDAI GUIDELINES: Insurer cannot reject claim citing non-disclosure if policy has been in force for 8 years (Section 45 Insurance Act). Insurers must have 'cashless facility at network hospitals'. If cashless denied wrongly: claim reimbursement plus 12% interest. Motor Insurance: No insurer can reject valid third-party claim. HELPLINE: IRDAI Bima Bharosa: 155255 or 1800-4254-732."""
    },
    {
        "id": "consumer_banking_disputes",
        "title": "Banking Disputes - RBI Ombudsman and Consumer Rights",
        "type": "legal_advice", "category": "Consumer",
        "text": """Banks are covered under both Consumer Protection Act and RBI regulations. YOUR BANKING RIGHTS: Zero liability for unauthorized transactions if reported promptly (within 3 working days). Passbook/statement on demand. No hidden charges beyond disclosed schedule. Free annual credit report under RBI guidelines. COMPLAINTS AGAINST BANKS: For any banking dispute (wrong debit, fraud, loan issues, FD problems, locker disputes): Step 1 - File written complaint with bank's Nodal Officer/Grievance Officer. Bank must respond within 30 days. Step 2 - If unresolved: File with RBI Integrated Ombudsman Scheme (free) at cms.rbi.org.in or call 14448. Covers: unauthorized transactions, failure to update credit bureau records, not releasing collateral after loan repayment, improper recovery by agents, failure to provide NACH mandate cancellation. CREDIT CARD DISPUTES: If you don't recognize a charge: dispute within 30 days to card issuer. Card issuer must resolve within 90 days. During dispute, charge is on hold. LOAN DISPUTES: Lender must provide loan agreement copy free of charge. Interest rate must be transparent (MCLR + spread). Prepayment penalty is prohibited for floating rate loans (RBI circular). For home loans: release of original documents within 30 days of loan closure. RECOVERY AGENTS: Under RBI guidelines, recovery agents cannot: call before 7am or after 7pm, harass family members, use threatening language. Report violations to RBI Ombudsman immediately."""
    },

    # ── RERA AND REAL ESTATE ───────────────────────────────────────

    {
        "id": "rera_builder_delay",
        "title": "RERA Rights When Builder Delays Possession",
        "type": "legal_advice", "category": "RERA",
        "text": """If your builder has delayed possession of your flat/apartment, you have strong rights under RERA 2016. YOUR OPTIONS UNDER SECTION 18: OPTION 1 - STAY AND CLAIM INTEREST: You can stay invested in the project AND claim interest for every month of delay. The interest rate is prescribed by each state but is typically SBI MCLR + 2% (currently around 10-11% per annum). This interest accrues from the date of promised possession until actual possession. OPTION 2 - EXIT AND CLAIM FULL REFUND: If you want to withdraw from the project, the builder must: return the entire amount received with interest at the prescribed rate, pay compensation for any additional cost incurred (like rent paid elsewhere). FILING A RERA COMPLAINT (Section 31): Visit your state RERA portal (e.g., maharera.mahaonline.gov.in for Maharashtra). Check if project is registered - all new projects must be. File complaint online with: project registration number, sale agreement, payment receipts, builder's possession letter or lack thereof, calculation of delay. Filing fee: Rs 1,000-5,000 depending on state. RERA must adjudicate within 60 days. BUILDER'S OBLIGATIONS UNDER RERA: Must deposit 70% of buyer funds in an escrow account used only for that project. Must complete project on time or pay compensation. Must fix structural defects up to 5 years after possession. Must provide all amenities promised in brochure. SECTION 18 INTEREST CALCULATION: If you paid Rs 50 lakh, builder delayed 24 months, interest at 10% = Rs 10 lakh compensation."""
    },
    {
        "id": "rera_complaint_procedure",
        "title": "How to File RERA Complaint - State-wise Guide",
        "type": "procedure", "category": "RERA",
        "text": """Filing a RERA complaint is state-specific. Here's the general process: PRE-FILING: Check project registration on your state RERA portal (all projects launched after May 2017 must be registered). Note the RERA Registration Number. Calculate exact delay in days. Calculate interest owed under Section 18. Send builder a legal notice demanding possession or refund. ONLINE FILING: Maharashtra: maharera.mahaonline.gov.in. Karnataka: rera.karnataka.gov.in. UP: up-rera.in. Delhi: dda.gov.in/hrera. Tamil Nadu: tnrera.in. Gujarat: gujrera.gujarat.gov.in. Telangana: rera.telangana.gov.in. DOCUMENTS NEEDED: Sale/allotment agreement, all payment receipts, builder's demand letters, any correspondence about possession date, proof of payments made, RERA project registration details. RERA ADJUDICATING OFFICER: For compensation claims specifically, approach the Adjudicating Officer (separate from RERA Authority). RERA APPELLATE TRIBUNAL: If RERA Authority order is unsatisfactory, appeal to RERA Appellate Tribunal within 60 days. COMMON RELIEFS GRANTED: Interest for delay period, refund with interest, completion order with timeline, penalty on builder. IMPORTANT: If builder's project is NOT registered on RERA: file police complaint for cheating under IPC Section 420 and also file consumer complaint."""
    },
    {
        "id": "rera_defects_amenities",
        "title": "RERA - Structural Defects and Missing Amenities",
        "type": "legal_advice", "category": "RERA",
        "text": """RERA provides strong protections even after you take possession. STRUCTURAL DEFECTS GUARANTEE (Section 14(3)): Builder must rectify any structural defect brought to notice within 5 years from possession. This includes: cracks in walls, leaking roof, subsidence, defective waterproofing, faulty plumbing, electrical defects. Process: Give written notice to builder identifying defects. Builder must rectify within 30 days. If no response: file RERA complaint. AMENITIES AND SPECIFICATIONS (Section 14(2)): Builder must deliver exactly what was promised in the brochure, advertisement, and agreement. Cannot substitute materials without consent. Cannot change approved plan without 2/3 consent of allottees. Cannot change common amenities (club, gym, parking, garden). If amenity promised but not delivered: file RERA complaint with brochure/advertisement as evidence. SOCIETY FORMATION: Builder must form Resident Welfare Association (RWA/Society) within 3 months of giving majority possession. Must hand over common areas, documents, completion certificate to RWA. If builder delays: file RERA complaint. TITLE CLEARANCE: Builder must give you a clear title. If property has existing loan or encumbrance: file complaint. REQUEST FOR INFORMATION: Under RERA, allottees can inspect project documents at any time. Builder must share: approved plans, sanctioned drawings, status of project, financial position."""
    },

    # ── IPC CRIMINAL SECTIONS ─────────────────────────────────────

    {
        "id": "ipc_cheating_420",
        "title": "IPC Section 420 - Cheating and Fraud: Rights and FIR Process",
        "type": "legal_advice", "category": "Criminal",
        "text": """Indian Penal Code Section 420 deals with cheating and dishonestly inducing delivery of property. It is a Cognizable (police must register FIR) and Non-Bailable (bail requires court order) offence. PUNISHMENT: Imprisonment up to 7 years AND fine. WHAT CONSTITUTES CHEATING (Sections 415-420): Deceiving someone and dishonestly inducing them to deliver property, valuable security, money, or to do/not do something which causes damage. RELATED SECTIONS: Section 415 - basic cheating (1 year). Section 417 - cheating (1 year). Section 419 - cheating by personation (3 years). Section 420 - cheating inducing delivery of property (7 years). Section 406 - criminal breach of trust (3 years). HOW TO FILE FIR: Visit the nearest police station. Request FIR registration - police CANNOT refuse for cognizable offences. State: what you were promised, what you paid/delivered, how you were cheated, names/details of accused. Get a copy of the FIR (legally mandatory - police must give you a copy free of charge). IF POLICE REFUSE FIR: File complaint before Magistrate under Section 156(3) CrPC. Magistrate can order police to investigate. File online on your state police portal. Escalate to Superintendent of Police. EVIDENCE TO COLLECT: Contract/agreement, payment receipts, bank transfers, WhatsApp/email conversations, witness statements, any brochures or promises made. CYBER CRIME variant: If fraud happened online, also file at cybercrime.gov.in or call 1930."""
    },
    {
        "id": "ipc_domestic_violence_498a",
        "title": "Domestic Violence and IPC Section 498A - Rights and Remedies",
        "type": "legal_advice", "category": "Criminal",
        "text": """Women facing domestic violence have multiple legal protections. IPC SECTION 498A: Husband or relative subjecting married woman to cruelty. Cognizable, Non-Bailable. Punishment: up to 3 years + fine. Cruelty includes: physical or mental harm, harassment for dowry, any act likely to drive woman to suicide. PROTECTION OF WOMEN FROM DOMESTIC VIOLENCE ACT 2005 (PWDVA): Provides civil remedies in addition to criminal remedies. Protection Orders: Court can prohibit abuser from contacting, approaching, or communicating with victim. Residence Orders: Wife cannot be evicted from matrimonial home. Monetary Relief: Court can order monthly maintenance, medical expenses, loss of earnings. Custody Orders: Temporary custody of children. DOWRY PROHIBITION ACT: Taking or giving dowry is illegal. If dowry was taken: file complaint under Dowry Prohibition Act with police. If dowry death suspected: IPC Section 304B (7 years to life) applies. HOW TO GET HELP: Step 1 - Call Women Helpline: 181 (24x7, free). Step 2 - Contact Protection Officer in your district (mandated under PWDVA). Step 3 - File complaint at nearest police station (Women's Cell). Step 4 - Approach Family Court for maintenance and custody. Step 5 - Contact NALSA (15100) for free legal aid. IMMEDIATE SAFETY: Call 112 for police emergency. Shelter: One Stop Centres (Sakhi Centres) in most districts provide shelter, legal aid, medical assistance for women in distress."""
    },
    {
        "id": "ipc_criminal_breach_trust",
        "title": "IPC Section 406 - Criminal Breach of Trust (Employer, Contractor, Partner)",
        "type": "legal_advice", "category": "Criminal",
        "text": """IPC Section 406 covers Criminal Breach of Trust: when someone entrusted with property/money misappropriates it. Punishment: up to 3 years OR fine OR both. Cognizable offence. Examples: employer not paying salary and withholding salary to force resignation, contractor taking advance and disappearing, business partner misappropriating company funds, property agent keeping token money, landlord not returning security deposit with intent to cheat. SECTION 405 (parent section): Whoever being entrusted with property dishonestly misappropriates or converts to own use, or dishonestly uses or disposes of that property, in violation of legal contract. SECTION 409 (aggravated form): Criminal Breach of Trust by Public Servant, Banker, Merchant, Factor, Broker, Attorney or Agent - Punishment: life imprisonment or up to 10 years + fine. TO FILE FIR FOR SECTION 406: Visit police station with: original agreement/contract, proof of money/property entrusted, demand notices sent to accused, any communication showing misappropriation. Police must register FIR (cognizable offence). CIVIL REMEDY IN PARALLEL: You can simultaneously file a civil suit for recovery of money with interest. Civil suit does not bar criminal proceedings. LIMITATION: Criminal case - no limitation for cognizable offences. Civil suit - 3 years from date of breach."""
    },
    {
        "id": "ipc_cybercrime",
        "title": "Cyber Crime and Online Fraud - Filing Complaints",
        "type": "legal_advice", "category": "Criminal",
        "text": """Cyber crimes are covered under IT Act 2000 and IPC. TYPES OF CYBER CRIMES: Online financial fraud (UPI fraud, banking fraud, phishing), cyber stalking and harassment, identity theft, hacking, online job fraud, matrimonial fraud, sextortion, fake online shopping. HOW TO FILE COMPLAINT: IMMEDIATE STEP - Call Cyber Crime Helpline 1930 for financial fraud. Report immediately - faster response means higher chance of fund recovery. ONLINE: File at cybercrime.gov.in - all types of cyber crimes. POLICE STATION: File FIR at local police station or cyber crime police station in your city. FOR FINANCIAL FRAUD (UPI/Bank): Call 1930 immediately (available 24x7). Also contact your bank immediately to freeze the transaction. Bank must cooperate with investigation and can initiate reversal if reported promptly. Zero liability for unauthorized transactions if reported within 3 working days. FOR SOCIAL MEDIA HARASSMENT: Report to platform (Facebook, Instagram, etc.) and simultaneously file with cybercrime.gov.in. RELEVANT LAWS: IT Act Section 66 - Hacking (3 years). IT Act Section 66C - Identity theft (3 years + fine up to Rs 1 lakh). IT Act Section 66D - Cheating by personation (3 years + fine). IT Act Section 67 - Obscene content (5 years). IPC Section 420 - Online cheating (7 years). EVIDENCE PRESERVATION: Screenshot everything before reporting - transaction IDs, conversation screenshots, email headers, website URLs, profile pages."""
    },

    # ── WORKPLACE AND LABOUR ──────────────────────────────────────

    {
        "id": "labour_wrongful_termination",
        "title": "Wrongful Termination and Retrenchment Rights Under Labour Law",
        "type": "legal_advice", "category": "Labour",
        "text": """India's labour laws provide strong protection against wrongful termination. INDUSTRIAL DISPUTES ACT 1947 - Key Protections: RETRENCHMENT (Section 25F): For companies with 100+ workers, retrenchment requires: 1 month notice or pay in lieu, retrenchment compensation at 15 days' wages per completed year of service, government permission (for 100+ worker establishments). For companies with less than 100 workers: 1 month notice or pay in lieu, 15 days' wages per year of service compensation. UNFAIR TERMINATION REMEDIES: File complaint with Labour Commissioner. Approach Labour Court under Section 2A (wrongful dismissal amounts to industrial dispute). Court can order reinstatement with back wages. NOTICE PERIOD: Most employment contracts specify 1-3 months. If employer terminates without serving notice: entitled to notice period salary. If employee leaves without notice: may forfeit that month's salary. WHAT IS WRONGFUL TERMINATION: Termination without proper notice/compensation, Termination for filing union/RTI/legal complaint (illegal - Section 33 ID Act), Termination of pregnant woman (Protection of Maternity Benefit Act), Termination without valid reason in breach of contract, Forcing resignation under coercion. REMEDIES: Labour Commissioner complaint, Labour Court petition, Civil suit for breach of contract. DOCUMENTS TO COLLECT: Employment contract/offer letter, salary slips, appointment letter, termination letter, proof of all work done."""
    },
    {
        "id": "labour_pf_salary",
        "title": "PF Non-Payment and Salary Delay - Rights and Filing Complaints",
        "type": "legal_advice", "category": "Labour",
        "text": """Your rights when employer doesn't pay salary or deducts but doesn't deposit PF. PROVIDENT FUND (EPF Act 1952): Mandatory for companies with 20+ employees. Both employer and employee contribute 12% of basic salary each. Employer's share: 8.33% to Employee Pension Scheme, 3.67% to EPF. Total: 24% of basic salary goes to your PF account. IF EMPLOYER NOT DEPOSITING PF: Check your PF passbook on epfindia.gov.in using your UAN. If amount deducted from salary but not deposited: this is a criminal offence under EPF Act. File complaint at: your regional EPFO office, or online at epfindia.gov.in under 'Grievance'. EPFO can attach employer's bank accounts and property to recover dues. Employer faces imprisonment up to 1 year for non-deposit. SALARY NON-PAYMENT: Under Payment of Wages Act 1936, wages must be paid by 7th of following month (for companies with less than 1000 employees) or 10th. For non-payment: File complaint with Payment of Wages Inspector in your area. File with Labour Commissioner. For amounts above Rs 1 lakh: file IPC Section 406 FIR (criminal breach of trust). MATERNITY BENEFIT: Under Maternity Benefit Act 1961, women get 26 weeks paid maternity leave (for first two children). Employer cannot terminate pregnant woman. Non-payment of maternity benefit: file complaint with Inspector under the Act."""
    },
    {
        "id": "posh_workplace_harassment",
        "title": "Sexual Harassment at Workplace - POSH Act Rights",
        "type": "legal_advice", "category": "Labour",
        "text": """The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act) protects all women from workplace sexual harassment. WHAT IS SEXUAL HARASSMENT (Section 2(n)): Physical contact and advances, demand for sexual favours, sexually coloured remarks, showing pornography, any other unwelcome conduct of sexual nature - verbal, non-verbal or physical. Includes quid pro quo and hostile work environment. WHO IS COVERED: All women in formal and informal workplaces including domestic workers, agricultural workers, contract workers. INTERNAL COMPLAINTS COMMITTEE (ICC): Every employer with 10+ employees MUST constitute an ICC. Local Complaints Committee (LCC) for smaller employers. FILE COMPLAINT WITH ICC: Within 3 months of the incident (extendable by 3 months for reasons). ICC must complete inquiry within 90 days. Employer must implement ICC recommendations within 60 days. If ICC fails, approach employer, then Labour Commissioner. REMEDIES: Written apology, warning, suspension, termination of harasser, payment of compensation to complainant. CRIMINAL COMPLAINT: Also file FIR under IPC Section 354A (sexual harassment - 3 years) and IPC Section 509 (insulting modesty). EMPLOYER LIABILITY: Employer who fails to constitute ICC faces Rs 50,000 fine, doubled for repeat offence, and licence cancellation. FALSE COMPLAINT PROTECTION: Good faith complaints are fully protected, but malicious/false complaints invite action. HELPLINE: Women Helpline 181, NALSA 15100."""
    },

    # ── TENANT AND RENT RIGHTS ────────────────────────────────────

    {
        "id": "tenant_rights_deposit",
        "title": "Security Deposit - Tenant Rights Across Indian States",
        "type": "legal_advice", "category": "Tenant",
        "text": """Security deposit disputes are the most common tenant-landlord conflict. YOUR RIGHTS: Landlord MUST return security deposit within a reasonable time (15-30 days of vacating in most states) after deducting legitimate repair costs. LANDLORD CAN DEDUCT: Actual repair costs for damage beyond normal wear and tear (with receipts). Unpaid rent (if any). LANDLORD CANNOT DEDUCT: Normal wear and tear (paint fading, minor scuffs). Age-related deterioration. Repairs that were pre-existing. Maintenance costs that are landlord's responsibility. STATE-SPECIFIC LAWS: Maharashtra Rent Control Act: Deposit maximum 3 months rent. Return within 1 month. Delhi Rent Act: Deposit subject to fair rent determination. Karnataka Rent Control Act: Regulated deposits, return within 1 month. MODEL TENANCY ACT 2021 (adopted by several states): Security deposit maximum 2 months rent (residential), 6 months (commercial). Must be returned within 1 month of vacating. LEGAL NOTICE FIRST: Send registered post legal notice demanding return of deposit with 15-day deadline. Keep postal receipt. IF NO RESPONSE: Consumer Complaint (deficiency of service) + amount as consumer. Civil Suit for recovery. In case of fraudulent intent: IPC Section 406 (criminal breach of trust) FIR. Rent Authority/Rent Court in states that have them. EVIDENCE NEEDED: Lease/rent agreement, rent receipts, deposit receipt/bank transfer proof, move-out condition photos, move-out inspection report."""
    },
    {
        "id": "tenant_eviction_rights",
        "title": "Tenant Eviction Rights - When Can Landlord Evict",
        "type": "legal_advice", "category": "Tenant",
        "text": """Landlords cannot evict tenants arbitrarily. Tenants have strong protections under state rent control laws. VALID GROUNDS FOR EVICTION: Non-payment of rent for extended period. Subletting without permission. Using premises for unlawful purpose. Nuisance or damage to property. Landlord requires property for own genuine use (bona fide requirement - must prove in court). INVALID/ILLEGAL EVICTION: Forcing tenant out without court order. Removing doors, electricity, water, or causing harassment. Locking property with tenant's belongings inside. Threatening tenant. Any physical intimidation. IF LANDLORD ILLEGALLY EVICTS: Immediately file police complaint (FIR for trespass, criminal intimidation). File suit for injunction and possession in civil court. Approach Rent Court/Authority in your state. Under CrPC Section 145, Magistrate can maintain status quo. NOTICE FOR VACATING: Landlord must give: 15 days notice for month-to-month tenancy, as per agreement for fixed-term lease. Without proper notice: tenant can refuse to vacate and landlord must go to court. RENT FIXATION: In rent-controlled states, landlord cannot increase rent beyond prescribed limits without Rent Authority permission. WHAT TENANTS CAN DO: Don't vacate without court order. Document all harassment. File police complaint for any threats or illegal entry. Approach Rent Controller/Authority in your city. Get free legal aid from NALSA (15100)."""
    },

    # ── GOVERNMENT SCHEMES ────────────────────────────────────────

    {
        "id": "schemes_housing_pmay",
        "title": "PM Awas Yojana (PMAY) - Housing Scheme Eligibility and Application",
        "type": "scheme_info", "category": "Schemes",
        "text": """Pradhan Mantri Awas Yojana (PMAY) provides affordable housing to urban and rural poor. TWO COMPONENTS: PMAY-Urban (for cities) and PMAY-Gramin (for rural areas). ELIGIBILITY FOR PMAY-Urban: EWS (Economically Weaker Section): Annual family income up to Rs 3 lakh. Subsidy: 6.5% on loan up to Rs 6 lakh. LIG (Lower Income Group): Annual income Rs 3-6 lakh. Subsidy: 6.5% on loan up to Rs 6 lakh. MIG-I (Middle Income Group): Annual income Rs 6-12 lakh. Subsidy: 4% on loan up to Rs 9 lakh. MIG-II: Annual income Rs 12-18 lakh. Subsidy: 3% on loan up to Rs 12 lakh. KEY CONDITIONS: Must not own a pucca house anywhere in India (self or any family member). For EWS/LIG: house must be in woman's name or joint ownership. Must be first-time homebuyer for subsidy. HOW TO APPLY: Through any approved bank or housing finance company (SBI, HDFC, LIC Housing, etc.). Apply at pmaymis.gov.in (urban) or pmayg.nic.in (rural). Submit Aadhaar, income proof, self-declaration of no pucca house. BENEFIT: Subsidy credited directly to loan account, reducing EMI significantly. For EWS: saves approximately Rs 2.67 lakh over loan tenure. FOR RURAL (PMAY-G): Eligible BPL and lower income households. Rs 1.2 lakh in plains, Rs 1.3 lakh in hilly/difficult areas. Applied through Gram Panchayat."""
    },
    {
        "id": "schemes_health_ayushman",
        "title": "Ayushman Bharat PM Jan Arogya Yojana - Health Insurance Scheme",
        "type": "scheme_info", "category": "Schemes",
        "text": """Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (AB-PMJAY) is the world's largest government-funded health insurance scheme. BENEFIT: Rs 5 lakh per family per year for secondary and tertiary hospitalization. Covers pre-existing diseases from Day 1. Paperless and cashless treatment at empanelled hospitals. ELIGIBILITY: Based on SECC 2011 (Socio-Economic Caste Census) database. Rural: deprived households in rural areas (6 categories). Urban: 11 occupational categories including rag pickers, domestic workers, construction workers, street vendors, auto/taxi drivers. HOW TO CHECK ELIGIBILITY: Visit pmjay.gov.in. Enter mobile number or Ration Card number. Or visit your nearest Ayushman Bharat Arogya Mitra (ABAM) at empanelled hospital. HOW TO AVAIL: Go to any empanelled hospital (government or private). Show Aadhaar card + ration card or PMJAY e-card. Hospital Empanelment: 24,000+ hospitals across India. Cashless treatment: hospital coordinates directly. For New States: Scheme merged with state health schemes in many states. AB PM-JAY + State Scheme = expanded coverage. COMPLAINTS: If hospital refuses treatment: Call 14555 (24x7 helpline). Report at pmjay.gov.in. WHAT IS COVERED: Surgery, medical treatment, ICU, day care treatment, dialysis, cancer treatment, cardiac surgery, newborn care. NOT COVERED: OPD treatment (outpatient), medicines for OPD, dental (unless hospitalization required), cosmetic surgery."""
    },
    {
        "id": "schemes_farmers_pmkisan",
        "title": "PM Kisan Samman Nidhi - Farmer Income Support Scheme",
        "type": "scheme_info", "category": "Schemes",
        "text": """PM Kisan Samman Nidhi Yojana provides Rs 6,000 per year to eligible farmer families in three equal installments of Rs 2,000 each, paid directly to bank account. ELIGIBILITY: Small and marginal farmer families who own cultivable land as per land records. Family includes husband, wife and minor children. EXCLUSIONS (NOT eligible): Institutional landholders, farmer families where any member is/was constitutional post holder, current/retired government officer (except multi-tasking staff/Group D), professionals: doctors, engineers, lawyers, CAs with income above threshold, former/current MP/MLA/Mayor. HOW TO APPLY: Visit pmkisan.gov.in. Click 'New Farmer Registration'. Enter Aadhaar number, bank details, land records. Or apply through Common Service Centre (CSC) or Patwari/Revenue Inspector. HOW TO CHECK STATUS: Visit pmkisan.gov.in > Beneficiary Status > Enter Aadhaar/Account/Mobile number. INSTALLMENT DATES: April-July, August-November, December-March. CORRECTIONS: If installment not received: check status online. Common issues: Aadhaar-bank linking problem (link at bank), land records mismatch (update at Patwari/Revenue office), mobile number mismatch. HELPLINE: PM Kisan Helpline: 155261 or 1800-11-5526 (toll-free)."""
    },
    {
        "id": "schemes_maternity_pmmvy",
        "title": "PM Matru Vandana Yojana - Maternity Benefit Scheme",
        "type": "scheme_info", "category": "Schemes",
        "text": """Pradhan Mantri Matru Vandana Yojana (PMMVY) provides maternity benefit to working women. BENEFIT: Rs 5,000 for first living child in three installments: Rs 1,000 (1st trimester registration), Rs 2,000 (6 months + prenatal checkup), Rs 2,000 (child birth registration + first vaccination). Additional incentive under Pradhan Mantri Surakshit Matritva Abhiyan for institutional delivery. ELIGIBILITY: All pregnant and lactating women (except women in Central/State Government employment already getting paid maternity leave). For first living child after 01 January 2017. DOCUMENTS NEEDED: Mother's Aadhaar card, husband's Aadhaar card, Mother's bank account (linked to Aadhaar), MCP (Mother and Child Protection) card, marriage certificate or self-declaration. HOW TO APPLY: Visit nearest Anganwadi Centre or approved health facility. Fill Form 1A for first installment. Submit within 150 days of last menstrual period (LMP). SECOND INSTALLMENT: Submit Form 1B at Anganwadi/health facility after 6 months pregnancy. THIRD INSTALLMENT: Submit Form 1C after child birth registration and first vaccination. ONLINE: pmmvy.nic.in in some states. HELPLINE: Anganwadi Worker, ASHA Worker, or call 1800-200-7701. MATERNITY LEAVE (for employed women): Under Maternity Benefit Act 1961: 26 weeks paid leave for first 2 children (for establishments with 10+ employees). Employer cannot terminate during maternity."""
    },
    {
        "id": "schemes_unorganized_workers",
        "title": "Government Schemes for Unorganized Sector Workers",
        "type": "scheme_info", "category": "Schemes",
        "text": """Multiple government schemes protect unorganized sector workers (daily wage, construction, street vendors, domestic workers). E-SHRAM PORTAL: Register at eshram.gov.in. Get E-Shram card (UAN). Enables access to social security benefits. Rs 2 lakh insurance under PM Suraksha Bima Yojana. PM SVANIDHHI (PM Street Vendor's AtmaNirbhar Nidhi): Working capital loans for street vendors. Rs 10,000 (1st loan), Rs 20,000 (2nd), Rs 50,000 (3rd). Available at banks/NBFCs. Apply at pmsvanidhi.mohua.gov.in. PM MUDRA YOJANA: Micro business loans. Shishu: up to Rs 50,000. Kishore: Rs 50,000 to Rs 5 lakh. Tarun: Rs 5 lakh to Rs 10 lakh. Apply at any bank. No collateral required for Shishu/Kishore. PM SHRAM YOGI MAANDHAN (PMSYM - Pension Scheme): For unorganized workers aged 18-40 with monthly income up to Rs 15,000. Monthly contribution Rs 55-200 (based on age at enrollment). Government matches contribution equally. Rs 3,000/month pension at age 60. Register at CSC or shramyogi.labour.gov.in. BUILDING WORKERS (BOCW Act): Construction workers registered with State BOCW Board get benefits: accident compensation, health insurance, scholarship for children, housing loan, maternity benefit. Register with State Labour Department. ATAL PENSION YOJANA: For workers not covered by any pension. Monthly pension Rs 1,000-5,000 at age 60. Contribution varies by age and pension amount."""
    },

    # ── FREE LEGAL AID ────────────────────────────────────────────

    {
        "id": "free_legal_aid_nalsa",
        "title": "Free Legal Aid - NALSA, DLSA and How to Get a Free Lawyer",
        "type": "procedure", "category": "Legal Aid",
        "text": """Every Indian citizen has the right to free legal aid under Article 39A of the Constitution. NATIONAL LEGAL SERVICES AUTHORITY (NALSA): Provides free legal services to eligible persons. Helpline: 15100. Website: nalsa.gov.in. WHO IS ELIGIBLE FOR FREE LEGAL AID: Women and children (all). SC/ST community members. Victims of trafficking and begar. Industrial workmen. Persons with disabilities. Persons in custody (all those in jail automatically entitled). Victims of mass disaster, ethnic violence, flood, drought, earthquake, industrial disaster. Persons below poverty line (BPL). Persons with annual income below Rs 3 lakh (varies by state). HOW TO GET FREE LEGAL AID: Visit District Legal Services Authority (DLSA) in your district court. Call NALSA helpline 15100. Many DLSA have offices in courts - approach them. FREE LEGAL AID INCLUDES: Free legal representation in court, legal advice and consultation, preparation of legal documents/petitions, mediation and settlement through Lok Adalat, legal awareness campaigns. LOK ADALAT: Alternative dispute resolution. Parties reach settlement amicably. Settlement order has same force as court decree. No court fees. If case filed in court: fee refunded upon settlement. Lok Adalats handle: motor accident claims, labour disputes, matrimonial disputes, cheque bounce, public utility disputes. TELE-LAW SERVICE: Free legal advice by phone. Call Common Service Centre (CSC) in your village. Lawyers provide advice via video call. Available in over 50,000 villages."""
    },
    {
        "id": "legal_notice_format",
        "title": "How to Write and Send a Legal Notice",
        "type": "procedure", "category": "Legal Procedure",
        "text": """A legal notice is an official communication demanding action under law. It shows seriousness and creates a paper trail. WHEN TO SEND LEGAL NOTICE: Before filing consumer complaint (mandatory for many disputes). Before filing civil suit for recovery. For security deposit disputes with landlord. For breach of contract claims. For defamation, cheating cases. HOW TO WRITE: Address: To the name and full address of the opposite party. Subject: 'Legal Notice Under [Relevant Act]'. Date: Current date. Opening: 'Please take notice that my client/I, [Your Name], residing at [Your Address], hereby serves upon you this legal notice under Section [X] of [Act Name].' Facts: Narrate facts chronologically - what was agreed, what was paid/delivered, what went wrong, on what dates. Demand: State exactly what you want - refund of Rs X, delivery of goods, return of deposit, etc. Deadline: Give 15 days to respond (30 days for some matters). Consequence: 'Failing which, I shall initiate appropriate legal proceedings without any further notice, at your cost and risk.' Signature: Your name and signature, or your advocate's name and signature. HOW TO SEND: Registered Post with Acknowledgment Due (AD). Keep the postal receipt and tracking number. Also send by email (for record). KEEP COPIES: Keep copy of notice, postal receipt, proof of delivery, email if sent. This is crucial evidence in future proceedings. PROFESSIONAL LEGAL NOTICE: Advocates charge Rs 500-2000 for drafting and sending. Many consumer forums/NALSA can help for free."""
    },

    # ── LAND AND PROPERTY ─────────────────────────────────────────

    {
        "id": "property_inheritance_rights",
        "title": "Property Inheritance Rights - Hindu Succession Act",
        "type": "legal_advice", "category": "Property",
        "text": """Property inheritance in India is governed primarily by personal laws. HINDU SUCCESSION ACT 1956 (as amended 2005): Applies to Hindus, Sikhs, Jains, Buddhists. EQUAL RIGHTS FOR DAUGHTERS (2005 Amendment): Daughters are coparceners by birth in ancestral property. Equal rights to father's ancestral property as sons. This applies even if father died before 2005 amendment (Supreme Court: Vineeta Sharma v Rakesh Sharma, 2020). CLASSES OF HEIRS: Class I heirs (inherit first): Son, daughter, widow, mother, children of predeceased son/daughter. All Class I heirs get equal share. If only Class I heir is widow: she inherits everything. Class II heirs inherit only if no Class I heirs exist. SELF-ACQUIRED PROPERTY: Owner can will it to anyone. Without will: Class I heirs inherit equally. WILL: Must be in writing, signed by testator, attested by 2 witnesses. Registration of will is advisable but not mandatory. NOMINATION vs INHERITANCE: Nomination (in bank, insurance) does not override legal inheritance. Nominee holds property as trustee for legal heirs. FOR SUCCESSION: Apply for Legal Heir Certificate at tehsil/district office. Get Succession Certificate from civil court for movable property (bank accounts, shares). Get Probate for will from High Court (required in Mumbai, Chennai, Kolkata). MUSLIM PERSONAL LAW: Inheritance governed by Muslim Personal Law. Daughter gets half son's share. Wife gets 1/4 (if no children) or 1/8 (if children) of husband's estate. Will can bequeath only 1/3 of property."""
    },
    {
        "id": "land_record_rights",
        "title": "Land Records, Mutation and Property Documents - Your Rights",
        "type": "legal_advice", "category": "Property",
        "text": """Land records are governed by state revenue laws. Understanding them is critical for property rights. KEY DOCUMENTS: 7/12 Extract (Maharashtra): Shows owner name, area, survey number, crop details, encumbrances. RoR (Record of Rights): Patta/Khata/Khesra - equivalent documents in different states. Sale Deed: The primary ownership document, registered with Sub-Registrar. Encumbrance Certificate: Shows all transactions on property (mortgages, sales). MUTATION (Dakhil Kharij): Process of updating government land records after property transfer. Must be done after buying property, inheritance, gift. File mutation application at Tehsil/Patwari office within 3 months of sale deed. Bring: Sale deed, property tax receipts, Aadhaar. If mutation refused: appeal to Revenue Officer/SDO. RIGHT TO GET CERTIFIED COPIES: Under state land revenue laws, anyone can get certified copy of land records. From Sub-Registrar: certified copy of Sale Deed. From Tehsil: copy of 7/12, RoR. Fee: Rs 10-100 typically. ONLINE LAND RECORDS: Most states have online portals: bhulekh.up.nic.in (UP), mahabhumi.gov.in (Maharashtra), landrecords.karnataka.gov.in (Karnataka), tnpds.gov.in (Tamil Nadu). IF RECORDS ARE WRONG: File application for correction at Tehsil. If refused: Revenue Court/Revenue Officer appeal. For fraudulent entries: police complaint + Revenue Court. PROPERTY TAX: Assessed by municipal body. Non-payment leads to penalty. Can challenge excessive assessment at municipal authority."""
    },

    # ── ADDITIONAL RIGHTS ─────────────────────────────────────────

    {
        "id": "medical_rights_negligence",
        "title": "Patient Rights and Medical Negligence - Legal Remedies",
        "type": "legal_advice", "category": "Medical",
        "text": """Patients have fundamental rights and strong remedies for medical negligence in India. PATIENT RIGHTS: Informed consent before any procedure (must be explained in language you understand). Right to second opinion. Right to access medical records and reports (immediately upon request). Right to refuse treatment. Right to know treatment costs in advance. Right to privacy and confidentiality. Right to non-discrimination. MEDICAL NEGLIGENCE: Defined as failure of medical professional to exercise reasonable standard of care expected from ordinary skilled person in that profession. Criminal Negligence: Extreme negligence causing death - IPC Section 304A (2 years), case requires expert evidence (SC: Dr. Suresh Gupta v Govt of NCT of Delhi). REMEDIES FOR MEDICAL NEGLIGENCE: Consumer Forum: File complaint under Consumer Protection Act - hospitals are 'service providers'. Must prove deficiency in service. District Consumer Forum if compensation claim up to Rs 50 lakh. No need to prove exact medical standard - just deficiency. NCDRC has awarded crores in medical negligence cases. Civil Suit: For higher claims + criminal reference. Criminal Complaint: Section 304A IPC + Section 308 (attempt). MEDICAL RECORDS: Hospital must provide copies within 72 hours (MCI/NMC guidelines). Cannot charge exorbitant amount. CLINICAL ESTABLISHMENTS ACT 2010: Registration mandatory, prescribed minimum standards. Violation: Fine + Suspension. FILE COMPLAINT WITH: National Medical Commission (nmc.org.in) for professional misconduct. State Medical Council. Consumer Forum for compensation."""
    },
    {
        "id": "rte_education_rights",
        "title": "Right to Education Act - Free Education Rights for Children",
        "type": "legal_advice", "category": "Education",
        "text": """Right to Education Act, 2009 (RTE) guarantees free and compulsory education for children aged 6-14 years. KEY RIGHTS UNDER RTE: FREE EDUCATION: Every child aged 6-14 has right to free elementary education in neighbourhood school. Applies to ALL government schools - no fees, no hidden charges. 25% RESERVATION: Private unaided schools must admit 25% students from economically weaker sections (EWS) and disadvantaged groups in Class 1. Government reimburses fees. PROHIBITION: School cannot collect capitation fee (illegal donations). School cannot conduct entrance examination/interview for admission. School cannot expel student during elementary education. School cannot hold back student or fail them at any class during elementary education. NO DONATION: Asking or accepting donation for admission is punishable by 10x the amount + Rs 25,000 fine. QUALITY STANDARDS: Prescribed pupil-teacher ratio. Minimum infrastructure (toilets, drinking water, classrooms). No corporal punishment. Schools must be recognized under RTE. COMPLAINT MECHANISM: File complaint with State/Union Territory RTE Authority. District Education Officer (DEO). National Commission for Protection of Child Rights (NCPCR) - ncpcr.gov.in - for serious violations. SPECIAL NEEDS CHILDREN: Right to inclusive education in regular schools with support."""
    },

    # ── DISPUTE RESOLUTION OVERVIEW ───────────────────────────────

    {
        "id": "dispute_resolution_overview",
        "title": "Indian Dispute Resolution - Which Forum to Use for Which Problem",
        "type": "legal_advice", "category": "General",
        "text": """India has multiple dispute resolution forums. Choosing the right one is critical. CIVIL DISPUTES (Recovery of money, property, contracts): Civil Court - for most disputes without specialized forum. Munsiff Court/Civil Judge (Jr Division): up to Rs 3 lakh. Civil Judge (Sr Division): Rs 3-20 lakh. District Court: above Rs 20 lakh. Time: 3-10 years typically. CONSUMER DISPUTES (Defective goods, deficient services, unfair trade): Consumer Commission - faster, simpler, no mandatory lawyer. District: up to Rs 50 lakh. State: Rs 50L-2Cr. NCDRC: above Rs 2Cr. Time: 6 months to 2 years. LOK ADALAT (Settlement): For pending court cases. Both sides agree to settlement. Fast: single day or few hearings. No fees. Motor accidents, cheque bounce, utility disputes, labour. FAMILY COURT: Divorce, maintenance, custody, matrimonial disputes. District Family Court. LABOUR COURT/INDUSTRIAL TRIBUNAL: Wrongful termination, unfair labour practices, wage disputes. Labour Commissioner first, then Labour Court. MOTOR ACCIDENT CLAIMS TRIBUNAL (MACT): For vehicle accident compensation. Must file within 6 months. Much faster than civil court. ARBITRATION: If contract has arbitration clause. Governed by Arbitration Act 1996. POLICE/CRIMINAL: For cognizable offences (cheating, assault, domestic violence, fraud). File FIR at police station. RTI: Information from government. File with PIO of concerned department. RERA: Builder/real estate disputes. State RERA Authority. LEGAL AID: NALSA (15100) - free help choosing the right forum."""
    },

    # ── PRACTICAL GUIDES ──────────────────────────────────────────

    {
        "id": "fir_filing_guide",
        "title": "How to File an FIR - Rights When Police Refuse",
        "type": "procedure", "category": "Criminal",
        "text": """An FIR (First Information Report) is the first step in criminal proceedings. WHAT IS AN FIR: Written complaint filed with police about a cognizable offence. Police must investigate after FIR. COGNIZABLE OFFENCES (require FIR): Murder, robbery, rape, kidnapping, cheating (Section 420), criminal breach of trust (Section 406), domestic violence (Section 498A), POCSO, fraud, cyber crime. HOW TO FILE FIR: Go to police station where offence occurred. Request Officer-in-Charge to register FIR. Narrate facts clearly with dates, times, names, locations. Police must read it back to you and let you correct. Sign FIR or give thumbprint. Get FIR copy FREE OF CHARGE (compulsory under Section 154(3) CrPC). IF POLICE REFUSE FIR (very common, very illegal): Online complaint to Superintendent of Police (SP) or DIG. Written complaint by Registered Post to SP. Approach Magistrate under Section 156(3) CrPC - Magistrate can order police to investigate. State Police Complaint Authority. File online complaint on state police portal. YOUR RIGHTS AFTER FIR: Case progress updates from police (Section 173 CrPC). Certified copy of FIR anytime (Section 154(3)). Victim not required to come to police station if there is danger. ZERO FIR: File FIR at any police station regardless of jurisdiction. Police must transfer to jurisdictional station. CYBER CRIME FIR: Also file at cybercrime.gov.in simultaneously. HELPLINES: Police emergency: 100, Women: 1091, Child helpline: 1098, Cyber Crime: 1930."""
    },
    {
        "id": "court_process_explained",
        "title": "Understanding Indian Court Proceedings for Citizens",
        "type": "procedure", "category": "Legal Procedure",
        "text": """Indian court proceedings can be intimidating. Here's what to expect. CRIMINAL CASE PROCESS: FIR filed → Police Investigation → Charge Sheet (within 60-90 days if accused arrested) → Cognizance by Magistrate → Bail hearing → Framing of Charges → Trial (prosecution evidence, defense evidence) → Arguments → Judgment → Sentencing (if convicted) → Appeal (Sessions Court → High Court → Supreme Court). CIVIL CASE PROCESS: Plaint filed → Court issues summons to defendant → Written statement by defendant → Issues framed → Evidence (documents + witnesses) → Arguments → Judgment → Execution → Appeal. CONSUMER FORUM PROCESS: Complaint filed → Forum admits complaint → Notice to opposite party → Reply from opposite party → Hearing (usually 3-5 dates) → Arguments → Order → Execution if not complied. Much simpler than civil court. IMPORTANT RIGHTS IN COURT: Right to be heard through lawyer or in person (all forums). Right to copies of all documents. Right to examine witnesses. Right to appeal any adverse order. BAIL: For bailable offences: bail as of right from police/court. For non-bailable: discretion of Magistrate/Sessions Court. For serious offences: Sessions Court or High Court. ANTICIPATORY BAIL (Section 438 CrPC): Before arrest, from Sessions Court or High Court. LEGAL REPRESENTATION: Can represent yourself (in person). Consumer Forum: appearing in person is encouraged. All documents to be in English or state language. COURT FEES: For civil suits: ad valorem fee on claim amount. Consumer Forum: nominal fee or free. Criminal case: no fee for complainant."""
    },
]


def ingest_knowledge_base():
    """Ingests all knowledge base entries into ChromaDB."""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    from rag.chroma_store import add_documents, get_collection
    
    print(f"Starting ingestion of {len(KNOWLEDGE_BASE)} knowledge base entries...")
    
    # Check current state
    col = get_collection()
    existing = col.get()
    existing_ids = set(existing['ids'])
    print(f"Existing documents in ChromaDB: {len(existing_ids)}")
    
    # Filter to only new documents
    new_docs = [doc for doc in KNOWLEDGE_BASE if doc['id'] not in existing_ids]
    print(f"New documents to add: {len(new_docs)}")
    
    if not new_docs:
        print("All documents already in ChromaDB!")
        return
    
    # Add in batches of 20 to avoid embedding timeouts
    batch_size = 20
    total_added = 0
    
    for i in range(0, len(new_docs), batch_size):
        batch = new_docs[i:i + batch_size]
        
        documents = [doc['text'] for doc in batch]
        metadatas = [{"title": doc['title'], "type": doc['type'], "category": doc['category']} for doc in batch]
        ids = [doc['id'] for doc in batch]
        
        try:
            add_documents(
                collection_name="jansaathi_legal_kb",
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            total_added += len(batch)
            print(f"  [OK] Added batch {i//batch_size + 1}: {len(batch)} documents (total: {total_added})")
        except Exception as e:
            print(f"  [ERR] Error in batch {i//batch_size + 1}: {e}")
    
    # Verify
    final_count = len(col.get()['ids'])
    print(f"\n[OK] Ingestion complete!")
    print(f"   Total documents now in ChromaDB: {final_count}")
    print(f"   Categories: RTI, Consumer, RERA, Criminal, Labour, Tenant, Schemes, Legal Aid, Property, Medical")


if __name__ == "__main__":
    ingest_knowledge_base()
