import re
import pdfplumber
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF resume."""
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def extract_email(text):
    """Extract email from resume text."""
    email_pattern = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+"
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def extract_phone(text):
    """Extract phone number from resume text."""
    phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    match = re.search(phone_pattern, text)
    # print(match)
    return match.group(0) if match else None

def extract_skills(text):
    """Extract skills using NLP."""
    doc = nlp(text)
    skills = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return list(set(skills))

def parse_resume(pdf_path):
    """Parse the resume and extract key details."""
    # pdf_path = r
    text = extract_text_from_pdf(pdf_path)
    extracts__ = extract_resume_info(text)
    print(extracts__, "Extracts")
    return {
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text),
    }

def extract_resume_info(text):
    doc = nlp(text)
    
    skills = []
    experience = []
    education = []
    
    # Common keywords for classification
    job_titles = ["Software Engineer", "Backend Developer", "Data Scientist"]
    degrees = ["Bachelor", "Master", "PhD", "HND"]
    
    for ent in doc.ents:
        if ent.label_ in ["ORG", "WORK_OF_ART"]:  # Organizations (Can be job titles too)
            experience.append(ent.text)
        elif any(word in ent.text for word in degrees):  # Education detection
            education.append(ent.text)
        elif any(word in ent.text for word in job_titles):  # Job titles
            experience.append(ent.text)
    
    return {"Skills": skills, "Experience": experience, "Education": education}


