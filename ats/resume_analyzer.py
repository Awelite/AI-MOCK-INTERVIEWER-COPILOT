import re
from ats.skill_match import extract_skills
from ats.score import SKILL_VOCAB

def analyze_resume(resume_text):
    """
    Mode A: Standalone Resume Analysis (No JD needed).
    Returns Quality Score, Skills, Experience, Education, Projects, and Suggestions.
    """
    text_lower = resume_text.lower()
    
    # 1. Experience
    exp_keywords = ["experience", "employment", "work history"]
    has_experience = any(kw in text_lower for kw in exp_keywords)
    
    # 2. Education
    edu_keywords = ["education", "degree", "b.tech", "btech", "b.s", "bachelor", "master", "phd", "university", "college"]
    has_education = any(kw in text_lower for kw in edu_keywords)
    
    # 3. Projects
    proj_keywords = ["projects", "personal projects", "portfolio"]
    has_projects = any(kw in text_lower for kw in proj_keywords)
    
    # 4. Contact Info (Simple heuristics)
    has_email = "@" in resume_text
    has_phone = bool(re.search(r"\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b", resume_text))
    
    # 5. Skills
    extracted_skills = list(extract_skills(resume_text, SKILL_VOCAB))
    
    # Calculate Quality Score (Base 100)
    score = 100
    suggestions = []
    
    if not has_experience:
        score -= 20
        suggestions.append("Add a clear 'Experience' or 'Work History' section.")
    
    if not has_education:
        score -= 15
        suggestions.append("Add your educational background.")
        
    if not has_projects:
        score -= 10
        suggestions.append("Consider adding a 'Projects' section to showcase your work.")
        
    if not has_email or not has_phone:
        score -= 10
        suggestions.append("Ensure your email and phone number are clearly visible.")
        
    if len(extracted_skills) < 3:
        score -= 15
        suggestions.append("List more technical skills and keywords relevant to your field.")
        
    # Word count penalty
    words = len(resume_text.split())
    if words < 100:
        score -= 20
        suggestions.append("Your resume is very short. Add more details about your responsibilities and achievements.")
    elif words > 1000:
        score -= 10
        suggestions.append("Your resume might be too long. Keep it concise and relevant.")

    score = max(0, score)

    if score == 100:
        suggestions.append("Your resume looks great!")

    return {
        "quality_score": score,
        "skills": extracted_skills,
        "has_experience": has_experience,
        "has_education": has_education,
        "has_projects": has_projects,
        "suggestions": suggestions,
        "word_count": words
    }
