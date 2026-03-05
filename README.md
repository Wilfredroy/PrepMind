<div align="center">

# PrepMind

### AI-Powered Mock Interview Coach

**Upload your resume. Get interviewed by AI. Land your dream job.**

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=flat-square)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-22c55e?style=flat-square)]()

<br/>

[**Features**](#-features) · [**Quick Start**](#-quick-start) · [**How It Works**](#-how-it-works) · [**Tech Stack**](#-tech-stack) · [**Roadmap**](#-roadmap)

<br/>

> *"It asked me about my exact Django project from my resume. Felt like a real interview."*

<br/>

</div>

---

## What is PrepMind?

PrepMind is a **full-stack AI interview preparation web app** built with Flask and powered by LLaMA 3.3 70B via Groq. It reads your resume, extracts your real skills, projects, internships, and certifications — then conducts a structured 8-question mock interview tailored entirely to your background.

No generic questions. No one-size-fits-all prompts. Every question is grounded in **your** actual experience.

```
📄 Upload Resume  ──▶  🧠 AI Analyses Profile  ──▶  💬 8-Question Interview  ──▶  📊 Scored Feedback
```

---

## Features

| | Feature | Description |
|--|---------|-------------|
| 🧠 | **Resume Intelligence** | AI extracts skills, technologies, projects, internships, certifications, and education from your PDF |
| 🎯 | **Personalised Questions** | Every question directly references something from your resume — your real projects, your real skills |
| 📋 | **Structured Interview Plan** | 8 questions covering HR, technical (basic + intermediate), project deep-dive, experience, behavioral, and career goals |
| 📊 | **Detailed Feedback Report** | Scores for Communication, Technical depth, and Confidence — plus a hire recommendation |
| 💬 | **Real Interview Feel** | Typing indicators, animated chat bubbles, and smooth transitions create a genuine interview atmosphere |
| 🎨 | **Polished Animated UI** | Spin-in logo, dust particle burst, floating animation, and staggered page entrances |
| ⚡ | **LLM-Agnostic Backend** | Swap between Groq, DeepSeek, or any OpenAI-compatible provider with two lines of code |

---

## Screenshots

<div align="center">

| Resume Upload | Live Interview | Feedback Report |
|:---:|:---:|:---:|
| ![Upload your resume](https://i.postimg.cc/Qx2vGt2r/Screenshot_(20).png) | ![Parsing](https://i.postimg.cc/7YFj86Fk/Screenshot_(22).png) | ![Interview Chat](https://i.postimg.cc/pXw3bTwv/Screenshot_(23).png) |
| *Drag & drop your PDF resume* | *Extracts data from your resume in seconds* | *Chat-style interview with typing indicator* |

</div>

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- A free API key from [Groq](https://console.groq.com) *(recommended — completely free)*

### 1. Clone the Repository

```bash
git clone https://github.com/Wilfredroy/PrepMind.git
cd PrepMind
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Your API Key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq key at [console.groq.com](https://console.groq.com) → API Keys → Create API Key

### 4. Run the App

```bash
python app.py
```

Open **[http://localhost:5000](http://localhost:5000)** in your browser. 🎉

---

## 🔧 Switching LLM Providers

PrepMind uses an OpenAI-compatible client, so switching providers takes two lines in `app.py`:

<details>
<summary><b>Groq — Free & Recommended</b></summary>

```python
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
MODEL = "llama-3.3-70b-versatile"
```
</details>

<details>
<summary><b>DeepSeek</b></summary>

```python
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
MODEL = "deepseek-chat"
```
</details>

<details>
<summary><b>OpenAI</b></summary>

```python
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"
```
</details>

---

## How It Works

### Step 1 — Resume Analysis

Your PDF is parsed with `pypdf` and the extracted text is sent to the LLM, which returns a structured profile:

```json
{
  "name": "Alex Johnson",
  "current_role": "Final Year B.Tech CSE Student",
  "skills": ["Python", "React", "SQL", "REST APIs"],
  "technologies": ["Django", "PostgreSQL", "Docker"],
  "companies": ["TechCorp (Intern)", "StartupXYZ (Intern)"],
  "key_projects": ["E-commerce platform using Django + PostgreSQL + Stripe"],
  "certifications": ["AWS Cloud Practitioner", "Meta Front-End Developer"],
  "education": "B.Tech Computer Science, 2025"
}
```

### Step 2 — The 8-Question Interview Plan

PrepMind uses a fixed question plan — not random generation. Each slot has a defined purpose:

```
Q1  ──  HR Ice-breaker         →  "Tell me about yourself and your background"
Q2  ──  Project Deep-dive      →  "Walk me through [your actual project name]"
Q3  ──  Technical Basic        →  "Explain how [your listed skill] works"
Q4  ──  Internship/Experience  →  "At [company you interned at], what did you build?"
Q5  ──  Technical Intermediate →  "How would you approach [real scenario using your stack]?"
Q6  ──  Certification/Learning →  "You completed [your cert]. How did you apply it?"
Q7  ──  Behavioral (STAR)      →  "Tell me about a time you faced a challenge and overcame it"
Q8  ──  HR Career Goals        →  "Where do you see yourself in 3-5 years?"
```

Every question is generated dynamically using your resume data — referencing real project names, real technologies, and real companies.

### Step 3 — AI Feedback Report

After the 8th answer, the full conversation and resume are evaluated by the LLM:

| Metric | Description |
|--------|-------------|
| 🏆 Overall Score | 1–10 holistic rating |
| 💬 Communication | Clarity, structure, and articulation |
| ⚙️ Technical | Depth and accuracy of technical answers |
| 💪 Confidence | Assertiveness and ownership of responses |
| ✅ Strengths | Specific examples pulled from your answers |
| 📈 Improvements | Concrete, actionable advice |
| ⭐ Best Answer | Your single strongest response highlighted |
| 📚 Focus Areas | Topics to study before your real interview |
| 🎯 Hire Recommendation | Strong Yes / Yes / Maybe / No |

---

## Project Structure

```
PrepMind/
│
├── app.py                    # Flask server — all routes and AI prompt logic
├── requirements.txt          # Python dependencies
├── .env                      # Your API key (never committed)
├── .gitignore
│
├── templates/
│   ├── upload.html           # Resume upload + analysis preview page
│   └── interview.html        # Live interview chat interface
│
└── assets/
    ├── logo.svg
    └── screenshots/
```

### API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Resume upload page |
| `GET` | `/interview` | Interview chat page |
| `POST` | `/analyze-resume` | Parse PDF and extract structured resume data |
| `POST` | `/start-interview` | Generate personalised opening question |
| `POST` | `/next-question` | Acknowledge answer and ask next question |
| `POST` | `/end-interview` | Evaluate full conversation and return feedback JSON |

---

## Tech Stack

**Backend**
- [Flask](https://flask.palletsprojects.com/) — Python web framework
- [pypdf](https://pypdf.readthedocs.io/) — PDF text extraction
- [openai](https://github.com/openai/openai-python) — OpenAI-compatible API client
- [python-dotenv](https://github.com/theskumar/python-dotenv) — Environment variable management

**Frontend**
- Vanilla HTML, CSS, JavaScript — zero framework dependencies
- [Tailwind CSS](https://tailwindcss.com/) — utility-first styling via CDN
- Custom CSS animations — spin-in, line-draw, float, dust particles, message bubbles

**AI / LLM**
- [Groq](https://groq.com/) + LLaMA 3.3 70B — free, ultra-fast inference (primary)
- [DeepSeek](https://deepseek.com/) — alternative provider
- Any OpenAI-compatible API endpoint supported

---

## Roadmap

- [ ] 🎙️ Voice input — speak your answers instead of typing
- [ ] 💾 Interview history — save and replay past sessions
- [ ] 🎭 Role selector — SDE / Data Analyst / Product Manager / DevOps tracks
- [ ] 🏢 Company mode — Google, Amazon, Microsoft interview simulations
- [ ] 📄 Export feedback as downloadable PDF report
- [ ] 🌐 Multi-language resume support
- [ ] 🔁 Follow-up questions based on weak or incomplete answers
- [ ] 📱 Mobile-optimised layout

---

## Acknowledgements

- [Groq](https://groq.com/) for providing blazing-fast free LLM inference
- [pypdf](https://pypdf.readthedocs.io/) for robust PDF text extraction
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first styling system

---

<div align="center">

<br/>

**Built to help every developer walk into their next interview with confidence.**

<br/>

</div>
