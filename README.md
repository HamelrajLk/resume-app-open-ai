# Resume Screening App

An AI-powered resume screening tool that evaluates how well a candidate's CV matches a given Job Description (JD). Upload a resume and a JD in PDF format — the system extracts key details from both and returns a structured evaluation with a match score.

---

## How It Works

```
Resume (PDF) ──┐
               ├──► Extract Details ──► Evaluate Match ──► Result (Selected / Rejected)
Job JD (PDF) ──┘
```

1. **Resume Parser** — extracts name, email, phone, education, years of experience, skills, and certifications from the CV.
2. **JD Parser** — extracts required skills and experience range from the job description.
3. **Evaluation Agent** — compares both and returns a decision with a skill match percentage and reasoning.

---

## Tech Stack

| Layer     | Technology           |
|-----------|----------------------|
| Backend   | FastAPI              |
| Frontend  | Streamlit            |
| AI        | OpenAI GPT-4         |
| PDF Parse | PyPDF2               |
| Config    | python-dotenv        |

---

## Project Structure

```
resume/
├── app/
│   ├── main.py                  # FastAPI app & endpoints
│   ├── prompts.py               # LLM prompt templates
│   ├── agents/
│   │   ├── resume_extractor.py  # Extracts candidate details from CV
│   │   ├── jd_extractor.py      # Extracts requirements from JD
│   │   └── evaluation.py        # Evaluates candidate against JD
│   ├── services/
│   │   └── parsepdf.py          # PDF text extraction
│   └── ui/
│       └── index.py             # Streamlit frontend
├── .env                         # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd resume
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
.venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Running the App

### Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### Start the Streamlit frontend (in a separate terminal)

```bash
streamlit run app/ui/index.py
```

UI will open at `http://localhost:8501`

---

## API Endpoints

### `POST /screen_resume`

Screens a resume against a job description.

**Request:** `multipart/form-data`
| Field    | Type | Description          |
|----------|------|----------------------|
| `resume` | file | Resume PDF file      |

**Response:**
```json
{
  "candidate_status": "Selected",
  "reason": "The candidate has 7 years of experience which falls within the required range of 5–10 years. They matched 6 out of 8 required skills including Python, FastAPI, and Machine Learning.",
  "matched_skills": ["Python", "FastAPI", "Machine Learning"],
  "skill_match_percentage": 75,
  "experience": 7
}
```

---

## Evaluation Logic

A candidate is marked **Selected** only if **both** conditions are met:

- **Skill match** — at least 50% of the JD's required skills are present in the CV
- **Experience** — candidate's years of experience falls within the JD's min/max range

Related skills are also considered (e.g. "DevOps" counts toward "CI/CD").

---

## License

MIT — free to use, learn from, and modify.
