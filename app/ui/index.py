import streamlit as st
import requests

st.title("Resume Screening App")

uploaded_file = st.file_uploader("Upload a resume (PDF)", type="pdf")

if uploaded_file is not None:
    st.write("File uploaded successfully:", uploaded_file.name)

    if st.button("Process Resume"):
        files = {"resume": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post("http://localhost:8000/screen_resume", files=files)

        if response.status_code == 200:
            st.success("Resume processed successfully!")
            response_data = response.json()
            st.json(response_data)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
else:
    st.warning("Please upload a resume file.")