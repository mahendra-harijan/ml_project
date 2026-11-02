import re

def process_job_description(jd_text: str):
    common_skills = [
        "python", "java", "c++", "javascript", "react", "node.js", "mongodb",
        "sql", "docker", "kubernetes", "aws", "azure", "machine learning",
        "git", "fastapi", "django", "pandas", "scikit-learn", "vue", "angular",
        "tensorflow", "pytorch", "ci/cd"
    ]
    
    jd_lower = jd_text.lower()
    required_skills = [skill for skill in common_skills if skill in jd_lower]
    
    role = "Software Engineer"
    if "data scientist" in jd_lower:
        role = "Data Scientist"
    elif "data analyst" in jd_lower:
        role = "Data Analyst"
    elif "web developer" in jd_lower:
        role = "Web Developer"
        
    return {
        "required_skills": required_skills,
        "role": role
    }

def calculate_skill_match(resume_text: str, required_skills: list):
    resume_lower = resume_text.lower()
    
    matched_skills = []
    missing_skills = []
    
    for skill in required_skills:
        # Use regex to find whole words where possible, or just string match
        pattern = r'\b' + re.escape(skill) + r'\b'
        # Some skills like c++ don't play well with \b because + is not a word character.
        # Fallback to simple substring match for special cases.
        if '+' in skill or '.' in skill:
            if skill in resume_lower:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        else:
            if re.search(pattern, resume_lower):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
            
    total_required = len(required_skills)
    match_score = (len(matched_skills) / total_required * 100) if total_required > 0 else 100.0
    
    return {
        "match_score": round(match_score, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
