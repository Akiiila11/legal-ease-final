#templates/prompts.py
"""
prompts.py
-----------
Prompt templates used to instruct the Generative AI model (Google Gemini)
to produce structured, clause-by-clause legal document content.
 
Each function returns a single prompt string built from user-supplied
fields. The model is instructed to return clean, section-labelled text
so the downstream document builder (doc_generator.py) can format it
consistently into PDF / DOCX / TXT.
"""
 
from datetime import date
 
 
def employment_contract_prompt(data: dict) -> str:
    """Scenario 1: Startup founder hiring a new employee."""
    return f"""
You are a contract-drafting assistant. Draft a professional, legally
sound EMPLOYMENT CONTRACT using the details below. Use clear section
headings (numbered) and formal legal language. Do not include any
commentary, only the contract text.
 
Company Name: {data['company_name']}
Employee Name: {data['employee_name']}
Job Title / Role: {data['job_title']}
Start Date: {data['start_date']}
Compensation: {data['compensation']}
Work Location: {data.get('work_location', 'Remote')}
Employment Type: {data.get('employment_type', 'Full-time')}
 
Include the following numbered sections:
1. Parties and Effective Date
2. Position and Duties
3. Compensation and Benefits
4. Working Hours and Location
5. Confidentiality
6. Intellectual Property Assignment
7. Termination Conditions
8. Governing Law
9. Signatures block (with blank lines for both parties)
 
Today's date for reference: {date.today().isoformat()}.
"""
 
 
def nda_prompt(data: dict) -> str:
    """Scenario 2: Freelancer needing an NDA for a client."""
    return f"""
You are a contract-drafting assistant. Draft a professional, legally
sound NON-DISCLOSURE AGREEMENT (NDA) using the details below. Use clear
numbered section headings and formal legal language. Do not include any
commentary, only the agreement text.
 
Disclosing Party: {data['disclosing_party']}
Receiving Party: {data['receiving_party']}
Purpose of Disclosure: {data['purpose']}
Scope of Confidential Information: {data['scope']}
Effective Date: {data['effective_date']}
Term / Duration: {data.get('term', '2 years from the Effective Date')}
 
Include the following numbered sections:
1. Parties and Effective Date
2. Definition of Confidential Information
3. Obligations of the Receiving Party
4. Exclusions from Confidential Information
5. Term and Termination
6. Remedies for Breach
7. Governing Law
8. Signatures block (with blank lines for both parties)
 
Today's date for reference: {date.today().isoformat()}.
"""
 
 
def lease_agreement_prompt(data: dict) -> str:
    """Scenario 3: Landlord drafting a residential lease."""
    security_deposit = data.get("security_deposit", "One month's rent")

    return f"""
You are a contract-drafting assistant. Draft a professional, legally
sound RESIDENTIAL LEASE AGREEMENT using the details below. Use clear
numbered section headings and formal legal language. Do not include
any commentary, only the agreement text.
 
Landlord Name: {data['landlord_name']}
Tenant Name: {data['tenant_name']}
Property Address: {data['property_address']}
Lease Start Date: {data['lease_start']}
Lease End Date: {data['lease_end']}
Monthly Rent: {data['monthly_rent']}
Security Deposit: {security_deposit}
 
Include the following numbered sections:
1. Parties and Property
2. Lease Term
3. Rent and Payment Terms
4. Security Deposit
5. Use of Premises
6. Maintenance and Repairs
7. Termination and Renewal
8. Governing Law
9. Signatures block (with blank lines for both parties)
 
Today's date for reference: {date.today().isoformat()}.
"""
 
 
PROMPT_BUILDERS = {
    "employment_contract": employment_contract_prompt,
    "nda": nda_prompt,
    "lease_agreement": lease_agreement_prompt,
}
