import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Resume Screening App")

resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
jd_file = st.file_uploader("Upload Job Description (PDF)", type="pdf")

if st.button("Screen Resume"):
    if not resume_file:
        st.warning("Please upload a resume PDF.")
    elif not jd_file:
        st.warning("Please upload a job description PDF.")
    else:
        with st.spinner("Analysing..."):
            files = {
                "resume": (resume_file.name, resume_file, "application/pdf"),
                "jd": (jd_file.name, jd_file, "application/pdf"),
            }
            try:
                response = requests.post(f"{API_URL}/screen_resume", files=files)
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("candidate_status", "Unknown")
                    color = "green" if status == "Selected" else "red"
                    st.markdown(f"### Status: :{color}[{status}]")
                    st.write(f"**Skill Match:** {data.get('skill_match_percentage', 'N/A')}%")
                    st.write(f"**Experience:** {data.get('experience', 'N/A')} years")
                    st.write(f"**Reason:** {data.get('reason', '')}")
                    st.write(f"**Matched Skills:** {', '.join(data.get('matched_skills', []))}")
                    with st.expander("Full JSON Response"):
                        st.json(data)
                else:
                    st.error(f"Error {response.status_code}: {response.json().get('detail', response.text)}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend. Make sure the FastAPI server is running on port 8000.")
