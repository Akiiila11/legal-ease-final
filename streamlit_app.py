"""LegalEase single-service Streamlit application."""

import uuid
from pathlib import Path

import streamlit as st

from ai_core import generate_legal_text
from doc_generator import OUTPUT_DIR, generate_all_formats
from templates.prompts import PROMPT_BUILDERS


st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="centered")


def generate_document(doc_type: str, data: dict, logo=None) -> dict:
    """Generate the document locally in this Streamlit service."""
    logo_path = None

    if logo is not None:
        extension = Path(logo.name).suffix.lower()
        if extension not in {".png", ".jpg", ".jpeg"}:
            raise ValueError("Logo must be a PNG or JPEG image.")

        logo_path = Path(OUTPUT_DIR) / f"logo_{uuid.uuid4().hex[:10]}{extension}"
        logo_path.write_bytes(logo.getvalue())

    prompt = PROMPT_BUILDERS[doc_type](data)
    preview_text = generate_legal_text(prompt)
    filename = f"{doc_type}_{uuid.uuid4().hex[:10]}"
    output_paths = generate_all_formats(
        doc_type, data, preview_text, filename, str(logo_path) if logo_path else None
    )

    return {
        "preview_text": preview_text,
        "files": {
            file_format: Path(file_path).read_bytes()
            for file_format, file_path in output_paths.items()
        },
        "filename": filename,
    }


def submit_generation(doc_type: str, data: dict, logo=None) -> None:
    try:
        with st.spinner("Generating your document..."):
            st.session_state["result"] = generate_document(doc_type, data, logo)
    except (RuntimeError, ValueError, OSError) as error:
        st.session_state["result"] = {"error": str(error)}


st.title("⚖️ LegalEase — AI-Powered Legal Document Generator")
st.caption("Generate employment contracts, NDAs, and lease agreements in seconds.")

doc_type = st.selectbox(
    "What would you like to create?",
    ["Employment Contract", "Non-Disclosure Agreement (NDA)", "Residential Lease Agreement"],
)

st.divider()

if doc_type == "Employment Contract":
    with st.form("employment_form"):
        company_name = st.text_input("Company Name")
        employee_name = st.text_input("Employee Name")
        job_title = st.text_input("Job Title / Role")
        start_date = st.date_input("Start Date")
        compensation = st.text_input("Compensation (e.g. $85,000/year)")
        work_location = st.text_input("Work Location", "Remote")
        employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract"])
        logo = st.file_uploader("Company Logo (optional, for branding)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Generate Contract")

    if submitted:
        submit_generation(
            "employment_contract",
            {
                "company_name": company_name,
                "employee_name": employee_name,
                "job_title": job_title,
                "start_date": str(start_date),
                "compensation": compensation,
                "work_location": work_location,
                "employment_type": employment_type,
            },
            logo,
        )

elif doc_type == "Non-Disclosure Agreement (NDA)":
    with st.form("nda_form"):
        disclosing_party = st.text_input("Disclosing Party")
        receiving_party = st.text_input("Receiving Party (Freelancer/Client)")
        purpose = st.text_area("Purpose of Disclosure")
        scope = st.text_area("Scope of Confidential Information")
        effective_date = st.date_input("Effective Date")
        term = st.text_input("Term / Duration", "2 years from the Effective Date")
        submitted = st.form_submit_button("Generate NDA")

    if submitted:
        submit_generation(
            "nda",
            {
                "disclosing_party": disclosing_party,
                "receiving_party": receiving_party,
                "purpose": purpose,
                "scope": scope,
                "effective_date": str(effective_date),
                "term": term,
            },
        )

else:
    with st.form("lease_form"):
        landlord_name = st.text_input("Landlord Name")
        tenant_name = st.text_input("Tenant Name")
        property_address = st.text_input("Property Address")
        lease_start = st.date_input("Lease Start Date")
        lease_end = st.date_input("Lease End Date")
        monthly_rent = st.text_input("Monthly Rent (e.g. $1,500)")
        security_deposit = st.text_input("Security Deposit", "One month's rent")
        submitted = st.form_submit_button("Generate Lease Agreement")

    if submitted:
        submit_generation(
            "lease_agreement",
            {
                "landlord_name": landlord_name,
                "tenant_name": tenant_name,
                "property_address": property_address,
                "lease_start": str(lease_start),
                "lease_end": str(lease_end),
                "monthly_rent": monthly_rent,
                "security_deposit": security_deposit,
            },
        )


result = st.session_state.get("result")
if result:
    if "error" in result:
        st.error(result["error"])
    else:
        st.divider()
        st.subheader("📄 Preview")
        st.text_area("Generated document text", result["preview_text"], height=350)

        st.subheader("⬇️ Download")
        columns = st.columns(len(result["files"]))
        for column, (file_format, content) in zip(columns, result["files"].items()):
            column.download_button(
                label=f"Download .{file_format}",
                data=content,
                file_name=f"{result['filename']}.{file_format}",
            )
