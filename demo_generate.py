#demo_generate.py
"""
demo_generate.py
------------------
Offline demo runner. Uses realistic *sample* AI-drafted text (the same
shape Gemini returns for the prompts in templates/prompts.py) and feeds
it through the REAL doc_generator.py pipeline, so the .docx/.txt files
this produces are byte-for-byte what the running app would create for
that AI output. Lets the whole pipeline be demonstrated without a live
API key.
"""
 
import os
from doc_generator import build_docx, build_txt
 
SAMPLE_TEXTS = {
    "employment_contract":,
 
    "nda":,
 
    "lease_agreement":,
}
 
SAMPLE_DATA = {
    "employment_contract": {
        "company_name": , "employee_name": ,
        "job_title": , "start_date": ,
        "compensation":, "work_location": ",
        "employment_type": ,
    },
    "nda": {
        "disclosing_party":, "receiving_party": ,
        "purpose":, "scope": "Design specs, pricing, client materials",
        "effective_date": , "term":,
    },
    "lease_agreement": {
        "landlord_name": , "tenant_name": ,
        "property_address": ,
        "lease_start": , "lease_end": ,


         "monthly_rent": , "security_deposit": ,
    },
}
 
if __name__ == "__main__":
    os.makedirs("generated_docs", exist_ok=True)
    for doc_type, text in SAMPLE_TEXTS.items():
        data = SAMPLE_DATA[doc_type]
        docx_path = build_docx(doc_type, data, text, f"sample_{doc_type}")
        txt_path = build_txt(doc_type, text, f"sample_{doc_type}")
        print(f"[OK] {doc_type}: {docx_path}, {txt_path}")
 
