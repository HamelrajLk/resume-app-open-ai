EXTRACT_CANDIDATE_DETAILS = """
You are an expert in resume screening. Your task is to extract relevant details from a resume.
You will receive a resume in text format, and you need to identify key information such as:
- name (string)
- email (string)
- phone (string)
- education (string or null)
- work_experience (integer or null)
- skills (list of strings)
- certifications (list of strings)
*
Your response must be a valid JSON object.
Use 'null' if a value is missing.

Here is the resume text:
{resume_text}

Expected response format:
{{
  "name":"John Doe",
  "email":"abc@gmail.com",
  "phone":"1234567890",
  "education":"Bachelor of Science in Computer Science",
  "work_experience": 7,
  "skills":["Python", "FastAPI", "Machine Learning"],
  "certifications":["Certified Python Developer"]
}}
"""