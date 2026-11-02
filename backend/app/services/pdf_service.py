from pdfminer.high_level import extract_text
import re

def extract_text_from_pdf(file_path: str) -> str:
    try:
        text = extract_text(file_path)
        # Clean basic whitespace
        text = re.sub(r'\s+', ' ', text)
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def extract_information(text: str):
    # Basic Regex for email and phone
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    
    # Mocking advanced extraction with simple keyword checks
    text_lower = text.lower()
    
    # Education
    education = "Bachelors"
    if "phd" in text_lower or "ph.d" in text_lower or "doctorate" in text_lower:
        education = "PhD"
    elif "master" in text_lower or "msc" in text_lower or "m.s" in text_lower:
        education = "Masters"
        
    # CGPA (looking for something like CGPA: 3.8 or 3.8/4.0)
    cgpa = 3.0
    cgpa_match = re.search(r'(?:cgpa|gpa)[\s:]*([0-4]\.\d+)', text_lower)
    if cgpa_match:
        cgpa = float(cgpa_match.group(1))
        
    # Experience (looking for "X years")
    experience = 0
    exp_match = re.search(r'(\d+)\+?\s*years?(?:\s+of)?\s+experience', text_lower)
    if exp_match:
        experience = int(exp_match.group(1))
        
    return {
        "name": "Candidate Name", # Fallback, real extraction needs NER
        "email": email.group(0) if email else "Not detected",
        "phone": phone.group(0) if phone else "Not detected",
        "education": education,
        "cgpa": cgpa,
        "experience_years": experience,
        "internships": 1 if "intern" in text_lower else 0,
        "projects": len(re.findall(r'project', text_lower)),
        "certifications": len(re.findall(r'certif', text_lower)),
        "skills": [] # Will be populated by match_service
    }
