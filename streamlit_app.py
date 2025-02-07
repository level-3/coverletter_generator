
import streamlit as st
import os
#from google import genai
from openai import OpenAI
from anthropic import Anthropic

# Replace with your actual Gemini API key

def openai_generate_cover_letter(resume_text, job_description_text):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
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



def gemini_generate_cover_letter(resume_text, job_description_text):
    gemini = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])  # Initialize Client

    prompt = f"""
    You are an expert career advisor with extensive experience in crafting highly professional, tailored, and persuasive cover letters. Your goal is to ensure the cover letter aligns perfectly with the job description, highlights the candidate's strengths, and maintains a confident and engaging tone while remaining concise and impactful.
    
    Resume:
    {resume_text}

    Job Description:
    {job_description_text}

    Cover Letter:
    """

    response = gemini.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    return response.text


def claude_generate_cover_letter(resume_text: str, job_description_text: str) -> str:
    """
    Generate a cover letter using Claude, given a resume and job description.
    
    Args:
        resume_text (str): The text content of the resume
        job_description_text (str): The text content of the job description
    
    Returns:
        str: The generated cover letter
    """
    # Initialize the Claude client
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    system_prompt = """You are an expert career advisor with extensive experience in crafting highly professional, tailored, and persuasive cover letters. Your goal is to ensure the cover letter aligns perfectly with the job description, highlights the candidate's strengths, and maintains a confident and engaging tone while remaining concise and impactful."""
    
    user_prompt = f"""
    Resume:
    {resume_text}
    
    Job Description:
    {job_description_text}
    
    Please write a cover letter based on the above information.
    """
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )
    
    return message.content[0].text


t_resume, t_jobdescription, t_coverletter = st.tabs(["Resume", "Job Description", "Cover Letter"])


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")
    "[Get an Gemini API key](https://ai.google.dev/gemini-api/docs/api-key)"
    anthropic_api_key = st.text_input("Anthropic API Key", key="anthropic_api_key", type="password")
    "[Get an Anthropic API key](https://console.anthropic.com/settings/keys)"
    options = ["OpenAI", "Google", "Anthropic"]
    selection = st.segmented_control("llm", options, selection_mode="multi")
    resume_file = st.file_uploader("Upload your resume (txt)", type="txt")
    job_description_file = st.file_uploader("Upload the job description (txt)", type="txt")


st.title("Cover Letter Generator")
st.write("Upload your resume and job description to generate a personalized cover letter.")

if resume_file and job_description_file:
    resume_text = resume_file.read().decode("utf-8")
    job_description_text = job_description_file.read().decode("utf-8")

    
    with t_resume:
        st.subheader("Resume")
        st.text_area("Resume Text", resume_text, height=300)
    with t_jobdescription:
        st.subheader("Job Description")
        st.text_area("Job Description Text", job_description_text, height=300)


    llm_to_use = st.radio(
        "Choose LLM to use",
        ["ChatGPT", "Gemini", "Claude"],
        captions=[
            "OpenAI (recommended)",
            "Google",
            "Anthropic",
        ],
    )

    if st.button("Generate Cover Letter"):

        if llm_to_use == "ChatGPT":
            cover_letter = openai_generate_cover_letter(resume_text, job_description_text)
        elif llm_to_use == "Gemini":
            cover_letter = gemini_generate_cover_letter(resume_text, job_description_text)
        elif llm_to_use == "Claude":
            cover_letter = claude_generate_cover_letter(resume_text, job_description_text)


        #cover_letter = openai_generate_cover_letter(resume_text, job_description_text)

        st.subheader("Generated Cover Letter:")
        st.text_area("Cover Letter", cover_letter, height=300)

        # Save the cover letter to a file
        with open("/content/drive/My Drive/CoverLetter/cover_letter.txt", "w") as f:
            f.write(cover_letter)

        
        with t_coverletter:
            st.subheader("Cover Letter")
            st.text_area("Cover Letter Text", cover_letter, height=300)
        

        st.success("Cover letter saved to cover_letter.txt")