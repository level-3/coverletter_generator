
import streamlit as st
import os

from openai import OpenAI


# Replace with your actual Gemini API key

def openai_generate_cover_letter(resume_text, job_description_text):
    client = OpenAI(
        api_key=openai_api_key,  # This is the default and can be omitted
    )

    prompt = f"""
    You are an expert career advisor with extensive experience in crafting highly professional, tailored, and persuasive cover letters. Your goal is to ensure the cover letter aligns perfectly with the job description, highlights the candidate's strengths, and maintains a confident and engaging tone while remaining concise and impactful.

    Resume:
    {resume_text}

    Job Description:
    {job_description_text}

    Cover Letter:
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
    )
    
    return chat_completion.choices[0].message.content


t_coverletter, t_resume, t_jobdescription  = st.tabs(["Cover Letter","Resume", "Job Description" ])


with st.sidebar:
    st.title("Cover Letter Generator")
    st.write("Upload your resume and job description to generate a personalized cover letter.")
    openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    resume_file = st.file_uploader("Upload your resume (txt)", type="txt")
    job_description_file = st.file_uploader("Upload the job description (txt)", type="txt")


if resume_file and job_description_file:
    resume_text = resume_file.read().decode("utf-8")
    job_description_text = job_description_file.read().decode("utf-8")

    
    with t_resume:
        st.subheader("Resume")
        st.text_area("Resume Text", resume_text, height=600)
    with t_jobdescription:
        st.subheader("Job Description")
        st.text_area("Job Description Text", job_description_text, height=600)


    if st.button("Generate Cover Letter"):

        cover_letter = openai_generate_cover_letter(resume_text, job_description_text)
      
        with t_coverletter:
            st.subheader("Cover Letter")
            st.text_area("Cover Letter Text", cover_letter, height=600)
        
        with st.sidebar:
            st.success("Cover letter created")