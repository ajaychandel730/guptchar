from pydantic import BaseModel
from typing import List

class ExecutiveContact(BaseModel):
    name: str = "N/A"
    title: str = "N/A"
    phone: str = "N/A"
    email: str = "N/A"
    source: str = "N/A"

class CompanyData(BaseModel):
    company_name: str = "N/A"
    address: str = "N/A"
    website: str = "N/A"
    generic_contact_number: str = "N/A"
    primary_email: str = "N/A"
    one_sentence_description: str = "N/A"
    executives_and_contacts: List[ExecutiveContact] = []