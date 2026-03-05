from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
import json
import os
import pypdf
import io
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"  # or https://api.deepseek.com
)

MODEL = "llama-3.3-70b-versatile"  # or "deepseek-chat"


def ask(prompt, json_mode=False):
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        **kwargs
    )
    return response.choices[0].message.content.strip()


def extract_pdf_text(file_bytes):
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


# ── Question plan: defines the focus of each question slot ────
QUESTION_PLAN = [
    {
        "slot": 1,
        "type": "HR / Ice-breaker",
        "focus": "Ask a warm opening HR question — e.g. tell me about yourself, why they chose their field, or their overall career journey. Reference their name and background."
    },
    {
        "slot": 2,
        "type": "Project Deep-dive",
        "focus": "Pick the most impressive or relevant PROJECT from their resume and ask a specific question about it — what they built, their role, challenges faced, or tech decisions made."
    },
    {
        "slot": 3,
        "type": "Technical — Basic",
        "focus": "Ask a basic-to-intermediate conceptual question about one of their PRIMARY SKILLS or technologies listed. E.g. explain a core concept, difference between two things, or how something works."
    },
    {
        "slot": 4,
        "type": "Internship / Experience",
        "focus": "Ask about their internship or work experience — what they worked on, what they learned, a challenge they solved, or how they contributed to the team."
    },
    {
        "slot": 5,
        "type": "Technical — Intermediate",
        "focus": "Ask a slightly deeper technical question on a DIFFERENT skill or technology from their resume. Could be about architecture, best practices, debugging, or a real-world scenario."
    },
    {
        "slot": 6,
        "type": "Certification / Course",
        "focus": "If they have certifications or courses, ask about something specific they learned or how they applied that knowledge. If none, ask about a skill they self-learned and how."
    },
    {
        "slot": 7,
        "type": "Behavioral (STAR)",
        "focus": "Ask a behavioral question using STAR format — e.g. a time they faced a conflict, handled pressure, led something, failed and recovered, or collaborated cross-functionally."
    },
    {
        "slot": 8,
        "type": "HR — Career Goals",
        "focus": "Ask a closing HR question about their career goals, where they see themselves in 3-5 years, why they want this role/company, or their biggest motivation."
    },
]


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/interview')
def interview():
    return render_template('interview.html')


@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    try:
        file = request.files.get('resume')
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400

        pdf_text = extract_pdf_text(file.read())
        if not pdf_text:
            return jsonify({'error': 'Could not extract text from PDF. Make sure it is not a scanned image.'}), 400

        prompt = f"""Analyze this resume thoroughly and return ONLY a valid JSON object (no markdown, no backticks, no extra text):
{{
  "name": "candidate's full name",
  "current_role": "most recent job title or student if fresher",
  "years_experience": "estimated years of experience or 'Fresher' if none",
  "skills": ["skill1", "skill2"],
  "technologies": ["tech1", "tech2"],
  "companies": ["company or internship name"],
  "internships": ["internship role and company description"],
  "education": "degree, field, institution",
  "key_projects": ["project name: brief description of what was built and tech used"],
  "certifications": ["certification or course name"],
  "specializations": ["area1", "area2"],
  "summary": "2-3 sentence professional summary"
}}

Resume text:
{pdf_text}"""

        text = ask(prompt, json_mode=True)
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        resume_data = json.loads(text)
        session['resume_data'] = resume_data
        return jsonify({'success': True, 'resume': resume_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/start-interview', methods=['POST'])
def start_interview():
    try:
        resume_data = request.json.get('resume_data') or session.get('resume_data')
        if not resume_data:
            return jsonify({'error': 'No resume data found'}), 400

        slot = QUESTION_PLAN[0]

        prompt = f"""You are a professional interviewer conducting a mock interview. Here is the candidate's resume:

Name: {resume_data.get('name')}
Role/Level: {resume_data.get('current_role')}
Skills: {', '.join(resume_data.get('skills', []))}
Technologies: {', '.join(resume_data.get('technologies', []))}
Projects: {', '.join(resume_data.get('key_projects', []))}
Internships/Experience: {', '.join(resume_data.get('internships', []) or resume_data.get('companies', []))}
Certifications: {', '.join(resume_data.get('certifications', []))}
Education: {resume_data.get('education')}

This is Question 1 of 8. Question type: {slot['type']}
Your task: {slot['focus']}

Instructions:
- Greet the candidate warmly by name
- Mention 1 specific thing from their background that caught your attention
- Then ask your question naturally as part of the conversation
- Keep it to 3-5 sentences total
- Do NOT number the question or say "Question 1"
- Sound like a real human interviewer, not a robot"""

        message = ask(prompt)
        return jsonify({'success': True, 'message': message, 'question_number': 1})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/next-question', methods=['POST'])
def next_question():
    try:
        data = request.json
        resume_data = data.get('resume_data') or session.get('resume_data')
        conversation_history = data.get('history', [])
        question_number = data.get('question_number', 1)
        is_final = question_number >= 8

        conv_text = "\n".join([
            f"{'Interviewer' if m['role'] == 'interviewer' else 'Candidate'}: {m['text']}"
            for m in conversation_history
        ])

        # Get the plan for the next slot (0-indexed, so slot index = question_number)
        slot_index = min(question_number, len(QUESTION_PLAN) - 1)
        slot = QUESTION_PLAN[slot_index]

        prompt = f"""You are a professional interviewer conducting a mock interview.

Candidate Resume Summary:
- Name: {resume_data.get('name')}
- Skills: {', '.join(resume_data.get('skills', []))}
- Technologies: {', '.join(resume_data.get('technologies', []))}
- Projects: {', '.join(resume_data.get('key_projects', []))}
- Internships/Experience: {', '.join(resume_data.get('internships', []) or resume_data.get('companies', []))}
- Certifications: {', '.join(resume_data.get('certifications', []))}
- Education: {resume_data.get('education')}

Conversation so far:
{conv_text}

This is Question {question_number + 1} of 8. Question type: {slot['type']}
Your task: {slot['focus']}

Instructions:
- Start with a brief 1-sentence acknowledgment of their previous answer (be specific, not generic)
- Then transition naturally into your next question
- The question MUST be directly based on something SPECIFIC from their resume (a real project name, a real skill they listed, a real company/internship they mentioned, a real certification)
- For technical questions: start basic/conceptual, don't ask for code
- Keep it to 3-5 sentences total
- Do NOT number the question or say "Question X"
- Sound like a real human interviewer"""

        message = ask(prompt)
        return jsonify({
            'success': True,
            'message': message,
            'question_number': question_number + 1,
            'is_final': is_final
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/end-interview', methods=['POST'])
def end_interview():
    try:
        data = request.json
        resume_data = data.get('resume_data') or session.get('resume_data')
        conversation_history = data.get('history', [])

        resume_summary = json.dumps(resume_data, indent=2) if resume_data else "Not provided"
        conv_text = "\n".join([
            f"{'Interviewer' if m['role'] == 'interviewer' else 'Candidate'}: {m['text']}"
            for m in conversation_history
        ])

        prompt = f"""You are a professional interview coach reviewing a completed mock interview.

Candidate Resume:
{resume_summary}

Full Interview Transcript:
{conv_text}

Evaluate the candidate thoroughly across all 8 questions covering their projects, skills, experience, and HR answers.
Return ONLY a valid JSON object (no markdown, no backticks):
{{
  "overall_score": <number 1-10>,
  "overall_summary": "2-3 sentence honest overall assessment referencing specific answers",
  "strengths": [
    "Specific strength observed with exact example from the interview",
    "Another specific strength"
  ],
  "improvements": [
    "Specific area to improve with concrete actionable advice",
    "Another improvement area"
  ],
  "communication_score": <1-10>,
  "technical_score": <1-10>,
  "confidence_score": <1-10>,
  "best_answer": "Paraphrase of their single strongest answer and why it was good",
  "focus_areas": ["Specific topic/skill they should study or practice more"],
  "hire_recommendation": "Strong Yes / Yes / Maybe / No",
  "closing_message": "Encouraging but honest 2-3 sentence closing message to the candidate"
}}"""

        text = ask(prompt, json_mode=True)
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        feedback = json.loads(text)
        return jsonify({'success': True, 'feedback': feedback})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)