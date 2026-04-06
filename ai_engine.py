import requests


# ---------------- EVALUATE ANSWER ----------------
def evaluate_answer(question, answer, lang='en'):
    if lang == 'hi':
        prompt = f"""
आप एक साक्षात्कारकर्ता हैं।

प्रश्न: {question}
उत्तर: {answer}

दे:
1. 10 में से स्कोर
2. छोटी प्रतिक्रिया (हिंदी में)
        """
    else:
        prompt = f"""
You are an interviewer.

Question: {question}
Answer: {answer}

Give:
1. Score out of 10
2. Short feedback
        """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()['response']


# ---------------- GENERATE QUESTIONS ----------------
def generate_questions(role, lang='en'):
    if lang == 'hi':
        prompt = f"""
{role} के लिए 5 साक्षात्कार प्रश्न उत्पन्न करें।
केवल क्रमांकित सूची में प्रश्न लौटाएं।
        """
    else:
        prompt = f"""
Generate 5 interview questions for a {role}.
Only return questions in numbered list.
        """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    output = response.json()['response']

    # Convert text → list
    questions = output.split("\n")

    clean_questions = []
    for q in questions:
        if q.strip():
            clean_questions.append(q.split('.', 1)[-1].strip())

    return clean_questions[:5]