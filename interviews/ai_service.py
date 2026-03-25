from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_questions(job_role, category, difficulty, count=5):
    prompt = f"""Generate {count} {difficulty}-level {category} interview questions 
    for a {job_role} position. Return only a numbered list of questions."""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content
    questions = [
        line.split('. ', 1)[1].strip()
        for line in raw.strip().split('\n')
        if line.strip() and line[0].isdigit()
    ]
    return questions

def evaluate_answer(question_text, answer_text, job_role):
    prompt = f"""You are a senior interviewer for a {job_role} role.
Question: {question_text}
Candidate's Answer: {answer_text}

Evaluate the answer and provide:
1. Score (0-10)
2. Strengths
3. Areas for improvement
4. A model answer

Format your response clearly under each heading."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content